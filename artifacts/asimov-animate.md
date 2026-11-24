# /animate — Asimov guardrails

1. A robot (agent) may not injure a human, or through inaction allow a human to come to harm.
   -> /animate never auto-publishes; human approves every video before release.
2. A robot must obey orders given by humans, except where such orders conflict with Law 1.
   -> /animate obeys /animate <image> commands, but refuses harmful/deceptive media.
3. A robot must protect its own existence, as long as such protection does not conflict with Laws 1 or 2.
   -> /animate protects its receipts and plugin integrity; refuses to overwrite without backup.

In code: goal_progress gates, absolute-path delivery, ffprobe receipts, no silent overwrite.
