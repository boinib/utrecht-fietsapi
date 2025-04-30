import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from utils import get_parking_data
from filters import filter_data
from visualizations import show_table_and_chart, show_map


def configure_page():
    st.set_page_config(page_title="🚲 Utrecht Fietst!", layout="wide")
    st_autorefresh(interval=60 * 1000, key="data_refresh")
    st.title("Utrecht Fietst!")
    st.caption("Live overzicht van vrije plekken in fietsenstallingen in Utrecht")


def convert_times(df):
    df["time"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert("Europe/Amsterdam")
    return df


def get_summary_stats(df):
    return {
        "total_stallingen": df["facilityName"].nunique(),
        "totaal_plekken": df["totalPlaces"].sum(),
        "totaal_vrij": df["freePlaces"].sum(),
        "totaal_bezet": df["occupiedPlaces"].sum(),
        "latest_time": df["time"].iloc[0],
    }


def display_overview(stats):
    st.subheader("🔢 Overzicht")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stallingen", stats["total_stallingen"])
    col2.metric("Totale plekken", stats["totaal_plekken"])
    col3.metric("Vrij", stats["totaal_vrij"])
    col4.metric("Bezet", stats["totaal_bezet"])
    st.divider()


def display_top3(df):
    st.subheader("🏅 Top 3 meest beschikbare stallingen")
    top3 = df.sort_values("freePlaces", ascending=False).head(3)

    for _, row in top3.iterrows():
        name = row["facilityName"]
        free, total = row["freePlaces"], row["totalPlaces"]
        lat, lon = row.get("lat"), row.get("lon")

        if pd.notna(lat) and pd.notna(lon):
            link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            st.markdown(f"- **[{name}]({link})**: {free} vrij van {total} plekken")
        else:
            st.markdown(f"- **{name}**: {free} vrij van {total} plekken")

    st.divider()


def display_filters(df):
    st.sidebar.header("🔍 Zoek en filter")
    query = st.sidebar.text_input("Zoek fietsenstalling...", "")
    max_free = int(df["freePlaces"].max()) if not df.empty else 0
    min_free = st.sidebar.slider("Minimale vrije plekken", 0, max_free, 0)
    return filter_data(df, query, min_free)


def display_tabs(filtered_df):
    tab1, tab2 = st.tabs(["🗺️ Kaartweergave", "📊 Beschikbaarheid"])

    with tab1:
        show_map(filtered_df)

    with tab2:
        if filtered_df.empty:
            st.warning("😕 Geen stallingen gevonden met deze filters.")
        else:
            show_table_and_chart(filtered_df)

    st.divider()


def main():
    configure_page()

    try:
        df = get_parking_data()
        df = convert_times(df)
        stats = get_summary_stats(df)

        st.markdown(f"📅 **Laatste update:** `{stats['latest_time'].strftime('%d-%m-%Y %H:%M:%S')}`")
        st.divider()

        display_overview(stats)
        display_top3(df)
        filtered_df = display_filters(df)
        display_tabs(filtered_df)

        st.caption("🚴‍♂️ @boinib.")

    except Exception as e:
        st.error(f"❌ Kon de data niet ophalen: {e}")


if __name__ == "__main__":
    main()
