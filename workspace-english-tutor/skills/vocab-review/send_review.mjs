#!/usr/bin/env node
// Send daily vocab review to Feishu
// Called by cron after vocab.py generates the .docx

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const SCRIPT_DIR = '/root/.openclaw/agents/english-tutor/workspace/skills/vocab-review';
const DOCX_FILE = path.join(SCRIPT_DIR, 'daily_review.docx');
const LOG_FILE = path.join(SCRIPT_DIR, 'review.log');
const FEISHU_CHAT = 'oc_55bf80b97398600ff6da478ae62937de';

function log(message) {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(LOG_FILE, `${timestamp}: ${message}\n`);
}

async function main() {
  try {
    const today = new Date().toISOString().split('T')[0];
    
    if (!fs.existsSync(DOCX_FILE)) {
      log(`ERROR - Document not found: ${DOCX_FILE}`);
      process.exit(1);
    }
    
    log('Sending document to Feishu via message tool...');
    
    // The message tool is available through OpenClaw's tool system
    // We need to use a different approach - write a signal file
    // that the agent's heartbeat will detect and send
    
    const signalFile = path.join(SCRIPT_DIR, '.send_review');
    fs.writeFileSync(signalFile, JSON.stringify({
      chatId: FEISHU_CHAT,
      filePath: DOCX_FILE,
      filename: `daily_review_${today}.docx`,
      caption: `📚 Daily Vocabulary Review - ${today}`,
      timestamp: new Date().toISOString()
    }));
    
    log(`Signal file created: ${signalFile}`);
    log('Review complete - waiting for heartbeat to send');
    
  } catch (error) {
    log(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

main();
