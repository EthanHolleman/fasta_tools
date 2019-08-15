import unittest
from unittest.mock import patch

from fasta_tools.consensus_tools import *


DUMMY_FASTA = 'test_files/dummy_fasta.fna'
TEMP_OUT = 'temp.fasta'


class Test_Clustalo(unittest.TestCase):

    # @mock.patch('consensus_tools.subprocess')
    def test_call(self):
        clustal_correct = ['clustalo', '-i',
                           DUMMY_FASTA, '-o', TEMP_OUT, '-v', '--force']
        with patch('fasta_tools.consensus_tools.subprocess.call') as mock_call:
            mock_call.return_value = DUMMY_FASTA
            clustalo_result = clustalize(DUMMY_FASTA, TEMP_OUT)

            mock_call.assert_called_with(clustal_correct)
            self.assertEqual(clustalo_result, TEMP_OUT)


class Test_Embosser(unittest.TestCase):
    command = 'em_cons -sformat pearson -datafile EDNAFULL -sequence {} -outseq {} -snucleotide1 -name {}'.format(
        DUMMY_FASTA, TEMP_OUT, os.path.basename(TEMP_OUT))
    formated_command = command.split(' ')

    def test_emboss_positive(self):
        with patch('fasta_tools.consensus_tools.subprocess.call') as mock_call:
            mock_call.return_value = 1
            emboss_result = embosser(DUMMY_FASTA, TEMP_OUT)

            mock_call.assert_called_with(Test_Embosser.formated_command)
            self.assertEqual(emboss_result, 1)

    def test_emboss_negative(self):
        with patch('fasta_tools.consensus_tools.subprocess.call') as mock_call:
            mock_call.return_value = FileNotFoundError
            emboss_result = embosser(DUMMY_FASTA, TEMP_OUT)

            mock_call.assert_called_with(Test_Embosser.formated_command)
            self.assertEqual(emboss_result, FileNotFoundError)



class Test_Make_Consensus(unittest.TestCase):
    pass

    def test_results(self):
        pass


if __name__ == '__main__':
    unittest.main()
