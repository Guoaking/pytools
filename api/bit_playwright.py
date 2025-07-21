import asyncio
from dataclasses import dataclass

from playwright.async_api import BrowserContext, Locator, Playwright, async_playwright

from api.bit_api import *
from tools import utils


async def get_image_count(page: BrowserContext.pages):
    parent = page.locator(
        'div[aria-label="Marketplace"] > div > div:nth-child(3) > div '
    ).nth(1)
    b = parent.locator("> div ")
    # count = await b.locator("> div").count()
    # print(f"b 下面有 {count} 个同级 div")
    await b.screenshot(path="../b_with_images.png")
    return await b.locator("> div img").count()
    # for i in range(count):
    #     child_div = b.locator("> div").nth(i)
    #     html = await child_div.inner_html()
    #     print(f"\n子 div {i+1} 的 HTML 片段:")
    #     print(html[:100] + "...")
    #     img = child_div.locator("img")
    #
    #     # 检查是否存在 img 标签
    #     if await img.count() > 0:
    #         src = await img.get_attribute("src")
    #         print(f"子 div {i+1} 中 img 的 src: {src}")
    #     else:
    #         print(f"子 div {i+1} 中没有找到 img 标签")


async def fileupload(page: BrowserContext.pages, dir):
    max_retries = 3  # 最大重试次数
    retry_count = 0  # 当前重试次数

    try:
        file_paths = utils.get_image_files(dir)
        if len(file_paths) == 0:
            print("没有拿到文件, 无法上传")
            return False

        file_input = await page.query_selector('input[type="file"][multiple]')

        while True:
            count = await get_image_count(page)
            print(f"当前图片数量: {count}")
            if count >= 3 or retry_count >= max_retries:
                break  # 数量达标或达到最大重试次数，退出循环

            await file_input.set_input_files(file_paths)
            print(f"已上传 {len(file_paths)} 个文件")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000 * (2**retry_count))

            retry_count += 1
            print(f"上传数量不足，正在进行第 {retry_count}/{max_retries} 次重试...")
            await page.wait_for_timeout(2000)  # 重试前等待一段时间

        # 检查最终结果
        if count < 3:
            print(f"警告：重试 {retry_count} 次后，上传的图片数量仍不足 3 张")
        else:
            print(f"成功上传 {count} 张图片")
            return True
        return False
    except Exception as e:
        print(f"上传失败: {e}")

    finally:
        await page.wait_for_timeout(2000)


@dataclass
class SalePostConfig:
    def __init__(self, title, desc, status, price, cate, filedir):
        self.title = title
        self.desc = desc
        self.status = status
        self.price = price
        self.cate = cate
        self.filedir = filedir

    def to_dict(self):
        return {
            "title": self.title,
            "desc": self.desc,
            "status": self.status,
            "price": self.price,
            "cate": self.cate,
            "filedir": self.filedir,
        }


async def ConfigSalePost(page: BrowserContext.pages, config: SalePostConfig):
    title = config.title
    price = config.price
    cate = config.cate
    status = config.status
    desc = config.desc
    filedir = config.filedir
    try:
        # 1. title
        span_locator = page.locator('span:text("标题")')
        input_locator = span_locator.locator(":scope + input")
        await input_locator.wait_for(state="visible", timeout=5000)
        await input_locator.fill(title)
        await page.wait_for_timeout(1000)

        # 2. price
        span_locator = page.locator('span:text("价格")')
        input_locator = span_locator.locator(":scope + input")
        await input_locator.wait_for(state="visible", timeout=5000)
        await input_locator.fill(price)

        # 3. cate
        span_locator = page.locator('span:text("类别")')
        new_span = span_locator.locator(":scope + div")
        # new_span = span_locator.locator("..").filter(has=page.locator("div"))
        new_span = span_locator.locator("xpath=parent::div")
        await new_span.click()
        await page.wait_for_timeout(3000)
        # 5.1  弹出下拉 找到目标类别
        # new_span = await page.wait_for_selector('span:text-matches(".*类别.*", "i")', timeout=5000)
        dropdown = page.locator("div[role='dialog'][aria-label='Dropdown menu']")
        await dropdown.wait_for(state="visible", timeout=3000)
        elements = dropdown.locator("text=" + cate)
        count = await elements.count()
        if count > 0:
            # 无论多少个元素，都使用第一个
            await elements.first.click()
        else:
            print("未找到匹配元素")

        # 4. status
        span_locator = page.locator('span:text("商品状况")')
        new_span = span_locator.locator(":scope + div")
        await new_span.click()
        await page.wait_for_timeout(1000)

        dropdown = page.locator("div[role='listbox'][aria-label='选择一项']")
        await dropdown.wait_for(state="visible", timeout=3000)
        elements = dropdown.locator("text=" + status)
        count = await elements.count()
        if count > 0:
            await elements.first.click()
        else:
            print("未找到匹配元素")

        # 5. friends
        await check_fierily(page)

        # 6. desc
        await input_desc(page, desc)

        # 7. 图片
        await fileupload(page, filedir)
        await page.wait_for_timeout(1000)
    except Exception as e:
        print(f"操作失败: {e}")

    finally:
        await page.wait_for_timeout(3000)


