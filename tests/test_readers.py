import os
import unittest
from unittest.mock import patch
from fasta_tools.fasta_readers import *


DUMMY_FASTA = '{}/test_files/dummy_fasta.fna'.format(os.path.dirname(os.path.abspath(__file__)))
TUPLES = [tuple(['>Line One', 'ATGTGATGTGATGTGAAAAATGTGATTGTGTG']), tuple(
    ['>Line Two', 'AAAATGTGATTGTGTGAAAATGTGATTGTGTGAAAATGTGATTGTGTG']), tuple(['>Line Three', 'GTGATTGTGTGAAGTGATTGTGTGAAGAAAATGTGATAATGTGATTG'])]

class Test_Readers(unittest.TestCase):

    def test_read_tuples(self):
        result = read_as_tuples(DUMMY_FASTA)
        self.assertEqual(result, TUPLES)
