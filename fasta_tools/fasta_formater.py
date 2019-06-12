import os


def check_formating(fasta_file):
<<<<<<< HEAD
    # runs all existing format check and fix methods, will expand as needed
    # change this to fasta tuples list or something so only read data once
=======
    '''runs all existing format check and fix methods, will expand as needed'''
>>>>>>> 01d4e3c6005bcd6148e3780bb331fe38f89b4b54
    no_error = True

        if no_error:
            print('No errors found')


def check_1h1s_error(fasta_file):
    with open(fasta_file, 'r') as fasta:
        for i, line in enumerate(fasta):
            if i % 2 == 0 and line[0] != '>':
                return False


def correct_1h1s_error(fasta_file):
    '''
    corrects file having sequence on multible lines
    1h1s = 1 header, 1 sequence
    '''
    header_list = []
    seq_list = []
    current_seq = ''

    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line[0] == '>':
                header_list.append(line.strip())
                if current_seq != '':
                    seq_list.append(current_seq)
                    current_seq = ''
            else:
                current_seq += line.strip()

    with open(fasta_file, 'w') as fasta:
        seq_list.append(current_seq)
        for header, seq in zip(header_list, seq_list):
            fasta.write('{}\n{}\n'.format(header, seq))
