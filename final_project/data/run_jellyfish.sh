jellyfish count -m 16 -s 5000 -t 10 -C phi_x.fastq
jellyfish dump mer_counts.jf > jellyfish_16mer_results.fa
jellyfish mem -m 24 -s 5000