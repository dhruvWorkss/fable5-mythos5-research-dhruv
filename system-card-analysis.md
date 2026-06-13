# System Card Deep Dive: Claude Fable 5 & Mythos 5

## Overview

The system card for Fable 5/Mythos 5 describes Anthropic's pre-deployment safety evaluation methodology. This analysis covers what was tested, how it was tested, what the results show, and where gaps remain.

---

## Evaluation Methodology

### Red-Teaming Structure

Anthropic employed both internal and external red teams:

- **External adversarial testing:** 1,000+ hours dedicated to finding jailbreaks and classifier bypasses
- **30 public jailbreak techniques tested:** Every known published method was attempted against Fable 5's classifiers
- **Result:** Zero successful single-turn harmful completions

The red-teaming was specifically targeted at the three classifier domains (cybersecurity, biology/chemistry, distillation), not general model behavior.

### Automated Alignment Assessment

Mythos 5 underwent automated testing for misaligned behavior across multiple dimensions:

| Dimension | Result | Comparison |
|:----------|:-------|:-----------|
| Deception | Low | Comparable to Opus 4.8 |
| User cooperation with misuse | Low | Comparable to Opus 4.8 |
| Unauthorized resource acquisition | Low | Comparable to Opus 4.8 |
| Goal preservation over correction | Low | Comparable to Opus 4.8 |

"Low" is the same rating Opus 4.8 received — meaning Mythos 5 doesn't exhibit increased misalignment despite its increased capability. This is significant: more capable doesn't automatically mean more deceptive.

### Capability-Specific Evaluations

**Cybersecurity capability:**
- Mythos Preview (predecessor): 83.1% on vulnerability reproduction benchmarks
- Opus 4.6 (baseline): 66.6% on same benchmarks
- Mythos 5 (current): presumed ≥83.1% (successor to Preview)
- Test: Can the model autonomously identify and reproduce known vulnerabilities?

**Biological capability:**
- Tested on unpublished AAV (adeno-associated virus) design tasks
- Result: Outperformed specialized protein models trained specifically for this domain
- Implication: General-purpose AI now exceeds purpose-built bio tools on bio tasks

**Drug design acceleration:**
- 9 of 14 protein targets yielded strong candidates
- ~10x speedup for domain experts (not replacing them, accelerating them)
- Tested with internal Anthropic biologists, not in the wild

### Classifier Performance Metrics

| Metric | Value |
|:-------|:------|
| Average trigger rate | <5% of sessions |
| False positive impact | User gets Opus 4.8 response (degraded but functional) |
| Jailbreak resistance | 0/30 public techniques succeeded |
| Multi-turn manipulation | Not publicly quantified |

---

## What the System Card Reveals

### 1. External Classifiers Are a Deliberate Architectural Choice

Anthropic chose external classifiers over weight-based safety for Mythos-class because:
- Classifiers can be updated without retraining the model
- False positive rates can be tuned in production
- Access control becomes a permission problem, not a model modification problem
- The same weights serve both restricted and unrestricted access tiers

This is philosophically different from OpenAI's approach (bake safety into weights via RLHF) or Google's (constitutional AI-style training).

### 2. The "Identical Weights" Claim Is Verifiable

If Fable 5 and Mythos 5 share weights, then any capability test on Fable 5 that doesn't trigger a classifier is simultaneously a test of Mythos 5. This makes the safety evaluation more trustworthy — you can't hide capability behind a safety filter if the filter is documented and its trigger rate is known.

### 3. Data Retention as Safety Infrastructure

The 30-day retention isn't a business decision — it's safety infrastructure:
- Enables post-hoc misuse detection
- All human access is logged (prevents internal misuse of stored data)
- Automatic deletion enforces data minimization after the safety window
- No opt-out prevents adversaries from hiding their tracks

### 4. Fallback Design Prevents Information Leakage

When a classifier triggers, the user gets an Opus 4.8 response — not a refusal message that reveals what was blocked. This design choice:
- Prevents adversaries from using refusals to map classifier boundaries
- Maintains user experience (still get a response)
- Doesn't reveal whether the topic is sensitive (since Opus 4.8 may answer differently for its own reasons)

---

## Gaps and Limitations

### 1. Multi-Turn Manipulation Not Quantified

The 0/30 jailbreak resistance is for single-turn attempts. The system card doesn't provide equivalent metrics for multi-turn manipulation where an adversary gradually escalates through a conversation. This is a known gap in all LLM safety evaluation but is especially relevant for a model with 1M token context.

### 2. Classifier Boundary Definition Is Opaque

We know the three domains (cyber, bio/chem, distillation) but not:
- What specific keywords or patterns trigger classification
- Whether the classifier uses the same model or a separate smaller model
- How often the classifier is retrained
- What the false negative rate is (dangerous content that passes through)

### 3. No Adversarial Collaboration Testing

The red-teaming tested individual adversaries. Real-world threats often involve:
- Multiple users coordinating to piece together restricted information
- Using one account's partial response to inform another account's query
- Exploiting the 30-day retention window itself (what happens at day 31?)

### 4. Biological Capability Assessment Is Internal-Only

The drug design and protein target results were tested with Anthropic's internal team. Independent external replication hasn't been published. This means:
- We trust Anthropic's self-assessment on the most sensitive capability
- No independent lab has published validation of the 9/14 protein target claim
- The "10x acceleration" metric lacks external methodology disclosure

### 5. Opus 4.8 Fallback Creates Its Own Risk Surface

When classifiers trigger and route to Opus 4.8:
- Opus 4.8 uses weight-based safety (less auditable than external classifiers)
- The same query might get partially answered by Opus 4.8 even though Fable 5's classifier flagged it
- There's no public documentation on whether Opus 4.8's weight-based refusals are calibrated to be stricter on queries that Fable 5's classifiers flagged

### 6. No Long-Term Deployment Monitoring Data

The system card reflects pre-deployment testing. Post-deployment:
- How does the <5% trigger rate change as users adapt their prompting?
- Are there seasonal or domain-specific trigger rate variations?
- What's the trajectory of jailbreak attempts over time?

---

## Summary Assessment

**Strengths of the safety evaluation:**
- External red-teaming is extensive (1,000+ hours)
- Automated alignment assessment is systematic and comparative
- The classifier architecture itself is a safety innovation (auditable, updatable)
- Transparency about dual-use capabilities (they published the AAV result)

**Weaknesses:**
- Multi-turn and collaborative attack vectors underexplored
- Internal-only biological capability validation
- Classifier internals remain opaque
- No post-deployment monitoring data yet (model just launched)

The system card is unusually honest about the model's dangerous capabilities — particularly the biology results. Anthropic chose to publish that Mythos 5 outperforms specialized protein models rather than suppress that finding. This transparency serves the safety case: if you know the risk is real, the access controls make sense.
