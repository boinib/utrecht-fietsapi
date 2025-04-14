import altair as alt
import pydeck as pdk
import streamlit as st

def show_table_and_chart(df):
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("📊 Beschikbaarheid")
        st.dataframe(
            df[["facilityName", "totalPlaces", "freePlaces", "occupiedPlaces"]]
            .sort_values("freePlaces", ascending=False)
            .rename(columns={
                "facilityName": "Stalling",
                "totalPlaces": "Totaal",
                "freePlaces": "Vrij",
                "occupiedPlaces": "Bezet"
            }),
            use_container_width=True
        )

    with col2:
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("freePlaces:Q", title="Vrije plekken"),
            y=alt.Y("facilityName:N", sort='-x', title=None),
            tooltip=[
                alt.Tooltip("facilityName", title="Stalling"),
                alt.Tooltip("freePlaces", title="Vrij"),
                alt.Tooltip("occupiedPlaces", title="Bezet"),
                alt.Tooltip("totalPlaces", title="Totaal")
            ]
        ).properties(
            height=500,
            title="Vrije plekken per stalling"
        )
        st.altair_chart(chart, use_container_width=True)

# Functie om de kaart weer te geven
def show_map(df):
    df = df.dropna(subset=["lat", "lon"]).copy()

    if df.empty:
        st.info("Geen locatiegegevens beschikbaar voor deze selectie.")
        return

    max_free = df["freePlaces"].max()
    df["color"] = df["freePlaces"].apply(
        lambda x: [255 - int((x / max_free) * 255), int((x / max_free) * 255), 0]
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_fill_color='color',
        get_radius=30,
        pickable=True,
        radius_min_pixels=4,
        radius_max_pixels=10,
    )

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=13,
        pitch=0,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{facilityName}\nVrij: {freePlaces} / {totalPlaces}"}
    ))
