<<<<<<< HEAD
=======
# methods that get return information from a fasta file
# methods do not modify the original file

>>>>>>> 01d4e3c6005bcd6148e3780bb331fe38f89b4b54

def get_entry(identifier, fasta_file):
    '''
    Get an entry of fasta file with a line number or a header keyword
    If keyword is not unique the first hit will be returned
    Both ints and str identifiers will return the target line and the
    next line as a tuple
    '''
    try:
        with open(fasta_file) as fasta:
            if type(identifier) == int:
<<<<<<< HEAD
                fasta_lines = fasta.readlines()
                return (fasta_lines[identifier], fasta_lines[identifier+1])
=======
                    fasta_lines = fasta.readlines()
                    return (fasta_lines[identifier], fasta_lines[identifier+1])
>>>>>>> 01d4e3c6005bcd6148e3780bb331fe38f89b4b54
            elif type(identifier) == str:
                headers = get_fasta_headers()
                headers = [set(header.split(' ')) for header in headers]
                for header in headers:
                    if identifier in header:
                        return header

    except FileNotFoundError as e:
        return e


def get_fasta_headers(fasta_file, header_character='>'):
    '''
    returns all headers in given fasta file
    headers found using defualt header start character, '>'
    to chane this pass character to header_character
    '''
    try:
        with open(fasta_file) as fasta:
            headers = []
            for line in fasta:
                if line[0] == '>':
                    headers.append(line)
        return headers
    except FileNotFoundError as e:
        return e


def make_indexed_fasta(fasta_file):
    '''
    takes fasta file, returns a dictionary where keyword
    is line number (int) and value is string at that line
    line numbers start from 0
    '''
    try:
        dictionary = {}
        with open(fasta_file) as fasta:
            for i, line in enumerate(fasta):
                dict[i] = line
            return dictionary
    except (FileNotFoundError, KeyError) as e:
        return e
