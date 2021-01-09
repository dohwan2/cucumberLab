filenames=`ls /home/ubuntu/stock-project/result/bunbong_json/*.json`
for entry in $filenames
do
  echo $entry
  mongoimport --db trading --collection stock-bunbong --file $entry
done
