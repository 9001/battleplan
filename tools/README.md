# files in this folder
* ccc-select-all.ahk  
  autohotkey script which selects every booth inside CCC (the comiket dvd application); do that before using the in-app export feature to get a csv file

* csv2html-03-json.py
  takes the above csv file and creates json files (the circle databases, one each day) for battleplan

* sjisclip.py
  after copying some text from CCC, run this to unbreak it

# why autohotkey though
the sqlite2 database on the CCC DVD is trivially loadable however it becomes outdated as the comiket crew releases patches and updates for the circle list that ships on the DVD

idk where the update data is stored and it doesn't appear in the exported csv file either but that was the rationale anyhow
