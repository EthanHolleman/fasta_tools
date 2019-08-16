
def read_as_tuples(fasta_file):
    fasta_file = str(fasta_file)
    '''
    reads a fasta file and returns a list of tuples
    with format [('header', 'sequence')]
    '''
    try:
        with open(fasta_file) as fasta:
            fasta = fasta.readlines()
            fasta = [x.strip() for x in fasta]
            return [tuple(fasta[i:i + 1]) for i in range(0, len(fasta), 2)]
    except FileNotFoundError as e:
        return e

def read_as_list():
    pass
    '''
    reads a fasta file and returns as a list
    '''

def read_as_indexed_dict(fasta_file):
    pass

def chunk(l, n):
    '''Yield successive n-sized chunks from l.'''
    for i in range(0, len(l), n):
        yield l[i:i + n]
