# from circle.ms / webcata
currently the only data source so use this

## CMS: step by step

* grab `genres.json` from https://webcatalog-free.circle.ms/Map/GetGenrePosition2
  * use it to discover halls / days; e123 e456 w12 / 1 2  
    ```bash
    jq . <GetGenrePosition2.json | sort | uniq | grep -E '"(hall|day)"'
    ```

* grab `map-{hall}.json` from https://webcatalog-free.circle.ms/Map/GetMapDataFromExcel?hall=$hall  
  ```bash
  for hall in e123 e456 e7 w12; do curl -o map-$hall.json "https://webcatalog-free.circle.ms/Map/GetMapDataFromExcel?hall=$hall" ⋯; done
  ```

* grab `booth-{d}-{hall}.json` from https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day$d&hall=$hall  
  ```bash
  for d in 1 2; do for hall in e123 e456 e7 w12; do curl -o booth-$d-$hall.json "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day$d&hall=$hall" ⋯; done; done
  ```

* magically obtain the circle info; something like:
  ```bash
  mkdir i o; cd i
  jq . < booth-2-e123.json | grep A76a -A2  # wid:17313948 id:10073981 (wid=Id, id=CircleId)
  for f in ../booth-*; do jq '.[].wid' < $f; done | sort | uniq | sed -r 's#(.*)#https://webcatalog-free.circle.ms/Circle/\1/DetailJson#' | wget --header='Cookie: ⋯' --post-data '' -nv -i-
  tar -c . | zstd --long=31 -T0 -9 >../v1.tzst  # backup just in case
  # split files into 4 subfolders to parallelize a bit
  mkdir {1..4}; n=0; find -type f -maxdepth 1 | while IFS= read -r f; do n=$((n+1)); [ $n -gt 4 ] && n=1; mv -v -- "$f" $n/; done
  for d in {1..4}; do (cd $d && find -name DetailJson\* | while IFS= read -r f; do mv -nv $f $(jq .Id $f).json; done) & done; wait
  for d in {1..4}; do (cd $d && find -name \*.json | while IFS= read -r f; do jq -r '.WebCircleCutUrls[0] // .CircleCutUrls[0], .WebCircleCutUrls[1] // .CircleCutUrls[1]' $f; done | grep -vE ^null | sed -r 's#^#https://webcatalog-free.circle.ms#' | uniq | tee thumbs.txt) & done; wait
  cat {1..4}/thumbs.txt | sort | uniq > thumbs.txt
  cat thumbs.txt | wget --header='Cookie: ⋯'  -nv -i- 2>&1 | tee thumbs.log
  tar -c . | zstd --long=31 -T0 -9 >../v2.tzst  # backup just in case
  cat thumbs.log | awk -F/ '/CachedImage.* -> "/{v=$NF;sub(/[^"]+"/,"",v);sub(/".*/,"",v);print$6" "v}' | while read wid fn; do mv -vn "$fn" "../o/$wid.webm"; done
  ```
  * heads up -- conjoined booths have both pics in both booths, so look at the URL to decide which goes where
  * and sometimes there's mistakes in the circlems data with the same wid being used for multiple pics, easy to spot since there's stray files in the folder after the final rename step above,  
    ```
    https://webcatalog-free.circle.ms/Spa/CachedImage/18004151/1/866f046e-b11d-4c1e-9206-d5ca5a5234f4/3903477661565
    https://webcatalog-free.circle.ms/Spa/CachedImage/18004152/1/279c0236-6bdd-41b7-a589-64b1fe396fcf/3903477661893
    https://webcatalog-free.circle.ms/Spa/CachedImage/18004152/2/4aa5f87c-3824-41ac-9a01-08dbe1bb066c/3908605552869
    https://webcatalog-free.circle.ms/Spa/CachedImage/18004154/2/0186c618-4c48-476b-e405-08db97daf671/3901101511702
    ```
    just fix it by renaming `3908605552869` to `../o/18004153.png` which they probably will in the next update

* install kanji-hiragana-romaji translator
  ```bash
  yum install mecab-devel
  python3 -m pip install --user -U fugashi[unidic] cutlet
  python3 -m unidic download
  ```

* `./cms2json.py`

* `tar -c i | zstd -T0 -9 > i.tzst`

----

# from the DVD / CCC
there used to be an official dvd catalog with an sqlite2 database on it

**none of the below is relevant anymore**

## DVD: the tools
* `ccc-select-all.ahk`  
  autohotkey script which selects every booth inside CCC (the comiket dvd application); do that before using the in-app export feature to get a csv file

* `csv2html-03-json.py`  
  takes the above csv file and creates json files (the circle databases, one each day) for battleplan

* `sjisclip.py`  
  after copying some text from CCC, run this to unbreak it

### autohotkey??
the sqlite2 database on the CCC DVD is trivially decodable, and also contains additional convenient info such as the genre id => genre title mapping... however for some reason CCC does not update the database file with corrected info (circle names mostly) when you download update patches from the comiket crew

idk where the update data is stored, so since there was no time to research further this felt like a good idea at the time. However! The update data doesn't seem to appear in the exported csv file either so ┐(ﾟ∀ﾟ)┌

`// todo: just grab data from the db next time`

## DVD: step by step

    iconv -f ms932//TRANSLIT -t utf8//IGNORE < 新規チェックリスト.csv > the.csv
    python3 -m venv ~/pe/ve.battleplan/
    . ~/pe/ve.battleplan/bin/activate
    pip install romkan jaconv
    ./csv2html-03-json.py the.csv

## DVD: the experimental stuff

`xor.py` and `db2json.py` extracts data straight from the comiket dvd, replacing csv/autohotkey

it doesn't work at all yet since drawing the map was non-trivial (relative coordinates)

for now you can use xor.py to get the genre list:

    ./xor.py ccatalog97.db > sqlite2.db
    ~/pe/sqlite2/bin/sqlite sqlite2.db .dump > sql.sjis
    iconv -f ms932//TRANSLIT -t utf8//IGNORE < sql.sjis | tee sql.utf8 | sqlite3 sqlite3.db
    
    sqlite3 sqlite3.db '.tables'
    sqlite3 sqlite3.db '.schema ComiketGenre'
    sqlite3 sqlite3.db 'select code, name from ComiketGenre order by code asc'

