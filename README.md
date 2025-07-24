# MangoUI
The basicest MangoHUD config editor
------------------------------------
![image](https://github.com/user-attachments/assets/c1fa7f16-0f1c-4085-bbd1-505f27c4d3c8)
------------------------------------
### Overview:
The GUI simply displays the MangoHUD config for convenient editing through check- and textboxes.<br>
An example config file is provided.

------------------------------------
### How to use:
- you may set the default folder for load file, at the top of the script in:<br>`our $default_path = $userhome."/.config/MangoHud/";           # "load" dialog default location`
- you may set the default file to load on startup, at the top of the script in:<br>`our $file_path = $userhome."/.config/MangoHud/MangoHud.conf"; # default file to load upon startup`
- change stuff and see the results immediately in mangohud! ;)
- most of what the script does and sees is printed to the terminal. So if problems arise, running from terminal may provide extra info.
------------------------------------
#### What it does:
- it reads the config file, line by line, and presents each relevant line in the GUI. (see: "Known Line Types" below)
- lines identified as either "option" or "option+value" are presented as "lines with checkboxes" and "lines with check+textboxes" respectively.
- the checkbox adds/removes "#", from the start of the line, to disable/enable an option.
- the textbox sets an options value.
- comments are shown as text lines between GUI elements.
- empty lines are not shown.
------------------------------------
### Known Line types:
- `emt` = empty line
- `com` = comment<br>any line with more than exactly one `#` is considered a comment.
- `ioo` = inactive option
- `iov` = inactive option+value
- `aoo` = active option
- `aov` = active option+value
- `und` = lines, unmatched by any regex, likely a bug. please report.
