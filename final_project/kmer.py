import sys

#Source: Professor Langmead
def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
    reads = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads.append((name, seq, qual))
    return reads


def make_kmer_table(reads, k):
    """ Given read dictionary and integer k, return a dictionary that
    maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for read in reads:
        for i in range(0, len(read) - k + 1):
            kmer = read[i:i+k]
            if kmer not in table:
                table[kmer] = 1
            else:
                table[kmer] += 1
    return table


fastqfile = sys.argv[1]
K = int(sys.argv[2])        #length of k-mer being made
outputfile = sys.argv[3]    

#fastq file processing
with open(fastqfile) as fq:
    fastq_data = parse_fastq(fq)
fq.close()

reads = []

for fq in fastq_data:
    cur_read = fq[1]
    reads.append(cur_read)

kmer_table = make_kmer_table(reads, K)

output = open(outputfile, "w")
for kmer in kmer_table.keys():
    frequency = kmer_table[kmer]
    output.write(">" + str(frequency) + "\n" + kmer + "\n")

output.close()