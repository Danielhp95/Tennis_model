import unittest
import os, sys
atp_path = os.path.abspath(os.path.join('..','data','dao'))
sys.path.append(atp_path)
import tennisAtpDao as dao
import pandas as pd


class tennis_atp_dao_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        return 

    def test_can_concatenate_multiple_files(self):
        directory = r'test_data/single_match'

        c_df = dao.load_by_year(directory, 3, earliest_year=1)

        # Technical debt: Compare whole row, not just winner name
        assert(len(c_df[c_df.winner_name == 'Stanislas Wawrinka']) == 1)
        assert(len(c_df[c_df.winner_name == 'Tatsuma Ito']) == 1)
        assert(len(c_df[c_df.winner_name == 'Austin Krajicek']) == 1)

    def test_calculates_set_common_opponents(self):
        directory         = r'test_data/'
        dao.DATA_DIR      = directory
        dao.MATCH_FILES = 'common_opponents'
        set_com_opps, df_com_opps = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                                          latest_year=1,
                                                          earliest_year=1)

        assert(len(set_com_opps) == 1)
        assert('Austin Krajicek' in set_com_opps)

    def test_ignores_input_players_as_comm_opponents(self):
        directory = r'test_data/'
        dao.DATA_DIR = directory
        dao.MATCH_FILES = 'common_opponents_ignore_players'

        set_com_opps, df_com_opps = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                                         latest_year=1,earliest_year=1, courts=["Hard"])

        assert(len(set_com_opps) == 1)
        assert('Austin Krajicek' in set_com_opps)
        assert('Stanislas Wawrinka' not in set_com_opps)
        assert('Tatsuma Ito' not in set_com_opps)
                

    # Should have 2 of these, one for common opponents and another for data.
    def test_ignores_if_row_contains_nan_values(self):
        directory = r'test_data/'
        dao.DATA_DIR = directory
        dao.MATCH_FILES = 'common_opponents_nan_values'
        com_opps, df = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                            latest_year=1,earliest_year=1)
       
        assert(len(com_opps) == 0)
        assert(len(df) == 0)

    def test_can_filter_courts(self):
        directory = 'test_data/'
        dao.DATA_DIR = directory
        dao.MATCH_FILES = 'common_opponents'

        com_opps, df = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                            latest_year=1,earliest_year=1,
                                            courts=["Hard"])
        self.assertEqual(len(com_opps),1)
        self.assertEqual(len(df),2)

            
if __name__ == '__main__':
    unittest.main()
