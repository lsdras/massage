
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


response = requests.get(
    f"http://xn--hz2b11ew7coa499cy81avya.kr/skin/sub_page.php?page_idx=141",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    },
)  # headers need to pass firewall
assert response.status_code == 200
# make BS parse object
bs_obj = BeautifulSoup(response.text, "html.parser")
# get table contents
bs_obj = bs_obj.find("section", id="bodycontent")
bs_obj = bs_obj.find("div", class_="spec_cont esensmobilemenu img-visual")

table_list = []
for t in bs_obj.table.tbody.find_all("tr"):
    cols = [i.text.strip() for i in t.find_all("td")]
    table_list.append(cols)

df = pd.DataFrame(table_list[1:], columns=table_list[0])
df.fillna("", inplace=True)

df.rename(columns={"상호명": "name", "주소": "addr", "전화번호": "phone", "비고": "etc"}, inplace=True)
df.to_csv("../regions/Busan.csv")
