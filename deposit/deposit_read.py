import requests
from bs4 import BeautifulSoup

from deposit.models import Deposit


def deposit_crawler():
    URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.xml?auth=25b5ef6b804f2acbe32fbca6f79f17a0&topFinGrpNo=020000&pageNo=1'
    req = requests.get(URL).text
    xmlsoup = BeautifulSoup(req,'html.parser')
    # 전체 상품 개수
    count = xmlsoup.select("total_count")[0].get_text()
    result = []

    bank = xmlsoup.select("kor_co_nm")
    product = xmlsoup.select("fin_prdt_nm")
    options = xmlsoup.find_all("options")
    join_way = xmlsoup.select("join_way")
    mtrt_int = xmlsoup.select("mtrt_int")
    spcl_cnd = xmlsoup.select("spcl_cnd")
    join_member = xmlsoup.select("join_member")
    etc_note = xmlsoup.select("etc_note")
    max_limit = xmlsoup.select("max_limit")

    for i in range(0,int(count)):
        save_trm = options[i].select("option save_trm")
        intr_rate = options[i].select("option intr_rate")

        deposit_obj ={
            'deposit_id': i+1,
            'bank': bank[i].get_text(),
            'product':product[i].get_text().replace('\n',''),
            'rate_type':options[i].select("option intr_rate_type_nm")[0].get_text(),
            'join_way':join_way[i].get_text(),
            'mtrt_int':mtrt_int[i].get_text(),
            'spcl_cnd':spcl_cnd[i].get_text(),
            'join_member':join_member[i].get_text(),
            'etc_note':etc_note[i].get_text(),
            'max_limit':max_limit[i].get_text()
        }
        for j in range(0, len(intr_rate)):
            deposit_obj['rate_'+save_trm[j].get_text()] = float(intr_rate[j].get_text())
        result.append(deposit_obj)
    return result

