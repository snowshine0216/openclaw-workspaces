#!/usr/bin/env node
// Send daily vocab review to Feishu as attachment
// Uses Feishu Open API directly

import fs from 'fs';
import path from 'path';
import https from 'https';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SCRIPT_DIR = __dirname;
const DOCX_FILE = path.join(SCRIPT_DIR, '../../projects/vocabulary/output/daily_review.docx');
const LOG_FILE = path.join(SCRIPT_DIR, 'review.log');
const FEISHU_CHAT = 'oc_eb619c8fea8c56afb88b44bf92abaca1';

// Feishu credentials from environment
const APP_ID = process.env.FEISHU_APP_ID || 'cli_a904c9a46978dcd4';
const APP_SECRET = process.env.FEISHU_APP_SECRET_ENGLISH_TUTOR;

function log(message) {
  const timestamp = new Date().toISOString();
  const logMsg = `${timestamp}: ${message}\n`;
  console.log(logMsg.trim());
  fs.appendFileSync(LOG_FILE, logMsg);
}

function httpsRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

async function getTenantAccessToken() {
  log('Getting tenant access token...');
  const postData = JSON.stringify({
    app_id: APP_ID,
    app_secret: APP_SECRET
  });

  const options = {
    hostname: 'open.feishu.cn',
    path: '/open-apis/auth/v3/tenant_access_token/internal',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  const result = await httpsRequest(options, postData);
  
  if (result.code !== 0) {
    throw new Error(`Failed to get token: ${result.msg}`);
  }
  
  log('✓ Got tenant access token');
  return result.tenant_access_token;
}

async function uploadFile(token, filePath) {
  log(`Uploading file: ${filePath}`);
  
  const fileContent = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);
  
  const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
  
  const formData = [
    `--${boundary}`,
    `Content-Disposition: form-data; name="file_type"`,
    '',
    'stream',
    `--${boundary}`,
    `Content-Disposition: form-data; name="file_name"`,
    '',
    fileName,
    `--${boundary}`,
    `Content-Disposition: form-data; name="file"; filename="${fileName}"`,
    `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`,
    '',
    fileContent.toString('binary'),
    `--${boundary}--`
  ].join('\r\n');

  const options = {
    hostname: 'open.feishu.cn',
    path: '/open-apis/im/v1/files',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': `multipart/form-data; boundary=${boundary}`,
      'Content-Length': Buffer.byteLength(formData, 'binary')
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.code !== 0) {
            reject(new Error(`Upload failed: ${result.msg}`));
          } else {
            log(`✓ File uploaded, file_key: ${result.data.file_key}`);
            resolve(result.data.file_key);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.write(formData, 'binary');
    req.end();
  });
}

async function sendMessage(token, chatId, fileKey) {
  log(`Sending message to chat: ${chatId}`);
  
  const today = new Date().toISOString().split('T')[0];
  const postData = JSON.stringify({
    receive_id: chatId,
    msg_type: 'file',
    content: JSON.stringify({
      file_key: fileKey
    })
  });

  const options = {
    hostname: 'open.feishu.cn',
    path: '/open-apis/im/v1/messages?receive_id_type=chat_id',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  const result = await httpsRequest(options, postData);
  
  if (result.code !== 0) {
    throw new Error(`Failed to send message: ${result.msg}`);
  }
  
  log(`✓ Message sent successfully`);
  return result;
}

async function main() {
  try {
    log('=== Starting vocabulary review delivery ===');
    
    if (!APP_SECRET) {
      throw new Error('FEISHU_APP_SECRET_ENGLISH_TUTOR not set in environment');
    }
    
    if (!fs.existsSync(DOCX_FILE)) {
      throw new Error(`Document not found: ${DOCX_FILE}`);
    }
    
    const token = await getTenantAccessToken();
    const fileKey = await uploadFile(token, DOCX_FILE);
    await sendMessage(token, FEISHU_CHAT, fileKey);
    
    log('=== Delivery complete ===');
    process.exit(0);
    
  } catch (error) {
    log(`ERROR: ${error.message}`);
    console.error(error);
    process.exit(1);
  }
}

main();
