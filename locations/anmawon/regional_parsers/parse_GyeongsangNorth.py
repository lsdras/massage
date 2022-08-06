# http://kbanma.or.kr/bbs/board.php?bo_table=e_b

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

lastnum = None

response = requests.get(
    f"http://kbanma.or.kr/bbs/board.php?bo_table=e_b",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    },
)
assert response.status_code == 200
# make BS parse object
bs_obj = BeautifulSoup(response.text, "html.parser")
get_last_page = re.compile(r"(.*)(&page=)(\d+)")
for a in bs_obj.find_all('a', href=True):
    if a.text == "맨끝":
        lastnum = int(get_last_page.match(a["href"])[3])

table_list = []
for pagenum in tqdm(range(1, lastnum + 1)):
    # get html
    response = requests.get(
        f"http://kbanma.or.kr/bbs/board.php?bo_table=e_b&page={pagenum:d}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        },
    )  # headers need to pass firewall
    assert response.status_code == 200

    # make BS parse object
    bs_obj = BeautifulSoup(response.text, "html.parser")
    bs_obj = bs_obj.find("div", id="BodyBox")
    bs_obj = bs_obj.find("div", id="CttBox")
    bs_obj = bs_obj.find("div", class_="tbl_head01 tbl_wrap")
    
    if len(table_list) == 0:
        for t in bs_obj.table.thead.find_all("tr"):
            cols = [i.text.strip() for i in t.find_all("th")]
            cols.append("link")
            table_list.append(cols)
    else:
        pass
    # get table contents
    for t in bs_obj.table.tbody.find_all("tr"):
        cols = [i.text.strip() for i in t.find_all("td")]
        cols.append(t.find("a").get("href"))
        table_list.append(cols)


df = pd.DataFrame(table_list[1:], columns=table_list[0])
df.fillna("", inplace=True)
df.rename(columns={"번호":"number", "지역":"region", "상호": "name", "주소": "addr", "전화번호": "phone"}, inplace=True)

df.to_csv("../regions/GyeongsangNorth.csv")
