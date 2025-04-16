#!/usr/bin/env python3
"""
MangoUI - The basicest MangoHUD config editor (v0.2, Python version)
Original idea from the Perl script.

Requirements:
  - PyGObject (GTK+3)
  - Python 3.x
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib
import os
import re
import io

# Global variables (set defaults similar to the Perl script)
prog_name = "(py) MangoUI"
default_path = os.path.expanduser("~/.config/MangoHud")
file_path = os.path.join(default_path, "MangoHud.conf")
icon_path = "/tmp/minimango.png"  # Ensure this file exists for an icon, or update the path as needed.

# Global storage for configuration options.
# Each option is stored as a dict with keys:
#   idx: line number (1-indexed)
#   key: parsed key
#   value: parsed value
#   id: type identifier ("emt", "ioo", "iov", "aoo", "aov", "com", or "und")
#   line: the original full line text
options = []

class MangoUI(Gtk.Window):
    def __init__(self):
        super().__init__(title=f"{prog_name} - MangoHud Config Editor")
        self.set_border_width(10)
        self.set_default_size(1360, 768)
        try:
            self.set_icon_from_file(icon_path)
        except Exception as e:
            print(f"Warning: Couldn't load icon from {icon_path}: {e}")

        # Main vertical box layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)

        # --- New Search Bar ---
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search (regex)...")
        self.search_entry.connect("changed", self.on_search_changed)
        vbox.pack_start(self.search_entry, False, False, 0)

        # --- Scrolled Window and FlowBox ---
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.scrolled_window, True, True, 0)

        # Using a FlowBox for one-column layout (similar to GTK3 FlowBox in Perl)
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_max_children_per_line(1)
        self.flowbox.set_min_children_per_line(1)
        self.flowbox.set_valign(Gtk.Align.START)
        self.scrolled_window.add(self.flowbox)

        # --- Buttons ---
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        vbox.pack_start(button_box, False, False, 0)

        load_button = Gtk.Button(label="Load Config")
        load_button.connect("clicked", self.new_config)
        button_box.pack_start(load_button, False, False, 0)

        reload_button = Gtk.Button(label="Reload Config")
        reload_button.connect("clicked", self.reload_config)
        button_box.pack_start(reload_button, False, False, 0)

        # Show the window and load the config on startup
        self.show_all()
        self.load_config()

    def on_search_changed(self, widget):
        self.display_options()

    def load_config(self):
        global file_path, options

        # If file_path is not set, open a file chooser dialog
        if not file_path or file_path == "":
            dialog = Gtk.FileChooserDialog(
                title="Select a file",
                parent=self,
                action=Gtk.FileChooserAction.OPEN)
            dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                               Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
            dialog.set_current_folder(default_path)

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_path = dialog.get_filename()
                print("Selected file:", file_path)
            else:
                print("File selection canceled.")
                dialog.destroy()
                return
            dialog.destroy()

            if file_path and not file_path.endswith(".conf"):
                print("Invalid file selected. Please select a .conf file.")
                file_path = ""
                return

        options = []
        self.clear_flowbox()

        try:
            with io.open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        self.set_title(f"{prog_name} - MangoHud Config Editor [{file_path}]")
        idx = 1
        for line in lines:
            line = line.rstrip('\n')
            if re.match(r'^\s*$', line):
                options.append({'idx': idx, 'key': "", 'value': "", 'id': self.id_line(line), 'line': line})
            elif re.match(r'^\s*#+\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\./:;,\s\'"\\\}\{\]\[-]+)?\s*$', line):
                m = re.match(r'^\s*#+\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\./:;,\s\'"\\\}\{\]\[-]+)?\s*$', line)
                key, value = m.group(1), m.group(2)
                options.append({'idx': idx, 'key': key, 'value': value, 'id': self.id_line(line), 'line': line})
            elif re.match(r'^\s*#+\s*([0-9a-zA-Z_-]+)\s*$', line):
                m = re.match(r'^\s*#+\s*([0-9a-zA-Z_-]+)\s*$', line)
                key = m.group(1)
                options.append({'idx': idx, 'key': key, 'value': "", 'id': self.id_line(line), 'line': line})
            elif re.match(r'^\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\./:;,\s-]+)?\s*$', line):
                m = re.match(r'^\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\./:;,\s-]+)?\s*$', line)
                key, value = m.group(1), m.group(2)
                options.append({'idx': idx, 'key': key, 'value': value, 'id': self.id_line(line), 'line': line})
            elif re.match(r'^\s*([0-9a-zA-Z_-]+)\s*$', line):
                m = re.match(r'^\s*([0-9a-zA-Z_-]+)\s*$', line)
                key = m.group(1)
                options.append({'idx': idx, 'key': key, 'value': "", 'id': self.id_line(line), 'line': line})
            elif re.match(r'^\s*#+', line):
                options.append({'idx': idx, 'key': "#", 'value': "", 'id': self.id_line(line), 'line': line})
            else:
                options.append({'idx': idx, 'key': "#", 'value': "", 'id': self.id_line(line), 'line': line})
            idx += 1

        self.display_options()

    def id_line(self, input_line):
        """Determine the type of a line."""
        if input_line is None:
            return "und"
        elif re.match(r'^\s*$', input_line):
            return "emt"
        elif re.match(r'^\s*#+\s*([0-9a-zA-Z_-]+)\s*$', input_line):
            return "ioo"
        elif re.match(r'^\s*#+\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\.,\/:;\'"\\\}\{\]\[-]+)?\s*$', input_line):
            return "iov"
        elif re.match(r'^\s*([0-9a-zA-Z_-]+)\s*$', input_line):
            return "aoo"
        elif re.match(r'^\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\.,\/:;\'"\\\}\{\]\[-]+)?\s*$', input_line):
            return "aov"
        elif re.match(r'^\s*#+.*$', input_line):
            return "com"
        else:
            return "und"

    def display_options(self):
        """Refresh the display of config options with optional regex filtering."""
        self.clear_flowbox()
        
        rx = None
        regex_text = self.search_entry.get_text()
        if regex_text != "":
            try:
                rx = re.compile(regex_text)
            except re.error:
                rx = None
        
        for opt in options:
            # If a valid regex filter was given, skip lines that don't match.
            if rx and not rx.search(opt['line']):
                continue

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

            # For options that represent editable configuration lines.
            if opt['id'] in ["ioo", "iov", "aoo", "aov"]:
                check_active = True if opt['id'] in ["aoo", "aov"] else False
                cb = Gtk.CheckButton()
                cb.set_active(check_active)
                cb.connect("toggled", self.on_toggle_option, opt['idx'])
                hbox.pack_start(cb, False, False, 0)

                label_text = f"{opt['key']}" if opt['id'] in ["ioo", "aoo"] else f"{opt['key']} = "
                label = Gtk.Label(label=label_text)
                label.set_xalign(0)
                hbox.pack_start(label, False, False, 0)

                if opt['id'] in ["iov", "aov"]:
                    entry = Gtk.Entry()
                    entry.set_text(opt['value'] if opt['value'] is not None else "")
                    entry.connect("focus-out-event", self.on_value_update, opt['idx'])
                    hbox.pack_start(entry, True, True, 0)
            elif opt['id'] == "com":
                # For comment lines, display the text using monospace.
                # Escape the text for proper markup rendering.
                safe_text = GLib.markup_escape_text(opt['line'])
                label = Gtk.Label()
                label.set_markup(f"<span font='monospace'>{safe_text}</span>")
                label.set_xalign(0)
                label.set_line_wrap(True)
                hbox.pack_start(label, True, True, 0)
            else:
                # For empty or unmatched lines, skip creating a widget.
                continue

            self.flowbox.add(hbox)
        self.flowbox.show_all()

    def clear_flowbox(self):
        for child in self.flowbox.get_children():
            self.flowbox.remove(child)

    def on_toggle_option(self, widget, idx):
        """Toggle the active state of an option. (Switch 'aoo' and 'ioo', 'aov' and 'iov'.)"""
        for opt in options:
            if opt['idx'] == idx:
                if opt['id'].startswith("a"):
                    opt['id'] = "i" + opt['id'][1:]
                    print(f"toggled off [{idx}]: [{opt['key']}] [{opt.get('value','')}]")
                elif opt['id'].startswith("i"):
                    opt['id'] = "a" + opt['id'][1:]
                    print(f"toggled on [{idx}]: [{opt['key']}] [{opt.get('value','')}]")
        self.save_config()

    def on_value_update(self, widget, event, idx):
        new_value = widget.get_text()
        for opt in options:
            if opt['idx'] == idx:
                if opt['value'] == new_value:
                    print(f"unchanged [{idx}]: [{opt['key']}] is [{opt['value']}]")
                    return
                else:
                    opt['value'] = new_value
                    print(f"changed [{idx}]: [{opt['key']}] to [{opt['value']}]")
        self.save_config()

    def save_config(self):
        global file_path
        if not file_path:
            return
        try:
            with io.open(file_path, "w", encoding="utf-8") as f:
                for opt in options:
                    if opt['id'] == "emt":
                        f.write(opt['line'] + "\n")
                    elif opt['id'] == "ioo":
                        f.write(f"# {opt['key']}\n")
                    elif opt['id'] == "iov":
                        f.write(f"# {opt['key']}={opt['value']}\n")
                    elif opt['id'] == "aoo":
                        f.write(f"{opt['key']}\n")
                    elif opt['id'] == "aov":
                        f.write(f"{opt['key']}={opt['value']}\n")
                    elif opt['id'] == "com":
                        f.write(opt['line'] + "\n")
                    else:
                        f.write(f"# unmatched line: [{opt['line']}]\n")
            print(f"saved {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def reload_config(self, widget):
        if file_path:
            self.load_config()

    def new_config(self, widget):
        global file_path
        file_path = ""
        self.load_config()


if __name__ == "__main__":
    app = MangoUI()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()

