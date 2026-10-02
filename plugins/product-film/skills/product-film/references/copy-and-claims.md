# Copy, claims and reading time

## Claim registry
Every string that can appear on screen is listed with: id, exact text, source line
in `copy.txt` (or "owner-approved" with the date), required qualifier, and the
scene it belongs to. A required-items list (every claim, caveat, CTA, logo set) is
frozen before building; the gate fails if anything required is missing, not only
if something unsourced appears.

Allowed shortening: a clause of a page sentence that does not change scope
("Clients approve from an emailed link." from "Clients approve from an emailed
link, with no account needed."). Not allowed: dropping a qualifier that limits the
claim ("Emails from your verified domain" from "Supported approval and client
emails from your verified domain" overclaims).

## Line breaks
Write each headline as phrases. Each phrase is a `display:block; white-space:nowrap`
span; never a `<br>`. Good: "Still chasing / client approvals?". Bad: "Still chasing
client / approvals?".

## Reading rule R
`required = 0.3 s x words + 0.5 s readable + 0.4 s entrance`, per text node. A
block that enters together (stagger at most 0.4 s) is one node, measured from its
last element's entrance. `scripts/reading_rule.py nodes.json` checks a schedule.
