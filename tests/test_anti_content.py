#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-11 16:29:59
#LastEditTime: 2023-04-11 20:16:01
#LastEditors: leoking
# Description:
#

from pdd_sdk.core import get_anti_content

url = "https://mobile.yangkeduo.com/search_result.html?search_key=xxx&search_type=goods&page_id=10015_1681211339752_wjk1f0l231&is_back=&bsch_is_search_mall=&bsch_show_active_page=&list_id=yonidlfufc&sort_type=default&price_index=-1&filter=&opt_tag_name=&brand_tab_filter="


def test_anti_content():
    print(get_anti_content(url))
