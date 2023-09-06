import pandas as pd
import streamlit as st
import altair as alt

from .directories import DATA_DIR


def cost_of_living():
    df = load_dataset()
    lil_df = select_cities(df)
    bar_chart(lil_df)


def load_dataset():
    filepath = DATA_DIR / "numbeo-cost-of-living.csv"
    df = pd.read_csv(filepath)
    return df


def select_cities(df):
    default_selections = [
        "Tokyo, Japan",
        "Chicago, IL, United States",
        "San Francisco, CA, United States",
        "New York, NY, United States",
        "Columbus, OH, United States",
        "London, United Kingdom",
        "Paris, France",
        "Cape Town, South Africa",
        "Montreal, Canada",
        "Amsterdam, Netherlands",
    ]

    label = "Add a City to the Chart"
    with st.expander(label, expanded=False):
        options = sorted(df["City"].values.tolist())
        label = "Select or Deselect Cities"
        selections = st.multiselect(label, options, default=default_selections)
        filtered_df = df[df["City"].isin(selections)]

        source = "https://www.numbeo.com/cost-of-living/rankings_current.jsp"
        msg = f"See the data behind this chart a the [Numbeo Current Cost of Living Index]({source})."
        st.write(msg)

    return filtered_df


def bar_chart(df):
    column = "Cost of Living Plus Rent Index"
    df["city_name"] = df["City"].apply(lambda x: x.split(",")[0].strip())
    avocado_green = "#9EA856"
    blue = "#4099F5"
    label_angle = 0 if df.shape[0] < 10 else -90
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("city_name:N", 
                title=None,
                axis=alt.Axis(labelAngle=label_angle),
                ).sort('-y'),
        y=alt.Y(column),
        tooltip=[
            "City", 
            "Cost of Living Index", 
            "Cost of Living Plus Rent Index",
            "Groceries Index",
            "Restaurant Price Index",
            "Local Purchasing Power Index",
            ],
        color=alt.condition(
            alt.datum.city_name == "Tokyo",
            alt.value(avocado_green),
            alt.value(blue)
        ),
    ).properties(title={
        "text": "Tokyo is Surprisingly Affordable",
        "subtitle": f"{column}, Numbeo Current Cost of Living Index, July 2023"
    })
    st.altair_chart(chart, use_container_width=True)