#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-13 14:57:41
# LastEditTime: 2023-04-18 12:34:22
# LastEditors: leoking
# Description:
#
import time, pytest
from dew.orm.model.auth import Credential
from pdd_sdk.core import (
    get_anti_content,
    get_flip_from_search_page,
    get_list_id_from_search_page,
)
from pdd_sdk.models import Address, ApiSearchParams
from pdd_sdk.puppeteer import Pdd


@pytest.mark.asyncio
async def test_ws():
    id, phone = "COM95", "19316670351"
    auth = Credential(id=id, phone=phone)
    pdd = Pdd(
        sms_url="http://sms.newszfang.vip:3000/Pmb5vKbVCToMdoHbPNNXPh",
        credential=auth,
    )
    # pdd.wait_sms_code(auth.id)
    await pdd.connect(
        "ws://127.0.0.1:20014/devtools/browser/d60602bb-0cb8-470d-9aa0-c8e703e7b437"
    )
    # pdd.get("https://bot.sannysoft.com/")
    # await pdd.login()
    # await pdd.goto_product_page("goods.html?goods_id=467997300960")
    # sdk = await pdd.get_pdd_sdk_client()
    # print(sdk.get_uid_from_cookie())
    # print(sdk.get_user_info())

    # await pdd.make_order(
    #     sku_id=1295842089054,
    #     goods_id=420558911935,
    #     group_id=83615484549,
    #     goods_number=1,
    # )
    # # await pdd.pay_with_wechat()
    # await pdd.pay_with_alipay()
    # await pdd.goto_pay()

    time.sleep(2)
    pages = await pdd.browser.pages()
    for p in pages:
        print(p.url)
    # # 测试搜索
    # keyword = "iphone"
    # rawData = await pdd.search(keyword)
    # print(rawData)
    # resp = sdk.search_goods(
    #     ApiSearchParams(
    #         q=keyword,
    #         pdduid=sdk.get_uid_from_cookie(),
    #         list_id=get_list_id_from_search_page(rawData),
    #         anti_content=get_anti_content(pdd.page.url),
    #         flip=get_flip_from_search_page(rawData),
    #     )
    # )
    # print(resp)

    # # 创建地址
    # p = sdk.get_provinces()['regions'][0]
    # c = sdk.get_cities(p['region_id'])['regions'][0]
    # d = sdk.get_districts(c['region_id'])['regions'][0]
    # print(p, c, d, sep="\n")
    # resp = sdk.add_address(
    #     Address(
    #         name="张三",
    #         mobile="17142009876",
    #         province_id=p['region_id'],
    #         city_id=c['region_id'],
    #         district_id=d['region_id'],
    #         address="八大胡同64号",
    #         anti_content=get_anti_content(sdk.base_url),
    #     )
    # )
    # print(resp,get_anti_content(sdk.base_url))

    await pdd.check_validation()
