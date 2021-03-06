# sys.path.append('./fasta_tools')

from .version import __version__
from .fasta_formater import *
from .fasta_getters import *
from .fasta_writers import *
from .check_depends import *
from .consensus_tools import *
from .soy_tools import *

__all__ = [
    'write_from_list',
    'write_from_dictionary',
    'check_formating',
    'correct_1h1s_error',
    'write_from_list',
    'write_from_dictionary',
    'write_from_tuple_list',
    'check_dependencies',
    'read_as_tuples'
    'make_consensus',
    'get_entry',
    'get_random_elements',
    'clustalize',
    'embosser',
    'rename_emboss',
    'fasta_splitter',
    'one_consensus_method_to_rule_them_all',
    'fasta_getters'
]
