# html-commenter-plugin
sublime plugin that adds the bootstrap / ep - classes of a div-element as comment to the closing tags

adds options to the tools menu points allowing you to automatically run the script on save or trigger the plugin manually

# Keybindings
if you want to add a keybinding paste (and adapt) the following line to keybindings:
{"keys": ["shift+ctrl+c"], "command": "add_comments"}

# Installation:
to install the plugin [download](https://codeload.github.com/ep-friedel/sublime_html-commenter-plugin/zip/master) the folder into your Sublime/Packages folder ( Sublime > Preferences > Browse Packages )

Alternative:
The plugin is also available through Sublime Package Contol. Open the Command Palette (Command+Shift+P on OS X, Control+Shift+P on Linux/Windows) and choose "Package Control: Add repository". Enter following url:
```
https://raw.githubusercontent.com/ep-friedel/sublime_html-commenter-plugin/master/Repositroy.json
```
Now you can install the plugin:
Bring up the Command Palette (Command+Shift+P on OS X, Control+Shift+P on Linux/Windows).
Select "Package Control: Install Package", wait while Package Control fetches the latest package list.
Search for "HTML-Commenter".
The advantage of using this method is that Package Control will automatically keep the plugins up to date with the latest version.
