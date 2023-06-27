#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-11 16:25:04
# LastEditTime: 2023-04-21 22:43:29
# LastEditors: leoking
# Description:
#
import execjs
from pathlib import Path


def get_anti_content(
    url: str, js_path: str = Path(__file__).parent.joinpath('anti_content.js')
):
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
    return execjs.compile(js).call('get_anti', url)


def get_list_id_from_search_page(rawData: dict):
    return rawData['stores']['store']['data']['listID']


def get_flip_from_search_page(rawData: dict):
    return rawData['stores']['store']['data']['ssrListData']['flip']
