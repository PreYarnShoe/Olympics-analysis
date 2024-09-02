import pandas as pd
import numpy as np



def preprocess(df,regions_df):
    #filter summer olympics
    df = df[df['Season'] == 'Summer']
    #merge with region_df
    df = df.merge(regions_df, on='NOC', how='left')
    #drop duplicates
    df.drop_duplicates(inplace=True)
    #OHEncode medal column
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df