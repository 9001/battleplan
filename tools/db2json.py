#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import csv
import gzip
import codecs
import operator
import romkan
import jaconv
import html
import unicodedata
import json
import sqlite3


SJIS_WARN = False


s1 = u"アイウエオカキクケコ"  # a=wall
s2 = u"サシスセソタチツテト"
s3 = u"ナニヌネノハヒフヘホ"  # na=wall
s4 = u"マミムメモヤユヨラリ"
w1a = u"れぬねのはひふへほまみむめも"  # re=wall
w1b = u"やゆよらりる"
w2a = u"あくけこさしすせそたちつてと"  # a=wall
w2b = u"いうえおかき"
w3a = u"ＡＢＣＤＥＦＧＨＩＪＫＬ"  # a=wall
w3b = u"ＭＮＯＰＱＲ"

all_rows = w3a + w3b + w2a + w2b + w1a + w1b + s1 + s2 + s3 + s4

all_halls = {
    "s1": s1,
    "s2": s2,
    "s3": s3,
    "s4": s4,
    "w1a": w1a,
    "w1b": w1b,
    "w2a": w2a,
    "w2b": w2b,
    "w3a": w3a,
    "w3b": w3b,
}
all_days = ['土', '日', '月', '火']


def main():
    conn = sqlite3.connect(sys.argv[1])
    # conn.text_factory = lambda x: str(x, "sjis")

    cur = conn.cursor()
    cur.execute("select code, name from ComiketGenre")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur = conn.cursor()
    cur.execute(
        "select id, day, blockId, spaceNo, spaceNoSub, genreId, circleName, circleKana from ComiketCircle"
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)


main()

