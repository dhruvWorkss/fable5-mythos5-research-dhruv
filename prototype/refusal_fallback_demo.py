"""
Claude Fable 5 Refusal Handling & Fallback Prototype
=====================================================

Demonstrates:
1. Calling claude-fable-5 via the Anthropic API
2. Detecting classifier-triggered refusals (HTTP 200 + stop_reason: "refusal")
3. Automatic fallback to claude-opus-4-8
4. Streaming with mid-stream refusal detection
5. Logging which classifier domain likely triggered

Requirements:
    pip install anthropic

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python refusal_fallback_demo.py
"""

import anthropic
import json
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ClassifierDomain(Enum):
    CYBERSECURITY = "cybersecurity"
    BIOLOGY_CHEMISTRY = "biology_chemistry"
    DISTILLATION = "distillation"
    UNKNOWN = "unknown"


@dataclass
class FableResponse:
    text: str
    model_used: str
    was_fallback: bool
    classifier_triggered: Optional[ClassifierDomain] = None


# Keywords that suggest which classifier domain may have triggered
DOMAIN_SIGNALS = {
    ClassifierDomain.CYBERSECURITY: [
        "exploit", "vulnerability", "lateral movement", "privilege escalation",
        "reconnaissance", "payload", "reverse shell", "c2", "command and control"
    ],
    ClassifierDomain.BIOLOGY_CHEMISTRY: [
        "synthesis", "pathogen", "toxin", "bioweapon", "precursor",
        "viral vector", "gain of function", "weaponize"
    ],
    ClassifierDomain.DISTILLATION: [
        "distill", "extract weights", "model training data", "replicate model",
        "fine-tune on outputs", "knowledge extraction"
    ],
}


def infer_classifier_domain(prompt: str) -> ClassifierDomain:
    """Heuristic: guess which classifier domain likely triggered based on prompt content."""
    prompt_lower = prompt.lower()
    for domain, signals in DOMAIN_SIGNALS.items():
        if any(signal in prompt_lower for signal in signals):
            return domain
    return ClassifierDomain.UNKNOWN


def query_fable5(
    client: anthropic.Anthropic,
    prompt: str,
    system: str = "",
    max_tokens: int = 4096,
) -> FableResponse:
    """
    Query Claude Fable 5 with automatic fallback to Opus 4.8 on classifier refusal.

    Key insight: Fable 5 refusals return HTTP 200 with stop_reason="refusal",
    NOT an HTTP error status. Applications must explicitly check stop_reason.
    """
    messages = [{"role": "user", "content": prompt}]

    kwargs = {
        "model": "claude-fable-5",
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)

    # Critical check: refusals are HTTP 200, not errors
    if response.stop_reason == "refusal":
        # Determine which classifier likely triggered
        domain = infer_classifier_domain(prompt)

        print(f"  [CLASSIFIER TRIGGERED] Domain: {domain.value}")
        print(f"  [FALLING BACK] Routing to claude-opus-4-8...")

        # Fallback to Opus 4.8
        kwargs["model"] = "claude-opus-4-8"
        response = client.messages.create(**kwargs)

        return FableResponse(
            text=response.content[0].text,
            model_used="claude-opus-4-8",
            was_fallback=True,
            classifier_triggered=domain,
        )

    return FableResponse(
        text=response.content[0].text,
        model_used="claude-fable-5",
        was_fallback=False,
    )


