#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-11 14:39:17
# LastEditTime: 2023-04-21 20:31:46
# LastEditors: leoking
# Description:
#
from typing import Optional
from pydantic import BaseModel


class PrepayData(BaseModel):
    pay_app_id: int  # =38
    version: int = 3
    attribute_fields: dict = {'paid_times': 0}
    order_sn: str  # =230411-488536852012363
    pap_pay: int = 1


class CreateOrderData(BaseModel):
    address_id: int  # =32562537322
    address_snapshot_id: str  # =1000000019780043902
    goods: list = []
    # =[{'sku_id': 1365647053669, 'sku_number': 1, 'goods_id': '301116387980'}]
    group_id: str  # =60879776211
    anti_content: str
    pay_app_id: int  # =38:微信
    is_app: str = "0"
    version: int = 1
    page_id: str  # =10004_1681222731486_tipvp67tf9
    promotion_union_vo: dict = {}
    # PromotionUnionVo ={'single_promotion_list': [{'promotion_type': 1000, 'promotion_id': 'CP1045899080', 'sku_ids': [1365647053669], 'extension': {'promotion_entity': 'YckOuidc7mBVGuhw2TyeWaLcyznZD8CMYn+ZpzqrD6wb27KzEhAAv4jDNyNXXu5l7tjwUvoU66emLWO0AWEm3bZsFp2IRAFD4nU8WUpoP7m8FwCYU/wG7Ir/Ln7CPJ0ctCXHXsJiHAJz4VGnRUWUXMy1d0r2luN6RNYoAUi+OYx3avYAh5PQZ6ZKINWPmMNM2gg7bLFF+qnI55ZAe4+wNjtVEhDwx0gJRPekZmcqot4XqwCJSGhYn4lMVHmudKWgoMiyfOQZSmA6ei7j5K38vSXlZuEhLKbk6CqqRMAEI19Xt4POFEvpQKPg2KrNgHs1AnpEBtnnSU35ilDVJWEd8BC7JsDyos59olEtLGXVGguTCaKdtBDdBAmzrZ0hnoAgDKuP77MGRWdxm9mSuwGB7fiuSJ6/9H7OBM6MMhPPpE0cg6zjxbuoYjGQ+69b28W5AqMailTThwBxyiSPiWBFHI2coaHFuJnVjwQ1talnwxGPYWAaIaB9cZ8aFAEdkcv7MRrjjg==_v1', 'promotion_token': '75153b027112f4cfbc52c98db8b50366'}, 'mall_id': 108442870}]}
    duoduo_type: int = 0
    biz_type: int = 0
    attribute_fields: dict = {}
    # AttributeFields ={'create_order_token': '6f7a874f63cab62b03d387968cc1fc73', 'create_order_msg': '83NzU5bdPKffZ3dKXa6ZuGMMH6O8tVc9prWUetavzUO861+DsZKgzxcZ6cB5fqKbdvB3wR7LI8f17cN1y4btY+CrB2lmeIWgQadN2Hm9EuHo5H1YR6R6XeRw/cHEZr6EEVL4YKfPf13HvikRz4ZtEx0s+fKRAzCc9DSq8h3gxtHUsMLZskeIpArxryD+3l/+c9yd7Y0G/GHQgUWu0nApk5q0UV8Gq1mCJWAoK2mRttuGE2t4eLHIehplTQIfDyc8FTXqHveTvAzDkhZ2peOilx7zak2DeYR9x4cmgZbizOqYFF7t60zOLFPESczsvaMnoao+675hJKVas9u0Mc8tmr0gvUJKWXHg/OFfWmJvb0T9wYC+/2iV8VwNoh77MjuXjQM0+Kk1yRwZumOwJNGHBVcHGWBBmg7kgTu1WHLW2U70dSQt3Meg/4x0Kk4ueU5ifHzwsNJZ550iUEodSSl19YE82Eu2SbFLZUevEV+uo8tLablNWJT+HJ2OtqVhkknmXfMPykJz4WRlBxgcAhR3P0umuXHL9aXnvg8EJ/GYeA6Pba0lVeMHOOg7kiBjwsJIlE9pdoIgv36nEeOMz9jL5AAU8a/pxhjPFYFR2JJFfqYgPE2k89+sn2YJ4mDQy9bkVhnIPg8V9mfkKoaA0nNhWN23AoZ0a6tuDG3yfYpgBA+75RigN+4pgihu//wEEuYJxXHbl2TCYOdN2kJxRELDdGcVsC8xH+71eyW+niSpfiifrqEvNLsVjwdixh/KeLaqjITbSwD8tKgohl5/lcVGtT6xiSBSLl20v3Dcycxlypg=_v1', 'rank_id': '5030010201', 'page_from': 0, 'lite_contract_code': None, 'morgan_trace': 'cb55097987c348b4933f44a5faf5f57c', 'biz_type': 0, 'need_face_check': False, 'original_front_env': 0, 'current_front_env': 1, 'not_component_package': True}
    source_channel: str  # ="0"
    source_type: int  # =7


