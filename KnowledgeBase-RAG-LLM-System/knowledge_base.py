"""
知识库
"""
from datetime import datetime
import os

from requests_toolbelt.adapters import source

import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def check_md5(md5_str:str):
    """
    检查传入的md5字符串是否已经被处理过了
    return False表示文件未处理过
    """
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r',encoding='utf-8').readlines():
            line = line.strip()         # 处理字符串前后的空格和回车
            if line == md5_str:
                return True

        return False


def save_md5(md5_str:str):
    """
    将传入的md5字符串，记录到文件内保存
    """
    with open(config.md5_path, 'a',encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str:str,encoding='utf-8'):
    """将传入的字符串转化为md5字符串"""

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    # 创建md5对象
    md5_obj = hashlib.md5()             # 得到md5对象
    md5_obj.update(str_bytes)           # 更新内容(传入即将要转换的字节数组)
    md5_hex = md5_obj.hexdigest()       # 得到md5的十六进制字符串
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)    # 如果文件夹不存在则创建，如果存在则跳过

        self.chroma = Chroma(
            collection_name=config.collection_name,     # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v1"),
            persist_directory=config.persist_directory, # 数据可本地存储文件夹
        )          # 向量存储的实例Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,       # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,   # 连续文本段之间的字符重叠数量
            separators=config.separators,       # 自然段落划分的符号
            length_function=len,                   # 用python默认的方法
        )         # 文本分割器的对象

    def upload_by_str(self,data,filename):
        """将传入的字符串进行向量化，存入向量数据库中"""
        # 想得到传入字符串的md5值
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在在知识库中"
        if len(data) > config.max_spliter_char_num:
            knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        mata_data = {
            "source" :filename,
            "create_time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "operator":"自己",
        }

        self.chroma.add_texts(          # 内容加载到向量库中
            knowledge_chunks,
            metadatas=[mata_data for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"


if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("哈基米叮咚鸡","testfile")
    print(r)
    # r1 = get_string_md5("哈基米")
    # r2 = get_string_md5("哈基米")
    # r3 = get_string_md5("叮咚鸡")
    # save_md5("69c2b8eaf13c2ac823900dd1fe0eb116")
    # print(check_md5("69c2b8eaf13c2ac823900dd1fe0eb116"))
