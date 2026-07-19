# Project Principles

Journal Intelligence is guided by a small set of principles that influence every design decision.

When proposing a new feature, changing the architecture, or reviewing a contribution, contributors should evaluate whether the change aligns with these principles.

---

# 1. Solve One Problem Well

The primary goal of Journal Intelligence is to help researchers choose appropriate journals for their work.

Features that do not directly support this goal should be carefully evaluated before being included.

We prefer a small number of reliable features over a large number of incomplete ones.

---

# 2. Transparency Over Black Boxes

Every recommendation should be explainable.

Transparency extends beyond displaying a final result. Users should understand why a journal is recommended and be able to inspect the major factors that contributed to the recommendation.

Recommendations should be understandable by humans, not only interpretable by algorithms.

The project should avoid opaque algorithms whenever possible.

---

# 3. Evidence Before Assumptions

Recommendations should be based on verifiable information.

If information is unavailable, the system should clearly communicate that rather than guessing.

Unknown values are preferable to incorrect values.

---

# 4. Simplicity Before Complexity

Simple solutions should always be preferred when they adequately solve the problem.

New features should be introduced only when they provide clear value to researchers.

Complexity should never be added solely because it is technically possible.

---

# 5. Privacy by Design

Users should always remain in control of their data.

No personal information or manuscript data should be stored without explicit user consent.

Optional features that require data storage must always be transparent and voluntary.

---

# 6. Modular Architecture

Each component should have a single, well-defined responsibility.

Modules should be easy to replace, improve, or extend without affecting unrelated parts of the system.

---

# 7. Community First

Journal Intelligence is an open-source project.

Ideas, discussions, bug reports, and contributions are welcomed from the research community.

Respectful collaboration is considered one of the project's strengths.

---

# 8. Build for Researchers

Every feature should answer a simple question:

> Does this genuinely help a researcher make a better publishing decision?

If the answer is no, the feature probably belongs in a future version rather than the current release.

---

# Guiding Question

When uncertain about a design decision, ask:

> "Will this make Journal Intelligence more trustworthy, more understandable, or more useful to researchers?"

If not, reconsider the change.

---

**Document Version:** 0.1

**Last Updated:** July 2026

**Status:** Approved