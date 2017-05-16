import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('..','..','src')))
import daos
from daos import bettingDao as betdao
from daos import tennisAtpDao as atpdao
from daos.decorators import atp_to_betting as dec

years = range(2007, 2018)

def combine_tables(year):
    print("Year " + str(year))
    atp1, wta1 = atpdao.read_by_date(year, latest=year)

    atp1 = dec.change_name_atp_to_betting(dec.change_date_atp_to_betting(atp1))
    wta1 = dec.change_name_atp_to_betting(dec.change_date_atp_to_betting(wta1))

    atp2, wta2 = betdao.read_by_date(earliest=year, latest=year)

    print(atp2.columns.values)
    atp_combined = dec.join_atp_and_bet_tables(atp1, atp2)
    wta_combined = dec.join_atp_and_bet_tables(wta1, wta2)

    atp_combined = pd.DataFrame(zip([1],[1]))
    wta_combined = pd.DataFrame(zip([1],[1]))
    
    atp_combined.to_csv(str(year) + '.csv')
    wta_combined.to_csv(str(year) + 'w.csv')

combine_tables(int(sys.argv[1]))
