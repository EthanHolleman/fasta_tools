import os
import random
import subprocess
from fasta_readers import *
from fasta_writers import *
from check_depends import *


def make_consensus(fasta_file, output_name='consensus.fna', consensus_header=False, rep_elements=True):
    '''
    takes fasta file, runs clustal omega then uses
    embosser to make a consensus sequence returned
    in fasta format. You can also give a header to be used
    in the consensus file, otherwise emboss will rename it with
    a defualt name.
    '''
    check_dependencies()

    element_tuples = read_as_tuples(str(fasta_file))   # passes fasta as list to get list, returns list of tuples

    con_elements = []
    if rep_elements is True:
        con_elements = get_random_elements(element_tuples)
    else:
        con_elements = [element_tuples[index/2] for index in rep_elements]
        #  divide by two to avoid returning headers

    try:
        new_file = write_from_tuple_list(con_elements, output_name)
        print("file writen to " + output_name)
        embosser(clustalize(new_file, output_name), consensus_header, output_name)

    except (FileNotFoundError, OSError) as e:
        return e


def get_random_elements(elements):
    '''
    selects 10 random elements of the family to make fasta file of
    elements should be of one family
    '''
    rand_elements = []
    max_range = 0
    if len(elements) < 20:
        max_range = len(elements)
    else: max_range = 20

    for i in range(0, max_range):
        rand = random.randint(0, len(elements)-1)
        rand_elements.append(elements[rand])

    return rand_elements


def clustalize(rep_elements, output_name):
    '''
    runs clustal omega to create a clustalized file
    '''
    #print(clustal_command)
    #os.system(clustal_command)
    try:
        clustal_call = subprocess.call(['clustalo', 'i', rep_elements, '-o', output_name, '-v', '--force'])
        if clustal_call < 0:
            print('Clustal call to make: {} returned {}'.format(output_name, clustal_call))
        return output_name
    except OSError as e:
        return e


def embosser(clustalized_file, header, output_name):
    '''
    runs embosse to create a consensus file of a previously
    clustalized file
    '''
    command = 'em_cons -sformat pearson -datafile EDNAFULL -sequence {} -outseq {} -snucleotide1'.format(clustalized_file, output_name)
    formated_command = command.split(' ')
    try:
        subprocess.call(formated_command)
    except (FileNotFoundError, OSError) as e:
        return e
    #os.system(command)
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
