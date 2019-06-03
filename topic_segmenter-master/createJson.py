import re
import json

file = open("C:/Users/hp/Documents/Google Drive NIIT/Semester 7/NLP/Project/slack dataset/ref/cv_data/2", 'r')
d_text, d_user, d_ts, d_type, d = {}, {}, {}, {}, {}
i = 1

for line in file:
    if line.startswith("="):
        continue
    d_text[str(i)] = line.split("::: ")[1].split("\n")[0]
    d_user[str(i)] = line.split()[0]
    d_ts[str(i)] = float(''.join(re.findall('\[(\S*)\]', line.split()[2])))
    d_type[str(i)] = "message"
    i = i+1

d["anon_text"] = d_text
d["user"] = d_user
d["ts"] = d_ts
d["type"] = d_type

with open("sample/data.json", 'w') as outfile:
    json.dump(d, outfile)