async def BatchNext(page: BrowserContext.pages):
    try:
        marketplace_btn = await page.wait_for_selector('div[aria-label="下一页"]')
        await marketplace_btn.click()
        await marketplace_btn.wait_for(state="visible", timeout=8000)
        await page.wait_for_timeout(3000)
    except Exception as e:
        print(f"操作失败: {e}")


async def BatchPost(page: BrowserContext.pages):
    try:
        marketplace_btn = await page.wait_for_selector('div[aria-label="发布"]')
        await marketplace_btn.click()
        await marketplace_btn.wait_for(state="visible", timeout=15000)
    except Exception as e:
        print(f"操作失败: {e}")


async def openSalesPage(page: BrowserContext.pages):
    await page.wait_for_load_state("networkidle")
    try:
        marketplace_tab = await page.wait_for_selector('a[aria-label="Marketplace"]')
        await marketplace_tab.click()

        marketplace_btn = await page.wait_for_selector('a[aria-label="新建交易帖"]')
        await marketplace_btn.click()
        await page.wait_for_timeout(1000)

        new_span = await page.wait_for_selector(
            'span:text-matches(".*创建一篇交易.*", "i")', timeout=5000
        )
        await new_span.click()

        await page.wait_for_load_state("networkidle")

        # new_span.wait_for(state="visible", timeout=3000)
        # new_span = await page.query_selector_all('span:text-matches(".*卖东西.*", "i")')
        # print(f"找到 {len(new_span)} 个元素")
        # for i, element in enumerate(new_span):
        #     is_visible = await element.is_visible()
        #     text = await element.inner_text()
        #     print(f"元素 {i + 1}: 可见={is_visible}, 文本='{text}'")
        #     if is_visible:
        #         await  element.click()

        return page
    except Exception as e:
        print(f"操作失败: {e}")

    finally:
        await page.wait_for_timeout(3000)  # 等待5秒以便观察


async def openMPage(page: BrowserContext.pages):
    try:
        # 等待网络请求全部完成后再继续
        await page.goto(
            "https://www.facebook.com/marketplace/create/item", wait_until="networkidle"
        )

        return page
    except Exception as e:
        print(f"操作失败: {e}")


async def basics(page: BrowserContext.pages):
    await page.wait_for_load_state("networkidle")
    try:
        # 点击个人头像
        # profile_pic = await page.wait_for_selector('div[aria-label="你的个人主页"]', timeout=5000)
        # await profile_pic.click()
        # print("成功点击个人头像")
        # await page.wait_for_timeout(2000)  # 等待2秒

        # 返回Marketplace
        # marketplace_tab = await page.wait_for_selector('a[href="/marketplace/"]')
        marketplace_tab = await page.wait_for_selector('a[aria-label="Marketplace"]')
        await marketplace_tab.click()
        # await page.goto("https://www.facebook.com/marketplace/")
        # await page.wait_for_load_state("networkidle")

        # 点击位置筛选器
        location_filter = await page.wait_for_selector(
            "div[id=seo_filters]", timeout=5000
        )
        await location_filter.click()
        print("成功点击位置筛选器")

        location_filter = await page.wait_for_selector(
            'input[aria-label="位置"]', timeout=5000
        )
        await location_filter.click()

        print("成功点击位置筛选器2")

        await page.wait_for_timeout(2000)

        await location_filter.fill("New York")  # 直接填充文本
        # 选择第一个位置建议（示例）

        await page.wait_for_timeout(2000)

        new_span = await page.wait_for_selector(
            'span:text-matches(".*布鲁克.*", "i")', timeout=5000
        )
        await new_span.click()

        # first_location = await page.wait_for_selector('span[role=""]', timeout=5000)
        # await first_location.click()
        print("成功选择位置")

        new_span = await page.wait_for_selector(
            'span:text-matches(".*半径范围.*", "i")', timeout=5000
        )
        await new_span.click()

    except Exception as e:
        print(f"操作失败: {e}")

    finally:
        await page.wait_for_timeout(5000)  # 等待5秒以便观察


async def OpenTargetPage(playwright: Playwright, browser_id):
    res = openBrowser(browser_id)
    ws = res["data"]["ws"]
    print("ws address ==>>> ", ws)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    # print(default_context.pages)
    page = None
    for p in default_context.pages:
        # print(p)
        if "book" in p.url:
            print(p)
            page = p
            break
    await page.bring_to_front()

    return page


async def OpenPage(playwright: Playwright, browser_id):
    res = openBrowser(browser_id)
    ws = res["data"]["ws"]
    print("ws address ==>>> ", ws)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    # print(default_context.pages)
    page = None
    for p in default_context.pages:
        # print(p)
        if "book" in p.url:
            print(p)
            page = p
            break
    await page.bring_to_front()

    return page


def run2(id, config: SalePostConfig):
    # 使用 asyncio.run() 运行异步函数
    asyncio.run(run2_async(id, config))


