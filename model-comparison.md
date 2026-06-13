# Model Comparison: Fable 5, Mythos 5, Opus 4.8, Sonnet 4.6

## Specifications Overview

| Specification | Claude Fable 5 | Claude Mythos 5 | Claude Opus 4.8 | Claude Sonnet 4.6 |
|:--------------|:---------------|:----------------|:----------------|:------------------|
| **API Model ID** | `claude-fable-5` | `claude-mythos-5` | `claude-opus-4-8` | `claude-sonnet-4-6` |
| **Class** | Mythos | Mythos | Opus | Sonnet |
| **Release Date** | June 9, 2026 | June 9, 2026 | 2026 | 2025 |
| **Context Window** | 1M tokens | 1M tokens | 1M tokens | 1M tokens |
| **Max Output** | 128k tokens | 128k tokens | 128k tokens | 64k tokens |
| **Input Price** | $10/MTok | $10/MTok | $5/MTok | $3/MTok |
| **Output Price** | $50/MTok | $50/MTok | $25/MTok | $15/MTok |
| **Extended Thinking** | No | No | No | Yes |
| **Adaptive Thinking** | Yes (always on) | Yes (always on) | Yes | Yes |
| **Latency** | Moderate | Moderate | Moderate | Fast |
| **Access** | General | Invitation only | General | General |

## Safety & Classifier Differences

| Feature | Fable 5 | Mythos 5 | Opus 4.8 | Sonnet 4.6 |
|:--------|:--------|:---------|:---------|:-----------|
| **Cyber classifier** | ON | OFF (Glasswing partners) | N/A (weight-based safety) | N/A |
| **Bio/chem classifier** | ON | OFF (approved researchers) | N/A | N/A |
| **Distillation classifier** | ON | ON | N/A | N/A |
| **Data retention** | 30 days mandatory | 30 days mandatory | Standard API terms | Standard API terms |
| **Fallback on block** | Routes to Opus 4.8 | N/A | Self-handles | Self-handles |
| **Classifier trigger rate** | <5% average | N/A | N/A | N/A |

## Capability Comparison

| Capability | Fable 5 | Mythos 5 | Opus 4.8 | Sonnet 4.6 |
|:-----------|:--------|:---------|:---------|:-----------|
| **Software engineering** | Frontier (FrontierCode leader) | Same as Fable 5 | High | High |
| **Long-horizon agentic work** | Best available | Same as Fable 5 | Strong | Moderate |
| **Vision/image understanding** | Advanced (code from screenshots) | Same as Fable 5 | Strong | Strong |
| **Life sciences** | Advanced (with classifier limits) | Full unrestricted | Moderate | Moderate |
| **Finance/legal analysis** | State of the art | Same as Fable 5 | Strong | Good |
| **Offensive security** | Blocked by classifier | Full (Glasswing only) | Weight-based refusal | Weight-based refusal |
| **Long-context reliability** | Highest | Same as Fable 5 | High | High |

## Platform Availability

| Platform | Fable 5 | Mythos 5 | Opus 4.8 | Sonnet 4.6 |
|:---------|:--------|:---------|:---------|:-----------|
| Claude API | Yes | Invitation only | Yes | Yes |
| Amazon Bedrock | Yes | Limited | Yes | Yes |
| Google Vertex AI | Yes | Limited | Yes | Yes |
| Microsoft Foundry | Yes | — | — | — |
| Claude.ai (consumer) | Yes (Pro/Max/Team/Enterprise) | No | Yes | Yes |

## Key Architectural Differences

### Fable 5 vs Mythos 5
- **Identical model weights** — same neural network, different classifier configuration
- Both use adaptive thinking (always on, self-directed compute allocation)
- Both share 30-day mandatory data retention
- Difference is purely in which safety classifiers are active

### Mythos Class vs Opus Class
- Mythos class sits above Opus in the capability hierarchy
- Mythos uses external classifiers; Opus relies on weight-based (trained-in) safety
- Mythos demonstrates measurably higher performance on coding, reasoning, and life sciences benchmarks
- Mythos costs 2x the price of Opus
- When Fable 5's classifier triggers, it falls BACK to Opus 4.8 — confirming the hierarchy

### Opus 4.8 vs Sonnet 4.6
- Opus prioritizes reasoning depth; Sonnet prioritizes speed
- Opus has 128k max output; Sonnet has 64k
- Opus uses adaptive thinking; Sonnet supports both extended and adaptive thinking
- Opus costs ~67% more than Sonnet
- Both share 1M context windows

## Tokenizer Note

Fable 5 and Mythos 5 use the tokenizer introduced with Claude Opus 4.7. Compared to models before Opus 4.7, the same text produces roughly **30% more tokens**. This means the 1M context window is not directly comparable to pre-4.7 models' 1M windows — effective capacity is ~23% less text for the same token count.
