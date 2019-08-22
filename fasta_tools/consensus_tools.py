import os
import random
import subprocess
from fasta_tools.check_depends import check_dependencies
from fasta_tools.fasta_getters import *
from fasta_tools.fasta_readers import read_as_tuples
from fasta_tools.fasta_writers import *

#from fasta_tools.fasta_tools import fasta_getters
#from fasta_tools.fasta_tools import fasta_writers
#from fasta_tools.fasta_tools import fasta_readers
#from fasta_getters import *
#from fasta_tools import fasta_writers
#from fasta_tools import check_depends


def make_consensus(fasta_file, output_path='consensus.fna', consensus_header=False):
    '''
    takes fasta file, runs clustal omega then uses
    embosser to make a consensus sequence returned
    in fasta format. You can also give a header to be used
    in the consensus file, otherwise emboss will rename it with
    a defualt name.
    '''
    check_dependencies()
    # passes fasta as list to get list, returns list of tuples
    element_tuples = read_as_tuples(fasta_file)

    con_elements = []
    if len(element_tuples) >= 10:
        con_elements = get_random_elements(element_tuples)
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

def get_random_elements(elements):
    '''
    selects 10 random elements of the family to make fasta file of
    elements should be of one family
    '''
    rand_elements = []
    max_range = 0
    if len(elements) < 50:
        max_range = len(elements)
    else:
        max_range = 50

    for i in range(0, max_range):
        rand = random.randint(0, len(elements) - 1)
        rand_elements.append(elements[rand])

    return rand_elements


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
