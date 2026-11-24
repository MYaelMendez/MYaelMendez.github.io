---
name: asimov-c2
description: "Use when commanding the Asimov robot. Mobile command and control suite with receipts."
---

# Asimov 9:19 — Mobile Command and Control

## When to Use
Use when the user wants to command the Asimov robot, check its status, or review receipts.

## Tools
- `asimov_command(action, target)` — send a command (STAND, WALK, WAVE, SCAN, SIT, DANCE, SPEAK, GRAB, RELEASE, HOME, CALIBRATE, SHUTDOWN)
- `asimov_status()` — get current robot status
- `asimov_receipts(limit)` — get the receipt log

## Principles
- HUMAN://ROOT — every command traces to a human root
- Receipts on every action — public, verifiable
- Authority not transferable
- Mobile-first — terse output, quick commands

## Mobile Commands
```
æ STAND
æ WALK
æ WAVE
æ SCAN
æ SIT
æ DANCE
æ HOME
æ CALIBRATE
æ SHUTDOWN
```

## Receipts
Every action produces a receipt with timestamp, action, status, and authority.
