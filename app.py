import streamlit as st
import pandas as pd
import preprocessing,helper
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from helper import medal_tally

st. set_page_config(layout="wide")

df = pd.read_csv('athlete_events.csv')
regions_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocess(df, regions_df)
#df = df[df['Year'] != 1906]

#st.sidebar.header('Olympics Analysis')
st.sidebar.markdown("<h1 style='font-size: 36px;'><b>Olympics Analysis</b></h1>", unsafe_allow_html=True)
st.sidebar.image('pngwing.com (4).png')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    country,years = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_nations_overtime(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_nations_overtime(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_nations_overtime(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of events overtime in every sport")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    #country_list.insert(0,'Overall')

    selected_country = st.sidebar.selectbox('Select a country',country_list)

    country_df = helper.yearwise_country_madeltally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + ' Medal tally over years')
    if country_df.empty:
        st.write("No medals won till now.")
    else:
        st.plotly_chart(fig)

    country_heatmap = helper.country_event_heatmap(df,selected_country)
    st.title(selected_country + ' excels in following sports')
    if country_heatmap.empty:
        st.write("No medals won till now.")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(country_heatmap,annot=True)
        st.pyplot(fig)

    top10_df = helper.most_successful_countrywise(df,selected_country)
    if not top10_df.empty:
        st.title("Top 10 Athletes of " + selected_country)
        st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sport = df['Sport'].unique()
    remove_sports = ['Equestrianism', 'Modern Pentathlon', 'Trampolining', 'Lacrosse', 'Racquets', 'Motorboating',
                     'Croquet',
                     'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
                     'Alpinism', 'Aeronautics']
    famous_sport = famous_sport[~np.isin(famous_sport, remove_sports)]
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age by Sport(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("Weight Vs Height")
    selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x= temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],size=60)
    st.pyplot(fig)

    st.title("Men vs Women participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Men','Women'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)