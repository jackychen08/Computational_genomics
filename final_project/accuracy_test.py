import sys
from counting_bloom import CBloomFilter
from counting_cuckoo_np import Counting_Cuckoo

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


def parse_table(kmer_file):
    """
    Parses kmer_file to re-create the k-mer table generated from kmer.py; table[k-mer] = frequency
    """
    table = {}
    while True:
        first_line = kmer_file.readline()
        if len(first_line) == 0:
            break  # end of file
        frequency = first_line[1:].rstrip()
        kmer = kmer_file.readline().rstrip()
        table[kmer] = int(frequency)
    return table

fastq_file = sys.argv[1]        #fastq file 
kmer_file = sys.argv[2]         #kmer table of the data (obtained from kmer.py)
k = int(sys.argv[3])            #k-mer length
jellyfish_output = sys.argv[4]  #jellyfish output file for same fastq and k-mer length

with open(fastq_file) as fq:
    fastq_data = parse_fastq(fq)
fq.close()

reads = []
for fq in fastq_data:
    cur_read = fq[1]
    reads.append(cur_read)

#k-mer table will have true counts of all the k-mers
with open(kmer_file) as kf:
    kmer_table = parse_table(kf)
kf.close()

with open(jellyfish_output) as jfo:
    jf_table = parse_table(jfo)
jfo.close()

counting_cuckoo_np = Counting_Cuckoo(len(kmer_table.keys()), 3)
counting_bloom = CBloomFilter(len(kmer_table.keys()), 3)

#Inserting data into the two filters:
for read in reads:
    for i in range(0, len(read) - k + 1):
        kmer = read[i:i+k]
        counting_cuckoo_np.insert(kmer)
        counting_bloom.insert(kmer)

counting_cuckoo_np_incorrect = 0
counting_cuckoo_np_incorrect_mag = 0
counting_bloom_incorrect = 0
counting_bloom_incorrect_mag = 0
jellyfish_incorrect = 0
jellyfish_incorrect_mag = 0


for k in kmer_table.keys():
    true_frequency = kmer_table[k]

    if counting_cuckoo_np.search(k) != true_frequency:
        counting_cuckoo_np_incorrect += 1
        counting_cuckoo_np_incorrect_mag += abs(counting_cuckoo_np.search(k) - true_frequency)
    
    if counting_bloom.search(k) != true_frequency:
        counting_bloom_incorrect += 1
        counting_bloom_incorrect_mag += abs(counting_bloom.search(k) - true_frequency)
    
    if jf_table[k] != true_frequency:
        jellyfish_incorrect += 1
        jellyfish_incorrect_mag += abs(jf_table[k] - true_frequency)

total_kmers = len(kmer_table.keys())

print("Percentage incorrect")
print(" counting_cuckoo_np percentage incorrect:", float(counting_cuckoo_np_incorrect/total_kmers))
print(" counting_bloom percentage incorrect:" ,float(counting_bloom_incorrect/total_kmers))
print(" jellyfish incorrect:", float(jellyfish_incorrect/total_kmers))

print("========================")

print("Average error")
print(" counting_cuckoo_np average error:", float(counting_cuckoo_np_incorrect_mag/total_kmers))
print(" counting_bloom average error:" ,float(counting_bloom_incorrect_mag/total_kmers))
print(" jellyfish average error:", float(jellyfish_incorrect_mag/total_kmers))