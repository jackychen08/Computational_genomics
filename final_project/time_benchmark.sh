for ((i=1;i<=10000;i=i+100)); 
do
 # your-unix-command-here
 python3 query_time_benchmark.py $i > "${i}.csv"
 cat  "${i}.csv" >> time_benchmark.csv
 rm "${i}.csv"
done