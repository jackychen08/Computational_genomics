Jacky Chen
Jocelyn Hsu
Nick Bowen
Amy Mistri

Files:
counting_bloom.py - Counting bloom filter used to compare against the counting cuckoo filter
counting_cuckoo.py - Old implementation of the counting cuckoo filter
counting_cuckoo_np.py - Updated implementation of the counting cuckoo filter making use of numpy
counting_cuckoo_params.py - testing the counting cuckoo filter with different parameters
CBFtest.py - Unit tests for counting bloom filter
cuckoo.py - Cuckoo filter implementation
kmer.py - creates kmer dictionary that stores kmers and their frequenices
memory_benchmark.py - file used to conduct memory benchmarking
query_time_benchmark.py - file used to conduct query time benchmarking
test_counting_cuckoo.py - Unit tests for counting cuckoo filter
test_cuckoo.py - Unit tests for cuckoo filter

Note on accuracy testing:
- Raw fastq data file was first input into kmer.py to generate a file that reflects a kmer table
- accuracy_testing.py then inputs the kmers from the fastq itself into the different filters and then compares their frequencies.
- Command line: python3 accuracy_test.py data/phi_x.fastq data/mer_counts_dumps.fa 16 data/jellyfish_16mer_results.fa