# MangoUI
The basicest MangoHUD config editor
------------------------------------
The GUI simply displays the MangoHUD config for convenient editing through check- and textboxes.
An example config file is provided.

Rules:
- you may set the default folder for load file, at the top of the script in:
- `our $default_path = "/home/".getpwuid($>)."/.config/MangoHud/";  # "load" dialog default location`
- you may set the default file to load on startup, at the top of the script in:
- `our $file_path = "/home/".getpwuid($>)."/.config/MangoHud/MangoHud.conf"; # default file to load upon startup`
- most of what the script does and sees is printed to the terminal. So if problems arise, running from terminal may provide extra info.

- any line with more than exactly one "#" is considered a comment
- lines identified as either option on/off or option=value are presented as lines with chackboxes and also textboxes where apropriate.
- the checkbox adds/removes a "#" to enable/disable an option
- the textbox sets an options value

![image](https://github.com/user-attachments/assets/1abdc47c-d58d-4ec7-99c3-0dc12f37301d)
