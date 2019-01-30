# battleplan
offline comiket shopping list webapp

**live here:** https://dootnode.org/ed/c95/bp/

maintainers: see the tools folder for a separate readme

# fair warning
this was thrown together in a rush starting one week before comiket, and this definitely shows in the quality of the code

I'd really like to clean this up but my todo-list is already killing me for the next 6 months mengo

# features
* browse booths at comiket
* search for circles
* add booths to your shopping list by rating them from 1-9
* shopping list is color-coded according to score and sorted by rows, same order as in the comiket hall
* draw your shopping list onto the comiket map in realtime, right on your phone
* downloads all the booths to your web browser localStorage (cache) for less data consumption, similarly saves your shopping list to localStorage as well, no dependency on any sort of server
* from the shopping list page: switch an entry between purchased and todo with two taps, or browse the links in the catalog, or add additional links (crossfades) and notes, change rating, etc
* copy an entire tweet into the "paste here" field on the "Show all booths" page to automatically detect the first comiket booth and display it below -- try this example: 2日目(日曜日)東シ-81aにて頒布予定です。
* note: you need to have bp set to the correct day first
* export your shopping list to a json file which can be imported to a laptop or whatever (currently imports will overwrite the current shopping list, a merge feature will be added)
* possible to do all this fully offline by saving the html file and json files to your phone

# feature wishlist
* click the map to show nearby circles on your shopping list

# use it online
* https://dootnode.org/ed/c95/bp/
* each comiket day has its own database of circle locations + URLs, taking roughly 200KB to download
* bp will download the database into your browser cache (LocalStorage) to prevent excessive data usage
* once the website has loaded (and the database has been downloaded at some point), the webapp will no longer need an internet connection until you refresh the browser tab

# use it offline: Android
* install [termux](https://termux.com/)
* to either install or upgrade your offline bp installation, paste the following into your terminal and hit enter:  
  `pkg install -y wget; wget -qO- https://dootnode.org/ed/c95/bp/bp-android.sh | bash`
* to launch bp, paste this and hit enter:  
  `~/bp/run`
* note that the shopping list in your local installation is different from the online version -- use the import/export feature to synchronize them manually

# use it offline: iPhone/iPad
* using safari reading list: open the battleplan website in safari, tap the box with the arrow escaping upwards at the bottom of the screen, "Add to Reading List", and choose to make it available offline. Then tap the book icon at the bottom and select battleplan
* make sure to download all the days before disconnecting from the internet
* to update your offline battleplan installation, open reading list, hit edit, select battleplan, hit delete. Navigate to the battleplan website, download the days, re-add it to reading list
* deleting/re-adding battleplan to the reading list SHOULD not delete your shopping list, but always make backups to be safe

# cheat codes
* to erase your entire shopping list, paste the following in the text import box: `{"x":[]}`

# maintenance forecast
* database files will be available for summerket 2019
