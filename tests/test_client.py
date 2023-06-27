#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-10 17:46:26
# LastEditTime: 2023-04-18 23:30:12
# LastEditors: leoking
# Description:
#

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent.parent.parent.__str__())

from urllib.parse import quote

from pdd_sdk.core import get_anti_content


from pdd_sdk import Client
from pdd_sdk.models import (
    HtmlSearchParams,
    ApiSearchParams,
    GetOrderData,
    CommentParams,
)

c = Client(base_url="https://mobile.yangkeduo.com")

c.cookies.update(
    {
        "api_uid": "CkxQFmQgYyiPcgBrQL1sAg",
        "_nano_fp": "XpE8lpCYn0gYnqTjXo_epfmgDClHQ6YQUJXjxS0V",
        "webp": "1",
        "jrpl": "Qj2v3u6Uan1mzH0GSocJTM73H84cN9jn",
        "njrpl": "Qj2v3u6Uan1mzH0GSocJTM73H84cN9jn",
        "dilx": "q7TBxHLcVLlLofANpkoew",
        "pdd_user_id": "8634228117494",
        "pdd_user_uin": "GKBXTK2ADIA2H67KXC7DLARNEI_GEXDA",
        "rec_list_chat_list_rec_list": "rec_list_chat_list_rec_list_57l90m",
        "chat_config": "%7B%22host_whitelist%22%3A%5B%22.yangkeduo.com%22%2C%22.pinduoduo.com%22%2C%22.10010.com%2Fqueen%2Ftencent%2Fpinduoduo-fill.html%22%2C%22.ha.10086.cn%2Fpay%2Fcard-sale!toforward.action%22%2C%22wap.ha.10086.cn%22%2C%22m.10010.com%22%5D%7D",
        "PDDAccessToken": "YNTSOIEEFTYQWXPC34WWVBNUX5HPACR2X4S3EHM46ZGE3PEV5RJA113f656",
        "pdd_vds": "gaLpNCGCNpLYicbZadOYmDGqmCbYnuaDmCtYidQvOunZyZQfPrnrLuGhbvOq",
    }
)
c.set_verify_auth_token("rDwWrZUVDXAFvCd69lOo-gd89448db5d16e706d")
c.set_access_token(c.get_access_token_from_cookie())

print(c.get_raw_cookies(), c.get_uid_from_cookie())


def test_get_user_info():
    r = c.get_user_info()
    print(r)


def test_search_html():
    params = HtmlSearchParams(search_key="iphone")
    json = c.search_goods_in_html(params)
    print(json)


def test_search():
    keyword = "iphone"
    # p = ApiSearchParams.parse_obj(
    #     {
    #         "pdduid": uid,
    #         "item_ver": "lzqq",
    #         "coupon_price_flag": "1",
    #         "source": "search",
    #         "search_met": "",
    #         "list_id": "yonidlfufc",
    #         "sort": "default",
    #         "filter": "",
    #         "q": "xxx",
    #         "page": "2",
    #         "is_new_query": "1",
    #         "size": "50",
    #         "flip": "0;0;0;0;f22114e7-975f-416d-8a23-ca2d542679ea",
    #         "anti_content": "0aqAfxn5NiIyJ99aDYfnodhNR2fg4To-zJTYBZkO6zzIzLjeAML9RH_hExyxuPyQ3c-8QedgDw0mpHS02wYds9NxGaEQdFQPSPZp0xtPMCwGbttqPSvRCWPcrqJbDJ0CoC9klrshKhofrP7JPzrx0E42M9u6_GC6ua4Qx6CQQEPYEt9PDk07UQ2eRoI8UW242cV5jBoBA54pTaH2JIoRoqS2qDCamQCwc9LY2d4ciV0Afd9liVG84W99QH9Ma0CshEnhZG9szogQafC24iCQoVobnryMiIILTj5Yu2OPjkSRIrDlgewFFQzpevHxre-1gIpP_clwpvd8kOdvq8jypwiHcKD3OogBzSryz1jeZDwDrO1TMXmKTsxmrNhqoRMAMHx23Fbl21FEjxEEaZzKD-502i5o-XWE7URdc5l_8YWQ3QFOOr8cQHOeiMKLtEKdaafbyswOa7M79QQF74BfcFeW9qbx4qAbZXVQl-LKZ11ed6JtELnUZxQ2bvXkpFr20ujTN7pkHvoThV4j7XHFzPEV1pY4pNFIN-AQKFyC3tDzKfmpeDmdHj8Fpn-kDvA75hnea7wZ18oMZmLkDO1LGJYD-3namlaRQCFgb-s-WZuYTOB5pKIseOtwFVUOwluaep__-1fa9nUCsaxUm5qKNmjlehXMdoGwvBczaj31_0L6dhtkIrCkXvL_HxGmZmO8FPLzvCKehf_hKX7DtMS8-f2AoQR9U6SaqKlzuDpY",
    #     }
    # )
    resp = c.search(keyword)
    print(resp)


def test_search_orders():
    orders = c.search_orders("nihao")
    print(orders)


def test_aftersale():
    orders = c.get_aftersale_orders()
    print(orders)


def test_orders_v3():
    print(c.get_orders_v3(GetOrderData(anti_content=get_anti_content(c.base_url))))


def test_orders_v4():
    print(c.get_orders_v4(GetOrderData(anti_content=get_anti_content(c.base_url))))


def test_get_comments():
    print(
        c.get_goods_comments(
            "301116387980", CommentParams(pdduid=c.get_uid_from_cookie())
        )
    )


def save_region(data):
    import json, time

    dir = Path(__file__).parent.parent.parent.joinpath("data/addrs")
    assert dir.exists()

    with open(
        dir.joinpath(f"{data['region_id']}-{data['region_name']}.json"), 'w'
    ) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    time.sleep(2)


def test_get_regions():
    for x in c.get_provinces()['regions']:
        save_region(x)
        for y in c.get_cities(x['region_id'])['regions']:
            save_region(y)
            for z in c.get_districts(y['region_id'])['regions']:
                save_region(z)
