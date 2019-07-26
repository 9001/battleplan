#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import csv
import codecs
import operator
import romkan
import jaconv
import html
import unicodedata
import json


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
all_days = ["金", "土", "日", "月"]


def main():
    r = []
    print("loading csv")
    with open(sys.argv[1], "r", encoding="utf-8") as fgz:
        fcsv = csv.reader(fgz, delimiter=",")
        for cr in fcsv:
            if cr[0] != "Circle":
                # print('skipping; cr[0] =', cr[0])
                continue

            if len(cr) != 29:
                raise Exception("unexpected num fields {}".format(len(cr)))

            v = {
                "imageid": cr[1],
                "ccc-gui-color-probably": cr[2],
                "ccc-gui-page-number": cr[3],
                "ccc-gui-page-offset": cr[4],
                "day": cr[5],
                "hall": cr[6],
                "row": cr[7],
                "col": cr[8],
                "ngenre": cr[9],
                "cirnam1": cr[10],
                "cirnam2": cr[11],
                "authnam": cr[12],
                "prodnam": cr[13],
                "urlmain": cr[14],
                "mail": cr[15],
                "desc": cr[16],
                "x7": cr[17],  # always blank
                "x": cr[18],
                "y": cr[19],
                "x10": cr[20],
                "subcol": "ab"[int(cr[21])],
                "description": cr[22],
                "urlcata": cr[23],
                "urlcirc": cr[24],
                "x13": cr[25],  # always blank
                "urltwit": cr[26],
                "urlpxiv": cr[27],
                "x14": cr[28],  # always blank
            }
            v["loc"] = "".join(
                [v["hall"], v["row"], str(v["col"]).rjust(2, "0"), v["subcol"]]
            )
            r.append(v)

    for nday, cday in enumerate(all_days, 1):
        print("writing day {}".format(nday))
        ret = []
        rd = [x for x in r if x["day"] == cday]
        for hallname, rows in sorted(all_halls.items()):
            for row in rows:
                for v in [x for x in rd if x["row"] == row]:
                    romaji = jaconv.h2z(v["cirnam2"])
                    romaji = romkan.to_roma(romaji)
                    entry = {
                        "loc": str(nday) + v["loc"],
                        "kan": v["cirnam1"],
                        "rom": romaji,
                        "x": v["x"],
                        "y": v["y"],
                    }

                    if v["x13"] or v["x14"]:
                        print(v)
                        print(v["x13"])
                        print(v["x14"])
                        print("    !!!!!!!!!!!!!!!!!!!\n")

                    urls = []
                    for k in ["urlmain", "urlcata", "urlcirc", "urltwit", "urlpxiv"]:
                        url = v[k]
                        if (
                            "://webcatalog.circle.ms/Circle/" in url
                            or "://portal.circle.ms/Circle/Index" in url
                            or len(url) < 5
                            or url in urls
                        ):
                            continue

                        urls.append(url)

                    if urls:
                        entry["url"] = urls

                    ret.append(entry)

        with open("../json/lkrxy{}.json".format(nday), "wb") as f:
            f.write(
                json.dumps(ret, sort_keys=True)
                .replace('"}, {"kan": "', '"},\n{"kan": "')
                .encode("utf-8")
            )


main()

