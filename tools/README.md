# files in this folder
* `ccc-select-all.ahk`  
  autohotkey script which selects every booth inside CCC (the comiket dvd application); do that before using the in-app export feature to get a csv file

* `csv2html-03-json.py`  
  takes the above csv file and creates json files (the circle databases, one each day) for battleplan

* `sjisclip.py`  
  after copying some text from CCC, run this to unbreak it

# autohotkey??
the sqlite2 database on the CCC DVD is trivially decodable, and also contains additional convenient info such as the genre id => genre title mapping... however for some reason CCC does not update the database file with corrected info (circle names mostly) when you download update patches from the comiket crew

idk where the update data is stored, so since there was no time to research further this felt like a good idea at the time. However! The update data doesn't seem to appear in the exported csv file either so ┐(ﾟ∀ﾟ)┌

`// todo: just grab data from the db next time`
