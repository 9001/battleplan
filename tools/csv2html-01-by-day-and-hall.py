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


SJIS_WARN = False


all_rows = u"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺアイウエオカキクケコシサスセソタチツテトナニヌネノハパヒピフプヘペホポマミムメモヤユヨラリルレロあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめやゆもよらりれる"
e1 = u"ＢＣＤＥＦＧＨＩＪＫＬ"
e2 = u"ＡＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"  # a=wall
e3 = u"アイウエオカキクケコサ"
e6 = u"スセソタチツテトナニヌネ"
e5 = u"シノハパヒピフプヘペホポマ"  # tsu=wall
e4 = u"ミムメモヤユヨラリルレロ"
w1a = u"れにぬねのはひふへほまみむめも"  # re=wall
w1b = u"やゆよらりる"
w2a = u"あくけこさしすせそたちつてとな"  # a=wall
w2b = u"いうえおかき"
all_halls = {
    "e1": e1,
    "e2": e2,
    "e3": e3,
    "e6": e6,
    "e5": e5,
    "e4": e4,
    "w1a": w1a,
    "w1b": w1b,
    "w2a": w2a,
    "w2b": w2b,
}
all_days = ['土', '日', '月', '火']

genres_jp = {
    "111": "創作(少年)",
    "112": "創作(少女)",
    "113": "創作(JUNE/BL)",
    "114": "歴史・創作(文芸・小説)",
    "115": "学漫",
    "116": "オリジナル雑貨",
    "211": "ギャルゲ─",
    "212": "デジタル(その他)",
    "213": "同人ソフト",
    "221": "TYPE-MOON",
    "232": "アイドルマスター",
    "233": "ラブライブ！",
    "234": "東方 Project",
    "300": "ゲーム(その他)",
    "311": "ゲーム(電源不要)",
    "312": "ゲーム(ネット・ソーシャル)",
    "313": "ゲーム(RPG)",
    "314": "ゲーム(恋愛)",
    "315": "ゲーム(ソーシャル女性向け)",
    "321": "スクウェア・エニックス(RPG)",
    "331": "艦これ",
    "332": "刀剣乱舞",
    "333": "あんさんぶるスターズ！",
    "334": "アズールレーン",
    "400": "FC(ジャンプその他)",
    "431": "黒子のバスケ",
    "432": "ハイキュー！！",
    "500": "アニメ(その他)",
    "511": "アニメ(少女)",
    "531": "ガンダム",
    "532": "TIGER＆BUNNY",
    "534": "ユーリ!!! on ICE",
    "535": "ガルパン",
    "600": "評論・情報",
    "611": "鉄道・旅行・メカミリ",
    "700": "TV・映画・芸能・特撮",
    "711": "音楽(洋楽・邦楽・男性アイドル)",
    "811": "FC(小説)",
    "812": "FC(少年)",
    "813": "FC(少女・青年)",
    "831": "ヘタリア",
    "833": "進撃の巨人",
    "836": "名探偵コナン",
    "900": "その他",
    "911": "コスプレ",
    "912": "男性向",
    "999": "ノンジャンル"
}

genres_en = {  # thx google tl
    "111": "Creation/Boy",
    "112": "Creation/Girl",
    "113": "Creation/BL",
    "114": "History and Creation (literary arts and novels)",
    "115": "Academic",
    "116": "OC/Misc",
    "211": "Galge",
    "212": "Digital/Misc",
    "213": "Doujin Software",
    "221": "TYPE-MOON",
    "232": "IM@S",
    "233": "LoveLive",
    "234": "TOUHOU HIJACK",
    "300": "Games/Misc",
    "311": "Games/Analogue",
    "312": "Games/Net/Social",
    "313": "Games/RPG",
    "314": "Games/Love",
    "315": "Games/SocialWomen",
    "321": "Square Enix",
    "331": "Kancolle",
    "332": "Tokuen Ranbu",
    "333": "Ensemble Stars",
    "334": "Azur Lane",
    "400": "FC/ShonenJump",
    "431": "Kuroko no Basuke",
    "432": "Haikyu",
    "500": "Anime/Misc",
    "511": "Anime/Shoujo",
    "531": "Gundam",
    "532": "TIGER&BUNNY",
    "534": "Yuri on ice",
    "535": "Garupan",
    "600": "Critic/Info",
    "611": "Rail/Travel/Mechamy",
    "700": "TV/Movies/VFX",
    "711": "Music/Western/MaleIdol",
    "811": "FC/Novels",
    "812": "FC/Shonen",
    "813": "FC/Shoujo",
    "831": "Hetalia",
    "833": "Attack on Titan",
    "836": "Detective Conan",
    "900": "Misc",
    "911": "Cosplay",
    "912": "For dudes",
    "999": "Unclassified",
}


