filenames=`ls /home/ubuntu/files/past_stock_price_json/*.json`
for entry in $filenames
do
  echo $entry
  mongoimport --db trading --collection test --file $entry
done
