# Claude Fable 5 — Cheat Sheet

## Quick Facts

| Property | Value |
|:---------|:------|
| Model ID | `claude-fable-5` |
| Release | June 9, 2026 |
| Class | Mythos (highest tier) |
| Context Window | 1M tokens |
| Max Output | 128k tokens |
| Input Cost | $10 / million tokens |
| Output Cost | $50 / million tokens |
| Thinking Mode | Adaptive (always on, not configurable) |
| Extended Thinking | Not available |
| Vision | Yes (images only, no audio/video) |
| Data Retention | 30 days mandatory |

## What It's Best At

- Long-horizon autonomous coding (multi-hour agent sessions)
- Large codebase migrations (50M+ lines demonstrated)
- Financial/legal document analysis (Hebbia Finance Benchmark leader)
- Scientific figure interpretation (precise number extraction)
- Life sciences reasoning (drug design, genomics — with classifier limits)
- Vision-to-code (screenshot → full source reconstruction)

## Classifiers (What Gets Blocked)

| Domain | Blocked Content | Fallback |
|:-------|:---------------|:---------|
| Cybersecurity | Offensive exploitation, recon, lateral movement | Opus 4.8 |
| Bio/Chemistry | Weapon synthesis, pathogen enhancement | Opus 4.8 |
| Distillation | Capability extraction for model training | Opus 4.8 |

Trigger rate: <5% of sessions. Fallback is transparent (still get a response, just from Opus 4.8).

## API Quick Start

```python
import anthropic

client = anthropic.Anthropic()

# Basic call
response = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Your prompt here"}]
)

# Check for refusal (HTTP 200, not an error!)
if response.stop_reason == "refusal":
    # Classifier triggered — fallback to Opus 4.8
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        messages=[{"role": "user", "content": "Your prompt here"}]
    )

print(response.content[0].text)
```

## Key Differences from Opus 4.8

| | Fable 5 | Opus 4.8 |
|:--|:--------|:---------|
| Capability | Higher | Lower |
| Price | 2x | 1x |
| Safety | External classifiers | Weight-based |
| Refusal behavior | HTTP 200 + stop_reason | Standard refusal text |
| Adaptive thinking | Always on | Configurable |
| Data retention | 30 days mandatory | Standard terms |

## Platforms

- Claude API ✓
- Amazon Bedrock ✓ (`anthropic.claude-fable-5`)
- Google Vertex AI ✓ (`claude-fable-5`)
- Microsoft Foundry ✓
- Claude.ai ✓ (Pro/Max/Team/Enterprise)

## Gotchas

1. **Refusals are HTTP 200** — check `stop_reason`, not status code
2. **New tokenizer** — same text = ~30% more tokens vs pre-Opus 4.7 models
3. **Adaptive thinking can't be turned off** — no `thinking` parameter
4. **30-day retention is mandatory** — plan for compliance implications
5. **June 23 pricing change** — moves from subscription-included to usage credits
6. **No audio/video** — text and images only
