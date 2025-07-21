import json

import requests

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档

url = "http://127.0.0.1:54345"
headers = {"Content-Type": "application/json"}


def createBrowser():  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
    json_data = {
        "name": "google",  # 窗口名称
        "remark": "test",  # 备注
        "proxyMethod": 2,  # 代理方式 2自定义 3 提取IP
        # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
        "proxyType": "socks5",
        "host": "127.0.0.1",  # 代理主机
        "port": "7890",  # 代理端口
        "proxyUserName": "775846611",  # 代理账号
        "browserFingerPrint": {  # 指纹对象
            "coreVersion": "124",  # 内核版本，注意，win7/win8/winserver 2012 已经不支持112及以上内核了，无法打开
            "ostype": "PC",
            "os": "Win32",
            "osVersion": "11,10",
        },
    }

    res = requests.post(
        f"{url}/browser/update", data=json.dumps(json_data), headers=headers
    ).json()
    print(res)
    browserId = res["data"]["id"]
    print(browserId)
    return browserId


def updateBrowser():  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
    json_data = {
        "ids": ["93672cf112a044f08b653cab691216f0"],
        "remark": "我是一个备注",
        "browserFingerPrint": {},
    }
    res = requests.post(
        f"{url}/browser/update/partial", data=json.dumps(json_data), headers=headers
    ).json()
    print(res)


def openBrowser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f"{id}"}
    res = requests.post(
        f"{url}/browser/open", data=json.dumps(json_data), headers=headers
    ).json()
    return res


def closeBrowser(id):  # 关闭窗口
    json_data = {"id": f"{id}"}
    requests.post(
        f"{url}/browser/close", data=json.dumps(json_data), headers=headers
    ).json()


def deleteBrowser(id):  # 删除窗口
    json_data = {"id": f"{id}"}
    print(
        requests.post(
            f"{url}/browser/delete", data=json.dumps(json_data), headers=headers
        ).json()
    )


# 排列窗口以及调整窗口尺寸
def ChnageBrowserBounds(width, height):
    json_data = {
        "type": "box",  # diagonal box
        "width": width,  # 330  280
        "height": height,
        "startX": 0,
        "startY": 0,
        "col": 8,
        "offsetX": 0,
        "offsetY": 0,
        # "orderBy": "asc",
        # "ids": [
        #     "6bb433a5833245039c13c822402ab30f",
        #     "799f01cbd1dd4e28b5ac6edcc88a00b5",
        # ],  # 传入ids时会自动忽略 seqlist
        # "seqlist": [4348],
        "spaceX": 0,
        "spaceY": 0,
    }
    print(
        requests.post(
            f"{url}/windowbounds", data=json.dumps(json_data), headers=headers
        ).json()
    )


def ChnageBrowserBoundsMin():
    ChnageBrowserBounds(330, 550)


def ChnageBrowserBoundsMax():
    ChnageBrowserBounds(1200, 1000)


# 一键自适应排列窗口
# 窗口序号列表，如 [12, 14, 1889]， 不传则排列全部窗口
def FlexBrowser():
    ids = []
    json_data = {"seqlist": ids}
    print(json.dumps(json_data))
    print(
        requests.post(
            f"{url}/windowbounds/flexable", data=json.dumps(json_data), headers=headers
        ).json()
    )


# 获取所有活着的已打开的窗口的进程 ID，会自动过滤掉已死掉的进程，无参数
def listAllBrowser():
    data_dict = requests.post(f"{url}/browser/pids/all", headers=headers).json()

    # 创建一个空数组用于存储浏览器信息
    browser_list = []

    # 遍历响应数据，将每个浏览器信息添加到数组中
    for k, value in data_dict["data"].items():
        browser_info = {"pid": value, "id": k}
        browser_list.append(browser_info)

    # 返回包含所有浏览器信息的数组
    return browser_list


def listBrowser(size):  # 删除窗口
    json_data = {"page": 0, "pageSize": size}
    data_dict = requests.post(
        f"{url}/browser/list", data=json.dumps(json_data), headers=headers
    ).json()

    # 创建一个空数组用于存储浏览器信息
    browser_list = []

    # 遍历响应数据，将每个浏览器信息添加到数组中
    for value in data_dict["data"]["list"]:
        browser_info = {"name": value["name"], "seq": value["seq"], "id": value["id"]}
        browser_list.append(browser_info)

    # 返回包含所有浏览器信息的数组
    return browser_list
    # for key, v in value.items():
    #     print(f" Value: {value}")
    #     print(f"Key Value: {value}")

    # name: google,seq: 11,id: 6f305edcec9e4ace80266662196d18f4
    # name: _10,seq: 10,id: abbcfd4f1c3341b1bd4acaeb76fc893a
    # name: _9,seq: 9,id: 6b4d31069c53446dae1012f7d7b16de5
    # name: _8,seq: 8,id: 404c0736cd3a48aeb1179917c559ea42
    # name: _7,seq: 7,id: 00202c89347c45d2a4ed303fdb3f06e1
    # name: _6,seq: 6,id: 1f66a1ad532c41da8acbc25feda467f3
    # name: _5,seq: 5,id: 99ec4fd12fad403d8142b13be677d326
    # name: _4,seq: 4,id: c54d4127bc5f4a3695af245f2fa443c3
    # name: _3,seq: 3,id: 062f0c4ce7814a5c9bf7fe0fd13a5a3d
    # name: _2,seq: 2,id: 7d2e272464454a988e15b7de58f23afa
    # name: _1,seq: 1,id: 7979c0d0d08d4e93b3a64ed22f57c441


def OpenAllBrowser():
    lists = listBrowser(100)
    for value in lists:
        print(value)
        id = value["id"]
        openBrowser(id)


def CloseAllBrowser():
    lists = listAllBrowser()
    for value in lists:
        print(value)
        id = value["id"]
        closeBrowser(id)


if __name__ == "__main__":
    # browser_id = createBrowser()
    OpenAllBrowser()
    # CloseAllBrowser()

    # print(listAllBrowser())
    # FlexBrowser()
    # ChnageBrowserBoundsMax()
    # ChnageBrowserBoundsMin()
    # ChnageBrowserBounds(900, 550)
