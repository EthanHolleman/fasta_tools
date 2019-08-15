import unittest
print(__name__)
from fasta_tools.consensus_tools import *



DUMMY_FASTA = './test_files/dummy_fasta.fna'
TEMP_OUT = './temp.fasta'

class Test_Clustalo(unittest.TestCase):

    def test_output(self):
        output = clustalize(DUMMY_FASTA, TEMP_OUT)
        self.assertEqual(output, TEMP_OUT, 'Should be dummy fasta path')

class Test_verify(unittest.TestCase):

    def test_verify(self):
        output = verify_consensus_ready(DUMMY_FASTA)
        self.assertTrue(output)





if __name__ == '__main__':
    unittest.main()
