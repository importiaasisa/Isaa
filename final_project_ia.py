import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Starbucks in the Americas", page_icon=":coffee:",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>.stApp {background-color: #00704a; font-family: Helvetica; color: white;}</style>""",
            unsafe_allow_html=True)

american_countries = ["US", "CA", "MX", "PA", "GT", "CL", "AR", "CR", "SV"]
state_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
              "LA",
              "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
              "OK",
              "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
ownership_type = ["CO", "JV", "LS", "FR"]


def read_data():
    df = pd.read_csv("starbucks_10000_sample.csv").set_index("Id")
    return df


def filter_country(sel_countries):
    df = read_data()
    df = df.loc[df['CountryCode'].isin(sel_countries)]

    return df


def filter_state(df, select_state):
    filter_data = df[df['CountrySubdivisionCode'].isin(select_state)]
    return filter_data


def bar_graph(df):
    if df.empty:
        st.write("No data found.")
    else:
        ownership_count = df['OwnershipType'].value_counts()
        fig, ax = plt.subplots(figsize=(16, 12))
        ownership_count.plot(kind='bar', ax=ax)
        sns.countplot(x='OwnershipType', hue='CountryCode', data=df, ax=ax)
        ax.set_xlabel('Ownership Type')
        ax.set_ylabel('Number of Occurrences')
        ax.set_title('Most Popular Ownership Types in the Americas')
        st.pyplot(fig)


def america_map(df):
    map_df = df.filter(['Name', 'Longitude', 'Latitude'])
    map_df['Latitude'] = map_df['Latitude'].astype(float)
    map_df['Longitude'] = map_df['Longitude'].astype(float)
    st.write(map_df)
    map_info = pdk.ViewState(latitude=map_df["Latitude"].mean(), longitude=map_df["Longitude"].mean(), zoom=5)
    layer = pdk.Layer('ScatterplotLayer', data=map_df, get_position='[Longitude, Latitude]', get_radius=50000,
                      get_color=[0, 112, 74], pickable=True)
    map_visual = {'html': 'Listing:<b>{Name}</b>'}
    map = pdk.Deck(map_style="mapbox://styles/mapbox/dark-v9", initial_view_state=map_info, layers=[layer],
                   tooltip=map_visual)
    st.pydeck_chart(map)


def american_pie(df):
    if df.empty:
        st.write("No data found.")
    else:
        country_counts = df.groupby(['CountryCode', 'CountrySubdivisionCode']).size().reset_index(name='counts')
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.pie(country_counts['counts'],
               labels=country_counts['CountryCode'] + '-' + country_counts['CountrySubdivisionCode'],
               autopct='%1.1f%%')
        ax.set_title('Countries (and US states) with the Most Starbucks Stores')
        st.pyplot(fig)


def main():
    st.image('Starbucks_Corporation_Logo_2011.svg.png', width=150)
    st.title("Starbucks in the Americas")
    st.subheader("designed by Isabella Ampie")
    st.text("From the selection of 10,000 stores around the globe, check out some cool stats!")
    read_data()
    select_cty = st.multiselect('Choose Your Country', options=american_countries, default=[])
    df = filter_country(select_cty)

    if 'US' in select_cty:
        select_state = st.multiselect('Choose Your State', options=state_list)
        df = filter_state(df, select_state)

    america_map(df)
    bar_graph(df)
    american_pie(df)


main()
