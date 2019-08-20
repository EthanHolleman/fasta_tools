
def read_as_tuples(fasta_file):
    '''
    reads a fasta file and returns a list of tuples
    with format [('header', 'sequence')]
    '''
    try:
        with open(fasta_file) as fasta:
            n = 2
            fasta = fasta.readlines()
            fasta = [x.strip() for x in fasta]
            return [tuple(fasta[i * n:(i + 1) * n]) for i in range((len(fasta) + n - 1) // n )]
    except FileNotFoundError as e:
        return e

print(read_as_tuples('/media/ethan/Vault/Soy_fams/Gypsy/Gmr128SOLO.fna'))

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
