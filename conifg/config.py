import json
import os
from typing import Any, Dict, List


class MetaData:
    """表示 meta.json 中的语言特定数据"""

    def __init__(self, data: Dict[str, Any]):
        self.title = data.get("title", "")
        self.desc = data.get("desc", "")
        self.desc_all = data.get("desc_all", [])
        self.base_name = data.get("base_name", "")
        self.price = data.get("price", "")
        self.cate = data.get("cate", "")
        self.dir = data.get("dir", "")

    def __str__(self):
        return f"MetaData(title='{self.title}', base_name='{self.base_name}')"


class MetaFile:
    """表示整个 meta.json 文件"""

    def __init__(self, path: str, data: Dict[str, Dict[str, Any]]):
        self.path = path
        self.languages = {}
        for lang, lang_data in data.items():
            self.languages[lang] = MetaData(lang_data)

    def get_language(self, lang: str) -> MetaData:
        """获取指定语言的数据"""
        return self.languages.get(lang)

    def __str__(self):
        langs = ", ".join(self.languages.keys())
        return f"MetaFile(path='{self.path}', languages=[{langs}])"


def find_meta_json_files(root_dir: str) -> List[str]:
    """递归查找指定目录下的所有 meta.json 文件"""
    meta_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower() == "meta.json":
                meta_files.append(os.path.join(root, file))
    return meta_files


def load_meta_files(root_dir: str) -> List[MetaFile]:
    """加载并解析所有 meta.json 文件"""
    meta_files = []
    for file_path in find_meta_json_files(root_dir):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            meta_files.append(MetaFile(file_path, data))
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return meta_files


# 使用示例
if __name__ == "__main__":
    folder_path = "/Users/bytedance/Downloads/图片/"  # 替换为实际路径
    meta_objects = load_meta_files(folder_path)

    for meta in meta_objects:
        print(f"\n文件: {meta.path}")
        print(f"支持的语言: {list(meta.languages.keys())}")

        # 获取中文简体数据
        zh_cn = meta.get_language("zh-cn")
        if zh_cn:
            print(f"标题(简体): {zh_cn.title}")
            print(f"描述(简体): {zh_cn.desc}")

        # 获取中文繁体数据
        zh_tw = meta.get_language("zh-tw")
        if zh_tw:
            print(f"标题(繁体): {zh_tw.title}")
            print(f"目录路径(繁体): {zh_tw.dir}")
