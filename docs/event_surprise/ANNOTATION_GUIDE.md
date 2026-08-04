# Event Surprise Human Annotation Guide

Status: `PENDING_HUMAN_REVIEW`.

Reviewers label only the article available at the recorded source timestamp. Market outcomes, later summaries, model interpretations, and other reviewers' labels are hidden.

## Order of work

1. Identify the issuer or abstain.
2. Identify the primary event family.
3. Copy evidence spans for the event fact.
4. Determine whether an explicit, article-supported reference exists.
5. Label surprise availability before direction.
6. Label direction only when the reference and directional interpretation are defensible.
7. Record numeric actual, reference, and unit only when explicitly stated.
8. Score materiality and certainty from 1–5.
9. Record ambiguity; never guess.

## Evidence rules

- Offsets use zero-based character positions in the private article packet, with an exclusive end.
- Every factual field must map to at least one evidence span.
- Interpretation is not evidence.
- Do not infer consensus, guidance, or market expectations when absent.
- Conflicting sources, missing units, unclear periods, and corrected articles require abstention or adjudication.

## Human and AI boundaries

Human labels use reviewer type `HUMAN`. AI triage uses `AI_REVIEW_ONLY` and never enters the gold denominator. Agreement statistics remain unavailable until real double review occurs.

## Adjudication

Disagreements on issuer, family, direction, reference type, surprise availability, numeric values, or evidence support are adjudicated without access to market outcomes. Adjudicators preserve both original labels and a written resolution.
