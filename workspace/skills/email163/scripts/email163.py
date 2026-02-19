#!/usr/bin/env python3
"""
163.com Email Reader using POP3
163.com blocks IMAP SELECT, but POP3 works fine.
"""

import poplib
import email
from email.header import decode_header
import ssl
import json
import sys

# Configuration
EMAIL_ADDRESS = "snowshine@163.com"
AUTH_CODE = "DPeczLzezwXJc6jg"
POP3_SERVER = "pop.163.com"
POP3_PORT = 995

def decode_str(s):
    """Decode email header string."""
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            if charset:
                try:
                    result.append(part.decode(charset))
                except:
                    result.append(part.decode('utf-8', errors='ignore'))
            else:
                result.append(part.decode('utf-8', errors='ignore'))
        else:
            result.append(str(part))
    return ''.join(result)

def get_email_body(msg):
    """Extract plain text body from email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            if "attachment" in content_disposition:
                continue
                
            if content_type == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    body = payload.decode(charset, errors='ignore')
                    break
                except:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or 'utf-8'
            body = payload.decode(charset, errors='ignore')
        except:
            pass
    return body

def connect():
    """Connect to POP3 server."""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    pop = poplib.POP3_SSL(POP3_SERVER, POP3_PORT, context=context)
    pop.user(EMAIL_ADDRESS)
    pop.pass_(AUTH_CODE)
    return pop

def check_connection():
    """Test connection to POP3 server."""
    try:
        pop = connect()
        stats = pop.stat()
        email_count = stats[0]
        total_size = stats[1]
        pop.quit()
        return {
            "success": True, 
            "message": f"Connected! Found {email_count} emails ({total_size} bytes total)."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_emails(limit=10):
    """List recent emails (most recent first)."""
    try:
        pop = connect()
        stats = pop.stat()
        total_emails = stats[0]
        
        # Get email list
        email_list = pop.list()[1]
        
        # Get the most recent emails (POP3 lists oldest first)
        start_idx = max(1, total_emails - limit + 1)
        results = []
        
        for i in range(total_emails, start_idx - 1, -1):
            # Get email headers only (first few lines)
            try:
                lines = pop.top(i, 0)[1]  # Get headers only
                raw_email = b'\r\n'.join(lines)
                msg = email.message_from_bytes(raw_email)
                
                subject = decode_str(msg.get("Subject", ""))
                from_ = decode_str(msg.get("From", ""))
                date = msg.get("Date", "")
                
                results.append({
                    "id": i,
                    "from": from_,
                    "subject": subject,
                    "date": date
                })
            except Exception as e:
                results.append({
                    "id": i,
                    "error": str(e)
                })
        
        pop.quit()
        return {"success": True, "total": total_emails, "emails": results}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_email(email_id):
    """Get full email by ID."""
    try:
        pop = connect()
        
        # Get full email
        lines = pop.retr(int(email_id))[1]
        raw_email = b'\r\n'.join(lines)
        msg = email.message_from_bytes(raw_email)
        
        subject = decode_str(msg.get("Subject", ""))
        from_ = decode_str(msg.get("From", ""))
        to = decode_str(msg.get("To", ""))
        date = msg.get("Date", "")
        body = get_email_body(msg)
        
        pop.quit()
        
        return {
            "success": True,
            "email": {
                "id": email_id,
                "from": from_,
                "to": to,
                "subject": subject,
                "date": date,
                "body": body
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def search_emails(query, limit=20):
    """Search emails by subject or sender (downloads and searches)."""
    try:
        pop = connect()
        stats = pop.stat()
        total_emails = stats[0]
        query_lower = query.lower()
        results = []
        
        # Search from newest to oldest
        for i in range(total_emails, max(0, total_emails - 200), -1):  # Check last 200 emails
            try:
                lines = pop.top(i, 50)[1]  # Get headers + some body
                raw_email = b'\r\n'.join(lines)
                msg = email.message_from_bytes(raw_email)
                
                subject = decode_str(msg.get("Subject", ""))
                from_ = decode_str(msg.get("From", ""))
                date = msg.get("Date", "")
                
                # Check if query matches subject or sender
                if query_lower in subject.lower() or query_lower in from_.lower():
                    results.append({
                        "id": i,
                        "from": from_,
                        "subject": subject,
                        "date": date
                    })
                    
                    if len(results) >= limit:
                        break
            except:
                pass
        
        pop.quit()
        return {"success": True, "query": query, "results": results}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python email163.py <command> [args]\nCommands: check, list [limit], get <id>, search <query>"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        result = check_connection()
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = list_emails(limit)
    elif command == "get":
        if len(sys.argv) < 3:
            result = {"error": "Usage: python email163.py get <email_id>"}
        else:
            result = get_email(sys.argv[2])
    elif command == "search":
        if len(sys.argv) < 3:
            result = {"error": "Usage: python email163.py search <query>"}
        else:
            result = search_emails(sys.argv[2])
    else:
        result = {"error": f"Unknown command: {command}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
