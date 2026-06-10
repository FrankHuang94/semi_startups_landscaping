# Data Quality Policy

## Non-Fabrication Rule

Do not invent funding, valuation, revenue, customer, benchmark, employee, transaction,
or performance data. Use `null` when reliable information is unavailable. Label rumors
as rumored with low confidence and label estimates with their methodology.

## Source Hierarchy

1. Company, acquirer, lab, or investor primary sources.
2. SEC and other regulatory filings.
3. Official patent databases.
4. Academic papers and conference proceedings.
5. Official investor portfolio pages.
6. Reputable financial and technology press.
7. Attributed analyst reports or databases.
8. Clearly labeled estimates.

## Claim Standards

- Every non-obvious claim needs a source.
- Product status must distinguish concept, research, announced, sampling, shipping,
  deployed, and discontinued.
- Benchmarks must distinguish company claims from independently verified results.
- Funding dates and amounts should reflect the announced event, not an inferred total.
- Transaction values must remain `null` when undisclosed.
- Patent summaries are not legal opinions and do not establish freedom to operate.

## Confidence

- `high`: Primary or regulatory evidence with direct support.
- `medium`: Multiple credible sources or one strong secondary source.
- `low`: Incomplete, estimated, rumored, or placeholder information.

## Freshness

Each section has independent refresh metadata. High-velocity AI infrastructure sections
should generally be reviewed every 30-45 days; other sections every 90 days. Record
`last_verified` at the entity level and never advance it without checking the cited
information.
