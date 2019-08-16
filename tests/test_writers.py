import unittest
import subprocess
from unittest.mock import patch

from fasta_tools.fasta_writers import *

GOLD_PATH = 'GOLD.fasta'
GOLD_CONTENT = '>One\nATGC\n>Two\nATGTCATCG\n>Three\nATGTAT\n'
TEMP_PATH = 'temp.fasta'

LIST = GOLD_CONTENT.split('\n')
TUPLES = [tuple(['>One', 'ATGC']), tuple(
    ['>Two', '>ATGTCATCG']), tuple(['>hree', 'ATGTAT'])]


class Test_Writers(unittest.TestCase):
    # basic structure is write the gold content then read it back and compare
    def setUp(self):
        with open(GOLD_PATH, 'w') as gold:
            gold.write(GOLD_CONTENT)

    def tearDown(self):
        subprocess.call(['rm', TEMP_PATH])
        subprocess.call(['rm', GOLD_PATH])

    def test_list(self):
        write_from_list(fasta_list=LIST, output_name=TEMP_PATH)
        with open(TEMP_PATH, 'r') as temp:
            read = ''.join(temp.readlines())
            # print(read)
            self.assertEqual(read, GOLD_CONTENT)

    def test_tuples(self):
        write_from_tuple_list(fasta_tuples=TUPLES, output_name=TEMP_PATH)
        with open(TEMP_PATH, 'r') as temp:
            read = temp.readlines().strip()
            self.assertEqual(read, LIST)
