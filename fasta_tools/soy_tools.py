from fasta_writers import *
from fasta_readers import *
from fasta_formater import *
from consensus_tools import make_consensus
import os

allowed_fasta_types = ['fna', 'fasta', 'fa']

def parse_header_tuple(header):
    '''
    parses a soybase header into a tuple, not currently handling the reference
    for soy base headers
    '''
    return tuple(header.split(' '))

def parse_header_dict(header, delim=' ', delim_key_value='='):
    '''
    parses soybase header as a dictionary with the pre = strings of the header
    as the keys and post = as the values
    '''
    keys, values = [], []
    reference_info = ''
    split_header = header.split(delim)
    for item in split_header:
        e_split = item.split(delim_key_value)
        if len(e_split) == 2:
            keys.append(e_split[0])
            values.append(e_split[1])
        else:
            reference_info += ' ' + item

    dictionary = dict(zip(keys, values))
    dictionary['Reference'] += reference_info

    return dictionary

def identify_LTR(header):
    '''
    Takes in the header of a soybase element and returns true if of an LTR family
    and false otherwise by looking if intact. This is important for the
    transposer pipeline.
    '''
    dict = parse_header_dict(header)
    if dict['Order'] == 'LTR':
        return True
    else:
        return False

def get_clean_filename(filename):
    return os.path.basename(filename).split('.')[0]

def get_clean_file_ext(filename):
    return os.path.basename(filename).split('.')[-1]


def seperate_types(single_element_fasta, write_path='', file_ext='.fna'):
    '''
    Creates two fasta files one containing intact elements and another containing solo
    elements from a fasta file of a single family of elements but containg both solo and
    intacts. Important for creating consensus sequences to feed to transposer. New files are named
    as family name_status.fna and file names are returned as a tuple
    '''
    tuples = read_as_tuples(single_element_fasta)
    solos, intacts = [], []
    ind = ('SOLO', 'INTACT')
    filename = get_clean_filename(single_element_fasta)

    for element in tuples:
        header, seq = element
        temp_dict = parse_header_dict(header)
        description = temp_dict['Description']

        if description == 'SOLO':
            solos.append(element)
        elif description == 'INTACT':
            intacts.append(element)

    solo_path = os.path.join(write_path, filename + ind[0] + file_ext)
    intact_path = os.path.join(write_path, filename + ind[1] + file_ext)

    write_from_tuple_list(solos, solo_path)
    write_from_tuple_list(intacts, intact_path)

    return tuple([solo_path, intact_path])


def seperate_types_supfamily_wide(family_folder, write_path='', verbose=True):
    '''
    Seperates the solo and intact elements of all the fasta files contained
    within a folder. It is intended that all files are from the same family but
    this is not a requirement.
    '''
    write_log = []
    fam_files = os.listdir(family_folder)
    #fam_files = [file for file in fam_files if get_clean_file_ext(file) in allowed_fasta_types]
    # validates all files are of the fasta type

    for file in fam_files:
        file = os.path.join(family_folder, file)
        if verbose is True:
            print('Seperating {}'.format(file))
        solos, intacts = seperate_types(file, write_path)
        write_log.append(solos)
        write_log.append(intacts)

    return write_log

def make_consensus_name(og_file, keyword='consensus', new_path=None):
    base = os.path.basename(og_file)
    file, ext = tuple(base.split('.'))
    if new_path is None:
        path = og_file.replace(base, '')
    else:
        path = new_path
        if path[-1] != '/':
            path = '{}{}'.format(path, '/')

    return '{}{}_{}.{}'.format(path, keyword, file, ext)


def one_consensus_method_to_rule_them_all(super_family_dir, output_path=None, verbose=True, rm_seperated=True):
    '''
    given a directory of a superfamily, seperates each family into solo and intact
    elements, then creates a consensus for each of those element types.
    '''
    con_log = []
    type_log = seperate_types_supfamily_wide(super_family_dir, super_family_dir, verbose=verbose)
    print(type_log)

    for file in type_log:
        con_name = make_consensus_name(file)
        out_name = make_consensus_name(file, new_path=output_path)
        print(out_name + '============================')
        if verbose == True:
            print('Making consensus of: {}'.format(file))
        make_consensus(file, output_name=out_name)

        con_log.append(con_name)
        check_formating(con)

        if rm_seperated is True:
            os.remove(file)

    return con_log


one_consensus_method_to_rule_them_all(super_family_dir='/media/ethan/Vault/Soy_fams/Gypsy', output_path='/home/ethan/Documents/test_con')

def split_fasta_writer(element_dict, file_name_editor=False, file_ext='.fna'):
    '''
    Writes a fasta file containing only elements of a specific family as specified through
    the data structure created by the fasta_splitter method. It is not recommended to use
    this method on its own and should only be called by fasta_splitter
    '''
    file_name = ''

    for super_family in element_dict:
        try:
            os.mkdir(super_family)
            file_structure[super_family] = []
        except FileExistsError:
            print('Dir exists')

        for family in element_dict[super_family]: # access a given super family
            if file_name_editor is not False:  # apply file editing function if provided
                file_name = file_name_editor(family)
            else:
                file_name = os.path.join(super_family, family + '.fna')

            write_from_tuple_list(element_dict[super_family][family], file_name)


def fasta_splitter(big_fasta_file, dir_key = 'Super_Family', soy_key='Family', file_name_editor=False, file_ext='.fna'):
    '''
    Method that splits a large fasta file containing many different types of elements into
    many fasta files each with one type of element. Splitting is done based on content of the header and so
    each element should have a unique identifier at an index when split by some delimiter (default = ' ')
    To rename a file you can also pass a function that alters a the string at the file_namer_index if that string alone
    is not enough. Defualt file extension for renaming is .fna
    '''
    fasta_tuples = read_as_tuples(big_fasta_file)
    element_dict = {}
    file_names = []

    for header, seq in fasta_tuples:
        temp_dict = parse_header_dict(header)
        super_family = temp_dict[dir_key]
        family = temp_dict[soy_key].replace('/', '_')

        if super_family not in element_dict:
            element_dict[super_family] = {family: [(header, seq)]}
            file_names.append(super_family)
        else:
            family_dict = element_dict[super_family]
            if family not in family_dict:
                element_dict[super_family][family] = [(header, seq)]
            else:
                element_dict[super_family][family].append((header, seq))

    split_fasta_writer(element_dict, file_name_editor, file_ext)
    return get_clean_filename
