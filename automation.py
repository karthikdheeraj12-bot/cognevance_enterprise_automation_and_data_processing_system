
import os
import logging
import pandas as pd
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor, as_completed

from api_client import fetch_posts, fetch_users
from data_processor import (
    clean_posts_data,
    get_user_statistics,
    export_to_csv
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


logging.basicConfig(
    filename=os.path.join(LOG_DIR, "automation.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_posts_task():
    """Fetch posts from API."""

    logging.info("Fetching posts.")

    return fetch_posts()


def fetch_users_task():
    """Fetch users from API."""

    logging.info("Fetching users.")

    return fetch_users()


def execute_parallel_fetching():
    """Fetch posts and users concurrently."""

    results = {}

    tasks = {
        "posts": fetch_posts_task,
        "users": fetch_users_task
    }

    with ThreadPoolExecutor(max_workers=2) as executor:

        future_tasks = {
            executor.submit(function): name
            for name, function in tasks.items()
        }

        for future in as_completed(future_tasks):

            task_name = future_tasks[future]

            try:
                results[task_name] = future.result()

                logging.info("%s fetched successfully.", task_name)

            except Exception:
                logging.exception("%s fetching failed.", task_name)
                results[task_name] = None

    return results


def process_data(posts):
    """Clean and analyze fetched post data."""

    if not posts:
        logging.warning("No posts available.")
        return None, None

    df = pd.DataFrame(posts)

    cleaned_df = clean_posts_data(df)

    statistics = get_user_statistics(cleaned_df)

    export_to_csv(cleaned_df, "automated_posts.csv")

    export_to_csv(statistics, "automated_statistics.csv")

    return cleaned_df, statistics


def generate_automation_report(posts, users, df):

    """Generate a summary report."""

    total_posts = len(posts) if posts else 0
    total_users = len(users) if users else 0

    processed_posts = len(df) if df is not None else 0

    report = f"""
COGNEVANCE ENTERPRISE AUTOMATION REPORT
========================================

Execution Time: {datetime.now()}

Total Posts Retrieved: {total_posts}
Total Users Retrieved: {total_users}

Successfully Processed Posts: {processed_posts}

Automation Status: Completed
========================================
"""

    report_path = os.path.join(
        REPORT_DIR,
        "automation_report.txt"
    )

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    logging.info("Automation report generated.")

    return report_path


def run_automation():

    """Execute the complete automation workflow."""

    print("\n========================================")
    print(" COGNEVANCE ENTERPRISE AUTOMATION")
    print("========================================")

    logging.info("Automation workflow started.")

    try:

        # Step 1: Concurrent API fetching
        results = execute_parallel_fetching()

        posts = results.get("posts") or []
        users = results.get("users") or []

        if not posts or not users:
            raise RuntimeError(
                "API fetching incomplete. Check API connection."
            )

        # Step 2: Process data
        cleaned_df, statistics = process_data(posts)

        if cleaned_df is None:
            raise RuntimeError("Data processing failed.")

        # Step 3: Generate report
        report_path = generate_automation_report(
            posts,
            users,
            cleaned_df
        )

        print("\nAutomation completed successfully!")

        print("Posts retrieved:", len(posts))
        print("Users retrieved:", len(users))
        print("Processed records:", len(cleaned_df))

        print("Report saved:", report_path)

        logging.info("Automation workflow completed.")

        return True

    except Exception:

        logging.exception("Automation workflow failed.")

        print("Automation failed. Check logs/automation.log.")

        return False


if __name__ == "__main__":
    run_automation()
