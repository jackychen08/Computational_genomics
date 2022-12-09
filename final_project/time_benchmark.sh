
rm time_vs_fullness.csv
echo "filter,n,max_tries,b,search_total_time,insert_total_time,insert_average_time" >> time_vs_fullness.csv

#create an array going from 1 to 6.
#correspongs to indices of an array of hyper params in the python file
# loop through indices. run the python file for each filter twice
# one run keeps max tries constant, another keeps b constant. 
for ((j = 0; j <= 5 ; j = j+1));
do
    for ((i = 3;i <= 5000;i = i + 20)); #increase how many kmers to input the cuckoo counter is
    do

    # bench mark counting cuckoo as a function of how full it is while varying max tries
    python3 time_benchmark.py $i $"counting_cuckoo" $j $"1" >> time_vs_fullness.csv

    # bench mark counting cuckoo as a function of how full it is while varying b
    python3 time_benchmark.py $i $"counting_cuckoo" $"2" $j >> time_vs_fullness.csv

    # bench mark  cuckoo as a function of how full it is
    python3 time_benchmark.py $i $"cuckoo" $j $"1" >> time_vs_fullness.csv

    python3 time_benchmark.py $i $"cuckoo" $"2" $j >> time_vs_fullness.csv
    done
done