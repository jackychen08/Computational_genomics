import sys
from counting_bloom import CBloomFilter
from counting_cuckoo_np import Counting_Cuckoo
from countingbloom import CountingBloomFilter

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

fastq_file = sys.argv[1] #fastq file 
kmer_file = sys.argv[2]  #kmer table of the data (obtained from kmer.py)
k = int(sys.argv[3])     #k-mer length
jellyfish_output = sys.argv[4]

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
counting_bloom = CountingBloomFilter(len(kmer_table.keys()), 3)
#est_elements (int): The number of estimated elements to be added
# false_positive_rate (float): The desired false positive rate
# hash_function (function): Hashing strategy function to use `hf(key, number)`


#counting_bloom = CBloomFilter(len(kmer_table.keys()), 100, 4000, 2) 
    #self.n=n                # number of items to add
    # self.N=Counter_size     # size of each counter
    # self.m=bucket_size      # total number of the buckets
    # self.k=no_hashfn        # number of hash functions

#Inserting data into the three filters:
for read in reads:
    for i in range(0, len(read) - k + 1):
        kmer = read[i:i+k]
        counting_cuckoo_np.insert(kmer)
        counting_bloom.insert(kmer)

counting_cuckoo_np_incorrect = 0
counting_bloom_incorrect = 0
jellyfish_incorrect = 0
for k in kmer_table.keys():
    true_frequency = kmer_table[k]

    if counting_cuckoo_np.search(k) != true_frequency:
        counting_cuckoo_np_incorrect += 1
    
    if counting_bloom.search(k) != true_frequency:
        counting_bloom_incorrect += 1
        print("kmer:", k)
        print("true:", true_frequency)
        print("CB:", counting_bloom.search(k))
    
    if jf_table[k] != true_frequency:
        jellyfish_incorrect += 1

total_kmers = len(kmer_table.keys())
print(total_kmers)
print(counting_bloom_incorrect)

print("counting_cuckoo_np incorrect", float(counting_cuckoo_np_incorrect/total_kmers))
print("counting_bloom incorrect" ,float(counting_bloom_incorrect/total_kmers))
print("jellyfish incorrect", float(jellyfish_incorrect/total_kmers))