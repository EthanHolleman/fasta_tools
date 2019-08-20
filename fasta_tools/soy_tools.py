import os

from fasta_tools.check_depends import check_dependencies
from fasta_tools.fasta_getters import *
from fasta_tools.fasta_readers import read_as_tuples
from fasta_tools.fasta_writers import *
from fasta_tools.fasta_formater import check_formating
from fasta_tools.consensus_tools import *

ALLOWED_FASTAS = ['fna', 'fasta', 'fa']  # allowed file extensions for methods parsing fasta files


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
    written_files = []
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

    if len(solos) >= 1:  # ensures if only one type do not try to write empty file
        write_from_tuple_list(solos, solo_path)
        written_files.append(solo_path)
    if len(intacts) >= 1:
        write_from_tuple_list(intacts, intact_path)
        written_files.append(intact_path)

    return tuple(written_files)


def seperate_types_supfamily_wide(family_folder, write_path='', verbose=True):
    '''
    Seperates the solo and intact elements of all the fasta files contained
    within a folder. It is intended that all files are from the same family but
    this is not a requirement.
    '''
    write_log = []
    fam_files = os.listdir(family_folder)

    for file in fam_files:
        file = os.path.join(family_folder, file)
        if verbose is True:
            print('Seperating {}'.format(file))
        written_files = seperate_types(file, write_path)
        for file in written_files:
            write_log.append(file)

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
    given a directory of a collection of superfamily fasta files, seperates
    each family into solo and intact
    elements, then creates a consensus for each of those element types.
    WARNING: Currently the output directory cannot be a sub directory of the
    superfamily directory. Fix to this coming in the future.
    '''
    con_log = []
    error_log = {}
    type_log = seperate_types_supfamily_wide(super_family_dir, super_family_dir, verbose=verbose)
    #  type_log is the list of solo / intact element families created from fasta files
    #  at the faimly level. This means that the original superfamily fasta should have
    #  already been split using fasta_slitter methods
    for file in type_log:
        diagnostic = True
        check_formating(file)
        con_name = make_consensus_name(file)
        out_name = make_consensus_name(file, new_path=output_path)
        if verbose is True:
            print('Making consensus of: {}'.format(file))
        if verify_consensus_ready(file) is True:
            print('File can be alligned')
            diagnostic = make_consensus(file, output_path=out_name)
        else:
            single_seq = read_as_tuples(file)
            write_from_tuple_list(single_seq, out_name)
        # writes consensus, output will be
        #  true if successful or FileNotFoundError or  OSError if fails
        #  failures are logged as dictionary; key == file value == list
        #  with last item being the error object

        # verify consensus ensures consensus can be made of the file by testing
        # if has more than one entry.


        if diagnostic is not True:
            error_log[file] = [con_name, out_name, diagnostic]
            print(diagnostic)
            continue

        con_log.append(out_name)
        check_formating(out_name)

        if rm_seperated is True:  # removes the non consensus file is value is true
            os.remove(file)

    return tuple([con_log, error_log])


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
            #file_structure[super_family] = []
        except FileExistsError:
            print('Dir exists')

        for family in element_dict[super_family]:  # access a given super family
            if file_name_editor is not False:  # apply file editing function if provided
                file_name = file_name_editor(family)
            else:
                file_name = os.path.join(super_family, family + '.fna')

            write_from_tuple_list(element_dict[super_family][family], file_name)


def fasta_splitter(big_fasta_file, dir_key='Super_Family', soy_key='Family', file_name_editor=False, file_ext='.fna'):
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
