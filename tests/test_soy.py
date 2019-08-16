import unittest
import subprocess
from unittest.mock import patch

from fasta_tools.soy_tools import *

SOY = DUMMY_FASTA = '{}/test_files/soy_fasta.fna'.format(os.path.dirname(os.path.abspath(__file__)))
GOLD_HEADER = ''
GOLD_DICT = ''
PARSED_HEADER = {'>name': 'RLG_Gmr342_Gm11-1', 'Reference': 'Du et al. 2010 BMC Genomics 2010, 11:113', 'Class': 'I', 'Sub_Class': 'I', 'Order': 'LTR', 'Super_Family': 'Gypsy', 'Family': 'Gmr342', 'Description': 'SOLO'}

with open(SOY) as SOY:
    GOLD_HEADER = SOY.readline()

class Test_Soy(unittest.TestCase):

    def test_header_parser(self):
        result = parse_header_dict(GOLD_HEADER)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, PARSED_HEADER)
