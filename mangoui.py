#!/usr/bin/env python3
"""
mangoui.py – Python 3 + PyGObject port of mangoui.pl [written by ChatGPT and edited by mod@benjicom]
Exact replication of parsing, debug output, GUI behavior, and saving.

^ this is what chatgpt thinks XD ^
 it did an okay job, but it totally chokes on the large base64 blob when trying to generate anything
 it also missed some points, like skipping empty lines and differently colored linenumbers.
 but overall pretty impressive [also, I added the by-line]

"""

import gi
import os
import re
import io
import base64

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

# Globals
prog_name   = "MangoUI"
default_path = os.path.expanduser("~/.config/MangoHud")
file_path   = os.path.join(default_path, "MangoHud.conf")
icon_path   = "/tmp/minimango.png"
icon_base64 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA0GVYSWZJSSoACAAAAAoAAAEEAAEAAAAgAAAAAQEEAAEAAAAgAAAAAgEDAAMAAACGAAAAEgEDAAEAAAABAAAAGgEFAAEAAACMAAAAGwEFAAEAAACUAAAAKAEDAAEAAAACAAAAMQECAA0AAACcAAAAMgECABQAAACqAAAAaYcEAAEAAAC+AAAAAAAAAAgACAAIAEgAAAABAAAASAAAAAEAAABHSU1QIDIuMTAuMzgAADIwMjQ6MTA6MDggMTY6MDA6NDEAAQABoAMAAQAAAAEAAAAAAAAAjjR8+wAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfU8VSWgTtIOKQoTrZwQ/EsVahCBVCrdCqg8mlX9CkIUlxcRRcCw5+LFYdXJx1dXAVBMEPEGcHJ0UXKfF/SaFFrAfH/Xh373H3DhAaFaZZPXFA020znUyI2dyq2PeKIAIIYwATMrOMOUlKoev4uoePr3cxntX93J8jrOYtBvhE4jgzTJt4g3hm0zY47xNHWElWic+Jx026IPEj1xWP3zgXXRZ4ZsTMpOeJI8RisYOVDmYlUyOeJo6qmk75QtZjlfMWZ61SY6178heG8vrKMtdpjiCJRSxBgggFNZRRgY0YrTopFtK0n+jiH3b9ErkUcpXByLGAKjTIrh/8D353axWmJr2kUALofXGcj1Ggbxdo1h3n+9hxmieA/xm40tv+agOY/SS93taiR0D/NnBx3daUPeByBxh6MmRTdiU/TaFQAN7P6JtywOAtEFzzemvt4/QByFBXqRvg4BAYK1L2epd3Bzp7+/dMq78fkl1ys0DKXsYAAA14aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOmQ5MzM5NmI5LWMzYWUtNGYxYi04YTFjLTNkMDU5MzRkMjgzYSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5ODhlNDg5YS0wMWRlLTQzZWEtYTc0NC01OGUyMDE3ZjQ2ZWIiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDozMzIzNDFjOC05ZDBlLTQzMzYtYWEyMS0zODdkNDQ3N2RiNzEiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJMaW51eCIKICAgR0lNUDpUaW1lU3RhbXA9IjE3MjgzOTYwNDI3MjIyMDYiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zOCIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjQ6MTA6MDhUMTY6MDA6NDErMDI6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI0OjEwOjA4VDE2OjAwOjQxKzAyOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MjdkZDI1OGEtZDJjMC00MDU2LTlkNzgtZjQ4N2I3MzY3ZTE3IgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKExpbnV4KSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyNC0xMC0wOFQxNjowMDo0MiswMjowMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz5mAzoFAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH6AoIDgAqaOLn3QAABZZJREFUWMO9lltsHdUVhr+198yci89x7GAcU0KUNoGqlDiSE2KjKAUiJKSqfeGhUkVVaJAqtarUNiGOHC5BihTASQBBqsIjVyEBD1SpRAEhXkgUYlooLQohTZVLCVGx8eXYPufM7L14mOMTH9txEqMwTzOavdf/r9u/luUyP61bWJ7fyJbgRvmwepDyzP/2coIv/rW0soS9Jsd1wLKWdVe8Wzow2XDGXFb3v6O/kYA2BTVNdJd1cO3MI5eNQPEeaZOQm1XSbwHI0/OtEbAFXeEtIjVs7/EiXPmtEfAJ4wLKVAQMBuXszHPBxRg7uMWEbaFfW4zoCg3XKrQbQ1Gg6hzDCMfHqnw86Di49lH+D1CMzdHJih/UDIuNYMXh3TjvzLQt8wEf6WNlS8RdOcOPw5A2o3gHWAUn5+5L7T1xlMuOgYmYFyYC+2bPmOsO29nhEhId5qmRPbxxUQQO/V4WLW/WrdmIn4WGCEHlQmHS1JgDEUVLMf8YLvNQT0JePGcGH+fER5tZ1lZgfdayQqEQO+JZKfi0l9XtTbovsiwVQeYCV60BCnhQVbyAMSAioIA15OOE0aG9/PPYfaxvfohH8wFrBQyS3g+g2mD7+HZ+1Jbn6UDIi6BeMQIqgk4/F6ehfmvC8c5ohSMSU40iMvmA6zIBtyhcdbIkv1WV0tK8f7A5x50ovppwwsFHznMMQ7ma4OsEPttOZ3uOF0NDQaYlx2vaKTXHdKzKgS8n6Pvhbk7Ol5E3Npmwa6l/pinDrSLIaJnXTmrh3nU7SzqrDY/2SlNrhr2RpSjSWBlG8CjeKwxX2X983PzqQuAATfko8cqwpJnSQsBPr0hKcythMdBNOcP31OPnMiYgE44PTg2ZrTft8dWLad0N+8r6eUUerCacUkXEELREPPDB5qBh/piDvVLIZdlkBCMyR1coJI7Jr0ps7X7Kly9FjLr6tVRyvApgBZMNuaElm9zcQGBJqBsjwyKZo89U02If87z0/d0cX4giVhP+haamDJhiwB0NBAqWHgSjMlsVFEg88eAkzy1UkkPF+1oFYyCwbBj4g8nUCRjL9ee7LCBlx3ud/ZxYKAEJWCZ1sYTAUsgG/uppRU77+QTZg45WePabDKVMwO3TJrJakChg8bkICJkpZavLjSKqmPGYgRFy7y4U/ONeOrOW7tRizbqiZtoMNk45bbRRblWQcsLnZ8fZvObhSV0I+ECvia4qsDMQ7FT8lbQSR6p8WSfgHZ+oAZ2SOoVywpmhCr/s3M2phXq/JOO35SyrZpZE7CiFyBd1AqPKIXw9QBJ7yv8rcffKXXy2EODDf2qR0/fzu5aIu0UxOmPyJp4DnXu0rifBRCxvl0MdyltaSb1/e1U/RxYC/v4WE139xfADi3L8QiR1Sj1T8w8FnYh5vUEHOh/RUjnmea/ggEBYdnizDS4V/Ng2ulYU/WvNGe40NXdFUGPTtHpFJ2M+HRmzb81aSP6+TZquyepfchlWGkVLFf56tsyOVf3nimXOVW2ryXRk/IaC5efZiFsFJEjni9d64yE1QUtOT3LX9bt4b86N6GgfnR05Xg4sORRNHKWq528lx+HY8R9V4pwSaMQ11vLdrPIDY+mOLM1Gzr/a+bQB9asKf166k/55V7ITfdzWmuPJwJL3oEYBgxFFVUElXYYsiK81jUi6tMzUcF/Tfqf4kSqvnNWwr2tn7C+4E568j3XNGfZlAjrU4+RSF/fabuhBEk+1VOGZMz54Ys2uxJ1H7mc/n9zLlW15tucDfmINgRfESMOMmtOW1zRqNSE7MjrJjuWPcGjeWTHfz3/3sXpxxD15y8bI0jTtlkwjU7eROJKK48PRhOfPjNv96x937oLD6qL6+49S7MhrT2BZE1quFaHDCiGeJIFRVf5bSXh/aIKB1Y9dmnp+DZ8IS9977RoAAAAAAElFTkSuQmCC'

