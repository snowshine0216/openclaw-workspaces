# OpenClaw + Codex via tmux (server runbook)

This repo is the server-side workspace used by OpenClaw.

This README documents the **tmux-based Codex integration** we tested: run the `codex` CLI inside a persistent tmux session, then have OpenClaw interact with it by reading pane output and sending keystrokes.

## Why tmux (vs ACP)

- **tmux**: best when Codex is interactive (TTY prompts, approvals, UI). OpenClaw can drive it with `tmux capture-pane` + `tmux send-keys`.
- **ACP**: best for non-interactive, managed runs (`/acp spawn codex ...`). Great for automation, but can be blocked by non-interactive permission prompts.

If you prefer interactive control, tmux is the right choice.

## Prereqs

- `tmux` installed on the server
  - Check: `command -v tmux`
- `codex` CLI installed and runnable
  - Check: `codex --version`

## Create and run Codex in tmux

Create a persistent session named `codex` and start Codex inside it.

Option A (two-step):

```bash
tmux new-session -d -s codex
tmux attach -t codex
# inside tmux:
codex
```

Option B (auto-start Codex):

```bash
tmux new-session -d -s codex "codex"
```

Detach from tmux any time:
- `Ctrl-b` then `d`

## How OpenClaw interacts with Codex (the mechanics)

OpenClaw (or you) can control the Codex CLI by targeting the tmux session.

- **Read output** (tail last 50 lines):

```bash
tmux capture-pane -t codex -p | tail -50
```

- **Send a message** (text + Enter):

```bash
tmux send-keys -t codex -l -- "Explore the workspace and summarize findings."
tmux send-keys -t codex Enter
```

- **Stop current action** (Ctrl+C):

```bash
tmux send-keys -t codex C-c
```

Notes:
- If you have multiple panes/windows, you can target `session:window.pane` (example: `codex:0.0`).

## Suggested “routing rule” for humans

Default operating rule:

- Default tmux target: **`codex`**
- When you say: **“use codex to do X”**
- OpenClaw should: interact with the running Codex CLI by targeting tmux session **`codex`** and driving it via `tmux send-keys` + `tmux capture-pane`.

If you rename the session or move Codex to another pane/window, update the target (e.g. `codex:0.0`).

## Recovery / if tmux goes wrong

Yes — if tmux/Codex gets into a bad state, OpenClaw can re-initiate it (same as you would manually).

Common fixes:

1) Check sessions:
```bash
tmux ls
```

2) If `codex` session is missing, recreate it:
```bash
tmux new-session -d -s codex "codex"
```

3) If Codex is stuck, send Ctrl+C:
```bash
tmux send-keys -t codex C-c
```

4) If the session is irrecoverable, kill + recreate:
```bash
tmux kill-session -t codex
tmux new-session -d -s codex "codex"
```

## Safety notes

- tmux control is powerful: it can execute anything the server user can execute.
- Prefer a dedicated session name (like `codex`) to avoid sending keystrokes to the wrong process.
