from .version import __version__
from .fasta_formater import *
from .fasta_getters import *
from .fasta_writers import *

# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
    'write_from_list',
    'write_from_dictionary',
]
