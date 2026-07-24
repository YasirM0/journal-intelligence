# Recommendation engine: scoring, strategies, prestige, confidence

This documents what `services/recommender.py` actually does — not the
long-term vision, just the current, real behavior. Code is the source
of truth; if this drifts from `recommend()`, trust the code.

## Candidate search

Before scoring, candidates are pulled from the database by keyword
(title/subjects/keywords columns, substring match), then narrowed by
any language/free-only/indexing filters. If the person left the
keyword field blank, keywords are derived from the paper title +
abstract instead (plain substring word extraction — not NLP, not
embeddings, just words over 3 characters, de-duplicated, capped at 15).

## Scoring

Every candidate starts at score 0. For each keyword, points are added
per field it appears in (a keyword can score in more than one field):

| Field | Points |
|---|---|
| Title contains the keyword | +5 |
| Subjects contains the keyword | +4 |
| Keywords field contains the keyword | +2 |

A journal with score 0 (no keyword matched anywhere) is dropped, not
kept with a zero score. This is substring matching, not semantic
similarity — a keyword has to actually appear in the text.

## Strategies

Three strategies exist, all backed by real database columns. There is
no "Best Match" (would need semantic/embedding similarity — no such
data) and no "Beginner Friendly" (would need an acceptance rate — no
such data); they were deliberately left out rather than faked.

**Balanced (default)** — sorts by `score`, with a +2 bonus for
free-to-publish journals. Doesn't use quartile/APC-amount/review time
at all beyond that.

**Lowest APC** — sorts free journals first, then paid journals by
ascending confirmed USD amount (unconfirmed-amount journals sort last
within the paid group), with `score` as the final tiebreaker.

**Highest Prestige** — sorts by the journal's best quartile across all
its confirmed sources (Q1 > Q2 > Q3 > Q4 > untiered), then by its
highest SJR value as a tiebreak, then by `score`. "Best across sources"
matters when the same journal has, say, a Q1 in Scopus and no tier
elsewhere — the Q1 is what counts. Journals with no quartile at all
(most DOAJ-only journals, since DOAJ itself carries no quartile data)
rank at the bottom of this ordering regardless of topical score — this
strategy is only meaningful for journals also indexed in Scopus or WoS.

## APC / budget handling

`apc_amount` in the database is free text (e.g. `"40 USD"`, `"40 USD;
450000 IDR"`), not a clean number. Only a value explicitly labeled USD
is trusted; no currency conversion is guessed. A paid journal with no
parseable USD figure is excluded from any budget-limited search (Free
/ <$100 / $100–300 / >$300) rather than assumed to fit — see
`parse_usd_amount()`.

## Confidence levels

After sorting, each result is labeled Excellent / Strong / Moderate /
Weak / Poor by **its rank position within that search's own results**
— literally which fifth of the list it falls in (top 20% = Excellent,
next 20% = Strong, and so on).

This is NOT a calibrated probability of fit or acceptance. There's no
outcome data (acceptance/rejection history) behind it — it can't be,
since nothing in this database tracks that. It exists purely to help
scan a long results list, not as a claim about any individual
journal's real odds. The search page's help text says this explicitly;
keep that wording if this is ever reused elsewhere, so it isn't read
as more certain than it is.
