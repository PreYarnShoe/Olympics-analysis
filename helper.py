from typing import final

import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally_total = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally_total = medal_tally_total.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally_total['Total'] = medal_tally_total['Gold'] + medal_tally_total['Silver'] + medal_tally_total['Bronze']

    medal_tally_total['Gold'] = medal_tally_total['Gold'].astype('int')
    medal_tally_total['Silver'] = medal_tally_total['Silver'].astype('int')
    medal_tally_total['Bronze'] = medal_tally_total['Bronze'].astype('int')
    medal_tally_total['Total'] = medal_tally_total['Total'].astype('int')
    medal_tally_total.reset_index(drop=True, inplace=True)
    medal_tally_total.index = medal_tally_total.index + 1
    return medal_tally_total

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return country, years

def fetch_medal_tally(df, year, country):
    global temp_df
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City', 'Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()

        x['Year'] = x['Year'].astype(str)
        #y = pd.DataFrame({'Year': ['Total'], 'Gold': [x['Gold'].sum()], 'Silver': [x['Silver'].sum()], 'Bronze': [x['Bronze'].sum()]})
        #x = pd.concat([x,y], ignore_index=True)
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x.reset_index(drop=True, inplace=True)
    x.index = x.index + 1
    return x

def data_nations_overtime(df, col):
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    data_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return data_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medal','region':'Region'},inplace=True)
    return x

def yearwise_country_madeltally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'Year', 'NOC', 'Sport', 'Event', 'City', 'Medal', 'Games'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'Year', 'NOC', 'Sport', 'Event', 'City', 'Medal', 'Games'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    return final_df

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medal','region':'Region'},inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    male = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = male.merge(female, on='Year', how='left')
    final.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'},inplace=True)
    final = final.fillna(0).astype(int)
    return final
