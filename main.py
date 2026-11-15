
from automation import run_automation
from scheduler import run_scheduler


def main():

    while True:

        print("\n========================================")
        print(" COGNEVANCE ENTERPRISE AUTOMATION")
        print("========================================")

        print("1. Run Automation")
        print("2. Start Scheduled Automation")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            run_automation()

        elif choice == "2":

            run_scheduler()

        elif choice == "3":

            print("\nApplication closed.")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

