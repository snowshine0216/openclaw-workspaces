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

## Python env setup with `uv`

If you hit `error: externally-managed-environment` with system `pip`, use a project-local virtual environment.

Run this inside your project directory:

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# create and activate venv
uv venv
source .venv/bin/activate

# install package from GitHub zip
uv pip install "agent-reach @ https://github.com/Panniantong/agent-reach/archive/main.zip"
```

Notes:
- Run `uv venv` in the folder where you want `.venv` to live.
- Use `uv` (not `u`).

## MCPorter + Exa setup

Use this if you want `mcporter` to call Exa search tools via MCP.

```bash
# 1) install mcporter (optional globally; you can also use npx)
npm i -g mcporter

# 2) persist Exa API key in your shell
# replace with your real key
 echo 'export EXA_API_KEY="YOUR_EXA_API_KEY"' >> ~/.bashrc
source ~/.bashrc

# 3) add Exa MCP server to mcporter home config
mcporter config --config ~/.mcporter/mcporter.json add exa --transport stdio --stdio "npx -y exa-mcp-server" --env 'EXA_API_KEY=${EXA_API_KEY}'

# 4) verify tools are visible
mcporter list exa --all-parameters

# 5) smoke test
mcporter call exa.web_search_exa query="latest OpenClaw docs" numResults=5
```

Notes:
- Project-local config alternative: replace `--config ~/.mcporter/mcporter.json` with `--config ./config/mcporter.json`.
- If your shell is `zsh`, persist the key in `~/.zshrc` instead of `~/.bashrc`.
