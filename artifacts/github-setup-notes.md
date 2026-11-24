# GitHub Setup — Yæl Méndez

## Status
- ✅ SSH key generated: `~/.ssh/id_ed25519`
- ✅ SSH agent loaded: `ssh-add -l` confirms key is active
- ✅ Git config: `user.name = Yæl Méndez`, `user.email = yaelmendez@lutheraninstitute.github.io`
- ⏳ GitHub CLI (`gh` v2.65.0): installed but not authenticated
- ⏳ GitHub repos: not yet configured

## Next steps

### 1. Authenticate gh CLI
```
gh auth login
```
Options:
- Protocol: **HTTPS** (easiest, no SSH setup needed)
- Sign in with GitHub (browser flow)
- Or: **SSH protocol** (use existing `~/.ssh/id_ed25519`)

### 2. Verify authentication
```
gh auth status
```

### 3. Create repositories
```
# Personal/R&D
gh repo create MYaelMendez --description "Yæl Méndez — agentic engineering R&D" --public

# Lutheran Institute (LATAM)
gh repo create LutheranInstitute --description "Lutheran Institute — LATAM open classroom" --public
```

### 4. Set up GitHub Pages
Each repo needs a `gh-pages` branch or GitHub Pages source set to `main`:

```bash
# For lutheraninstitute.github.io
cd LutheranInstitute
git checkout -b gh-pages
git commit --allow-empty -m "Initial GitHub Pages deployment"
git push origin gh-pages
```

Or enable in repo settings: Settings → Pages → Source → Deploy from a branch

### 5. Verify SSH access
```
ssh -T git@github.com
# Should respond: Hi yaelmendez! You've successfully authenticated...
```

## Context — repos mentioned
- `MYaelMendez` (R&D): agentic engineering, hermes fork
- `LutheranInstitute` (LATAM): open classroom, diplomado, emprendelatam
- `NousResearch/hermes-agent`: the platform we fork from
- `cli.llc`: command interface
- `daollc.ai`: DAO LLC
- `privateclient.ai`: agent as draftsman
- `llm.store`: ecommerce blueprint
- `æææ.com`: omniversal portal
- `soværeign.com`: sovereignty thesis layer
- `Teologia.ai`: theology

## Local config
```bash
git config --global user.name "Yæl Méndez"
git config --global user.email "yaelmendez@lutheraninstitute.github.io"
```

## Key files
- `~/.ssh/id_ed25519` — private key
- `~/.ssh/id_ed25519.pub` — public key (add to GitHub: Settings → SSH and GPG keys)
