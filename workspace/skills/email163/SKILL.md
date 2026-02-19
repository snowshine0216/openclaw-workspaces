---
name: email163
description: Read and search 163.com (NetEase) email accounts via POP3. Use when the user wants to access their 163.com mailbox, check emails, search messages, or read specific emails from snowshine@163.com or other 163.com addresses. Handles the "Unsafe Login" IMAP issue by using POP3 protocol.
---

# Email163

Access 163.com (NetEase) email accounts using POP3 protocol.

## Important: Why POP3, Not IMAP

163.com blocks IMAP's SELECT command with "Unsafe Login" error even with valid credentials. POP3 works without this restriction.

## Quick Start

```bash
python3 scripts/email163.py check
```

## Configuration

Before using, edit `scripts/email163.py` and update:

```python
EMAIL_ADDRESS = "your_email@163.com"
AUTH_CODE = "your_authorization_code"
```

**Getting Authorization Code:**
1. Login to mail.163.com
2. Settings → POP3/SMTP/IMAP
3. Enable the service
4. Generate an authorization code (not your login password)

## Commands

### Check Connection
```bash
python3 scripts/email163.py check
```
Returns: Connection status and total email count.

### List Recent Emails
```bash
python3 scripts/email163.py list 10
```
Returns: Most recent 10 emails with id, from, subject, date.

### Read Full Email
```bash
python3 scripts/email163.py get 158
```
Returns: Complete email including body text.

### Search Emails
```bash
python3 scripts/email163.py search "招商银行"
```
Returns: Matching emails from last 200 messages.

## Output Format

All commands return JSON for easy parsing:

```json
{
  "success": true,
  "emails": [...]
}
```

## Limitations

- POP3 is read-only; cannot send or delete emails
- Search only checks last 200 emails (POP3 limitation)
- Cannot mark emails as read/unread
- Downloads full email content for reading

## Resources

### scripts/
- `email163.py` - Main script for all email operations
