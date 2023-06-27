#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-10 17:42:14
#LastEditTime: 2023-04-22 00:37:24
#LastEditors: leoking
# Description:
#
from fake_useragent import UserAgent
from http.cookiejar import CookieJar
from typing import Dict, List
import re, json
from urllib.parse import urljoin, urlparse
from requests import Session

from pdd_sdk.models import (
    Address,
    ApiSearchParams,
    HtmlSearchParams,
    GetOrderData,
    CommentParams,
    CheckoutParams,
    CreateOrderData,
    PrepayData,
)

from pdd_sdk.core import get_anti_content


class Client(Session):
    UA = UserAgent(browsers=['chrome'])

    @staticmethod
    def from_cookies(cookies: List[dict], **kw) -> 'Client':
        c = Client(**kw)
        for cookie in cookies:
            c.cookies.set(cookie["name"], cookie["value"])
        c.set_access_token(c.get_access_token_from_cookie())
        return c

    def __init__(self, base_url="https://mobile.yangkeduo.com", *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.base_url = base_url
        self.headers.setdefault("User-Agent", self.UA.random)
        self.headers.update(
            {
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
            }
        )

    def add_raw_cookies(self, cookie: str):
        for tmps in map(lambda s: s.strip().split("="), cookie.split(";")):
            self.cookies.set(tmps[0], tmps[1])
        return self

    def get_raw_cookies(self) -> str:
        tmps = []
        for k in self.cookies.keys():
            tmps.append(f'{k}={self.cookies.get(k)}')
        return "; ".join(tmps)

    def _format_url(self, url: str):
        if not url:
            return url
        if url.startswith('http'):
            return url
        return urljoin(self.base_url, url)

    def _add_headers_by_url(self, url: str):
        if not url:
            return
        if not url.startswith("http"):
            return
        obj = urlparse(url)
        self.headers.update(dict(referer=url))
        self.headers.update(dict(origin=f"{obj.scheme}://{obj.hostname}"))

    def set_access_token(self, s: str):
        self.headers.setdefault('accesstoken', s)
        return self

    def set_verify_auth_token(self, s: str):
        self.headers.setdefault('verifyauthtoken', s)
        return self

    def get(self, url, *args, **kwargs):
        url = self._format_url(url)
        self._add_headers_by_url(url)
        return super().get(url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        url = self._format_url(url)
        self._add_headers_by_url(url)
        return super().post(url, *args, **kwargs)

    def get_uid_from_cookie(self):
        uid = self.cookies.get("pdd_user_id")
        assert uid, 'uid is empty, please update cookies first'
        return uid

    def get_uin_from_cookie(self):
        uin = self.cookies.get("pdd_user_uin")
        assert uin, 'uin is empty, please update cookies first'
        return uin

    def get_access_token_from_cookie(self):
        token = self.cookies.get("PDDAccessToken")
        assert token, 'access token is empty, please update cookies first'
        return token

    def get_user_info(self):
        return self.get(
            "/proxy/api/api/apollo/v3/user/me",
            params=dict(pdduid=self.get_uid_from_cookie()),
        ).json()

    def search_goods(self, params: ApiSearchParams):
        x = self.get("/proxy/api/search", params=params.dict())
        return x.json()

    def search_goods_in_html(self, params: HtmlSearchParams):
        params.search_type = 'goods'
        r = self.get("/search_result.html", params=params.dict())
        # with open("./xx.html", 'w') as f:
        #     f.write(r.text)
        tmps = re.findall(r'rawData=(.+?)};', r.text)
        assert len(tmps) == 1, f'unexpected html response: {r.text}'
        # print(tmps[0])
        return json.loads(tmps[0] + "}")['stores']['store'], r

    def search(self, keyword: str):
        params = HtmlSearchParams(search_key=keyword)
        json, r = self.search_goods_in_html(params)
        p = ApiSearchParams(
            pdduid=self.get_uid_from_cookie(),
            q=keyword,
            # q=quote(keyword),
            list_id=json['data']['listID'],
            flip=json['data']['ssrListData']['flip'],
            anti_content=get_anti_content(r.url),
        )
        resp = self.search_goods(p)
        # print(r.url, resp)
        return resp

    def get_orders_v4(self, data: GetOrderData):
        return self.post(
            f"/proxy/api/api/aristotle/order_list_v4?pdduid={self.get_uid_from_cookie()}",
            json=data.dict(),
        ).json()

    def is_old_account(self):
        resp = self.get_orders_v4(
            GetOrderData(anti_content=get_anti_content(self.base_url))
        )
        return len(resp.get("orders", [])) > 0

    def get_orders_v3(self, data: GetOrderData):
        return self.post(
            f"/proxy/api/api/aristotle/order_list_v3?pdduid={self.get_uid_from_cookie()}",
            json=data.dict(),
        ).json()

    def cancel_order(self, order_id: str, cancel_type: int = 1):
        return self.post(
            f"/proxy/api/order/{order_id}/cancel?cancel_type={cancel_type}&pdduid={self.get_uid_from_cookie()}"
        ).json()

    def delete_order(self, order_id: str):
        return self.post(
            f"/proxy/api/order/{order_id}/delete?pdduid={self.get_uid_from_cookie()}"
        ).json()

    def get_aftersale_orders(self):
        return self.post(
            f"/proxy/api/api/blade/after_sales_list?pdduid={self.get_uid_from_cookie()}"
        ).json()

    def get_addr_options(self, region_id: int):
        return self.get(
            f'/proxy/api/api/galen/v2/regions/{region_id}?pdduid={self.get_uid_from_cookie()}'
        ).json()

    def get_provinces(self):
        return self.get_addr_options(1)

    def get_cities(self, region_id: int):
        assert region_id > 1, 'region_id should be greater than 1'
        return self.get_addr_options(region_id)

    def get_districts(self, region_id: int):
        assert region_id > 1, 'region_id should be greater than 1'
        return self.get_addr_options(region_id)

    def add_address(self, addr: Address):
        return self.post(
            f"/proxy/api/api/origenes/address?pdduid={self.get_uid_from_cookie()}",
            json=addr.dict(),
        ).json()

    def search_orders(self, keyword: str):
        html = self.get(
            "/transac_orders_search_results.html",
            params={
                "keyWord": keyword,
                "type": "0",
                "refer_page_name": "my_order",
                # "refer_page_id": "10032_1681196054860_0w1pm5j62h",
                # "refer_page_sn": "10032",
            },
        ).text
        # with open("./orders.html", 'w') as f:
        #     f.write(html)
        tmps = re.findall(r'rawData=(.+?)};', html)
        assert len(tmps) == 1, f'unexpected html response: {html}'
        # print(tmps[0])
        return json.loads(tmps[0] + "}")

    def get_goods_comments(self, goods_id: str, params: CommentParams):
        return self.get(
            f"/proxy/api/reviews/{goods_id}/list", params=params.dict()
        ).json()

    def get_checkout_page(self, params: CheckoutParams):
        return self.get("/order_checkout.html", params=params.dict())

    def get_address(self, addr_id: str):
        return self.get(
            f"/proxy/api/api/origenes/address/{addr_id}",
            params=dict(pdduid=self.get_uid_from_cookie(), address_id=addr_id),
        ).json()

    def comfirm_render(self):
        self.post(
            f"/proxy/api/api/morgan/confirm/render?pdduid={self.get_uid_from_cookie()}"
        )

    def create_order(self, data: CreateOrderData):
        return self.post(
            f"/proxy/api/order?pdduid={self.get_uid_from_cookie()}", json=data.dict()
        ).json()

    def refund_order(self, order_sn: str, phone_number: str, price: int):
        '''
        @description: 退货退款
            TODO：需要完善是退货退款还是仅退款；退款理由
        @param {*} self
        @param {str} order_sn
        @param {str} phone_number
        @param {int} price 需要转换成分，例如0.35转成35
        @return {*}
        '''
        return self.post(
            f'/proxy/api/after_sales/create?pdduid={self.get_uid_from_cookie()}',
            json={
                "order_sn": order_sn,
                "coupon_return_control_type": 0,
                "after_sales_type": 1,
                "user_ship_status": 0,
                "user_phone": phone_number,
                "images": [],
                "return_coupon_amount": 0,
                # 发现更便宜的了
                "question_type": 5000,
                "question_desc": "",
                "apply_amount": price,
                "refund_amount": price,
                "new_refund_amount": price,
                "is_lite": True,
            },
        ).json()

    def prepay(self, data: PrepayData):
        return self.post(
            f"/proxy/api/order/prepay?pdduid={self.get_uid_from_cookie()}",
            json=data.dict(),
        ).json()

    def get_pay_page(self, order_sn: str):
        return self.get(f"/order.html", dict(order_sn=order_sn))