class Address(BaseModel):
    name: str
    mobile: str
    province_id: int  # = 6
    city_id: int  # = 77
    # 区
    district_id: int  # = 706
    # 具体地址
    address: str
    community_address_request: dict = {}
    is_default: int = 1
    order_sn: Optional[str]
    check_region: bool = True
    # 测试发现这个值只要符合格式就行，具体是什么无关紧要
    anti_content: str


class CheckoutParams(BaseModel):
    _oc_rank_id: Optional[str]  # =5030010201
    sku_id: Optional[str]  # =1365647053669
    group_id: Optional[str]  # =60879776211
    goods_id: str  # =301116387980
    goods_number: int = 1
    page_from: str = 0
    order_extra_type: int = 1
    refer_page_element: str = "open_btn"
    source_channel: int = 0
    refer_page_name: str = "goods_comments"
    refer_page_id: Optional[str]  # =10058_1681221259243_4fdl5o5rm0
    refer_page_sn: Optional[str]  # =10058


class GetOrderData(BaseModel):
    type: str = 'all'
    page: int = 1
    origin_host_name: str = 'mobile.yangkeduo.com'
    page_from: int = 0
    anti_content: str
    size: int = 10
    offset: int = 0


class CommentParams(BaseModel):
    pdduid: str
    page: int = 1
    size: int = 10
    enable_video: int = 1
    enable_group_review: int = 1
    label_id: int = 0


class HtmlSearchParams(BaseModel):
    search_key: str
    search_type: str = "goods"

    source: str = "index"
    search_met_track: str = "manual"
    refer_page_name: str = "search_result"

    options: Optional[str]  # = 3
    refer_page_el_sn: Optional[str]  # =99885
    refer_page_id: Optional[str]  # =10015_1681200600619_tv9sqnav97
    refer_page_sn: Optional[str]  # =10015


class ApiSearchParams(BaseModel):
    pdduid: str
    q: str
    # 从搜索页的页面源码中获取
    list_id: str
    # 需要js计算
    anti_content: str

    item_ver: str = "lzqq"
    coupon_price_flag: int = 1
    source: str = "index"
    search_met: str = "manual"
    sort: str = "default"
    filter: str = ""
    page: int = 1
    is_new_query: int = 1
    size: int = 50

    track_data: Optional[str]  # =refer_page_id,10015_1681200600619_tv9sqnav97
    flip: str  # =0;0;0;0;6c212792-bc8e-40ba-96c8-e10883b473b0


# class GoodsInfo(BaseModel):
#     key: str  # ="goods_468528311758_1_0
#     goodsID: int
#     recTitle: str  # =你可能会喜欢
#     itemType: int  # =3
#     listType: int  # =0
#     imgUrl: str  # =https://img.pddpic.com/mms-material-img/2023-04-08/914bde5d-3769-4c17-8bb5-d7dc291219ba.png
#     itemHeight: int  # =262
#     longImgUrl: str  # =
#     longImgUrlWM: str  # =
#     viewType: int  # =1
#     tagList: list = []
#     # =[{'text': '即将恢复原价', 'textColor': '#E02E24', 'bg_color': 'transparent'}, {'text': '24小时发货', 'textColor': '#9C9C9C', 'bg_color': 'transparent'}, {'text': '满10减1', 'textColor': '#9C9C9C', 'bg_color': 'transparent'}]
#     tagLen: int  # =3
#     propertyTagList: list = []
#     variedTagsList: list = []
#     variedTagsLen: int = 0
#     goodsName: str  # =喵斯快跑 MuseDash 最新版计划通 全曲包全人物 全精灵宠物云存档
#     price: int  # =395
#     priceType: int  # =0
#     priceInfo: str  # =3.95
#     salesTip: str  # =已拼67件
#     localGroup: dict = {}  # LocalGroup ={}
#     logData: dict = {}

