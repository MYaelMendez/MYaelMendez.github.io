# NAICS Blueprint for Agentic Entrepreneurship Companies

This is classification guidance for #opensourceware #250 and related æ blueprints. NAICS choices should follow the company's **primary revenue activity**. This is not legal/tax advice.

## Core default

```txt
541511_custom-agent-services
```

Use **541511 — Custom Computer Programming Services** as the default when the business primarily builds custom agents, automations, software workflows, or AI implementations for customers.

## Blueprint mappings

### #startabusiness / cli.llc

```txt
541511 if custom automation/software services
541512 if systems design/integration
541618 if primarily business consulting
```

### #llmstore

```txt
513210 / 511210 if publishing software/tools
518210 if hosting/model/app infrastructure
541511 if custom AI implementation
```

### #daollc

```txt
541618 if consulting/formation guidance
541511 if building formation automation software
avoid implying legal services unless actually licensed
```

### #privateclient.ai

```txt
541511 custom private AI systems
541512 integrated private-client compute/session systems
518210 if hosted private agent infrastructure
```

### #commandprompt.ai

```txt
541511 custom CLI/agent software
513210 / 511210 if publishing CLI tools
```

### #reachy-clerk

```txt
541511 if software/app development for Reachy
541512 if integrating robot + payment + systems
541715 if actual robotics R&D
459999 / retail code only if the robot is selling goods directly
```

### #osw250

```txt
611430 if training/development program
541618 if business consulting
541511 if the deliverable is custom agent software
```

## Decision tree

```txt
custom AI/agent builds?          → 541511
integrated agentic systems?      → 541512
published SaaS/app/product?      → 513210 / 511210
hosted agent infrastructure?     → 518210
business consulting?             → 541618
training / owner development?    → 611430
robotics R&D?                    → 541715
retail/ecommerce?                → retail/ecommerce NAICS such as 459999 where appropriate
```

## ^æ notation

```txt
NAICS_agentic:
  custom_agentˢᵛᶜ → 541511
  systemsᶦⁿᵗᵉᵍ → 541512
  SaaSᵖᵘᵇ → 513210/511210
  hostingᶦⁿᶠʳᵃ → 518210
  consultingᵇⁱᶻ → 541618
  trainingᵉᵈᵘ → 611430
  robotᴿᴰ → 541715/541512
```

## Boundary

NAICS codes are administrative/statistical classifications. They do not create legal permissions, licenses, tax advice, or professional authorization. For formation, banking, tax, and government filings, the founder should choose the code that best matches actual revenue activity and consult qualified professionals when needed.
