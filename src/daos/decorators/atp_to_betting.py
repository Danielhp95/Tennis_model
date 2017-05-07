import pandas as pd
from dateutil.relativedelta import relativedelta
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

def join_atp_and_bet_tables(atp=None, bet=None):
    range_in_days = 3
    atp, bet = fix_dates_discrepancies(atp, bet, 3)
    res = pd.merge(bet, atp, how='inner',
                   left_on=['Date','Winner','Loser'],
                   right_on=['tourney_date','winner_name','loser_name'])
   
    # Many columns appear in both tables, Here we drop the repeated columns from bet
    # We will then stick to atp_dao from now on
    columns_to_drop = ['Winner','Loser','Date','Tournament','Court','Surface','ATP','Location','Date']
    res = res.drop(columns_to_drop)
    return res

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
    date_1 = datetime.strptime(d1,'%Y-%m-%d')
    date_2 = datetime.strptime(d2,'%Y-%m-%d')
    r = relativedelta(date_1,date_2)
    return abs(r.days) <= range_in_days


