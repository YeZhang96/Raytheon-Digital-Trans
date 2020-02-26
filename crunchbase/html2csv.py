from bs4 import BeautifulSoup
import os
import re
from IPython import embed

path = "./htmls/"
html_files = [f for f in os.listdir(path) if f.endswith(".html")]
print(len(html_files))

field_names = ['Announced Date',
 'Price',
 'Acquisition Type',
 'Acquisition Terms',
 'Acquiree Description',
 'Acquiree Last Funding Type',
 'Acquiree Industries',
 'Acquiree Headquarters Location',
 "Acquiree's Estimated Revenue Range",
 "Acquiree's Total Funding Amount",
 "Acquiree Funding Status",
 "Acquiree's Number of Funding Rounds",
 "Acquirer's Description",
 'Acquirer Industries',
 'Acquirer Headquarters Location',
 "Acquirer's Estimated Revenue Range",
 "Acquirer's Total Funding Amount",
 'Acquirer Funding Status',
 "Acquirer's Number of Funding Rounds"]

field_class_name = re.compile("component--field-formatter.*")

def parse(soup):
    acq = soup.find_all("div", {"class": "flex-no-grow cb-overflow-ellipsis identifier-label"})
    fields = soup.find_all("span", {"class" : field_class_name})
    data = []
    row_data = []
    count = 0
    i = 0
    while(i < len(fields)):
        field = fields[i]
        field_index = count % len(field_names)
        field_name = field_names[field_index]
        field_type = field["class"][1]
        if (("Range" in field_name or "Type" in field_name) \
             and field_type != "field-type-enum") :
            row_data.append("—")
        else:
            row_data.append(field.text.strip())
            i += 1
        if field_name == field_names[-1]:
            data.append(row_data)
            row_data = []
        count += 1
    if (len(row_data) > 0) :
        data.append(row_data)
    return data 

    
data = []
for html_file in html_files:
    f = open(path+html_file)
    soup = BeautifulSoup(f, "html.parser")
    data += parse(soup)
    f.close()

import pandas as pd
with open("crunchbase.csv", "w+") as f:
    df = pd.DataFrame(data)
    print(df.shape)
    # header = "Transaction Name,Acquiree Name,Acquirer Name,"
    header = ",".join(field_names)
    df.to_csv(f, index=False, header=header.split(","))



