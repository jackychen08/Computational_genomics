# Import the required modules
import sys
from Bio import SeqIO

# Read the k-mer length from the command line arguments
k = int(sys.argv[1])

# Open the input FASTQ file and read it using SeqIO
with open(sys.argv[2], "r") as handle:
    for record in SeqIO.parse(handle, "fastq"):
        # Get the k-mers from the sequence and write them to the output file
        for i in range(len(record.seq) - k):
            with open("{}-mers.fa".format(k), "a") as out_handle:
                out_handle.write(">" + "\n")
                out_handle.write(str(record.seq[i:i+k]) + "\n")