async def reLoadAndPost(page: BrowserContext.pages, config: SalePostConfig):
    if "marketplace/create/item" not in page.url:
        await openMPage(page)
    await ConfigSalePost(page, config)


async def run2_async(id, config: SalePostConfig):
    async with async_playwright() as playwright:
        page = await OpenPage(playwright, id)
        # 检查 基础配置 1.语言， 2.位置
        # await basics(page)
        # 进入市场
        # if "marketplace/create" not in page.url:
        #     page = await openSalesPage(page)

        await reLoadAndPost(page, config)
        await page.wait_for_timeout(3000)

        # await ConfigSalePost(page, config)
        await BatchNext(page)
        await BatchPost(page)


async def check_test(span_locator: Locator):
    await span_locator.get_attribute("aria-checked")


async def check_fierily(page: BrowserContext.pages):
    span_locator = page.locator('span:text("对好友隐藏这篇")')
    # grand_grand_parent = span_locator.locator("..").locator("..").locator("..").locator("..").locator("..").locator("..").
    grand_grand_parent = span_locator.locator("xpath=ancestor::*[6]")

    # b = grand_grand_parent.locator("> div:nth-child(1) > div:nth-child(3)")
    input_locator = grand_grand_parent.locator('input[role="switch"][type="checkbox"]')
    aria_checked = await input_locator.get_attribute("aria-checked")

    if aria_checked != "true":
        await input_locator.click()
        await page.wait_for_timeout(1000)
        aria_checked = await input_locator.get_attribute("aria-checked")
    print(f"对好友隐藏: {aria_checked}")


async def input_desc(page, desc):
    max_retries = 3  # 最大重试次数
    retry_count = 0  # 当前重试次数

    try:
        span_locator = page.locator('span:text("添加更多详情来")')
        new_span = span_locator.locator("xpath=parent::div")
        xpath = '//span[text()="说明"]/following-sibling::div/textarea'
        count = 0
        while True:
            if retry_count >= max_retries:
                break

            textarea_locator = page.locator(xpath)
            count = await textarea_locator.count()

            if count == 1:
                await textarea_locator.fill(desc)
                await page.wait_for_timeout(2000)
                break

            print("点击")
            await new_span.click()
            await page.wait_for_timeout(1000 * (2**retry_count))
            retry_count += 1

        if count == 0:
            print(f"警告：重试 {retry_count} 次后，还是获取desc配置失败")
    except Exception as e:
        print(f"填写失败: {e}")


async def del_product(page, name):
    div = page.locator('div[aria-label="你的 Marketplace 商品列表"]')
    span_locator = div.locator(f'span:text("{name}")')
    count = await span_locator.count()
    if count == 0:
        print(f"已经不存在的商品: {name}, 无需删除")
        return

    bb = (
        span_locator.locator("..")
        .locator("..")
        .locator("..")
        .locator("..")
        .locator("..")
        # .locator("..")
        # .locator("..")
    )
    h = await bb.inner_html()
    await bb.click()
    # return
    s2 = page.locator('div[role="dialog"][aria-label="你的商品"]')

    # s22 = s2.locator('div:text("交易帖点击")')
    # s22 = page.locator('div:text("交易帖点击")')
    # s22 = page.locator('xpath=//div[contains(text(), "次交易帖点击")]')
    # txt = await s22.inner_text()
    # print(txt)

    span2 = s2.locator('div[aria-label="删除"]')
    await span2.click()

    s3 = page.locator('div[role="dialog"][aria-label="删除交易帖"]')
    span3 = s3.locator('div[aria-label="删除"]:not([aria-disabled="true"])')
    await span3.click()

    await page.wait_for_timeout(5000)

    return

    cc = bb.locator('div[aria-label="莆田鞋舒適耐穿的更多选项"]')
    await cc.click()
    # await cc.is_visible()

    await page.wait_for_timeout(timeout=5000)

    s2 = page.locator('div[role="menu"]')
    span2 = s2.locator('span:text("标记为交易中")').locator("..").locator("..")
    await span2.click()

    # h = await bb.inner_html()
    # print(h)


async def findEle(id):
    prodcts = [
        "高清航拍玩具無人機",
        "柏林之聲藍牙耳機 全景音效狂甩不掉",
        # "磁吸快充充電寶,自帶線支架",
        "莆田鞋舒適耐穿",
    ]
    async with async_playwright() as playwright:
        page = await OpenPage(playwright, id)
        for v in prodcts:
            await del_product(page, v)


async def run2_async2(id, config: SalePostConfig):
    prodcts = [
        "高清航拍玩具無人機",
        "柏林之聲藍牙耳機 全景音效狂甩不掉",
        "磁吸快充充電寶,自帶線支架",
        "莆田鞋舒適耐穿",
    ]
    async with async_playwright() as playwright:
        page = await OpenPage(playwright, id)

        for v in prodcts:
            await del_product(page, v)

        # await page.reload()


if __name__ == "__main__":
    print()
    # findEle()
    OpenTargetPage()
