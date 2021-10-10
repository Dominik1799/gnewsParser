import time
from gnewsparser import GnewsParser
from time import process_time
import csv

# feed returns keys:['bozo', 'entries', 'feed', 'headers', 'href', 'status', 'encoding', 'version', 'namespaces']
# entries keys:['title', 'title_detail', 'links', 'link', 'id', 'guidislink', 'published', 'published_parsed', 'summary', 'summary_detail', 'source']
start = process_time()

g = GnewsParser()
g.setup_search("Jeffrey Epstein", "2020-12-25", "2020-12-31")
f = open("output.csv", "w", encoding="utf-8", newline="")
csvwriter = csv.DictWriter(f,
                           quotechar='"',
                           quoting=csv.QUOTE_ALL,
                           lineterminator='\n',
                           fieldnames=["published", "title", "link"],
                           extrasaction="ignore")
csvwriter.writeheader()
req_counter = 0
while True:
    res = g.get_results()
    req_counter += 1
    if res is None:
        break
    for entry in res:
        csvwriter.writerow(entry)
end = process_time()
print("Process time: ", end - start)
print("req_made: ", req_counter)
