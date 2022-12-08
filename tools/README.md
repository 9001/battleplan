# from circle.ms / webcata
currently the only data source so use this

## CMS: step by step
* grab `genres.json` from https://webcatalog-free.circle.ms/Map/GetGenrePosition2
  * use it to discover halls / days; e123 e456 w12 / 1 2
* grab `map-{hall}.json` from https://webcatalog-free.circle.ms/Map/GetMapDataFromExcel?hall=$hall
* grab `booth-{d}-{hall}.json` from https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day$d&hall=$hall
* magically obtain the circle info
* preprocess pics
  ```
  rm -rf i; mkdir i; cp -pR 1/*/*.png 2/*/*.png i/
  find i -iname '*.png' | while IFS= read -r x; do convert $x -shave 7x7 +repage $x.png; mv $x.png $x; pngquant --strip --nofs --quality 50 --speed 1 --skip-if-larger - <$x >tf; [ -s tf ] && mv tf $x; done
  ```
* ```
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

