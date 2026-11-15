
import pandas as pd
import os

from api_client import fetch_posts, fetch_users


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)


def fetch_posts_dataframe():
    """Convert API posts into a Pandas DataFrame."""

    posts = fetch_posts()

    if not posts:
        print("No post data available.")
        return pd.DataFrame()

    df = pd.DataFrame(posts)

    print("Posts converted into DataFrame successfully.")

    return df


def clean_posts_data(df):
    """Clean and organize post data."""

    if df.empty:
        print("No data available for cleaning.")
        return df

    df = df.copy()

    df.drop_duplicates(inplace=True)

    df.dropna(
        subset=["id", "userId", "title", "body"],
        inplace=True
    )

    df["title"] = df["title"].astype(str).str.strip()
    df["body"] = df["body"].astype(str).str.strip()

    df.reset_index(drop=True, inplace=True)

    print("Post data cleaned successfully.")

    return df


def filter_posts_by_user(df, user_id):
    """Filter posts belonging to a particular user."""

    if df.empty:
        return df.copy()

    filtered_df = df[df["userId"] == user_id].copy()

    print(f"Found {len(filtered_df)} posts for user {user_id}.")

    return filtered_df


def search_posts(df, keyword):
    """Search post titles and bodies."""

    if df.empty:
        return df.copy()

    keyword = keyword.strip()

    if not keyword:
        print("Please enter a search keyword.")
        return df.iloc[0:0].copy()

    result = df[
        df["title"].str.contains(keyword, case=False, na=False)
        | df["body"].str.contains(keyword, case=False, na=False)
    ].copy()

    print(f"Found {len(result)} matching posts.")

    return result


def get_user_statistics(df):
    """Generate user-wise post statistics."""

    if df.empty:
        print("No data available for statistics.")
        return pd.DataFrame()

    statistics = (
        df.groupby("userId")
        .agg(
            total_posts=("id", "count"),
            unique_titles=("title", "nunique")
        )
        .reset_index()
    )

    print("\n========== USER STATISTICS ==========")
    print(statistics.to_string(index=False))

    return statistics


def export_to_csv(df, filename):
    """Export processed data into CSV."""

    if df.empty:
        print("No data available to export.")
        return

    safe_filename = os.path.basename(filename)

    if not safe_filename.lower().endswith(".csv"):
        safe_filename += ".csv"

    file_path = os.path.join(DATA_DIR, safe_filename)

    df.to_csv(file_path, index=False)

    print(f"Data exported successfully: {file_path}")


def display_dataframe(df):
    """Display processed data."""

    if df.empty:
        print("No records to display.")
        return

    print("\n========== PROCESSED DATA ==========")
    print(df.to_string(index=False))
    print("====================================")
