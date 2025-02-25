class QuestionBank:
    # -------------------------------------------------------
    # 2. Functions for the Q&A and Scoring
    # -------------------------------------------------------
    def ask_questions():
        """
        Asks a series of questions to gather information about a potential data product.
        Returns the answers as a dictionary.
        """

        print("Welcome to the Data Product Assessment Tool!\n")
        print("Please answer the following questions to help us determine whether your dataset/use case qualifies as a data product.\n")

        answers = {}

        # NEW: Ask for the data product name
        answers["data_product_name"] = input("What do you want to name this potential data product? ")

        # 1. General Purpose
        answers["purpose"] = input("\n1) What is the main business purpose or outcome this data supports? ")

        # 2. Ownership
        answers["owner"] = input("\n2) Who is the primary data owner or steward? ")

        # 3. Consumer Readiness
        print("\n3) Is the data intended for consumption beyond its original team or domain?\n"
            "   (e.g., accessible for analytics, reporting, or other business units)")
        answers["consumer_readiness"] = input("   (yes/no): ").strip().lower()

        # 4. CDE Identification
        print("\n4) Does this dataset include Critical Data Elements (CDEs)?\n"
            "   (CDEs are data fields or elements that are vital to key business processes, compliance, or decision-making.)")
        answers["has_cdes"] = input("   (yes/no): ").strip().lower()

        # 5. OKR Alignment
        print("\n5) Does this data initiative tie directly into one of the organization's OKRs?\n"
            "   (e.g., cost reduction, revenue growth, regulatory compliance, etc.)")
        answers["okr_alignment"] = input("   (yes/no): ").strip().lower()

        # 6. Metadata & Discoverability
        print("\n6) Is the dataset documented with metadata that helps other teams understand and discover it?\n"
            "   (Azure Purview lens: can it be registered, labeled, or classified appropriately?)")
        answers["metadata"] = input("   (yes/no): ").strip().lower()

        # 7. Data Quality Metrics
        print("\n7) Are data quality metrics in place (e.g., completeness, accuracy, timeliness)?")
        answers["data_quality"] = input("   (yes/no): ").strip().lower()

        # 8. Security & Access Control
        print("\n8) Does the dataset have security and access controls defined?\n"
            "   (e.g., role-based access, data sensitivity labels in Azure Purview)")
        answers["security"] = input("   (yes/no): ").strip().lower()

        # 9. Longevity & Lifecycle
        print("\n9) Is the dataset expected to have a defined lifecycle (onboarding, maintenance, decommissioning)?")
        answers["lifecycle"] = input("   (yes/no): ").strip().lower()

        # 10. Potential for Reuse
        print("\n10) Do you anticipate that this dataset or service can be reused by other teams or domains in future projects?")
        answers["reuse_potential"] = input("    (yes/no): ").strip().lower()

        return answers
    
    def evaluate_data_product(answers):
        """
        Evaluates the user answers to decide if the dataset qualifies as a 'data product'.
        Returns a tuple of (is_data_product: bool, feedback: str, score: int).
        """

        score = 0
        feedback_items = []

        # Sample weighting logic
        if answers["consumer_readiness"] == "yes":
            score += 2
            feedback_items.append("• Data is intended for broader consumption (key sign of a data product).")

        if answers["metadata"] == "yes":
            score += 2
            feedback_items.append("• Metadata is documented (crucial for discoverability in Azure Purview).")

        if answers["security"] == "yes":
            score += 1
            feedback_items.append("• Security and access controls are defined.")

        if answers["data_quality"] == "yes":
            score += 1
            feedback_items.append("• Data quality metrics are in place (enhances trust).")

        if answers["has_cdes"] == "yes":
            score += 2
            feedback_items.append("• Includes Critical Data Elements (CDEs), which often indicates higher business value.")

        if answers["okr_alignment"] == "yes":
            score += 2
            feedback_items.append("• Aligned with organizational OKRs (directly supports strategic goals).")

        if answers["reuse_potential"] == "yes":
            score += 1
            feedback_items.append("• Potential for reuse (key factor in data product thinking).")

        if answers["lifecycle"] == "yes":
            score += 1
            feedback_items.append("• Lifecycle management considered (supports stable, long-term usage).")

        threshold = 6

        if score >= threshold:
            is_data_product = True
            feedback = (
                f"Based on your responses, this initiative scores {score} points, "
                f"which suggests it meets the criteria of a data product.\n"
                "Here’s a breakdown of the key points:\n" + "\n".join(feedback_items)
            )
        else:
            is_data_product = False
            feedback = (
                f"This initiative scores {score} points, falling below the threshold of {threshold}.\n"
                "It may not fully qualify as a data product under the current criteria.\n"
                "Here are the highlights:\n" + "\n".join(feedback_items) +
                "\n\nConsider enhancing discoverability, security, metadata coverage, or OKR alignment "
                "to move closer to a recognized data product."
            )

        return is_data_product, feedback, score