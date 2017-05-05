import pandas as pd
from datetime import datetime
import itertools

def change_date_atp_to_betting(df):
    df['tourney_date'] = df['tourney_date'].apply(lambda x: str(x)[:4]+'-'+str(x)[4:6]+'-'+str(x)[6:])
    df['tourney_date'] = pd.to_datetime(df['tourney_date'])
    return df

def change_date_betting_to_atp(df):
    df["Date"] = df["Date"].apply(lambda x: str(x).replace('-',''))
    return df

def change_name_atp_to_betting(df):
    format_change = lambda x: x.split(' ', 1)[1] + ' ' + x.split(' ', 1)[0][0] + '.'
    df['winner_name']  = df['winner_name'].apply(format_change)
    df['loser_name']   = df['loser_name'].apply(format_change)
    return df

'''
 Dates do not match in atp and betting databases. This could be due to different timezones.
 This function checks if dates are within a small range, and renders them equal in that case,
 substituting one with the other. Function assumes that The names used in the player fields are
 use the same format -> Surname FirstLetterOfFirstName.

 Warning: function is slow. O(n**2) where n is the length of the shortest data frame
'''
def fix_dates_discrepancies(atp_df, bet_df, range_in_days=1):
    # TODO: Copy initial dfs? Or change input parameters?
    for i_atp, r_atp in atp_df.iterrows():
        for i_bet, r_bet in bet_df.iterrows():
            matching_winner_and_loser = (r_atp['winner_name'] == r_bet['Winner']) and (r_atp['loser_name'] == r_bet['Loser'])   

            similar_dates = dates_within_range(range_in_days, r_atp['tourney_date'], r_bet['Date'])
            if matching_winner_and_loser and similar_dates:
                atp_df.set_value(i_atp, 'tourney_date', bet_df.loc[i_bet]['Date'])
                break
    return atp_df, bet_df
    

def dates_within_range(range_in_days, d1, d2):
    #d1 = datetime.strptime(d1, "%Y-%m-%d")
    #d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days) <= range_in_days


