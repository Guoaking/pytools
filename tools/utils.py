import os
import random
import secrets
from pathlib import Path
from typing import List


def get_all_files(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def get_image_files(folder_path):
    extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    return [
        str(file)
        for file in Path(folder_path).rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    ]


def find_meta_json_files(root_dir: str) -> List[str]:
    """递归查找指定目录下的所有 meta.json 文件"""
    meta_files = []

    for root, dirs, files in os.walk(root_dir):
        # print(root, dirs, files)
        for file in files:
            if file.lower() == "meta.json":
                meta_files.append(os.path.join(root, file))

    return meta_files


def random_integer(min_val, max_val):
    """
    生成指定区间 [min_val, max_val] 内的随机整数（包含两端点）
    """
    return random.randint(min_val, max_val)


def random_integer2(min_val, max_val, inclusive=True):
    """
    生成指定区间内的随机整数
    - inclusive=True: 区间为 [min_val, max_val]（包含上限）
    - inclusive=False: 区间为 [min_val, max_val)（不包含上限）
    """
    if inclusive:
        return random.randrange(min_val, max_val + 1)
    else:
        return random.randrange(min_val, max_val)


def secure_random_integer(min_val, max_val):
    """
    生成密码学安全的随机整数（包含两端点）
    """
    return secrets.randbelow(max_val - min_val + 1) + min_val


# 使用示例
if __name__ == "__main__":
    secure_num = secure_random_integer(200, 300)
    print(secure_num)
    print(random_integer(200, 300))
