# Database Design

## Purpose

The Journal Database stores publicly available metadata about academic journals.

It serves as the central data source for search, filtering, and ranking.

The database intentionally stores factual information only.

It does not contain ranking logic or recommendation algorithms.

---

# Design Principles

## Store Facts

The database should store verifiable information rather than calculated scores.

For example:

✔ Publisher

✔ Language

✔ APC

✔ Scope

❌ Recommendation Score

Scores are calculated by the Ranking Engine.

---

## Public Information First

Version 0.1 prioritizes information that can be obtained from public and reliable sources.

If information is unavailable, it should remain empty rather than estimated.

---

## Flexible Schema

The schema should allow additional fields to be added in future versions without requiring major redesign.

---

# Journal Record

Each journal should contain the following information where available.

## Basic Information

- Journal Name
- ISSN
- eISSN
- Publisher
- Country
- Website

---

## Indexing

- Scopus
- SINTA
- DOAJ
- ESCI
- Other indexes (future)

---

## Classification

- Subject Area
- Discipline
- Quartile
- SINTA Rank

---

## Publishing Information

- Publication Language
- Open Access
- APC
- Publication Frequency

---

## Scope

- Aims & Scope
- Journal Description
- Keywords

---

## Search Data

Fields used internally for semantic search.

Examples:

- Embeddings
- Search Index IDs

These fields are implementation details and are not displayed to users.

---

# Missing Data

Not every journal publishes the same information.

The system should distinguish between:

- Available
- Not Available
- Unknown

The project should never invent missing values.

---

# Future Extensions

Possible future additions include:

- First Decision Time
- Publication Time
- Fast Track Availability
- Historical Quartiles
- Community Statistics

These fields are outside the scope of Version 0.1.

---

# Version 0.1 Scope

Version 0.1 stores only the metadata required for:

- Search
- Filtering
- Ranking
- Displaying journal information

Additional fields will be introduced only when they support a concrete feature.

---

**Document Version:** 0.1

**Last Updated:** July 2026

**Status:** Approved