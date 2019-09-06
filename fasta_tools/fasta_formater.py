import os
import subprocess
from fasta_tools.fasta_readers import read_as_tuples


def sub_fasta(fasta_path, wrap):
    # wrap should be the number of elements in each new file
    try:
        subprocess.call(['split', '-l', wrap fasta_file])
        return 0
    except OSError as e:
        return e

def check_formating(fasta_file, overwrite=True):
    # TODO: Should check and try to correct carrot errors as this will effect 1h1s errors
    '''
    runs all existing format check and fix methods, will expand as needed
    by defualt a fasta file with errors found in it will be overwritten
    but you can edit this action by setting overwrite to false, this will
    return a tuple of error types but will make no corrections
    '''
    error_types = []
    with open(fasta_file) as fasta:
        fasta = fasta.readlines()

        if check_1h1s_error(fasta) == True:
            error_types.append('1h1s error')
            if overwrite:
                write_fasta_from_zip(correct_1h1s_error(fasta), fasta_file)
        if check_carrot_error(fasta) == tuple:
            error_types.append('carrot error')

        if error_types == []:
            return 'Passed all Tests'
        else:
            return tuple(error_types)


def check_1h1s_error(fasta_list):
    '''
    Checks fasta in list format for a 1h1s error
    returns true if present and false otherwise
    '''
    for i, line in enumerate(fasta_list):
        if i % 2 == 0 and line[0] != '>':
            return True
    return False


def check_carrot_error(fasta_list):
    '''Checks if all headers begins with >'''
    error_indicies = []
    for i in range(0, len(fasta_list), 2):
        if fasta_list[i][0] != '>':
            error_indicies.append(i)

    if error_indicies != []:
        return tuple(error_indicies)
    else:
        return False


def correct_1h1s_error(fasta_list):
    '''
    takes fasta file in list format that has multible sequence
    line per header and returns a zipped list of headers and corresponding
    complete sequences
    '''
    header_list = []
    seq_list = []
    current_seq = ''

    for line in fasta_list:
        if line[0] == '>':
            header_list.append(line.strip())
            if current_seq != '':
                seq_list.append(current_seq)
                current_seq = ''
        else:
            current_seq += line.strip()
    seq_list.append(current_seq)

    return zip(header_list, seq_list)
