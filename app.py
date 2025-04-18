import pandas as pd
import streamlit as st
import pytz
from utils import get_parking_data
from filters import filter_data
from visualizations import show_table_and_chart, show_map
from streamlit_autorefresh import st_autorefresh

def main():
    st.set_page_config(page_title="🚲 Utrecht Fietst!", layout="wide")

    st_autorefresh(interval=60 * 1000, key="data_refresh")

    st.title("Utrecht Fietst!")
    st.caption("Live overzicht van vrije plekken in fietsenstallingen in Utrecht")

    try:
        df = get_parking_data()

        utrecht_tz = pytz.timezone('Europe/Amsterdam')
        df["time"] = pd.to_datetime(df["time"]).dt.tz_convert(utrecht_tz)
        latest_time = df["time"].iloc[0]

        total_stallingen = df["facilityName"].nunique()
        totaal_plekken = df["totalPlaces"].sum()
        totaal_vrij = df["freePlaces"].sum()
        totaal_bezet = df["occupiedPlaces"].sum()

        st.markdown(f"📅 **Laatste update:** `{latest_time.strftime('%d-%m-%Y %H:%M:%S')}`")
        st.divider()

        st.subheader("🔢 Overzicht")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Stallingen", total_stallingen)
        col2.metric("Totale plekken", totaal_plekken)
        col3.metric("Vrij", totaal_vrij)
        col4.metric("Bezet", totaal_bezet)

        st.divider()

        st.subheader("🏅 Top 3 meest beschikbare stallingen")
        top3 = df.sort_values("freePlaces", ascending=False).head(3)
        for _, row in top3.iterrows():
            name = row["facilityName"]
            free = row["freePlaces"]
            total = row["totalPlaces"]
            lat = row.get("lat")
            lon = row.get("lon")
            if pd.notna(lat) and pd.notna(lon):
                maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                st.markdown(f"- **[{name}]({maps_link})**: {free} vrij van {total} plekken")
            else:
                st.markdown(f"- **{name}**: {free} vrij van {total} plekken")

        st.divider()

        st.sidebar.header("🔍 Zoek en filter")
        query = st.sidebar.text_input("Zoek fietsenstalling...", "")
        min_free = st.sidebar.slider("Minimale vrije plekken", 0, int(df["freePlaces"].max()), 0)

        filtered_df = filter_data(df, query, min_free)

        tab1, tab2 = st.tabs(["🗺️ Kaartweergave", "📊 Beschikbaarheid"])

        with tab1:
            show_map(filtered_df)

        with tab2:
            if filtered_df.empty:
                st.warning("😕 Geen stallingen gevonden met deze filters.")
            else:
                show_table_and_chart(filtered_df)

        st.divider()
        st.caption("🚴‍♂️ @boinib.")

    except Exception as e:
        st.error(f"❌ Kon de data niet ophalen: {e}")


if __name__ == "__main__":
    main()
