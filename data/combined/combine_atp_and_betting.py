import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('..','..','src')))
import daos
from daos import bettingDao as betdao
from daos import tennisAtpDao as atpdao
from daos.decorators import atp_to_betting as dec

years = range(2007, 2018)

def combine_tables():
    for year in years:
        print("Year " + str(year))
        atp1, wta1 = atpdao.read_by_date(year, latest=year)

        atp1 = dec.change_name_atp_to_betting(dec.change_date_atp_to_betting(atp1))
        wta1 = dec.change_name_atp_to_betting(dec.change_date_atp_to_betting(wta1))

        atp2, wta2 = betdao.read_by_date(earliest=year, latest=year)

        atp_combined = dec.join_atp_and_bet_tables(atp1, atp2)
        wta_combined = dec.join_atp_and_bet_tables(wta1, wta2)
        
        atp_combined.to_csv(str(year) + '.csv')
        wta_combined.to_csv(str(year) + 'w.csv')

#atp, wta = atpdao.read_by_date(2007, 2007)
#atp = dec.change_date_atp_to_betting(atp).sort(['tourney_date'], ascending=1)
#wta = dec.change_date_atp_to_betting(wta).sort(['tourney_date'], ascending=1)
#atp2,wta2 = betdao.read_by_date(2007,2007)
#
#print(atp.head().filter(items=['tourney_date','winner_name','loser_name']))
#print(atp2.head().filter(items=['Date','Winner','Loser']))

combine_tables()
