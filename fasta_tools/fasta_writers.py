def write_from_list(fasta_list, output_name):
    # writes fasta file from list [header, seq, header,..]
        with open(output_name, 'w') as out:
            for line in fasta_list:
                out.write(line.strip() + '\n')


def write_from_dictionary(fasta_dict,output_name):
    # writes fasta file from dictionary, assumes key = header, seq = value
        with open(output_name, 'w') as out:
            for key, value in fasta_dict.items():
                out.write('{}\n{}\n').format(key.strip(), value.strip())


def write_from_tuple_list(fasta_tuples, output_name):
    # writes fasta file from list tuples, [(header, seq)]
        with open(output_name, 'w') as out:
            for tuple in fasta_tuples:
                header, seq = tuple
                out.write('{}\n{}\n').format(key.strip(), value.strip())
