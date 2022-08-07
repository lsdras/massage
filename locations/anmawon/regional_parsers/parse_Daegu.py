# http://www.dganma.com/bbs/board.php?bo_table=find


import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

response = requests.get(
    f"http://www.dganma.com/bbs/board.php?bo_table=find",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    },
)  # headers need to pass firewall
assert response.status_code == 200
# make BS parse object
bs_obj = BeautifulSoup(response.text, "html.parser")
# get table contents
bs_obj = bs_obj.find("div", id="wrapper")
bs_obj = bs_obj.find("div", id="container")
bs_obj = bs_obj.find("div", id="bo_list")
bs_obj = bs_obj.find("div", class_="tbl_head01 tbl_wrap")


table_list = []
if len(table_list) == 0:
    for t in bs_obj.table.thead.find_all("tr"):
        cols = [i.text.strip() for i in t.find_all("th")]
        cols.append("link")
        table_list.append(cols)
else:
    pass
# get table contents
remove_span_text = re.compile(r"(.*)(댓글.*)")
for t in bs_obj.table.tbody.find_all("tr"):
    cols = []
    for i in  t.find_all("td"):
        try:
            data_string = remove_span_text.match(i.text.strip())[1].strip()
        except:
            data_string = i.text.strip()
        cols.append(data_string)
    cols.append(t.find("a").get("href"))
    table_list.append(cols)


df = pd.DataFrame(table_list[1:], columns=table_list[0])
df.fillna("", inplace=True)
df.rename(columns={"번호":"number", "지역":"region", "상호": "name", "주소": "addr", "전화번호": "phone"}, inplace=True)

df.to_csv("../regions/Daegu.csv")
