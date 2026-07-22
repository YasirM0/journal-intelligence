from services.recommender import JournalRecommender


def main():
    recommender = JournalRecommender()

    recommendations = recommender.recommend(
        title="Digital Inclusion",
        keywords=[
            "education",
            "digital",
            "sociology",
        ]
    )

    print(f"Found {len(recommendations)} recommendations\n")

    for recommendation in recommendations:

        print("=" * 80)
        print(f"Journal : {recommendation['title']}")
        print(f"Publisher : {recommendation['publisher']}")
        print(f"Country : {recommendation['country']}")
        print(f"Score : {recommendation['score']}")

        print("Reasons:")

        for reason in recommendation["reasons"]:
            print(f"  - {reason}")

        print()


if __name__ == "__main__":
    main()