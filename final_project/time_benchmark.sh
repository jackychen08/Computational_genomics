echo "n,search_total_time,insert_total_time,insert_average_time" >> time_benchmark.csv
for ((i=3;i<=5000;i=i+10)); 
do
 # your-unix-command-here
 python3 query_time_benchmark.py $i > "${i}.csv"
 cat  "${i}.csv" >> time_benchmark.csv
 rm "${i}.csv"
done