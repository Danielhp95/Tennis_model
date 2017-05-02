import unittest
from StringIO import StringIO

# Tests
from common_opponent_test import common_opponent_test
from tennis_atp_dao_test import tennis_atp_dao_test

stream = StringIO()
runner = unittest.TextTestRunner(stream=stream)

test_files = [common_opponent_test, tennis_atp_dao_test]
for suite in test_files:
    print(suite)
    result = runner.run(unittest.makeSuite(common_opponent_test))
    print(result)
