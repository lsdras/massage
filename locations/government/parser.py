import pandas as pd

data = pd.read_csv("localdata_gov_2022_07_02.csv", encoding="UTF-8", sep=",")
data = data.loc[data["영업상태구분코드"].isin([1])]  #  01: 영업/정상, 02:휴업, 03: 폐업, 04: 취소/말소/만료/정지/중지
data = data[["사업장명", "도로명전체주소", "소재지전화"]]
data.fillna("", inplace=True)
data.rename(columns={"도로명전체주소": "주소", "소재지전화": "전화"}, inplace=True)
data.to_csv("running_stores.csv", header=True, index=False)
