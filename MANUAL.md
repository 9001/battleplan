# how to battleplan

The main menu is opened by clicking the top-right blue `=` icon. Some of the items in the menu are also available in the toolbar at the top. A quick summary:
* 📌 opens the shopping list
* 🗺 opens the hall map
* 🔍 opens the search feature
* ⽥ opens the row browser
* ⭕ shows the complete list of circles
* 📂 to restore shopping list from a backup
* 💾 to create a backup of your shopping list
* ⚙️ for settings (table/grid-view, ...)
* 📆 to select which day to work on
* 📲 to download database for the current day


# 📆 `04. IOSYS — Find a Day.flac`

The first time you access bp, it will default to day 2. Choose which day to operate on with the calendar (📆) button in the toolbar or in the main menu.

When you access a new day for the first time, its database must be downloaded. Click download (📲) in the main menu to download the database of the currently selected day.

The comiket organizers may release updates to the database over time, so redownload each day occasionally to stay up to date.


# 🔍 `01. Yonder Voice — SEEKING.flac`

If you want to add a particular circle to your shopping list, you can use the 🔍search view. The default search term will be "stroemer", replace this with a circle name. Search results will be immediately displayed below.

By default, this is displayed as a plaintext list, but you can enable pictures (or change to grid-view) in "settings" 🠞 "configure list view".

Click a search result to modify its shopping list entry (described two sections further down).

By default, the search will scan through circle names in kanji, katakana and romaji. Change this by clicking `(settings)` under the search field. Twitter and pixiv is only searchable for the circles who remembered to mention their account names to the comiket organizers.

If you enable `regex query`, you have to write your searches according to https://www.regular-expressions.info/quickstart.html


# ⽥ `18. onoken — column.flac`

If you know the location of a circle, for example 東ノ25a, use the ⽥row view. You can copy and paste any piece of text which contains a location into the top left textfield which says "paste here" and the circle will be displayed below.

Click a search result to modify its shopping list entry (described in the next section).

Click the ⽥ icon in the toolbar to reset/blank the search field; this will show all the booths in the selected row.

You can click `List rows` to select a row of booths to display. To the left and right are buttons which will take you to the row of booths which are physically located next to the current row. This way you can walk through the comiket hall.


# 🖊 `かめりあ — ‮!الت حقق من ذل‬‎ - !!check this out.flac`

When clicking a search result, or an existing entry in your shopping list, you will see the shopping list editor.

Starting with the colored numpad; this is where you score the circle on a scale from 1 to 9. This will change the color of this circle in the shopping list, on the map, and everywhere else.

The topmost button switches between a green `💚 Set "Purchased"` and an orange `🔔 Set "Must Buy"`, use this button while at comiket to mark this circle as finished. Circles which are marked as *"Purchased"* will appear with a zebra-striped background in all lists, and will be faded down to a dark green on the map.

All of the URLs which the circle provided to the comiket crew are displayed underneath the numpad. You can add your own URLs or notes to this circle using the textbox right below which says *"paste stuff here"*.

Use the `Manage URLs` button to edit or delete any URLs or notes which you have added.

When you change the score of a circle, or its purchased state, you are sent back to the shopping list. If you want to instead see the next circle in your shopping list, this can be configured using the two radio buttons which says "return to list" and "go to next booth".

Finally, at the bottom of the shopping list editor are two pairs of buttons, "navigate shopping list" and "navigate booths". Use these to move to the previous or next circle in your shopping list, or to the previous/next booth in the row.

If you want to filter out circles which you gave a score of less than 7, put 7 in the `min. score` textbox above. The navigation buttons for the shopping list will now skip all circles with low scores.


# 📌 `04. Yogurtbox — スケジュール.flac`

The shopping list displays all the circles you have assigned a score. They are grouped by rows (ア イ ウ エ オ etc.) and the rows appear in the same order that they will be physically in the halls.

As you add circles to your shopping list, an information bar at the top is created. It shows the number of `done` circles (marked as purchased) and `todo` (left to buy), then the number of `todo` circles for each score.

Immediately underneath is a list of all the rows you have circles in. Click a row to jump to its first circle in the shopping list.


# 🗺 `06. めらみぽっぷ — A Sense Of Distance.flac`

The map view draws a map of one comiket hall. Everything in your shopping list will appear on the map in different colors. If you have marked something as purchased, it will be a dark green. Otherwise, the booth will have the same color as in the shopping list, in other words decided by your rating.

Currently the map is not interactive; you can only zoom and pan. Eventually you will be able to tap a location in the map to see which circles are nearby or something.


# 📂💾 `03. Nachi — Turn Back Time.flac`

Please make backups of your shopping list! Do that with the 💾export feature in the main menu. You can then either press the 
💾download button, or select all of the text in the textbox below.

To restore your shopping list, select 📂import in the main menu. Then, click the *"Browse..."* button to select a backup file. You may optionally paste the wall of text in the textbox below, followed by pressing the "📃 text import" button.
