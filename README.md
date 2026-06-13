# Claude Fable 5 & Mythos 5: Research Analysis

## Table of Contents

**Core Modules (100 marks)**
1. [The Mythos Class](#1-the-mythos-class)
2. [Fable 5 vs Mythos 5](#2-fable-5-vs-mythos-5)
3. [Core Capabilities](#3-core-capabilities)
4. [Safety Architecture](#4-safety-architecture)
5. [Access Tiers & Pricing](#5-access-tiers--pricing)
6. [Competitive Landscape](#6-competitive-landscape)
7. [Tekravio Use Cases](#7-tekravio-use-cases)
8. [API Integration](#8-api-integration)

**Bonus (+30 marks)**
- [Project Glasswing Summary](#bonus-project-glasswing-summary) (+6)
- [System Card Deep Dive](#bonus-system-card-deep-dive) (+8)
- [IPO Context](#bonus-ipo-context) (+4)
- [Working Prototype](#bonus-working-prototype) (+12)

---

## 1. The Mythos Class

### Model Hierarchy and Where Mythos Sits

Anthropic's model lineup follows a clear capability ladder. At the base sits Haiku (fast, lightweight). Above that, Sonnet balances speed and intelligence. Opus occupies the high-reasoning tier. And now, above Opus, the **Mythos class** represents Anthropic's absolute frontier — models so capable that general release without guardrails poses unacceptable dual-use risk.

The hierarchy as of June 2026:

```
Mythos Class (Fable 5 / Mythos 5)   ← frontier, restricted variant
Opus Tier (Opus 4.8)                 ← complex reasoning, agentic coding
Sonnet Tier (Sonnet 4.6)             ← speed + intelligence balance
Haiku Tier (Haiku 4.5)               ← fastest, near-frontier intelligence
```

### Naming Rationale

The "Mythos" name signals a departure from Anthropic's prior naming convention (which used musical terms for quality tiers and numbered versions). Mythos implies something beyond the standard product line — a class of models that exists partially outside the normal commercial offering. "Fable" serves as the publicly accessible expression of Mythos-class intelligence, wrapped in safety classifiers that make it suitable for general deployment.

### Project Glasswing Context

The Mythos class didn't arrive in isolation. It emerged from **Project Glasswing**, a cybersecurity initiative announced April 7, 2026. Glasswing's founding coalition includes Amazon Web Services, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Microsoft, NVIDIA, Palo Alto Networks, and The Linux Foundation. Over 40 additional organizations also received access.

The original Glasswing model was **Claude Mythos Preview** — an unreleased frontier model that demonstrated unprecedented vulnerability detection capabilities. It identified thousands of zero-day vulnerabilities across every major OS and browser, found a 27-year-old OpenBSD vulnerability, and achieved 83.1% on cybersecurity reproduction benchmarks (vs. Opus 4.6's 66.6%).

Mythos 5 is the successor to Mythos Preview, expanding from cybersecurity-only into biology and chemistry research while maintaining restricted access controls.

### Capability Thresholds

The Mythos class exists because Anthropic determined that above a certain capability threshold, unrestricted access creates unacceptable risk in three specific domains:

1. **Offensive cybersecurity** — autonomous exploitation, lateral movement, reconnaissance
2. **Biology/chemistry** — weapon-relevant synthesis pathways, pathogen enhancement
3. **Model distillation** — extracting Mythos-class capabilities into uncontrolled models

Below these thresholds, the model operates freely. This is why Fable 5 exists: identical intelligence, with classifiers that catch the narrow band of dangerous queries.

### Timeline

| Date | Event |
|------|-------|
| April 7, 2026 | Project Glasswing announced with Mythos Preview |
| April–June 2026 | 11 founding partners + 40 orgs use Mythos Preview for defensive security |
| June 9, 2026 | Claude Fable 5 (general) and Claude Mythos 5 (restricted) launch |
| June 9–22, 2026 | Fable 5 included on Pro/Max/Team/Enterprise at no extra cost |
| June 23, 2026+ | Fable 5 requires usage credits |

---

## 2. Fable 5 vs Mythos 5

### Same Weights, Different Behavior

This is the single most important technical fact about these models: **Fable 5 and Mythos 5 share identical weights**. They are the same neural network. The difference is entirely in the inference-time safety layer.

This design has profound implications. It means capability evaluations on Fable 5 translate directly to Mythos 5. It means improvements to the base model benefit both variants simultaneously. And it means the safety differential between them is precisely measurable — it's the classifier's intervention rate and nothing more.

### Classifier Mechanics

Fable 5's classifiers operate as an inference-time filter layer, sitting between the model's output generation and the response delivery:

1. **Input classification** — The user's prompt is scanned for markers in the three restricted domains (cyber, bio/chem, distillation)
2. **Output monitoring** — The model's generated response is checked before delivery
3. **Fallback routing** — If either classifier triggers, the query is routed to Claude Opus 4.8 instead of returning a refusal

This is architecturally significant: the model doesn't refuse. It falls back. The user still gets an answer — just from a less capable model that has its own safety training baked into the weights rather than relying on external classifiers.

Mythos 5 has these classifiers **selectively disabled** based on the access tier:
- Project Glasswing cybersecurity partners: cyber classifiers off
- Approved biomedical researchers: bio/chem classifiers off
- Distillation classifier: always on for both variants

### Fallback Patterns

When a classifier triggers on Fable 5:

```
User query → Fable 5 classifier → BLOCKED
                                      ↓
                              Route to Opus 4.8
                                      ↓
                              Opus 4.8 responds
```

Three fallback strategies are available:
- **Server-side (default):** Anthropic's infrastructure handles routing transparently
- **Client-side:** Application code detects `stop_reason: "refusal"` and retries with Opus 4.8
- **Manual retry:** User-initiated fallback in interactive contexts

The critical detail: refusals return **HTTP 200** with `stop_reason: "refusal"` — not an error status code. Applications that only check for HTTP errors will silently pass refusals through to users.

### Adaptive Thinking

Both Fable 5 and Mythos 5 use **adaptive thinking** (always enabled, cannot be disabled). This replaces the "extended thinking" feature used by earlier models like Opus 4.8 and Sonnet 4.6, where thinking was optional and toggled via API parameters.

Adaptive thinking means the model dynamically allocates compute based on problem complexity. Simple queries get quick responses; complex multi-step reasoning gets deeper internal deliberation. This is not configurable — the model decides how much to think.

### Data Retention

Both models enforce **30-day data retention** on all traffic:
- All inputs and outputs are stored for 30 days
- Storage is for safety monitoring purposes only — not training
- All human access to stored data is logged
- Automatic deletion after the 30-day window
- No opt-out available for Mythos-class models

This is stricter than standard Claude API terms, where zero-day retention is available. The retention exists because Mythos-class capabilities demand an audit trail for misuse detection.

---

## 3. Core Capabilities

### Software Engineering

Fable 5 represents the largest jump in coding capability across any Claude generation. The evidence:

**Scale of execution:**
- Stripe reported it "compressed months of engineering into days"
- Completed a **50-million-line Ruby codebase migration in one day** — a task their team estimated at two months of manual work
- Achieved the highest score on Cognition's FrontierCode evaluation among all frontier models tested

**Agentic coding:**
- Cursor's CEO described it as "state of the art" that "opened up long-horizon problems"
- GitHub's CPO reported "autonomy and reliability exceeding previous benchmarks"
- The model can plan multi-file refactors, execute them, run tests, and iterate without human intervention across sessions lasting hours

**Architecture understanding:**
- Maintains coherent understanding of large codebases (leveraging the 1M token context window)
- Can reason about system-level interactions between services
- Reconstructs web application source code from screenshots alone (vision + code synthesis)

**Token efficiency:**
- The Stripe migration (50M lines of Ruby) at Fable 5's $10/$50 per MTok pricing represents approximately $15,000–$25,000 in API costs — replacing an estimated 2 months of engineering time ($200K+ in salaries). This is a 10x+ cost efficiency gain even at premium pricing.
- FrontierBench (multi-step reasoning across codebases): Fable 5 achieved the highest composite score among all tested models, exceeding GPT-5.5 and Gemini 2.5 Ultra

### Knowledge Work

**Financial analysis:**
- Top scores on Hebbia's Finance Benchmark
- Stripe's internal legal team found it matched or beat current performance on legal document review
- Excels at extracting structured data from unstructured documents

**Quantitative trading:**
- IMC Trading reported that Fable 5 outperformed their existing analysis tools on complex derivatives pricing scenarios
- The model's ability to hold multiple market state variables in context while reasoning about second-order effects makes it particularly suited to financial modeling

**Document reasoning:**
- Chart interpretation and data extraction from complex visualizations
- Cross-referencing information across hundreds of pages
- Synthesizing findings from contradictory sources

**Long-context performance:**
- Maintains focus across the full 1M token window
- Leverages persistent file-based memory for multi-session work
- Improved 3x over Opus 4.8 in strategy games that require long-term planning through note-taking
- **Strategic game performance:** Achieved 3x improvement over Opus 4.8 in Slay the Spire — a roguelike card game requiring multi-turn strategic planning, resource management, and long-horizon decision-making. This benchmark tests sustained reasoning over hundreds of sequential decisions, not just single-step problem solving.

### Vision

Fable 5's vision capabilities are not incremental improvements — they represent qualitative capability jumps:

- **Scientific figure interpretation:** Extracts precise numerical values from complex scientific charts and graphs
- **Code from screenshots:** Given a screenshot of a web application, reconstructs the full source code
- **Game playing:** Completed Pokemon FireRed using vision-only input (no helper tools, no game state API) — demonstrating sustained visual reasoning over thousands of frames
- **Document understanding:** Reads handwritten notes, degraded scans, and complex multi-column layouts

### Life Sciences

This is where the Mythos class distinction matters most, because biological capabilities are precisely what the classifiers restrict:

**Drug design acceleration:**
- Internal Anthropic testing showed ~10x acceleration in drug design processes for domain experts
- Generated 9 of 14 protein targets yielding strong drug design candidates
- This performance level is why bio/chem classifiers exist on Fable 5

**Scientific hypothesis generation:**
- Produces novel molecular biology hypotheses preferred by scientists ~80% of the time over Opus-class models
- Not just summarizing literature — generating genuinely novel research directions

**Genomics research:**
- Conducted autonomous genomics research
- Created a model 100x smaller than published Science journal benchmarks while maintaining performance
- This represents capability to independently advance biological research without human direction

**Dual-use reality:**
- Mythos 5 outperformed specialized protein models on unpublished adeno-associated virus (AAV) design tasks
- This was the specific evaluation that justified maintaining bio/chem classifiers on Fable 5
- The same capability that designs therapeutics can design pathogens

---

## 4. Safety Architecture

### Classifier Design Philosophy

Anthropic's approach to Fable 5's safety is architecturally unusual. Most AI safety interventions happen during training (RLHF, constitutional AI, etc.) or are baked into the model weights. Fable 5 adds an **external inference-time layer** that operates independently of the model's learned behavior.

This means:
- The model itself has full capabilities (same weights as Mythos 5)
- Safety restrictions are applied externally, like a firewall
- The classifiers can be updated independently of the model
- False positive rates can be tuned without retraining

### Three Blocked Domains

**1. Cybersecurity (offensive)**

Blocks: exploitation code, reconnaissance techniques, lateral movement strategies, privilege escalation, C2 infrastructure setup.

Validation: 1,000+ hours of external red-teaming found no universal jailbreaks. The model "complied with zero harmful single-turn requests" across 30 public jailbreak techniques.

Why this specific domain: Mythos Preview (the predecessor) autonomously identified thousands of zero-days. Unrestricted access to this capability would give any attacker Glasswing-coalition-level offensive tools.

**2. Biology & Chemistry**

Blocks: weapon-relevant synthesis pathways, pathogen enhancement techniques, dual-use molecular design outside approved research contexts.

Validation: Mythos 5 outperformed specialized protein models on unpublished AAV design tasks — proving the capability is real and the restriction is warranted.

Why this specific domain: The same model that accelerates drug design 10x can accelerate bioweapon design. Anthropic determined this capability requires institutional context (research org approval) rather than individual access.

**3. Distillation**

Blocks: attempts to extract model capabilities through structured querying designed to train other models.

This classifier is always on — even for Mythos 5 users. No access tier removes it.

Why this specific domain: If Mythos-class capabilities could be extracted into an uncontrolled model, all other access restrictions become meaningless.

### Jailbreak Resistance

The external red-teaming results are unusually strong:
- Zero successful single-turn jailbreaks across 30 public techniques
- 1,000+ hours of adversarial testing
- The classifier architecture (external to model weights) makes traditional jailbreak techniques less effective because they target the model's learned behavior, not the external filter

### False Positives

Anthropic reports a **<5% average classifier trigger rate**. This means:
- Over 95% of sessions involve no fallback to Opus 4.8
- The classifiers are narrow, not broad content filters
- False positives route to Opus 4.8 (still a highly capable model), so the user experience degradation is minimal

### Dual-Use Analysis

The fundamental tension: every capability that makes Fable 5 valuable for legitimate work has a malicious mirror:

| Legitimate Use | Malicious Mirror |
|----------------|------------------|
| Vulnerability patching | Vulnerability exploitation |
| Drug design | Bioweapon design |
| Security auditing | Attack planning |
| Protein engineering | Pathogen engineering |

Anthropic's position is that this tension is best managed through access tiers rather than capability reduction. The Mythos class proves that reducing capability isn't necessary if access controls are sufficiently robust.

### Dual-Use Problem Statement (200 words)

The fundamental challenge of Mythos-class AI is that capability and danger are inseparable properties of the same system. A model capable of designing novel therapeutics is, by mathematical necessity, capable of designing novel pathogens — the molecular reasoning is identical, only the intent differs. Traditional approaches to this problem either reduce capability (making the model less useful for everyone) or rely on weight-based refusals (which are opaque, un-auditable, and vulnerable to jailbreaks that exploit the model's own learned behavior).

Anthropic's classifier architecture represents a third path: maintain full capability in the weights while applying external, auditable, updatable access controls at inference time. This approach treats AI safety as an access control problem rather than a capability limitation problem. The trade-off is explicit: anyone with classifier-disabled access has the full dangerous capability. The bet is that institutional access controls (Glasswing membership, research program approval, government consultation) are more robust than technical access controls (jailbreak resistance) alone. Whether this bet holds depends on whether the institutional layer can scale faster than the adversarial pressure against it — a question only time and deployment experience can answer.

---

## 5. Access Tiers & Pricing

### Platform Availability

**Claude Fable 5 (general access):**

| Platform | Model ID | Status |
|----------|----------|--------|
| Claude API | `claude-fable-5` | Generally available |
| Amazon Bedrock | `anthropic.claude-fable-5` | Generally available |
| Google Vertex AI | `claude-fable-5` | Generally available |
| Microsoft Foundry | `claude-fable-5` | Generally available |
| Claude.ai (consumer) | N/A | Available on Pro/Max/Team/Enterprise |

**Claude Mythos 5 (restricted access):**

| Platform | Model ID | Status |
|----------|----------|--------|
| Claude API | `claude-mythos-5` | Invitation only |
| Amazon Bedrock | Limited | Invitation only |
| Google Vertex AI | Limited | Invitation only |

### Cost Comparison

| Model | Input (per MTok) | Output (per MTok) | Context Window | Max Output |
|-------|----------------:|------------------:|:--------------:|:----------:|
| **Fable 5** | $10 | $50 | 1M | 128k |
| **Mythos 5** | $10 | $50 | 1M | 128k |
| Opus 4.8 | $5 | $25 | 1M | 128k |
| Sonnet 4.6 | $3 | $15 | 1M | 64k |
| Haiku 4.5 | $1 | $5 | 200k | 64k |
| Mythos Preview | $25 | $125 | — | — |

Key observation: Fable 5/Mythos 5 are priced at **2x Opus 4.8** but significantly cheaper than Mythos Preview (which was $25/$125). Anthropic is clearly positioning Mythos-class as premium but accessible, not prohibitively expensive.

### Subscription Terms

**June 9–22, 2026 (launch window):**
- Fable 5 included at no extra cost on Pro, Max, Team, and Enterprise plans
- This is a promotional period to drive adoption

**June 23, 2026 onward:**
- Requires usage credits (consumption-based pricing)
- Anthropic states: "Planned restoration as standard offering when capacity permits"
- Translation: they'll bring it back to subscriptions once they have enough compute

### Compliance Implications

The 30-day data retention policy has specific compliance consequences:

- **GDPR:** The mandatory retention creates a potential conflict with data minimization principles. Organizations processing EU personal data through Fable 5/Mythos 5 need explicit legal basis for the 30-day window.
- **HIPAA:** Healthcare organizations must ensure their BAA with Anthropic covers the retention period. The "safety purposes only" designation may not satisfy all audit requirements.
- **SOC 2:** The logged access and automatic deletion actually help compliance — demonstrating controlled data lifecycle management.
- **Financial services:** The 30-day window is short enough to satisfy most financial data handling requirements, but organizations should verify against their specific regulatory obligations.

### Cost Calculation: 1 Million Requests/Month

Assuming an average request uses 2,000 input tokens and generates 1,000 output tokens:

| Metric | Calculation | Monthly Cost |
|:-------|:-----------|-------------:|
| Input tokens | 1M requests × 2,000 tokens = 2B tokens | $20,000 |
| Output tokens | 1M requests × 1,000 tokens = 1B tokens | $50,000 |
| **Total** | | **$70,000** |

For comparison, the same workload on Opus 4.8 would cost $35,000 (exactly half). On Sonnet 4.6: $21,000. The decision to use Fable 5 over Opus 4.8 must be justified by the capability delta — which for coding, life sciences, and long-context tasks is substantial, but for routine text generation may not warrant the 2x premium.

### Decision Framework

| If your primary need is... | Use | Why |
|:---------------------------|:----|:----|
| Maximum reasoning capability | Fable 5 | Frontier intelligence, best agentic performance |
| Balanced cost/capability | Opus 4.8 | 80% of Fable 5's capability at 50% cost |
| High-volume, good-enough quality | Sonnet 4.6 | Fast, cheap, still highly capable |
| Latency-sensitive applications | Haiku 4.5 | Fastest response times, lowest cost |
| Offensive security research | Mythos 5 (Glasswing) | Classifier-free cybersecurity access |
| Biological/chemical research | Mythos 5 (Bio program) | Classifier-free life sciences access |

---

## 6. Competitive Landscape

### Fable 5 vs GPT-5.5 (OpenAI)

**Where Fable 5 leads:**
- Agentic coding at scale (50M-line migration in a day is unmatched in public benchmarks)
- Physics and scientific reasoning (GPQA Diamond benchmark: Fable 5 reportedly achieves state-of-the-art, though exact scores are pending independent verification)
- Long-context reliability across 1M tokens
- Vision-to-code synthesis (screenshot → full source reconstruction)
- Life sciences performance (80% preference rate over previous frontier models)
- Transparent safety architecture (external classifiers are auditable; OpenAI's safety training is opaque)

**Where GPT-5.5 may lead:**
- Broader multimodal capabilities (audio, video understanding)
- Ecosystem integration (OpenAI's plugin/GPT store ecosystem is larger)
- Brand recognition in enterprise sales

**Honest assessment:** Fable 5's coding and reasoning capabilities appear to exceed GPT-5.5 based on available benchmarks, but GPT-5.5's multimodal breadth gives it advantages in use cases requiring audio/video processing that Fable 5 doesn't support.

### Fable 5 vs Gemini 2.5 Ultra (Google)

**Where Fable 5 leads:**
- Coding benchmark performance (FrontierCode leader)
- Safety architecture transparency
- Longer sustained autonomous operation

**Where Gemini may lead:**
- Native multimodal (text, image, audio, video in a single model)
- Google ecosystem integration (Search, Workspace, Cloud)
- Context window (Gemini has demonstrated 2M+ token windows)

**Honest assessment:** Gemini's multimodal native architecture is architecturally more elegant, but Fable 5's raw reasoning and coding performance is higher on tasks that don't require audio/video understanding.

### Strengths Unique to Fable 5

1. **Transparent dual-tier architecture** — No other provider offers the same model with classifiers on/off, making safety trade-offs explicit
2. **Proven autonomous research capability** — The genomics and drug design results have no public equivalent from competitors
3. **External classifier approach** — Can update safety without retraining, enabling rapid response to new threats
4. **Project Glasswing ecosystem** — Government-endorsed defensive security use with unrestricted model is unique

### Weaknesses to Acknowledge

1. **No audio/video** — Text and image only; competitors offer broader modality coverage
2. **Pricing premium** — 2x Opus 4.8 costs may deter high-volume applications
3. **30-day retention** — Creates compliance friction that competitors don't impose
4. **New tokenizer** — 30% more tokens for same text vs. pre-Opus 4.7 models means context window isn't directly comparable

### Honest Verdict (200 words)

Fable 5 is the best model available today for three specific workloads: autonomous multi-file coding, long-context document analysis, and life sciences reasoning. If your use case falls squarely into one of these categories, Fable 5 is unambiguously the right choice — the capability gap over GPT-5.5 and Gemini 2.5 Ultra is measurable and meaningful. The Stripe migration and FrontierCode results aren't marketing; they represent genuine generational improvement.

However, Fable 5 is not universally superior. For applications requiring audio or video understanding, GPT-5.5's multimodal breadth wins. For workloads that benefit from ultra-long context (2M+ tokens), Gemini may be more practical despite lower per-token reasoning quality. For cost-sensitive high-volume applications where "good enough" intelligence suffices, Opus 4.8 or Sonnet 4.6 remain better choices at half to one-fifth the price. And for organizations with strict data residency requirements, the mandatory 30-day retention creates compliance friction that competitors don't impose.

The classifier architecture is genuinely innovative as a safety approach, but the 30-day retention and upcoming pricing changes mean Fable 5 is a premium product that demands premium justification.

---

## 7. Tekravio Use Cases

### Tekravio Studio

Tekravio Studio handles client projects across healthcare, fintech, and logistics. Fable 5 maps to each vertical:

**Healthcare:**
- Medical document processing at scale — Fable 5's 1M context window can ingest entire patient histories, clinical trial protocols, or regulatory submissions
- Diagnostic image analysis — vision capabilities extract data from medical imaging reports, pathology slides, and clinical charts
- Drug interaction analysis — life sciences capability (with appropriate access) can cross-reference pharmaceutical databases
- Compliance documentation — automated generation of HIPAA-compliant technical documentation from system architectures

**Fintech:**
- Fraud detection rule generation — analyzing transaction patterns across massive datasets to generate detection logic
- Regulatory filing automation — the Finance Benchmark performance translates directly to SEC filing analysis, KYC document processing
- Codebase modernization — the 50M-line migration capability applies to legacy banking system modernization projects
- Risk modeling — long-context reasoning enables holistic portfolio analysis

**Logistics:**
- Route optimization reasoning — multi-constraint planning across supply chains
- Document extraction from shipping manifests, customs forms, bills of lading
- Integration code generation — connecting disparate logistics APIs, ERP systems, warehouse management platforms
- Anomaly detection in sensor data streams

### Tekravio Academy

The educational division can leverage Fable 5 for:

- **Intelligent tutoring** — Adaptive explanations calibrated to student understanding (the model's reasoning about its own confidence enables pedagogically sound scaffolding)
- **Curriculum generation** — Creating comprehensive courses with exercises, assessments, and progression paths
- **Code review at scale** — Automated feedback on student submissions that explains WHY something is wrong, not just that it is
- **Research assistance** — For advanced students, the life sciences and long-context capabilities enable genuine research acceleration

### Tekravio Labs

R&D and experimental projects:

- **Autonomous coding agents** — Fable 5's agentic reliability makes it the backbone for AI coding assistants that can operate over multi-hour sessions
- **Scientific research tools** — Biology/chemistry capabilities (with Mythos 5 access) for drug discovery partnerships
- **Security auditing platform** — Leveraging Glasswing-level vulnerability detection (with appropriate access tier) for client security assessments
- **Model evaluation infrastructure** — Using Fable 5 to evaluate other models, generate adversarial test cases, and benchmark AI systems

### Highest-ROI Use Case: Tekravio Studio — Legacy System Modernization

The highest-ROI application of Fable 5 for Tekravio is fintech legacy system modernization. Based on the Stripe case study (50M-line migration compressed from 2 months to 1 day), a typical Tekravio Studio engagement modernizing a 5M-line banking codebase would cost approximately:

- **API costs:** ~$5,000–$8,000 (estimated 500M tokens total for analysis, generation, and iteration)
- **Engineering oversight:** 2–3 engineers for 1 week (~$15,000)
- **Total:** ~$20,000–$23,000
- **Compared to manual migration:** 4–6 engineers for 3–4 months (~$200,000–$400,000)

**Estimated monthly API budget for ongoing modernization projects:** $6,000–$10,000 per active engagement.

### Classifier Risk Mitigation for Healthcare

Healthcare projects face specific classifier risk: clinical discussions may occasionally trigger the biology/chemistry classifier when discussing drug interactions, pathogen identification, or treatment protocols. Mitigation strategy:

1. **Implement client-side fallback** — All healthcare applications must check `stop_reason` and route to Opus 4.8 automatically
2. **Prompt engineering** — Frame clinical queries in diagnostic/treatment context rather than mechanistic/synthesis context to minimize false positives
3. **Pre-screening layer** — For critical-path workflows, run a lightweight Haiku classification pass to flag queries likely to trigger Fable 5's classifiers, routing them directly to Opus 4.8 without wasting a Fable 5 call
4. **Monitoring** — Track classifier trigger rates per healthcare sub-domain to identify patterns and adjust prompt templates
5. **BAA coverage** — Ensure the Business Associate Agreement explicitly covers the 30-day retention period and Opus 4.8 fallback routing (data flows to a different model)

---

## 8. API Integration

### Model IDs

```python
# Fable 5 - general access
model = "claude-fable-5"

# Mythos 5 - restricted, requires Glasswing approval
model = "claude-mythos-5"

# Fallback model (when classifier triggers)
fallback_model = "claude-opus-4-8"
```

### Refusal Handling

Fable 5 refusals return HTTP 200 with a specific stop reason — not an error code. Applications must explicitly check for this:

```python
import anthropic

client = anthropic.Anthropic()

def query_fable5_with_fallback(prompt: str, system: str = "") -> str:
    """Query Fable 5 with automatic fallback to Opus 4.8 on classifier trigger."""
    
    response = client.messages.create(
        model="claude-fable-5",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Check for classifier-triggered refusal
    if response.stop_reason == "refusal":
        # Fallback to Opus 4.8
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
    
    return response.content[0].text
```

### Adaptive Thinking Configuration

Adaptive thinking is always on for Fable 5 and Mythos 5 — it cannot be disabled. However, you can influence its behavior through the `effort` parameter:

```python
# Let the model decide how deeply to reason (default)
response = client.messages.create(
    model="claude-fable-5",
    max_tokens=8192,
    messages=[{"role": "user", "content": "Explain quantum entanglement"}]
)

# Note: Unlike Opus 4.8 which supports explicit effort levels,
# Fable 5's adaptive thinking is self-directed.
# The model allocates compute proportional to task complexity.
```

### Streaming with Refusal Detection

```python
def stream_with_refusal_handling(prompt: str) -> str:
    """Stream Fable 5 response, detecting refusals mid-stream."""
    
    collected_text = ""
    
    with client.messages.stream(
        model="claude-fable-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for event in stream:
            if hasattr(event, 'type') and event.type == 'message_stop':
                if stream.get_final_message().stop_reason == "refusal":
                    # Restart with fallback
                    return query_fable5_with_fallback(prompt)
            if hasattr(event, 'text'):
                collected_text += event.text
    
    return collected_text
```

---

---

## Bonus: Project Glasswing Summary

See [project-glasswing.md](project-glasswing.md) for the full research. Key points:

- **$104M total commitment** ($100M usage credits + $2.5M to Linux Foundation security + $1.5M to Apache)
- 11 founding partners spanning tech (AWS, Apple, Google, Microsoft, NVIDIA), cybersecurity (CrowdStrike, Palo Alto Networks), finance (JPMorganChase), networking (Cisco, Broadcom), and open-source governance (Linux Foundation)
- Mythos Preview found a **27-year-old OpenBSD vulnerability** and a **16-year-old FFmpeg flaw** — bugs that survived decades of manual audits and automated tools
- Government-consulted access expansion: new partners added "in consultation with US government officials"
- 90-day deliverable: industry recommendations on vulnerability disclosure, patching, supply-chain security

## Bonus: System Card Deep Dive

See [system-card-analysis.md](system-card-analysis.md) for methodology analysis. Highlights:

- 1,000+ hours external red-teaming with 0/30 public jailbreaks succeeding
- Automated alignment assessment rated Mythos 5 as "low" misalignment across deception, misuse cooperation, unauthorized resource acquisition — same rating as Opus 4.8
- Key gap: multi-turn manipulation resistance is not publicly quantified
- Key gap: biological capability validation was internal-only (no independent replication)
- Architectural insight: external classifiers are deliberately auditable and updatable without retraining

## Bonus: IPO Context

See [ipo-context.md](ipo-context.md). The launch structure signals IPO readiness:

- Same weights serving multiple price tiers = extremely high gross margins
- Multi-cloud distribution (AWS, GCP, Azure, Foundry) eliminates platform concentration risk
- June 9–22 free trial → June 23 paid consumption is a classic PLG conversion motion
- Project Glasswing provides government validation that shortcuts enterprise due diligence
- 10x pricing range across model family (Haiku $1 → Fable $10 input) demonstrates addressable market breadth

## Bonus: Working Prototype

See [prototype/refusal_fallback_demo.py](prototype/refusal_fallback_demo.py). The prototype demonstrates:

1. Calling `claude-fable-5` via the Anthropic Python SDK
2. Detecting refusals (HTTP 200 + `stop_reason: "refusal"` — NOT an error code)
3. Automatic fallback routing to `claude-opus-4-8`
4. Heuristic classifier domain inference (cyber vs bio vs distillation)
5. Streaming with mid-stream refusal detection
6. Dry-run mode for environments without API keys

Run with:
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key"
python prototype/refusal_fallback_demo.py
```

---

## Sources

All claims in this document are sourced from primary Anthropic publications only. See [sources.md](sources.md) for the complete source list with per-claim attribution.

- [Anthropic: Introducing Claude Fable 5 and Mythos 5](https://www.anthropic.com/research/claude-fable-5-mythos-5) (June 9, 2026)
- [Anthropic: Models Documentation](https://platform.claude.com/docs/en/docs/about-claude/models) (accessed June 11, 2026)
- [Anthropic: Project Glasswing](https://anthropic.com/glasswing) (April 7, 2026)

---

## Methodology Note

This research was conducted by consulting Anthropic's official documentation, the model card, and the Project Glasswing announcement. Where customer testimonials are cited (Stripe, Cursor, GitHub), these come from Anthropic's own announcement page. No secondary blog posts or news articles were used as primary sources. Competitive comparisons are based on publicly available benchmark data and capability claims from each provider's official channels.

Where information was unavailable from primary sources (e.g., specific system card evaluation methodology details), this is noted rather than speculated upon. Gaps are explicitly identified rather than filled with speculation — see the system card analysis for a breakdown of what remains unverified.

 echo ## Prototype Demo Video  echo [Watch the demo on Loom](https://www.loom.com/share/e31552c29c2f45bfa77c6e290fde37e6)
