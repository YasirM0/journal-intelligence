import re

from services.repository import search_candidates

# Strategies we can actually support with the data currently in the
# database (title/subjects/keywords text, apc + apc_amount, review_weeks).
#
# "Best Match" (semantic similarity), "Highest Prestige" (needs a quartile
# or ranking source) and "Beginner Friendly" (needs acceptance rate) are
# in the long-term vision but there's no underlying data for them yet, so
# they are intentionally left out rather than faked with a made-up score.
STRATEGIES = ["Balanced", "Lowest APC", "Fast Publication"]

# apc_amount is free text like "40 USD" or "40 USD; 450000 IDR", not a
# clean number. We only trust a figure we can find explicitly in USD;
# we do not guess currency conversions for the rest.
_USD_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*USD", re.IGNORECASE)


def parse_usd_amount(raw):
    """
    Best-effort extraction of a USD figure from a free-text APC value.
    Returns None if no USD amount is present in the text.
    """
    if not raw:
        return None
    match = _USD_PATTERN.search(str(raw))
    if not match:
        return None
    return float(match.group(1))


class JournalRecommender:

    def recommend(
        self,
        title,
        keywords=None,
        abstract="",
        language=None,
        free_only=False,
        min_budget=None,
        max_budget=None,
        strategy="Balanced",
        limit=20,
    ):
        """
        Recommend journals based on a paper title, keywords, and
        (optionally) an abstract, narrowed by language/budget filters
        and reordered according to a recommendation strategy.
        """

        keywords = keywords or []

        # Clean keywords
        keywords = [
            keyword.strip()
            for keyword in keywords
            if keyword.strip()
        ]

        # If no keywords are provided, fall back to words from the title
        # and abstract (simple substring matching, not NLP/embeddings).
        if not keywords:
            fallback_text = f"{title} {abstract}"
            fallback_words = [
                word.strip(".,;:()").lower()
                for word in fallback_text.split()
                if len(word.strip(".,;:()")) > 3
            ]
            seen = set()
            keywords = []
            for word in fallback_words:
                if word not in seen:
                    seen.add(word)
                    keywords.append(word)
            keywords = keywords[:15]

        # Only push free_only to SQL (apc is clean 'Yes'/'No' text).
        # Budget filtering happens below, in Python, after parsing.
        candidates = search_candidates(
            keywords,
            language=language,
            free_only=free_only,
        )

        recommendations = []

        for journal in candidates:

            is_free = str(journal.apc).lower() == "no"
            usd_amount = None if is_free else parse_usd_amount(journal.apc_amount)

            # Budget filter (Python-side, since apc_amount is free text).
            # Free journals satisfy any band whose floor is $0/unset.
            # Paid journals only count if we found a confirmed USD figure
            # inside the requested range — an unconfirmed/non-USD fee is
            # excluded rather than guessed at.
            if not free_only and (min_budget is not None or max_budget is not None):
                if is_free:
                    if min_budget:  # a floor above $0 rules out free journals
                        continue
                else:
                    if usd_amount is None:
                        continue
                    if min_budget is not None and usd_amount < min_budget:
                        continue
                    if max_budget is not None and usd_amount > max_budget:
                        continue

            score = 0
            reasons = []

            for keyword in keywords:

                k = keyword.lower()

                if k in str(journal.title).lower():
                    score += 5
                    reasons.append(f'✓ Title contains "{keyword}"')

                if k in str(journal.subjects).lower():
                    score += 4
                    reasons.append(f'✓ Subject contains "{keyword}"')

                if k in str(journal.keywords).lower():
                    score += 2
                    reasons.append(f'✓ Keywords contain "{keyword}"')

            if score == 0:
                continue

            if is_free:
                reasons.append("✓ No publication fee (APC)")
            elif usd_amount is not None:
                reasons.append(f"APC: ~${usd_amount:.0f}")
            else:
                reasons.append("APC applies (amount not confirmed in USD — check journal site)")

            if journal.review_weeks is not None:
                reasons.append(f"Typical review time: ~{journal.review_weeks} weeks")

            recommendations.append({
                "title": journal.title,
                "publisher": journal.publisher or "",
                "country": journal.country or "",
                "website": journal.website or "",
                "doaj_url": journal.doaj_url or "",
                "languages": journal.languages or "",
                "license": journal.license or "",
                "apc": journal.apc or "",
                "apc_amount": usd_amount,
                "is_free": is_free,
                "review_weeks": journal.review_weeks,
                "score": score,
                "reasons": reasons,
            })

        recommendations = self._apply_strategy(recommendations, strategy)

        return recommendations[:limit]

    def _apply_strategy(self, recommendations, strategy):
        """
        Reorder recommendations according to the chosen strategy.
        Falls back to "Balanced" for any strategy we don't yet support.
        """

        if strategy == "Lowest APC":
            recommendations.sort(
                key=lambda r: (
                    0 if r["is_free"] else 1,
                    r["apc_amount"] if r["apc_amount"] is not None else float("inf"),
                    -r["score"],
                )
            )
            return recommendations

        if strategy == "Fast Publication":
            recommendations.sort(
                key=lambda r: (
                    r["review_weeks"] if r["review_weeks"] is not None else float("inf"),
                    -r["score"],
                )
            )
            return recommendations

        # Balanced (default): topical match first, small nudge for free access
        recommendations.sort(
            key=lambda r: (r["score"] + (2 if r["is_free"] else 0)),
            reverse=True,
        )
        return recommendations