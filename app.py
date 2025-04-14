import pandas as pd
import streamlit as st
import pytz
from utils import get_parking_data
from filters import filter_data
from visualizations import show_table_and_chart, show_map

def main():
    st.set_page_config(page_title="🚲 Utrecht Fietst!", layout="wide")

    st.title("🚲 Utrecht Fietst!")
    st.caption("Live overzicht van vrije plekken in fietsenstallingen in Utrecht.")

    try:
        df = get_parking_data()
        utrecht_tz = pytz.timezone('Europe/Amsterdam')
        df["time"] = pd.to_datetime(df["time"]).dt.tz_convert(utrecht_tz)
        latest_time = df["time"].iloc[0]
        st.markdown(f"📅 **Laatste update:** `{latest_time.strftime('%d-%m-%Y %H:%M:%S')}`")
        st.divider()
        st.sidebar.header("Zoek en filter")
        query = st.sidebar.text_input("🔍 Zoek fietsenstalling...", "")
        min_free = st.sidebar.slider("🔓 Min. vrije plekken", 0, int(df["freePlaces"].max()), 0)

        filtered_df = filter_data(df, query, min_free)

        tab = st.selectbox("Kies een weergave", ["Beschikbaarheid", "Kaartweergave"])

        if tab == "Beschikbaarheid":
            show_table_and_chart(filtered_df)
        elif tab == "Kaartweergave":
            show_map(filtered_df)

    except Exception as e:
        st.error(f"❌ Kon de data niet ophalen: {e}")


if __name__ == "__main__":
    main()
