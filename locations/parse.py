import json

import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

lastnum = 89
remove_page_api = re.compile(r"(.*)(&page=\d+)")
table_list = []

for pagenum in tqdm(range(1, lastnum + 1)):
    # get html
    response = requests.get(
        f"http://www.anmawon.com/FindShop/List?Page={pagenum:d}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        },
    )  # headers need to pass firewall
    assert response.status_code == 200

    # make BS parse object
    bs_obj = BeautifulSoup(response.text, "html.parser")

    # get table contents
    for t in bs_obj.table.tbody.find_all("tr"):
        cols = [i.text.strip() for i in t.find_all("td")]
        cols.append(remove_page_api.match(t.find("a").get("href"))[1])  # prefix: http://www.anmawon.com
        table_list.append(cols)

#with open("test.json", "w", encoding="UTF-8") as f:
#    json.dump(table_list, f, ensure_ascii=False)
print(table_list)
print(len(table_list))
# table_list.append({"region", "name", "addr", "phone", "href"})