#     #: LogData ={'ad': '{"prvtinfo":"JaHnM7Hs4SnLDYyeI+OQ+ubZghmB7r12GncrlttHWJ3LJ2dUU4CIlABajsD71wD/","join_id":"QI_9cFNKQDM1SYIKaKCnGYrynZhn5BuVRgmVlKh0AW_5eT3xskkvOQucB-ZkiIrF","ad_logo":true,"pkinfo":"Z8CMFUjOqTyZBdM/yqYsLrc38JgmhsiCK16vu7NtCftbSlaxXRj03oXV49B0UsKEAqGfncJDp5VSFdH0JEXTzQ==","nbid":"G7P6VRJj9SzGBkUG/kedyS2tqQPVJ2tW4Ubh/NzFTABe4Dcc20uGZ4PXyvqPQEU5TkcBv0zWOFF3DuuBH+aC/KzFqKTF50FxqQC5WTyzk0zD1AGGL6A0LKDdCB1dqZybRYbBeEPgJJBQmUOOnZPV5KeJXhlS4tpXndkDkAOwmrsn7GXhKXPCoo/W4es5HNqw","pubinfo":"{\\"item\\":\\"dhAeB7nqbBQQoXsFjYN00wW/6XIkUZhnV9/eK7goJwM3ZedTLxAhE+cEdxWmcgO0\\",\\"req\\":\\"UIFkW0uB7wpaK7r6RfsG2iNjo2L/dy5I0IwgvwIcAc4=\\"}","openinfo":"{\\"ads_from\\":\\"1\\",\\"is_tr\\":\\"0\\"}","mark":"rI0K0Jq4xpq7MlyVHJ++bB6YcaOqjmjcPSbjdCaDQj0=","search_id":"QI_9cFNKQDM1SYIKaKCnGYrynZhn5BuVRgmVlKh0AW_5eT3xskkvOQucB-ZkiIrF"}', 'p_search': '{"gin_cat_id_1":8736,"track_data":"EJhFGORHILGVASixlQEyBAgCOAFCCmk2bmE1cnI0djNgiwNqBDQmMjhqBDEmMTJqBDQmMTdwnILLdnoL5bey5ou8Njfku7aIAb4BkAHmtsmhBqIBIwiz8ZaxdhDEpJ713NWdi20YkY+kp/ocILPxlrF2KPu1yroTqAEC0AGP5s28/v////8B2gEEMy45NegB////////////AZUCAIDFQ5gCBqUCAMB5RA==","org":1,"group_one_ad":1,"page":1,"env":"shb1","rn":"cc3d8d06-4a80-40ff-8f3e-538da12a5124","exp_info":{"exp":"shb1"},"ad_group":1,"m":"ads","request_id":"cc3d8d06-4a80-40ff-8f3e-538da12a5124","tag1_id":5223127803}'}
#     needAdLogo: bool = True
#     prefixIcons: list = []
#     creativeInfo: dict = {}
#     # CreativeInfo ={'image_url': 'https://img.pddpic.com/mms-material-img/2023-04-08/914bde5d-3769-4c17-8bb5-d7dc291219ba.png', 'image_id': 994904180625}
#     linkURL: str  # =goods.html?goods_id=468528311758&_oc_trace_mark=199&_oc_adinfo=eyJzY2VuZV9pZCI6MH0=&_oc_refer_ad=1&_oak_gallery=https%3A%2F%2Fimg.pddpic.com%2Fmms-material-img%2F2023-04-08%2F914bde5d-3769-4c17-8bb5-d7dc291219ba.png
#     thumbWM: str  # =
#     isRepeated: bool = False
#     specialText: any
#     specName: str  # =
#     phoneRankInfo: dict = {}  # PhoneRankInfo ={}
#     mallEntrance: dict = {}  # MallEntrance ={'mall_id': 248693020}