class SPIRAL_KOMACHI_SPKM_0003(object):
    def __init__(self, binfile):
        self.binfile = binfile

    def __iter__(self):
        nline = 0
        for ln in self.binfile:
            nline += 1
            try:
                yield ln.decode("sjis").rstrip()
            except UnicodeDecodeError as uee:
                rv = ln.decode("sjis", "backslashreplace").rstrip()
                yield rv

                if SJIS_WARN:
                    print(
                        "WARNING: csv decode error line {} byte {}".format(
                            nline, uee.start
                        )
                    )
                    try:
                        ofs = len(ln[: uee.start].decode("sjis", "backslashreplace"))
                        print(
                            "{}\033[1;37;41m{}\033[0m{}".format(
                                rv[:ofs], rv[ofs : ofs + 3], rv[ofs + 3 :]
                            )
                        )
                    except:
                        print(rv)


wbuf = u""


def p(msg):
    global wbuf
    wbuf += msg + "\n"
    print(msg)


def main():
    global wbuf
    r = []
    print("loading csv")
    with gzip.open("../raw-data/everything-csv-ver2.csv.gz", "rb") as fgz:
        # fu8 = codecs.iterdecode(fgz, 'sjis')
        fu8 = SPIRAL_KOMACHI_SPKM_0003(fgz)
        fcsv = csv.reader(fu8, delimiter=",")
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
                "col": cr[8].rjust(2, "0"),
                "ngenre": cr[9],
                "cirnam1": cr[10],
                "cirnam2": cr[11],
                "authnam": cr[12],
                "prodnam": cr[13],
                "urlmain": cr[14],
                "mail": cr[15],
                "desc": cr[16],
                "x7": cr[17],  # always blank
                "x8": cr[18],
                "x9": cr[19],
                "x10": cr[20],
                "subcol": "ab"[int(cr[21])],
                "x12": cr[22],  # always blank
                "urlcata": cr[23],
                "urlcirc": cr[24],
                "x13": cr[25],  # always blank
                "urltwit": cr[26],
                "urlpxiv": cr[27],
                "x14": cr[28],  # always blank
            }
            v["loc"] = "".join([v["hall"], v["row"], v["col"], v["subcol"]])
            r.append(v)

            # ptab = [ 'day', 'loc', 'ngenre', 'x8', 'x9', 'x10', 'cirnam1' ]
            # for kn in ptab:
            # 	print('\033[36m{}\033[33m{:<8}\033[0m '.format(kn, v[kn][:8]), end='')
            # print()

            # if False:  # all rows
            # 	print()
            # 	print(cr)
            # 	for n, v in enumerate(cr):
            # 		print('  {} {}'.format(n, v))

    # print('counting genres per day')
    wbuf = u""
    for day in all_days:
        p("\nday {}:".format(day))
        count = {}
        for v in r:
            if v["day"] != day:
                continue

            genre = genres_en[v["ngenre"]]
            try:
                count[genre] += 1
            except:
                count[genre] = 1

        for k, v in sorted(count.items(), key=operator.itemgetter(1)):
            p("  {:>4} circles: {}".format(v, k))

    with open("../number-of-circles-in-each-genre-per-day.txt", "wb") as f:
        f.write(wbuf.encode("utf-8"))

    seen = []
    for v in r:
        row = v["row"]
        if row not in seen:
            seen.append(row)

    # print('rows:', ''.join(seen))
    for row in seen:
        if row not in all_rows:
            raise Exception("row not in all_rows: {}".format(row))

    for x, rowset in all_halls.items():
        for row in rowset:
            if row not in all_rows:
                raise Exception("hallrow not in all_rows: {}".format(row))

    for row in all_rows:
        found = False
        for x, rowset in all_halls.items():
            if row in rowset:
                found = True
                break

        if not found:
            raise Exception("row not found in hall: {}".format(row))

    with open("csv2html-01-by-day-and-hall.html", "rb") as f:
        header = f.read()

    if False:
        # debug: show info about a particular row
        for nday, cday in enumerate(all_days, 1):
            for v in r:
                if v["day"] != cday:
                    continue

                if v["row"] != e1[1]:
                    continue

                ptab = ["day", "loc", "ngenre", "x8", "x9", "x10", "cirnam1"]
                for kn in ptab:
                    print(
                        "\033[36m{}\033[33m{:<8}\033[0m ".format(kn, v[kn][:8]), end=""
                    )
                print()

    loc_ckanji_map = {}
    loc_cromaji_map = {}
    for nday, cday in enumerate(all_days, 1):
        rd = [x for x in r if x["day"] == cday]
        for hallname, rows in sorted(all_halls.items()):
            print("writing day {} hall {}".format(nday, hallname))
            for row in rows:
                # row_fn = jaconv.z2h(row, kana=False)
                # row_fn = jaconv.h2z(row_fn, ascii=False)
                row_fn = unicodedata.normalize("NFKC", row)
                # row_fn = row
                with open(
                    "../html/by-day-and-hall/day{}-{}-{}.html".format(
                        nday, hallname, row_fn
                    ),
                    "wb",
                ) as f:
                    f.write(header)
                    rdh = [x for x in rd if x["row"] == row]
                    if not rdh:
                        f.write(
                            b'<img class="nothing" src="/ed/c97/img2/nothing.png" />'
                        )

                    for v in rdh:
                        # romaji = romkan.to_hepburn(v['cirnam2'])
                        romaji = jaconv.h2z(v["cirnam2"])
                        # romaji = jaconv.kata2hira(romaji)
                        # romaji = jaconv.kana2alphabet(romaji)
                        romaji = romkan.to_roma(romaji)
                        # f.write(u'<tr><td>{}</td><td>{}</td></tr>'.format(v['cirnam1'], romaji).encode('utf-8'))
                        loc_ckanji_map["{}{}".format(nday, v["loc"])] = v["cirnam1"]
                        loc_cromaji_map["{}{}".format(nday, v["loc"])] = romaji
                        urls = []
                        for k in ["urlmain", "urltwit", "urlpxiv"]:
                            if k in v and len(v[k]) > 0:
                                url = html.escape(v[k])
                                urls.append(
                                    '<span class="url">{}: <a href="{}">{}</a></span>'.format(
                                        k[3:], url, url
                                    )
                                )

                        f.write(
                            u'<div class="c"><img src="/ed/c97/img/{}.png"><h1>{}</h1><h2>{} | {}</h2><span class="genre">{}</span>{}</div>\n'.format(
                                v["imageid"],
                                html.escape(v["cirnam1"]),
                                v["loc"],
                                romaji,
                                genres_en[v["ngenre"]],
                                "\n".join(urls),
                            ).encode(
                                "utf-8"
                            )
                        )

    with open("csv2html-basic-table.html", "rb") as f:
        head = f.read()

    for nday in range(1, 4):
        with open("../html/sorted-by-location/day{}.html".format(nday), "wb") as f:
            f.write(head)
            for k, v in sorted(loc_ckanji_map.items()):
                if k[0] != str(nday):
                    continue

                f.write(
                    "<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(
                        loc_cromaji_map[k], k, v
                    ).encode("utf-8")
                )
            f.write(b"</table></body></html>")

    with open("../html/sorted-by-circle-romaji.html", "wb") as f:
        f.write(head)
        for k, v in sorted(loc_cromaji_map.items(), key=operator.itemgetter(1)):
            f.write(
                "<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(
                    loc_cromaji_map[k], k, loc_ckanji_map[k]
                ).encode("utf-8")
            )
        f.write(b"</table></body></html>")

    with open("../html/sorted-by-circle-kanji.html", "wb") as f:
        f.write(head)
        for k, v in sorted(loc_ckanji_map.items(), key=operator.itemgetter(1)):
            f.write(
                "<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(
                    loc_cromaji_map[k], k, loc_ckanji_map[k]
                ).encode("utf-8")
            )
        f.write(b"</table></body></html>")

    # for v in r:
    # 	print(v['day'])


main()
