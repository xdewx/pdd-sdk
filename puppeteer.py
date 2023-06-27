#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-06 00:49:51
# LastEditTime: 2023-04-22 00:27:25
# LastEditors: leoking
# Description:
#
from urllib.parse import urljoin, urlparse
import requests, re, time
from typing import Awaitable, Union, Optional, List
from datetime import datetime
from pyppeteer import connect
from pyppeteer.page import Page
from conf import DIR4DATA
from pdd_sdk.core import get_anti_content
from pdd_sdk import Client

from dew.orm.model.auth import Credential
from dew.logger import Logger
from dew.annotation.printer import print_return_value

logger = Logger('pdd')


async def try_to_wait_xpath(page: Page, xpath: str, timeout=5 * 1000):
    try:
        return await page.waitForXPath(xpath, dict(timeout=timeout, visible=True))
    except Exception as e:
        logger.warning(e)
    return None


async def try_to_wait(func: Awaitable, value: str, timeout=5 * 1000):
    try:
        return await func(value, dict(timeout=timeout, visible=True))
    except Exception as e:
        logger.warning(e)
    return None


async def try_to_find_element(page: Page, xpath: str, timeout=1 * 1000):
    return await try_to_wait_xpath(page, xpath, timeout=timeout)


class Pdd:
    base_url = "https://mobile.yangkeduo.com"

    def format_url(self, url: str):
        if not url:
            return url
        if url.startswith("http"):
            return url
        return urljoin(self.base_url, url)

    def get_user_id(self):
        return self.credential.id

    def __init__(self, credential: Credential, sms_url: str = None, *args, **kwargs):
        super(Pdd, self).__init__(*args, **kwargs)
        self.credential = credential
        assert re.match(r'^\d{11}$', self.credential.phone), '手机号码格式不对'
        assert self.credential.id, 'COMID没设置'

        self.sms_url = None
        if sms_url:
            assert re.match(r'^https*://.+?:\d+?/.+$', sms_url), "验证码接收地址格式不符合预期"
            self.sms_url = urlparse(sms_url)
            self.sms_api_addr = f"{self.sms_url.scheme}://{self.sms_url.hostname}:{self.sms_url.port}/api/smslist"

            self.sms_api_token = self.sms_url.path.strip("/")

    async def connect(self, wsAddr: str):
        self.browser = await connect(
            dict(
                defaultViewport=None,
                browserWSEndpoint=wsAddr,
            )
        )
        pages = await self.browser.pages()
        if not pages:
            page = await self.browser.newPage()
        else:
            page = pages[0]

        self.page = page

    async def open(self, url, **kwargs):
        url = self.format_url(url)
        return await self.page.goto(url, **kwargs)

    async def has_logined(self) -> bool:
        await self.open('/personal.html')
        flag = await try_to_wait_xpath(
            self.page,
            '//*[@id="main"]/section/div[1]/div[1]/div[1]/div[2]/p',
            timeout=5 * 1000,
        )
        return flag is not None

    # @print_return_value
    def get_sms_history(self) -> List[dict]:
        assert self.sms_url, 'no sms_url specified'
        list = requests.get(
            self.sms_api_addr,
            params=dict(token=self.sms_api_token),
        ).json()
        for dc in list:
            print(
                dc.get('time'),
                (
                    datetime.now()
                    - datetime.strptime(
                        dc.get('time', "2000-01-01 01:00:00"), '%Y-%m-%d %H:%M:%S'
                    )
                ).seconds,
            )
        return list

    @print_return_value
    def wait_sms_code(self, com_id: Union[str, int], timeout=None) -> str:
        com_id = str(com_id).strip().lower().replace("com", "")
        start_time = datetime.now()

        def filter_method(com_id, item: dict):
            dt = (
                datetime.strptime(
                    item.get('time', '2000-01-01 01:00:00'), '%Y-%m-%d %H:%M:%S'
                )
                - start_time
            ).seconds
            flag = str(item.get('com')) == str(com_id) and (-10 <= dt < 60 * 2)
            print(start_time, item.get('time'), dt, flag, item.get('com'), com_id)
            return flag

        while True:
            if timeout is not None and (datetime.now() - start_time).seconds >= timeout:
                return ""

            tmps = list(
                filter(
                    lambda item: filter_method(com_id, item),
                    self.get_sms_history(),
                )
            )
            logger.info("等待验证码中: %s", tmps)
            if len(tmps) >= 1:
                return re.findall(r'验证码是(\d+)', tmps[0].get('content'))[0]
            time.sleep(1)

    async def login(self, check_login_status=True):
        logined = await self.has_logined()
        if check_login_status and logined:
            logger.info("logined before")
            return
        logger.info("not logined before")

        assert self.sms_url, "sms_url not set"
        com_id, phone = self.credential.id, self.credential.phone

        await self.open("/login.html")
        # 点手机登录
        await (
            await try_to_wait_xpath(
                self.page, '//*[@id="first"]/div[2]/div', timeout=10 * 1000
            )
        ).click()

        await self.page.waitFor(1 * 1000)

        # 输入手机号码
        await (
            await try_to_wait_xpath(
                self.page, '//*[@id="user-mobile"]', timeout=3 * 1000
            )
        ).type(phone)

        agreement = await try_to_wait_xpath(
            self.page, '//*[@id="container"]/form/div[2]/p/i', timeout=3 * 1000
        )
        logger.info("agreement found or not:%s", agreement)

        if agreement:
            await agreement.click()

        await (
            await try_to_wait_xpath(
                self.page,
                '//*[@id="code-button"]',
                timeout=1 * 1000,
            )
        ).click()

        code = self.wait_sms_code(com_id, timeout=60)
        assert code, '验证码不能为空'
        await (await try_to_find_element(self.page, '//*[@id="input-code"]')).type(code)

        await (
            await try_to_wait_xpath(
                self.page,
                '//*[@id="submit-button"]',
                timeout=3 * 1000,
            )
        ).click()

        await self.page.waitFor(2 * 1000)

    # async def dump_cookies(self):
    #     cookies = await self.page.cookies()
    #     for c in cookies:
    #         print(c)

    async def get_verify_auth_token(self):
        return await self.page.evaluate("localStorage.VerifyAuthToken")

    async def get_pdd_sdk_client(self) -> Client:
        client = Client(base_url=self.base_url)
        for c in await self.page.cookies():
            client.cookies.set(c.get('name'), c.get('value'))
        client.set_access_token(client.get_access_token_from_cookie())
        client.set_verify_auth_token(await self.get_verify_auth_token())
        return client

    async def goto_profile(self):
        if 'personal.html' not in self.page.url:
            await self.open("/personal.html")

        close = await try_to_wait_xpath(
            self.page,
            '//*[@id="alert-app-download"]/div[2]/div[1]',
            timeout=5,
        )
        if close:
            close.click()

    async def goto_product_page(self, url: str):
        assert 'goods.html?goods_id=' in url, 'unexpected product url'
        # 假装是别人分享的链接
        url += f"&page_from=35&thumb_url=https%3A%2F%2Fimg.pddpic.com%3FimageMogr2%2Fthumbnail%2F400x%257CimageView2%2F2%2Fw%2F400%2Fq%2F80%2Fformat%2Fwebp&refer_page_name=index&refer_page_id=10002_{int(time.time()*1000)}_jv05pyrjtw&refer_page_sn=10002&uin=AGAY3T7CWIGY7CTIWYBTPX5WRQ_GEXDA"
        await self.open(url)
        pur = await try_to_wait_xpath(
            self.page,
            '//*[@id="main"]/div/div[2]/div[26]/div[4]/div[2]',
            timeout=10 * 1000,
        )

        if not pur:
            logger.error("failed to wait product page:%s", url)
            return
        await pur.click()
        rawData = await self.page.evaluate("window.rawData;")
        print(rawData, type(rawData))

    async def fill_addr(
        self,
        name,
    ):
        addr = await try_to_wait_xpath(
            self.page, '//*[@id="main"]/div/div[1]/div[1]/div'
        )
        if not addr:
            return
        await addr.click()
        name = await try_to_wait_xpath(self.page, '//*[@id="name"]')
        pass

    async def make_order(self, sku_id: str, goods_id: str, goods_number: int, **kwargs):
        assert sku_id, "sku_id is required"
        url = f'/order_checkout.html?sku_id={sku_id}&goods_id={goods_id}&goods_number={goods_number}&page_from=35&order_extra_type=1&refer_page_element=open_btn&source_channel=0&refer_page_name=goods_detail&refer_page_id=10014_{int(time.time()*1000)}_ts8hyh7pq9&refer_page_sn=10014'

        await self.open(url)

        await self.page.waitFor(2 * 1000)

        coupon = await try_to_wait_xpath(self.page, '//span[text()="店铺优惠"]')
        if coupon:
            await coupon.click()
            await self.page.waitFor(500)
            x = await try_to_wait(
                self.page.waitForXPath, '//div[text()="关注并领取"]', timeout=1000
            )
            if x:
                await x.click()
                await self.page.waitFor(500)
                get = await try_to_wait_xpath(
                    self.page, '//*[@id="order_checkout"]/div[6]/div/div/div[1]/div[3]'
                )
                if get:
                    await get.click()
                else:
                    logger.warning("没有弹出【关注并领取】二次确认框")
            else:
                logger.warning("没有找到【关注并领取】的按钮")
        else:
            logger.warning("没有发现优惠券入口")

        await self.page.reload()
        await self.page.waitFor(1 * 1000)
        # anti_content = get_anti_content(url)

    async def pay_with_wechat(self):
        wechat = await try_to_wait_xpath(
            self.page,
            '//*[@id="main"]/div[1]/div[6]/div[1]/div/div/div',
            timeout=1000,
        )
        wechat = wechat or await try_to_wait_xpath(
            self.page, '//*[@id="main"]/div/div[4]/div[1]/div/div', timeout=1000
        )
        await wechat.click()

    async def pay_with_alipay(self):
        alipay = await try_to_wait_xpath(
            self.page, '//*[@id="main"]/div[1]/div[6]/div[2]/div/div/div', timeout=1000
        )
        alipay = alipay or await try_to_wait_xpath(
            self.page, '//*[@id="main"]/div/div[4]/div[2]/div/div', timeout=1000
        )
        await alipay.click()

    async def goto_pay(self):
        btn = await try_to_wait_xpath(
            self.page, '//*[@id="main"]/div[1]/div[9]/div[2]', timeout=500
        )
        btn = btn or await try_to_wait_xpath(
            self.page, '//*[@id="main"]/div/div[8]/div[2]', timeout=500
        )
        await btn.click()

    async def handle_alipay(self, username, password):
        assert username and password, "支付账号、密码均不能为空"
        await self.page.waitFor(2 * 1000)
        logger.info("正在为【%s】完成支付", username)

        jump = await try_to_wait_xpath(
            self.page,
            '//*[@id="v2020v2-login-warp"]/div[2]/div/div/a',
            timeout=10 * 1000,
        )
        if not jump:
            logger.warning("没有找到【支付密码支付】的按钮")
        else:
            await jump.click()
            if not re.match(r"^\d{11}$", username):
                logger.info("【%s】非手机号，将使用长密码支付", username)
                tmp = await try_to_wait_xpath(
                    self.page,
                    '//*[@id="J-v2020v2-login-switch-pwd"]',
                    timeout=10 * 1000,
                )
                assert tmp, "没有找到【使用长密码】的按钮"
                await tmp.click()

        u = await try_to_wait_xpath(self.page, '//*[@id="logon_id"]', timeout=3 * 1000)
        if not u:
            logger.warning('没找到账号输入框')
        else:
            await u.type(username)
            await self.page.keyboard.press("Tab")
            # p = await try_to_wait_xpath(
            #     self.page, '//*[@id="pwd_unencrypt"]', timeout=2 * 1000
            # )
            # if not p:
            #     logger.warning('没找到密码输入框')
            await self.page.keyboard.type(password)
            # await self.page.keyboard.press("Enter")

        next = await try_to_wait_xpath(
            self.page, '//*[@id="cashier"]/div[3]/button', timeout=5 * 1000
        )
        if next:
            await next.click()
        else:
            logger.warning("没有找到【下一步】的按钮")

        confirm = await try_to_wait_xpath(
            self.page, '//*[@id="cashierPreConfirm"]/div[2]/button', 5 * 1000
        )
        if confirm:
            await confirm.click()
            p = await try_to_wait_xpath(
                self.page, '//*[@id="pwd_unencrypt"]', timeout=5 * 1000
            )
            if p:
                await p.type(password)
                submit = await try_to_wait_xpath(
                    self.page, '//*[@id="cashier"]/div[2]/button'
                )
                if submit:
                    await submit.click()
        else:
            logger.warning("没有找到【确认付款】的按钮")

        await self.page.waitFor(1 * 1000)
        finish = await try_to_wait_xpath(self.page, '/html/body/div[8]/a')
        if finish:
            await finish.click()

    async def try_validation_shadow_root(self, page, distance=308):
        # 将距离拆分成两段，模拟正常人的行为
        distance1 = distance - 10
        distance2 = 10
        btn_position = await page.evaluate(
            '''
        () =>{
            return {
            x: document.querySelector('#captcha-dialog > div:nth-child(2)').getBoundingClientRect().x,
            y: document.querySelector('#captcha-dialog > div:nth-child(2)').getBoundingClientRect().y,
            width: document.querySelector('#captcha-dialog > div:nth-child(2)').getBoundingClientRect().width,
            height: document.querySelector('#captcha-dialog > div:nth-child(2)').getBoundingClientRect().height
            }
        }
            '''
        )
        print(btn_position)
        return
        x = btn_position['x'] + btn_position['width'] / 2
        y = btn_position['y'] + btn_position['height'] / 2
        # print(btn_position)
        await page.mouse.move(x, y)
        await page.mouse.down()
        await page.mouse.move(x + distance1, y, {'steps': 30})
        await page.waitFor(800)
        await page.mouse.move(x + distance1 + distance2, y, {'steps': 20})
        await page.waitFor(800)

        while True:
            await page.mouse.move(x + 30, y, {'steps': 30})
            await page.mouse.move(x, y, {'steps': 30})
            await page.waitFor(800)

    async def save_captcha(self, name, dialog_pos: dict, auto_clip: bool = False):
        return await self.page.screenshot(
            {
                'path': DIR4DATA.joinpath(name),
                'clip': dict(
                    x=dialog_pos['x'] + 40.96,
                    y=dialog_pos['y'] + 102.4 + 24.576,
                    width=512.01,
                    height=256,
                )
                if auto_clip
                else None,
            }
        )

    async def check_validation(self):
        validate = await try_to_wait_xpath(
            self.page, '//*[@id="intelVerify"]/div', 2 * 1000
        )
        if validate:
            await validate.click()

        dialog = await try_to_wait(
            self.page.waitForSelector, '#captcha-dialog', timeout=2 * 1000
        )
        if not dialog:
            return
        logger.warning("captcha dialog appears")

    async def verify2(self, dialog):
        slide_btn_shape = dict(
            width=143.36,
            height=143.36,
        )
        pos = await self.page.evaluate(
            '''(ele)=>{
                let rec=ele.getBoundingClientRect();
                return {
                    x:rec.x,
                    y:rec.y,
                    width:rec.width,
                    height:rec.height,
                }
            }''',
            dialog,
        )
        x = pos['x'] + slide_btn_shape['width'] / 2
        y = pos['y'] + (pos['height'] - slide_btn_shape['height'] / 2)
        print(pos, x, y)
        # return
        # with open('./x.html', 'w') as f:
        #     f.write(await self.page.content())

        await self.save_captcha("before.png", pos)
        await self.page.mouse.move(x, y)
        await self.page.mouse.down()
        await self.save_captcha("after.png", pos)
        return

        while True:
            await self.page.mouse.move(x + 100, y, {'steps': 30})
            await self.page.waitFor(800)
            await self.page.mouse.move(x, y, {'steps': 30})
            await self.page.waitFor(800)
            print(time.time())

    async def handle_shadow_root(self):
        slider = await try_to_wait_xpath(
            self.page, '//*[@id="slide-button"]/div', 2 * 1000
        )
        if not slider:
            return
        await self.try_validation_shadow_root(self.page)

    async def search(self, keyword: str) -> dict:
        url = f'/search_result.html?search_key={keyword}&search_met_track=history&search_type=goods&source=index&options=3&refer_search_met_pos=1&refer_page_el_sn=99887&refer_page_name=search_result&refer_page_id=10015_{int(time.time()*1000)}_7bgz7ibak6&refer_page_sn=10015'
        await self.open(url)
        return await self.page.evaluate("window.rawData;")


# 点击安全验证后的滑块 '//*[@id="slide-button"]/div')

if __name__ == '__main__':
    pass
