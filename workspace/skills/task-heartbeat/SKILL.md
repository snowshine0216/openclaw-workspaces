# Task-Heartbeat Skill

Background task monitoring with Feishu reporting.

## Overview

This skill enables Clover to:
- Track delegated/background tasks
- Monitor progress via heartbeat polls
- Report status updates to Feishu automatically

## Task Schema

Tasks are stored in `agents/tasks.json`:

```json
{
  "tasks": [
    {
      "id": "task-001",
      "title": "Research AI frameworks",
      "status": "in_progress",  // pending | in_progress | blocked | completed | failed
      "priority": "high",       // low | medium | high
      "createdAt": "2026-02-13T03:00:00Z",
      "updatedAt": "2026-02-13T03:30:00Z",
      "assignedTo": "sub-agent-name",  // or "self"
      "progress": 50,            // 0-100
      "notes": "Found 3 candidates",
      "reportToFeishu": true,
      "lastReportedStatus": "pending"  // track what was already reported
    }
  ],
  "lastUpdated": "2026-02-13T03:30:00Z"
}
```

## Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Created, not started |
| `in_progress` | Working on it |
| `blocked` | Stuck, needs input |
| `completed` | Done successfully |
| `failed` | Failed, needs attention |

## Heartbeat Behavior

On each heartbeat poll, Clover should:

### 1. Load Tasks
```bash
Read agents/tasks.json
```

### 2. Check Each Active Task
- Is status changed since last report?
- Is progress significant (>= 25% change)?
- Is task blocked or failed?

### 3. Report to Feishu IF:
- ✅ Status changed (pending → in_progress → completed)
- 📊 Progress milestone (25%, 50%, 75%, 100%)
- ⚠️ Blocked or failed (needs Snow's input)
- 🎉 Completed

### 4. Update Tracking
```json
// memory/heartbeat-state.json
{
  "lastReports": {
    "task-001": {
      "status": "in_progress",
      "progress": 50,
      "reportedAt": "2026-02-13T03:30:00Z"
    }
  }
}
```

## Feishu Report Format

Keep it concise:

**Progress Update:**
```
📊 [Task Name] - 50% complete
{brief status note}
```

**Blocked:**
```
⚠️ [Task Name] - Blocked
{what's needed from Snow}
```

**Completed:**
```
🎉 [Task Name] - Done!
{summary of result}
```

**Failed:**
```
❌ [Task Name] - Failed
{what went wrong + next steps}
```

## Task API

### Create Task
```javascript
// In agents/tasks.json
{
  "id": "unique-task-id",
  "title": "Task description",
  "status": "pending",
  "priority": "medium",
  "assignedTo": "self",
  "reportToFeishu": true
}
```

### Update Task
1. Read `agents/tasks.json`
2. Modify the task
3. Update `updatedAt` timestamp
4. Write back

### Complete Task
- Set `status: "completed"`, `progress: 100`
- Update `updatedAt`
- Next heartbeat will report

## File Locations

| File | Purpose |
|------|---------|
| `agents/tasks.json` | Task storage |
| `memory/heartbeat-state.json` | Track what was reported |
| `HEARTBEAT.md` | Main heartbeat instructions |

## Feishu Chat ID

```
oc_55bf80b97398600ff6da478ae62937de
```

## When NOT to Report

- Status unchanged since last report
- Progress change < 25%
- `reportToFeishu: false`
- Late night (23:00-08:00 UTC) unless urgent

---

*This skill integrates with the main HEARTBEAT.md system.*