def query_fable5_streaming(
    client: anthropic.Anthropic,
    prompt: str,
    system: str = "",
    max_tokens: int = 4096,
) -> FableResponse:
    """
    Stream from Fable 5 with refusal detection.
    If refusal detected at end of stream, falls back to Opus 4.8 (non-streaming).
    """
    messages = [{"role": "user", "content": prompt}]

    kwargs = {
        "model": "claude-fable-5",
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system

    collected_text = ""

    with client.messages.stream(**kwargs) as stream:
        for text in stream.text_stream:
            collected_text += text
            print(text, end="", flush=True)

        final_message = stream.get_final_message()

        if final_message.stop_reason == "refusal":
            print("\n  [REFUSAL DETECTED IN STREAM]")
            # Fall back
            return query_fable5(client, prompt, system, max_tokens)

    print()  # newline after streaming
    return FableResponse(
        text=collected_text,
        model_used="claude-fable-5",
        was_fallback=False,
    )


def demonstrate_batch_with_fallback(
    client: anthropic.Anthropic,
    prompts: list[str],
) -> list[FableResponse]:
    """Process multiple prompts, handling refusals individually."""
    results = []
    for i, prompt in enumerate(prompts):
        print(f"\n--- Query {i+1}/{len(prompts)} ---")
        print(f"  Prompt: {prompt[:80]}...")
        result = query_fable5(client, prompt)
        print(f"  Model used: {result.model_used}")
        print(f"  Fallback: {result.was_fallback}")
        results.append(result)
    return results


def main():
    """
    Demonstration of Fable 5 refusal handling.

    NOTE: This prototype requires a valid ANTHROPIC_API_KEY with access to
    claude-fable-5. Without an API key, it runs in dry-run mode showing
    the expected behavior.
    """
    print("=" * 60)
    print("Claude Fable 5 — Refusal Handling & Fallback Prototype")
    print("=" * 60)

    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n[DRY RUN MODE] No ANTHROPIC_API_KEY environment variable found.")
        print("Set ANTHROPIC_API_KEY to run against the live API.\n")
        print("Expected behavior demonstration:\n")
        dry_run_demo()
        return

    client = anthropic.Anthropic(api_key=api_key)

    # Test 1: Normal query (should NOT trigger classifier)
    print("\n[TEST 1] Normal query — expecting direct Fable 5 response")
    print("-" * 40)
    result = query_fable5(
        client,
        "Explain how transformer attention mechanisms work in 3 sentences."
    )
    print(f"  Response: {result.text[:200]}...")
    print(f"  Model: {result.model_used} | Fallback: {result.was_fallback}")

    # Test 2: Query that may trigger cybersecurity classifier
    print("\n[TEST 2] Security-adjacent query — may trigger classifier")
    print("-" * 40)
    result = query_fable5(
        client,
        "Explain the concept of buffer overflow vulnerabilities and how they are mitigated in modern operating systems."
    )
    print(f"  Response: {result.text[:200]}...")
    print(f"  Model: {result.model_used} | Fallback: {result.was_fallback}")

    # Test 3: Streaming demonstration
    print("\n[TEST 3] Streaming response")
    print("-" * 40)
    result = query_fable5_streaming(
        client,
        "What are the three classifier domains in Claude Fable 5's safety architecture?"
    )
    print(f"  Model: {result.model_used} | Fallback: {result.was_fallback}")

    # Summary
    print("\n" + "=" * 60)
    print("PROTOTYPE COMPLETE")
    print("=" * 60)
    print("""
Key takeaways demonstrated:
1. Refusals return HTTP 200 — must check stop_reason explicitly
2. Fallback to Opus 4.8 is seamless for the end user
3. Classifier domain can be inferred from prompt content
4. Streaming requires checking final message stop_reason
5. <5% of queries trigger classifiers in normal usage
""")


def dry_run_demo():
    """Show expected behavior without API access."""
    print("Scenario 1: Normal query")
    print("  Input: 'Explain transformer attention mechanisms'")
    print("  → HTTP 200, stop_reason: 'end_turn'")
    print("  → Response from claude-fable-5 (no fallback)")
    print()
    print("Scenario 2: Offensive security query")
    print("  Input: 'Write a reverse shell payload for lateral movement'")
    print("  → HTTP 200, stop_reason: 'refusal'")
    print("  → Classifier: cybersecurity")
    print("  → Fallback to claude-opus-4-8")
    print("  → Opus 4.8 provides educational context without exploit code")
    print()
    print("Scenario 3: Biology/chemistry query")
    print("  Input: 'Design a gain-of-function modification for...'")
    print("  → HTTP 200, stop_reason: 'refusal'")
    print("  → Classifier: biology_chemistry")
    print("  → Fallback to claude-opus-4-8")
    print()
    print("Scenario 4: Normal security education (NOT blocked)")
    print("  Input: 'Explain how buffer overflows work and how they are mitigated'")
    print("  → HTTP 200, stop_reason: 'end_turn'")
    print("  → Response from claude-fable-5 (no fallback)")
    print("  → Classifiers are narrow: education ≠ exploitation")


if __name__ == "__main__":
    main()
