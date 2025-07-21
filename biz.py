import asyncio

from api import bit_api, bit_playwright
from conifg.config import *


async def process_with_semaphore(bs, config, concurrency=5):
    # 创建信号量实例
    semaphore = asyncio.Semaphore(concurrency)

    async def process_single(b):
        async with semaphore:  # 使用信号量限制并发
            Id = b["id"]
            try:
                await bit_playwright.run2_async(Id, config)
            except Exception as e:
                print(f"Error processing {Id}: {e}")
            else:
                print(4)  # 只有当run2_async成功完成时才会打印

    tasks = [process_single(b) for b in bs]
    await asyncio.gather(*tasks)


async def process_with_semaphore2(bs, config, concurrency=5):
    # 创建信号量实例
    semaphore = asyncio.Semaphore(concurrency)

    async def process_single(b):
        async with semaphore:  # 使用信号量限制并发
            Id = b
            await bit_playwright.run2_async(Id, config)

    tasks = [process_single(b) for b in bs]
    await asyncio.gather(*tasks)


async def process_with_semaphore3(bs, config, concurrency=5):
    # 创建信号量实例
    semaphore = asyncio.Semaphore(concurrency)

    async def process_single(b):
        async with semaphore:  # 使用信号量限制并发
            Id = b["id"]
            await bit_playwright.run2_async2(Id, config)

    tasks = [process_single(b) for b in bs]
    await asyncio.gather(*tasks)


def getOneProd(file, lang):
    meta_path = file
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = MetaFile(meta_path, data)
    zh_tw = meta.get_language(lang)
    if not zh_tw:
        return

    config = bit_playwright.SalePostConfig(
        title=zh_tw.title,
        desc=zh_tw.desc,
        status="全新",
        price=zh_tw.price,
        cate=zh_tw.cate,
        filedir=zh_tw.dir,
    )
    return config


path = "/Users/bytedance/Downloads/图片/蓝牙耳机/1/meta.json"
# path = "/Users/bytedance/Downloads/图片/莆田鞋子/1/meta.json"
# path = "/Users/bytedance/Downloads/图片/玩具无人机/1/meta.json"
# path = "/Users/bytedance/Downloads/图片/磁吸充电宝/1/meta.json"
lang = "zh-tw"


def runAll():
    config = getOneProd(path, lang)
    bs = bit_api.listAllBrowser()
    asyncio.run(process_with_semaphore(bs, config, 10))


def runOne():
    bs = ["abbcfd4f1c3341b1bd4acaeb76fc893a"]
    config = getOneProd(path, lang)
    asyncio.run(process_with_semaphore2(bs, config, 5))


def runReload():
    config = getOneProd(path, lang)
    bs = bit_api.listAllBrowser()
    asyncio.run(process_with_semaphore3(bs, config, 10))


if __name__ == "__main__":
    # bit_api.ChnageBrowserBounds(900, 550)
    runAll()
    # runOne()
    # runReload()
