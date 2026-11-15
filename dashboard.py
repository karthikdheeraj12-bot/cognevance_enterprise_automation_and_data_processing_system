
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_processor import (
    fetch_posts_dataframe,
    clean_posts_data,
    get_user_statistics
)


st.set_page_config(
    page_title="Cognevance Automation Dashboard",
    page_icon="📊",
    layout="wide"
)


@st.cache_data(ttl=60)
def load_data():

    df = fetch_posts_dataframe()

    if df.empty:
        return pd.DataFrame()

    return clean_posts_data(df)


def main():

    st.title("📊 Cognevance Enterprise Automation Dashboard")

    st.caption(
        "API Data Processing, Analytics and Automation System"
    )

    st.sidebar.title("Dashboard Controls")

    if st.sidebar.button("Refresh Data"):
        load_data.clear()

    df = load_data()

    if df.empty:
        st.error("Unable to load data. Check your internet connection.")
        return

    # Sidebar filters
    st.sidebar.subheader("Filters")

    users = sorted(df["userId"].unique())

    selected_user = st.sidebar.selectbox(
        "Select User",
        ["All Users"] + users
    )

    if selected_user == "All Users":
        filtered_df = df.copy()
    else:
        filtered_df = df[
            df["userId"] == selected_user
        ].copy()

    # Search
    keyword = st.sidebar.text_input("Search Posts")

    if keyword.strip():
        filtered_df = filtered_df[
            filtered_df["title"].str.contains(
                keyword,
                case=False,
                na=False
            )
            | filtered_df["body"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    # KPI cards
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Posts", len(filtered_df))

    col2.metric(
        "Total Users",
        filtered_df["userId"].nunique()
    )

    col3.metric(
        "Unique Titles",
        filtered_df["title"].nunique()
    )

    st.divider()

    # Data table
    st.subheader("Post Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # User statistics
    st.subheader("User-wise Statistics")

    statistics = get_user_statistics(filtered_df)

    if not statistics.empty:

        st.dataframe(
            statistics,
            use_container_width=True,
            hide_index=True
        )

        # Bar chart
        fig, ax = plt.subplots()

        ax.bar(
            statistics["userId"].astype(str),
            statistics["total_posts"]
        )

        ax.set_title("Posts Per User")
        ax.set_xlabel("User ID")
        ax.set_ylabel("Number of Posts")

        st.pyplot(fig)

        plt.close(fig)

    # CSV download
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_posts.csv",
        mime="text/csv"
    )

    st.success("Dashboard loaded successfully!")


if __name__ == "__main__":
    main()
