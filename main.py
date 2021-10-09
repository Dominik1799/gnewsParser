import time
from gnewsparser import GnewsParser
from time import process_time

# feed returns keys:['bozo', 'entries', 'feed', 'headers', 'href', 'status', 'encoding', 'version', 'namespaces']
# entries keys:['title', 'title_detail', 'links', 'link', 'id', 'guidislink', 'published', 'published_parsed', 'summary', 'summary_detail', 'source']
start = process_time()

g = GnewsParser()
g.setup_search("murder", "2020-12-01", "2020-12-31")
counter = 0
req_c = 0
while True:
    res = g.get_results()
    req_c += 1
    if res is None:
        break
    for entry in res:
        counter += 1
    if req_c == 5:
        g.save_state("./state.txt")
        exit(0)


end = process_time()
print(end - start)
print("Processed: ", counter)