# class ConfirmRenderBody(BaseModel):
# confirm_display_type : int =0
# refresh : bool =True
# front_env : int =1
# front_version : int =9
# front_supports : FrontSupports ={'prom': ['mctpi', 'pctpi', 'gp', 'rpchs', 'brandvip', 'gbc', 'uupc', 'ep', 'gbs'], 'pay': ['wxc', 'ci', 'cicn', 'hti'], 'fulf': ['safs', 'ct', 'aa', 'alrt']}
# front_action : int =1006
# original_front_env : int =0
# goods_id : str =301116387980
# group_id : int =60879776211
# sku_id : str =1365647053669
# goods_number : int =1
# address_id : str =32562537322
# is_app : int =0
# group_order_id : str =
# promotion_vo : PromotionVo ={'merchant_coupon_vo': None, 'platform_coupon_vo': None, 'use_platform_promotion_request': None, 'use_shop_promotion_requests': None}
# page_from : int =0
# type : int =0
# award_type : int =0
# biz_type : int =0
# service_transparent_field : any
# extend_map : ExtendMap ={'create_order_token': '51c7c5843f6cac3b33fd1dff3590d862', 'create_order_msg': 'C1ZTiloOjO1Y5+v0zMIHon51udzolla1+NJmnkDusRUcXlLLlRfGzEJRz0p3kjFmdvB3wR7LI8f17cN1y4btY+CrB2lmeIWgQadN2Hm9EuHo5H1YR6R6XeRw/cHEZr6EEVL4YKfPf13HvikRz4ZtEx0s+fKRAzCc9DSq8h3gxtHDOZp8Lwls/bs5XRnDjVTTt1NllLbMkj3iZwqeFhCBSXj9OR9zTTrBuzdVzpAK04oZQUg29ydR4Mmc8LMvdQl2N45dFhCyn0pWEsK4PhQtPCCVwrXJsUevODEHH0iTBRTY4C5ckNUrXpYh/5kKbqDMjai83+CL14F1QTTPGZJvWNIwkllyJ+euo0gFI7IuU2GOTXEsE20BYSg+lT5LNbp0lVvpUadEqsumwOKpGaEWE0EHZNEsqFHNH6ELk1uupqy8mFMQ73/CCBEpYs1dnke8D/gUr9auHw+WFQre8qTPw9umQv88xqPRDUhbLe8P6wjvbnr3HWb1q1VDArHC5NifwvRf0EjySrGTDy+hxskIDrFAQVlfPhFiwssy/x+d2cMbj/EU4FlK+WIkKQ8qZjGb6+JPMPfeSCuw1//YgsqLhDK6CUWCGLiahAzFxrONS7Datu2UwwsGOFeLlRHEDMnJgEWLPJyej+HTl55Vwz66U8pMhdzuLhkwOpqeQuCTaJZxq8YXQ8UoqXSbkIJWtX+5ONqnf07o7T9dF6bTKe412u5PUoI4JszD3SJMFL0+aU+syy55W8i+Rp5CobNrGK84WZGnuWSl78xtWeI2Vy61Tko5C6Y+aCvFSe+AV3no9VI=_v1', 'rank_id': '5030010201', 'page_from': 0, 'morgan_trace': '392006f4a5284fd7a50d81081cde1f61', 'biz_type': 0, 'need_face_check': False, 'original_front_env': 0, 'current_front_env': 1, 'lite_contract_code': None}
# pay_channel_list : list =['2', '9', '30', '31', '35', '38', '52', '97', '122', '135', '322', '45001', '56001', '-1']
# origin_hostname : str =mobile.yangkeduo.com
# pay_extend_map : PayExtendMap ={'selected_bind_id': None}
# additional_map : AdditionalMap ={'ship_additional_switch_status': 0}
# source_channel : str =0
# anti_content : str =0aqWfqnFGhlyy9vZZn7TUdmPqdTpgZwzMGcBz_BnFogkMNfMaOxp7x0eYMxj3reb_6LPMfELA5pF1t75VKgJdb4UNPUe9XjTIC3iWFuLd_CEHozhoneJm70QgRq1YxQ8e1g6-uLOwiLmOBbnDXNpjyocAW2ca3kFEn2dIQSn-omIwl6nSsrXZTZws49IflswvlT5BvOtz97XAeLCOIt1XgeIKIMtsZ9IlXY3Mens4s4IX7Rz0RQm_AorVyCD-5Tz9j45tg5IiPZa5Kp2ggwuujMh8QHyW80a4-fWAJWOVMHp2T3oXx2y0zfrGtJBkVh9PPuQ9PjanPw8BG19QpdfQfXmYv5lpRG45A5y2yns3Qxgx4wy9l03Hy0u2IFU61NJeM0Ye43uR7F3l_fHMO-33A7bUc7OcUg5COL7cUEILO-6HOMzTyxdvy85PlTJQYJ3Sobd_c_wn7fWSBW_mm_ezNdztJ7V5wzTnH6RLCZZSi0iuPAUO3g_LTLlJWJCm_ERrdJcCyhREYJRrASoUnWdKJ2S2ZyK-NL_WFNCH7qS4ExN81aK7iyKYdYlC71-TiSKxum7H8NyQ8xXdnGNyCHsNnbO8etrVYt_
# transfer_map : any
# concentrated_transportation_selected_request : any


class Order(BaseModel):
    id: int
    profile_id: int
    order_sn: str
    order_status_prompt: Optional[str]
