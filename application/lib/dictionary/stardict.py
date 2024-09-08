#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#stardict离线词典支持
import os
from .pystardict import PyStarDict

#获取本地的stardict文件列表，只有列表，没有校验是否有效
def getStarDictList():
    dictDir = os.environ.get('DICTIONARY_DIR')
    if not dictDir or not os.path.exists(dictDir):
        return {}

    ret = {}
    for dirPath, _, fileNames in os.walk(dictDir):
        for fileName in fileNames:
            if fileName.endswith('.ifo'):
                dictName = os.path.splitext(fileName)[0]
                #为了界面显示和其他dict的一致，键为词典路径，值为词典名字
                ret[os.path.join(dirPath, dictName)] = dictName
    return ret

class StarDict:
    name = "stardict"
    #词典列表，键为词典缩写，值为词典描述
    databases = getStarDictList()

    #更新词典列表
    @classmethod
    def refresh(cls):
        cls.databases = getStarDictList()

    def __init__(self, database='', host=None):
        self.database = database
        self.dictionary = None
        if database in self.databases:
            try:
                self.dictionary = PyStarDict(database)
            except Exception as e:
                default_log.warning(f'Instantiate stardict failed: {self.databases[database]}: {e}')

    #返回当前使用的词典名字
    def __repr__(self):
        return 'stardict [{}]'.format(self.databases.get(self.database, ''))
        
    def definition(self, word, language=''):
        word = word.lower().strip()
        ret = self.dictionary.get(word) if self.dictionary else ''
        if isinstance(ret, bytes):
            ret = ret.decode('utf-8')
        lines = [line.strip() for line in str(ret).split('\n') if line.strip()]
        if lines and lines[0] in (word, f'<b>{word}</b>'):
            lines = lines[1:]
        return '\n'.join(lines)

