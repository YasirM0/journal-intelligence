# Models

This package contains the core domain models used throughout Journal Intelligence.

## Current Models

- `Journal` — Canonical representation of a journal.
- `Recommendation` — Recommendation result returned to users.

All external data sources (DOAJ, SINTA, Scopus, etc.) are transformed into the `Journal` model before being stored in the database.