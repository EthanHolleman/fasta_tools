import os
import sys
import random
import subprocess

import numpy as np
from fasta_tools.fasta_formater import check_formating
from fasta_tools.check_depends import check_dependencies
from fasta_tools.fasta_getters import *
from fasta_tools.fasta_readers import read_as_tuples
from fasta_tools.fasta_writers import *
#from fasta_tools.fasta_formater import sub_fasta


def make_consensus(fasta_file, output_path='consensus.fna', consensus_header=False, min_elements=10, n=20):
    '''
    takes fasta file, runs clustal omega then uses
    embosser to make a consensus sequence returned
    in fasta format. You can also give a header to be used
    in the consensus file, otherwise emboss will rename it with
    a defualt name.
    '''
    check_dependencies()
    check_formating(fasta_file)
    # passes fasta as list to get list, returns list of tuples
    element_tuples = read_as_tuples(fasta_file)

    con_elements = []
    if len(element_tuples) >= min_elements:
        con_elements = get_random_elements(element_tuples, n)
    else:
        con_elements = element_tuples
        #  divide by two to avoid returning headers
    try:
        new_file = write_from_tuple_list(con_elements, output_path)
        print('new file written')
        # new_file is overwritten as location of consensus seq
        print("file writen to " + output_path)
        clustal_file = clustalize(new_file, output_path)
        embosser(clustal_file, output_path)

        return True

    except (FileNotFoundError, OSError) as e:
        return e

def get_random_elements(elements, n=20):
    '''
    Uses random choice without replacement to pick n indexes of the elements
    list. Elements at these indexes are then returned as a new list.
    '''
    n = verify_n(len(elements), n)
    choices = np.random.choice(len(elements), n, replace=False).tolist()
    return [elements[i] for i in choices]


def verify_n(len_elements, n, default_val=20):
    '''
    Checks to ensure that n < number of elements in the tuple list. If false
    then will return default val if n > default if this is also false then
    will return the length of the list of elements.
    '''
    if n > len_elements:
        if len_elements < default_val:
            return len_elements
        else:
            return default_val
    else:
        return n


def clustalize(rep_elements, output_path):
    '''
    runs clustal omega to create a clustalized file. Output path should include
    the filename.
    '''
    # print(clustal_command)
    # os.system(clustal_command)
    try:
        subprocess.call(['clustalo', '-i', rep_elements,
                         '-o', output_path, '-v', '--force'])
        return output_path
    except OSError as e:
        return e

def iter_consensus(rep_elements, num_elements, output, extension='.fasta'):
    '''
    Creates multible small consensus sequences then makes a composite of all
    of those consensus sequences. num_elements refers to the desired number of
    elements in each sub fasta file. Must be at least 2 to allow for clustal
    omega to work
    '''
    if num_elements < 2:
        print('num_elements must be > 2')
        sys.exit(1)

    TEMP_DIR = os.path.join(os.getcwd, 'temp')
    temp_dir = os.path.join(os.getcwd, TEMP_DIR)
    if not os.path.exists(temp_dir):  # make temp dir if does not exist
        os.mkdir(temp_dir)

    split_result = sub_fasta(rep_elements, num_elements)
    if split_result is 0:  # worked correctly
        split_list = [os.path.join(temp_dir, file + extension) for file in os.listdir(temp_dir)]
        # concat the temp file path with the names of all the files created
        # by the sub_fasta method
        for file in split_list:
            make_consensus(file, output_path=file)  # make consensus of all files
            # overwrite the file with the consensus to retain filenames
            # filename that split makes does not have extension so need
            # make sure that consensus methods will still work with that
            # attempted to fix using extension and to make it work better
            # with the cat command

        try:
            subprocess.call(['cat', '*{}'.format(extension), '>', output])
        except (OSError, FileNotFoundError, IsADirectoryError):
            return 1
        make_consensus(output, output_path=output)
        # make the final average consensus and overwrite the temp fasta of
        # the average consensus sequences




def remove_high_n(fasta_file, threshold=0.3):
    '''
    Parses a fasta file and writes a new fasta with only the elements that contain
    lower % of Ns then the given threshold. If overwrite is specified will over
    write the original file. If only one seq is present then will not rewrite
    even if sequence does reach the n threshold.
    '''
    fasta_file_tuples = read_as_tuples(fasta_file)
    seq_removed = 0
    if len(fasta_file) > 1:
        verified_entries = []
        for header, seq in fasta_file_tuples:
            if seq.count('N') / len(seq) >= 0.4:
                verified_entries.append(tuple([header, seq]))
            else:
                seq_removed += 1
        print('{} seqs removed from {}'.format(seq_removed, fasta_file))
        write_from_tuple_list(verified_entries, output_name=fasta_file)

    return fasta_file  # must return the filename so can be intgrated

def verify_consensus_ready(fasta_file):
    try:
        lines = []
        with open(fasta_file, 'r') as fasta:
            lines = fasta.readlines()
        if len(lines) >= 4:  # indicating only one entry will cause issues with consensus
            return True
        else:
            return False
    except FileNotFoundError:
        print('{} does not exist'.format(fasta_file))
        return False


def embosser(clustalized_file, output_path):
    '''
    runs embosse to create a consensus file of a previously
    clustalized file
    '''
    command = 'em_cons -datafile EDNAFULL -identity 2 -plurality 0.4 -sequence {} -outseq {} -snucleotide1 -name {}'.format(
        clustalized_file, output_path, os.path.basename(output_path))
    formated_command = command.split(' ')
    try:
        subprocess.call(formated_command)
        return 1
    except (FileNotFoundError, OSError) as e:
        return e
    # os.system(command)
    #rename_emboss(header, output_name)


def rename_emboss(header, embossed_file):
    '''
    renames the defualt emboss given header in the consensus fasta
    to a user supplied one
    '''
    if header is not False:
        lines = []
        with open(embossed_file, 'r') as emboss:
            lines = emboss.readlines()
        with open(embossed_file, 'w') as emboss:
            emboss.write(header + '\n' + lines[1])


def format_consensus(consensus_file):
    '''
    reformats a consensus file
    '''
    lines = []
    with open(consensus_file, 'r') as con:
        lines = con.readlines()
    with open(consensus_file, 'w') as con:
        for line in lines:
            if line[0] == '>':
                con.write('> ' + consensus_file + '\n')
            else:
                con.write(line.strip())
