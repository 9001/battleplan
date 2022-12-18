#!/usr/bin/env python3
# coding: utf-8

import cutlet
import json
import os
import shutil


DAYS = "土 日".split()
HALLS = "e123 e456 w12".split()
CJ = "/home/ed/Downloads/c101/m"
CI = "/home/ed/Downloads/c101/i"


katsu = cutlet.Cutlet()


def gen(nday, cday, hall):
    with open(f"map-{hall}.json", "rb") as f:
        hj = json.loads(f.read().decode("utf-8", "replace"))
    
    with open(f"booth-{nday}-{hall}.json", "rb") as f:
        bj = json.loads(f.read().decode("utf-8", "replace"))

    kan_ew = "東" if hall.startswith("e") else "西"

    hmap = {}  # カ04 -> hall cell
    for ent in hj["mapcsv"]:
        # isLocationLabel:false hall:e123 locate:[19,32] space:カ04 dirbase:下 direction:3
        hmap[ent["space"]] = ent

    ret = []
    for booth, ids in bj.items():
        # カ04a: {wid:16806471 id:10000270}
        x, y = hmap[booth.rstrip("ab")]["locate"]
        
        wid = ids["wid"]
        with open(f"{CJ}/{wid}.json", "rb") as f:
            cj = json.loads(f.read().decode("utf-8", "replace"))

        kanji = cj["Name"]
        romaji = katsu.romaji(kanji)

        urls = []
        ks = "Author WebSite PixivUrl TwitterUrl NiconicoUrl ClipstudioUrl" #Description
        for k in ks.split():
            v = cj.get(k, "")
            if v and v not in urls:
                urls.append(v)

        ent = {
            "loc": f"{nday}{kan_ew}{booth}",
            "kan": kanji,
            "rom": romaji,
            "x": f"{x*10}",
            "y": f"{y*10}",
        }
        if urls:
            ent["url"] = urls
        
        ret.append(ent)
        po = f"i/{ent['loc']}.png"
        if not os.path.exists(po):
            pi = f"{CI}/{ids['wid']}.png"
            shutil.copy2(pi, po)
    
    return ret


def main():
    for nday, cday in enumerate(DAYS, 1):
        print("writing day {}".format(cday))
        ret = []
        for hall in HALLS:
            ret.extend(gen(nday, cday, hall))
    
        with open(f"lkrxy{nday}.json", "wb") as f:
            f.write(json.dumps(ret).encode("utf-8"))

    # create ROWS for the webapp
    for hall in HALLS:
        with open(f"map-{hall}.json", "rb") as f:
            hj = json.loads(f.read().decode("utf-8", "replace"))
        
        rows = {}
        for cell in hj["mapcsv"]:
            if cell["isLocationLabel"]:
                continue

            # split top/bottom half of west (top-lowest = 28, bottom-lowest = 58)
            rows[cell["space"][:1]] = cell["locate"][0] - (9001 if cell["locate"][1] > 40 else 0)

        print(hall)
        print("".join([k for k,_ in sorted(rows.items(), key=lambda x: -x[1])]))


if __name__ == "__main__":
    main()


"""
jq -r <map-e123.json '.mapcsv[] | "\(.dirbase) \(.direction)"' | sort | uniq -c | sort -n
    121 null 5
    288 左 2
    339 右 4
    648 上 1
    648 下 3

jq -r <map-w12.json '.mapcsv[] | "\(.dirbase) \(.direction)"' | sort | uniq -c | sort -n
     12 右← 4
     12 左← 2
    102 null 5
    211 右 4
    211 左 2
    406 上 1
    426 下 3

jq -r <map-w12.json '.mapcsv[] | select(.dirbase=="右←") | .space' | sort | tr '\n' ' '
あ38 あ39 あ40 あ43 あ44 あ45 あ46 あ47 あ48 あ51 あ52 あ53 
# あ01..15 wall left2right
# あ21..37 wall bottom2top
# あ38..53 wall right2left

jq -r <map-w12.json '.mapcsv[] | select(.dirbase=="左←") | .space' | sort | tr '\n' ' '
め38 め39 め40 め43 め44 め45 め46 め47 め48 め51 め52 め53 
# same but mirrored (w1 is left-side)
# め01..15 wall right2left
# め21..37 wall bottom2top
# め38..53 wall left2right
"""