# Storage for parsed lines:
# each entry is a dict with keys: idx, key, value, id, line
options = []


class MangoUI(Gtk.Window):
    def __init__(self):
        super().__init__(title=f"{prog_name} - MangoHud Config Editor")
        self.set_border_width(10)
        self.set_default_size(1360, 768)

        with open(icon_path, "wb") as f:
            f.write(base64.b64decode(icon_base64))
        self.set_icon_from_file(icon_path)
        try:
            self.set_icon_from_file(icon_path)
        except Exception as e:
            print(f"Warning: cannot load icon: {e}")

        # Vertical container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)

        # Search entry
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search (regex)...")
        self.search_entry.connect("changed", lambda e: self.display_options())
        vbox.pack_start(self.search_entry, False, False, 0)

        # Scrolled window + ListBox
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.scrolled, True, True, 0)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.scrolled.add(self.listbox)

        # Button row
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        vbox.pack_start(btn_box, False, False, 0)

        load_btn = Gtk.Button(label="Load Config")
        load_btn.connect("clicked", lambda b: self.new_config())
        btn_box.pack_start(load_btn, False, False, 0)

        reload_btn = Gtk.Button(label="Reload Config")
        reload_btn.connect("clicked", lambda b: self.reload_config())
        btn_box.pack_start(reload_btn, False, False, 0)

        # Show and load
        self.show_all()
        self.load_config()

    def id_line(self, line: str) -> str:
        if re.match(r'^\s*$', line):
            return "emt"
        if re.match(r'^\s*#+\s*([0-9A-Za-z_-]+)=', line):
            return "iov"
        if re.match(r'^\s*#+\s*([0-9A-Za-z_-]+)\s*$', line):
            return "ioo"
        if re.match(r'^\s*([0-9A-Za-z_-]+)=', line):
            return "aov"
        if re.match(r'^\s*([0-9A-Za-z_-]+)\s*$', line):
            return "aoo"
        if re.match(r'^\s*#+', line):
            return "com"
        return "und"

    def load_config(self):
        global file_path, options
        # choose file if needed
        if not file_path or not os.path.isfile(file_path):
            dlg = Gtk.FileChooserDialog(
                title="Select a file", parent=self,
                action=Gtk.FileChooserAction.OPEN,
                buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OPEN,   Gtk.ResponseType.OK)
            )
            dlg.set_current_folder(default_path)
            resp = dlg.run()
            if resp == Gtk.ResponseType.OK:
                file_path = dlg.get_filename()
            dlg.destroy()
            if not file_path.endswith(".conf"):
                print("Invalid file; must end with .conf")
                file_path = ""
                return

        options.clear()
        self.listbox.foreach(lambda w: self.listbox.remove(w))

        # read & parse
        try:
            with io.open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        self.set_title(f"{prog_name} - MangoHud Config Editor [{file_path}]")
        idx = 1
        for raw in lines:
            line = raw.rstrip("\n")
            lnid = self.id_line(line)
            key = ""
            value = ""
            # extract key/value for options
            m = re.match(r'^\s*#+\s*([0-9A-Za-z_-]+)=?(.*)?', line)
            if not m:
                m = re.match(r'^\s*([0-9A-Za-z_-]+)=?(.*)?', line)
            if m:
                key = m.group(1)
                value = m.group(2) or ""
            options.append({
                "idx": idx,
                "key": key,
                "value": value,
                "id": lnid,
                "line": line
            })
            print(f"(PARSE){lnid}:{line}")
            idx += 1

        self.display_options()

    def display_options(self):
        # clear
        self.listbox.foreach(lambda w: self.listbox.remove(w))

        # compile regex
        pattern = self.search_entry.get_text()
        rx = None
        if pattern:
            try:
                rx = re.compile(pattern)
            except re.error:
                rx = None

        for opt in options:
            if rx and not rx.search(opt["line"]):
                continue

            lnid = opt["id"]
            line = opt["line"]
            key   = opt["key"]
            value = opt["value"]
            idx   = opt["idx"]

            print(f"(DISPLAY){lnid}:[{key}][{line}]")
            if lnid == "emt":
                continue
            # row container
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

            # line number label
            ln_lbl = Gtk.Label()
            text = GLib.markup_escape_text(f"{idx}:")
            ln_lbl.set_markup(f"<span font='monospace' foreground='gray'>{text}</span>")
            ln_lbl.set_xalign(0)
            hbox.pack_start(ln_lbl, False, False, 0)

            if lnid in ("ioo", "aoo"):
                cb = Gtk.CheckButton()
                cb.set_active(lnid == "aoo")
                cb.connect("toggled", self.on_toggle, idx)
                hbox.pack_start(cb, False, False, 0)

                lbl = Gtk.Label(label=key)
                lbl.set_xalign(0)
                lbl.set_hexpand(True)
                hbox.pack_start(lbl, True, True, 0)

            elif lnid in ("iov", "aov"):
                cb = Gtk.CheckButton()
                cb.set_active(lnid == "aov")
                cb.connect("toggled", self.on_toggle, idx)
                hbox.pack_start(cb, False, False, 0)

                lbl = Gtk.Label(label=f"{key} = ")
                lbl.set_xalign(0)
                hbox.pack_start(lbl, False, False, 0)

                entry = Gtk.Entry()
                entry.set_text(value)
                entry.set_alignment(0)
                entry.set_hexpand(True)
                entry.connect("focus-out-event",
                              lambda e, i=idx, w=entry: self.on_value(i, w.get_text()))
                entry.connect("activate",
                              lambda e, i=idx, w=entry: self.on_value(i, w.get_text()))
                hbox.pack_start(entry, True, True, 0)

            elif lnid == "com":
                esc = GLib.markup_escape_text(line)
                lbl = Gtk.Label()
                lbl.set_markup(f"<span font='monospace'>{esc}</span>")
                lbl.set_xalign(0)
                lbl.set_line_wrap(True)
                hbox.pack_start(lbl, True, True, 0)

            # add to listbox
            self.listbox.insert(hbox, -1)

        self.listbox.show_all()

    def on_toggle(self, widget, idx):
        for opt in options:
            if opt["idx"] == idx:
                if opt["id"].startswith("a"):
                    opt["id"] = "i" + opt["id"][1:]
                    print(f"toggled off [{idx}]:[{opt['key']}]")
                else:
                    opt["id"] = "a" + opt["id"][1:]
                    print(f"toggled on  [{idx}]:[{opt['key']}]")
                break
        self.save_config()

    def on_value(self, idx, newval):
        for opt in options:
            if opt["idx"] == idx and opt["value"] != newval:
                opt["value"] = newval
                print(f"changed [{idx}]:[{opt['key']}] to [{newval}]")
                break
        self.save_config()

    def save_config(self):
        global file_path
        if not file_path:
            return
        try:
            with io.open(file_path, "w", encoding="utf-8") as f:
                for opt in options:
                    lnid = opt["id"]
                    line = opt["line"]
                    k    = opt["key"]
                    v    = opt["value"] or ""
                    if lnid == "emt":
                        f.write(line + "\n")
                    elif lnid == "ioo":
                        f.write(f"# {k}\n")
                    elif lnid == "iov":
                        f.write(f"# {k}={v}\n")
                    elif lnid == "aoo":
                        f.write(f"{k}\n")
                    elif lnid == "aov":
                        f.write(f"{k}={v}\n")
                    elif lnid == "com":
                        f.write(line + "\n")
                    else:
                        f.write(line + "\n")
            print(f"saved {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def reload_config(self):
        if file_path:
            self.load_config()

    def new_config(self):
        global file_path
        file_path = ""
        self.load_config()


if __name__ == "__main__":
    app = MangoUI()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()

