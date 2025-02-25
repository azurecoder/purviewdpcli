import argparse
from QuestionBank import QuestionBank
from Purview import PurviewDataProducts

def main():
    parser = argparse.ArgumentParser(
        description="Data Product Assessment with optional Purview integration."
    )
    parser.add_argument(
        "--q", "-q",
        help="Run the question flow to create a data product if it qualifies.",
        action="store_true"
    )
    parser.add_argument(
        "--dp", "-dp",
        help="List all existing data products in Purview.",
        action="store_true"
    )
    args = parser.parse_args()

    questions = QuestionBank()
    products = PurviewDataProducts()

    if args.q:
        # --q (Questionnaire) Flow
        answers = questions.ask_questions()
        is_data_product, feedback, score = questions.evaluate_data_product(answers)

        print("\n===== Data Product Assessment Result =====\n")
        if is_data_product:
            print("✅ This appears to qualify as a Data Product!")
        else:
            print("❌ This does not fully qualify as a Data Product yet.")

        print("\n--- Detailed Feedback ---")
        print(feedback)

        if is_data_product:
            data_product_name = answers["data_product_name"]
            owner = answers["owner"]
            print(f"\nAttempting to create a Purview entity for '{data_product_name}' ...")
            products.create_data_product_in_purview(data_product_name, owner, score)

    if args.dp:
        # --dp (List Data Products) Flow
        print("\n=== Published Governance Domains ===")
        governance_domains = products.list_governance_domains()
        for name, guid in governance_domains.items():
            print(f"Name: {name} | GUID: {guid}")
            print("\nRetrieving list of all existing data products...")
            data_product_names = products.list_data_products_in_purview(guid)
            if data_product_names:
                print(f"\n=== Data Products in Purview for {name} ===")
                for name in data_product_names:
                    print(f"• {name}")
            else:
                print("No data products found or an error occurred.")

    if not args.q and not args.dp:
        parser.print_help()


if __name__ == "__main__":
    main()
