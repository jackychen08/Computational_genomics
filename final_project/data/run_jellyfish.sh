jellyfish count -m 16 -s 5000 -t 10 -C phi_x.fastq
jellyfish dump mer_counts.jf > jellyfish_16mer_results.fa
jellyfish mem -m 16 -s 5000

jellyfish count -m 16 -s 50000 -t 10 -C 2A_fastq.txt
jellyfish dump mer_counts.jf > jellyfish_2A_results.fa
jellyfish mem -m 16 -s 50000

jellyfish count -m 16 -s 50000 -t 10 -C 2B_fastq.txt
jellyfish dump mer_counts.jf > jellyfish_2B_results.fa
jellyfish mem -m 16 -s 50000

jellyfish count -m 16 -s 50000 -t 10 -C 2C_fastq.txt
jellyfish dump mer_counts.jf > jellyfish_2C_results.fa
jellyfish mem -m 16 -s 50000