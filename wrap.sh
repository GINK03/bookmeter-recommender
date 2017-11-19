while true
do
  python3 ./misc/freeporxylist_builder.py 
  mv ./proxies.json ./misc/
  python3 ./scrape.py --dump
  python3 ./scrape.py --scrape --resume
done
