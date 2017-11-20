while true
do
  python3 ./scrape.py --dump
  python3 ./scrape.py --scrape --resume
done
