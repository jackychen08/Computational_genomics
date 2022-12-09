import sys
from counting_bloom import CBloomFilter
from cuckoo import Cuckoo
from counting_cuckoo import Counting_Cuckoo

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

#parses kmer_file to re-create the k-mer table -> table[k-mer] = frequency
def parse_table(kmer_file):
    table = {}
    while True:
        first_line = kmer_file.readline()
        if len(first_line) == 0:
            break  # end of file
        frequency = first_line[1:].rstrip()
        kmer = kmer_file.readline().rstrip()
        table[kmer] = int(frequency)
    return table

fastq_file = sys.argv[1]
kmer_file = sys.argv[2]
n = int(sys.argv[3])

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

#(Just saw that the other files used 3 I also used that here) -> making the three types of filters
counting_cuckoo = Counting_Cuckoo(n, 3)
counting_bloom = CBloomFilter(len(kmer_table.keys()), 100, 3, 3) 
    #self.n=n                # number of items to add
    # self.N=Counter_size     # size of each counter
    # self.m=bucket_size      # total number of the buckets
    # self.k=no_hashfn        # number of hash functions

#Inserting data into the three filters:
for read in reads:
    for i in range(0, len(read) - n + 1):
        kmer = read[i:i+n]
        counting_cuckoo.insert(kmer)
        counting_bloom.insert(kmer)

print(counting_bloom.bit_array)

counting_cuckoo_incorrect = 0
counting_bloom_incorrect = 0
correct = 0
for k in kmer_table.keys():
    true_frequency = kmer_table[k]
    print("kmer:", k)
    print("true freq:", true_frequency)
    
    if counting_cuckoo.search(k) != true_frequency:
        counting_cuckoo_incorrect += 1
    
    if counting_bloom.search(k) != true_frequency:
        counting_bloom_incorrect += 1
        print("CB freq", counting_bloom_incorrect)
        print("\n")

print(counting_cuckoo_incorrect)
print(counting_bloom_incorrect)