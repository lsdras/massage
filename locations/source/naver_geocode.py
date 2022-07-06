import requests
import json


class NAVERGeocoding:
    # https://api.ncloud-docs.com/docs/ai-naver-mapsgeocoding-geocode
    def __init__(self, secret_key_path: str, geocode_url: str) -> None:
        with open(secret_key_path, "r") as f:
            secret = json.load(f)
        self.__HEADER = {
            "X-NCP-APIGW-API-KEY-ID": secret["NAVER"]["ID"],
            "X-NCP-APIGW-API-KEY": secret["NAVER"]["SECRET_KEY"],
            "Accept": "application/json",
        }
        self.__GEOCODE_URL = geocode_url

    def _get_response(self, params: dict) -> dict:
        res = requests.get(url=self.__GEOCODE_URL, params=params, headers=self.__HEADER)
        assert res.status_code == int(200), res.status_code
        assert res.json()["status"] == "OK", res.json()["status"]
        return res.json()

    def get_normalized_address(self, address: str, count: int = 1) -> tuple[str, str, str]:

        inp = {"query": address, "count": count}

        response = self._get_response(inp)
        list_responsed_address = response["addresses"]

        assert len(list_responsed_address) == count, print(response)
        responsed_address = list_responsed_address[0]

        NAVER_roadAddress = responsed_address["roadAddress"]
        x_coord = responsed_address["x"]
        y_coord = responsed_address["y"]
        return x_coord, y_coord, NAVER_roadAddress

    def __call__(self, *args, **kwargs):
        return self.get_normalized_address(*args, **kwargs)
