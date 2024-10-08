#!/usr/bin/perl
#
# 2024 mod@benjicom
#
# MangoUI - The basicest MangoHUD config editor
# v0.2
# special tahnks to https://github.com/Skarbrand
# for the 3 column version \o/
#
use strict;
use warnings;
use Gtk3 '-init';
use File::Slurp;
use HTML::Entities;
use MIME::Base64;

our $prog_name = "MangoUI";
# Variables
our $default_path = "/home/".getpwuid($>)."/.config/MangoHud/";  # "load" dialog default location
our $file_path = "/home/".getpwuid($>)."/.config/MangoHud/MangoHud.conf"; # default file to load upon startup
our $icon_path = "/tmp/minimango.png"; # logo, will be unpacked from base64 below
my $base64_image = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA0GVYSWZJSSoACAAAAAoAAAEEAAEAAAAgAAAAAQEEAAEAAAAgAAAAAgEDAAMAAACGAAAAEgEDAAEAAAABAAAAGgEFAAEAAACMAAAAGwEFAAEAAACUAAAAKAEDAAEAAAACAAAAMQECAA0AAACcAAAAMgECABQAAACqAAAAaYcEAAEAAAC+AAAAAAAAAAgACAAIAEgAAAABAAAASAAAAAEAAABHSU1QIDIuMTAuMzgAADIwMjQ6MTA6MDggMTY6MDA6NDEAAQABoAMAAQAAAAEAAAAAAAAAjjR8+wAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfU8VSWgTtIOKQoTrZwQ/EsVahCBVCrdCqg8mlX9CkIUlxcRRcCw5+LFYdXJx1dXAVBMEPEGcHJ0UXKfF/SaFFrAfH/Xh373H3DhAaFaZZPXFA020znUyI2dyq2PeKIAIIYwATMrOMOUlKoev4uoePr3cxntX93J8jrOYtBvhE4jgzTJt4g3hm0zY47xNHWElWic+Jx026IPEj1xWP3zgXXRZ4ZsTMpOeJI8RisYOVDmYlUyOeJo6qmk75QtZjlfMWZ61SY6178heG8vrKMtdpjiCJRSxBgggFNZRRgY0YrTopFtK0n+jiH3b9ErkUcpXByLGAKjTIrh/8D353axWmJr2kUALofXGcj1Ggbxdo1h3n+9hxmieA/xm40tv+agOY/SS93taiR0D/NnBx3daUPeByBxh6MmRTdiU/TaFQAN7P6JtywOAtEFzzemvt4/QByFBXqRvg4BAYK1L2epd3Bzp7+/dMq78fkl1ys0DKXsYAAA14aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOmQ5MzM5NmI5LWMzYWUtNGYxYi04YTFjLTNkMDU5MzRkMjgzYSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5ODhlNDg5YS0wMWRlLTQzZWEtYTc0NC01OGUyMDE3ZjQ2ZWIiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDozMzIzNDFjOC05ZDBlLTQzMzYtYWEyMS0zODdkNDQ3N2RiNzEiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJMaW51eCIKICAgR0lNUDpUaW1lU3RhbXA9IjE3MjgzOTYwNDI3MjIyMDYiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zOCIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjQ6MTA6MDhUMTY6MDA6NDErMDI6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI0OjEwOjA4VDE2OjAwOjQxKzAyOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MjdkZDI1OGEtZDJjMC00MDU2LTlkNzgtZjQ4N2I3MzY3ZTE3IgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKExpbnV4KSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyNC0xMC0wOFQxNjowMDo0MiswMjowMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz5mAzoFAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH6AoIDgAqaOLn3QAABZZJREFUWMO9lltsHdUVhr+198yci89x7GAcU0KUNoGqlDiSE2KjKAUiJKSqfeGhUkVVaJAqtarUNiGOHC5BihTASQBBqsIjVyEBD1SpRAEhXkgUYlooLQohTZVLCVGx8eXYPufM7L14mOMTH9txEqMwTzOavdf/r9u/luUyP61bWJ7fyJbgRvmwepDyzP/2coIv/rW0soS9Jsd1wLKWdVe8Wzow2XDGXFb3v6O/kYA2BTVNdJd1cO3MI5eNQPEeaZOQm1XSbwHI0/OtEbAFXeEtIjVs7/EiXPmtEfAJ4wLKVAQMBuXszHPBxRg7uMWEbaFfW4zoCg3XKrQbQ1Gg6hzDCMfHqnw86Di49lH+D1CMzdHJih/UDIuNYMXh3TjvzLQt8wEf6WNlS8RdOcOPw5A2o3gHWAUn5+5L7T1xlMuOgYmYFyYC+2bPmOsO29nhEhId5qmRPbxxUQQO/V4WLW/WrdmIn4WGCEHlQmHS1JgDEUVLMf8YLvNQT0JePGcGH+fER5tZ1lZgfdayQqEQO+JZKfi0l9XtTbovsiwVQeYCV60BCnhQVbyAMSAioIA15OOE0aG9/PPYfaxvfohH8wFrBQyS3g+g2mD7+HZ+1Jbn6UDIi6BeMQIqgk4/F6ehfmvC8c5ohSMSU40iMvmA6zIBtyhcdbIkv1WV0tK8f7A5x50ovppwwsFHznMMQ7ma4OsEPttOZ3uOF0NDQaYlx2vaKTXHdKzKgS8n6Pvhbk7Ol5E3Npmwa6l/pinDrSLIaJnXTmrh3nU7SzqrDY/2SlNrhr2RpSjSWBlG8CjeKwxX2X983PzqQuAATfko8cqwpJnSQsBPr0hKcythMdBNOcP31OPnMiYgE44PTg2ZrTft8dWLad0N+8r6eUUerCacUkXEELREPPDB5qBh/piDvVLIZdlkBCMyR1coJI7Jr0ps7X7Kly9FjLr6tVRyvApgBZMNuaElm9zcQGBJqBsjwyKZo89U02If87z0/d0cX4giVhP+haamDJhiwB0NBAqWHgSjMlsVFEg88eAkzy1UkkPF+1oFYyCwbBj4g8nUCRjL9ee7LCBlx3ud/ZxYKAEJWCZ1sYTAUsgG/uppRU77+QTZg45WePabDKVMwO3TJrJakChg8bkICJkpZavLjSKqmPGYgRFy7y4U/ONeOrOW7tRizbqiZtoMNk45bbRRblWQcsLnZ8fZvObhSV0I+ECvia4qsDMQ7FT8lbQSR6p8WSfgHZ+oAZ2SOoVywpmhCr/s3M2phXq/JOO35SyrZpZE7CiFyBd1AqPKIXw9QBJ7yv8rcffKXXy2EODDf2qR0/fzu5aIu0UxOmPyJp4DnXu0rifBRCxvl0MdyltaSb1/e1U/RxYC/v4WE139xfADi3L8QiR1Sj1T8w8FnYh5vUEHOh/RUjnmea/ggEBYdnizDS4V/Ng2ulYU/WvNGe40NXdFUGPTtHpFJ2M+HRmzb81aSP6+TZquyepfchlWGkVLFf56tsyOVf3nimXOVW2ryXRk/IaC5efZiFsFJEjni9d64yE1QUtOT3LX9bt4b86N6GgfnR05Xg4sORRNHKWq528lx+HY8R9V4pwSaMQ11vLdrPIDY+mOLM1Gzr/a+bQB9asKf166k/55V7ITfdzWmuPJwJL3oEYBgxFFVUElXYYsiK81jUi6tMzUcF/Tfqf4kSqvnNWwr2tn7C+4E568j3XNGfZlAjrU4+RSF/fabuhBEk+1VOGZMz54Ys2uxJ1H7mc/n9zLlW15tucDfmINgRfESMOMmtOW1zRqNSE7MjrJjuWPcGjeWTHfz3/3sXpxxD15y8bI0jTtlkwjU7eROJKK48PRhOfPjNv96x937oLD6qL6+49S7MhrT2BZE1quFaHDCiGeJIFRVf5bSXh/aIKB1Y9dmnp+DZ8IS9977RoAAAAAAElFTkSuQmCC';
my $decoded_image = decode_base64($base64_image); # Decode the Base64 string and write to $icon_path
write_file($icon_path, $decoded_image);

# Main window
my $mw = Gtk3::Window->new('toplevel');
$mw->set_title("$prog_name - MangoHud Config Editor");
$mw->set_border_width(10);
$mw->set_default_size(1360, 768);
# Load the logo image and set it as the window icon
$mw->set_icon_from_file($icon_path);
$mw->signal_connect(delete_event => sub { Gtk3->main_quit; });

my @options = ();

# VBox for vertical layout
my $vbox = Gtk3::Box->new('vertical', 5);
$mw->add($vbox);

# Create a scrolled window
my $scrolled_window = Gtk3::ScrolledWindow->new();
$scrolled_window->set_policy('automatic', 'automatic');
$vbox->pack_start($scrolled_window, 1, 1, 0);

# Create a frame inside the scrolled window
my $scrollable_frame = Gtk3::FlowBox->new;
$scrolled_window->add($scrollable_frame);
$scrollable_frame->set_min_children_per_line(3);

# Button for loading the configuration
my $load_button = Gtk3::Button->new("Load Config");
$load_button->signal_connect(clicked => \&new_config);
$vbox->pack_start($load_button, 0, 0, 0);

my $reload_button = Gtk3::Button->new("Reload Config");
$reload_button->signal_connect(clicked => \&reload_config);
$vbox->pack_start($reload_button, 0, 0, 0);

# Load config
sub load_config {
#    print "fp:[$file_path]\n";
    if (!$file_path || $file_path eq ""){
        print "Path not set, selecting...\n";
        my $dialog = Gtk3::FileChooserDialog->new(
            "Select a file",
            undef,
            'open',
            'gtk-cancel' => 0,
            'gtk-open'   => 1,
        );
        $dialog->set_current_folder($default_path);
        my $response = $dialog->run();
        print "Dialog response: $response\n";  # Debug line to show the response
        if ($response eq '1') {
            $file_path = $dialog->get_filename();
            print "Selected file: $file_path\n";
        } else {
            print "File selection canceled.\n";
            $dialog->destroy();
            return;  # Exit if no file is selected
        }
        $dialog->destroy();

        # Ensure the selected file has a .conf extension
        if ($file_path && $file_path !~ /\.conf$/) {
            print "Invalid file selected. Please select a .conf file.\n";
            $file_path = "";  # Clear invalid file path
            return;
        }
    }

    return unless $file_path;

    @options = ();
    clear_options_frame();

    # Try to read the file
    my @lines;
    eval {
        @lines = read_file($file_path);
    };
    if ($@) {
        print "Error reading file: $@\n";
        return;
    }
    $mw->set_title("$prog_name - MangoHud Config Editor [$file_path]");
    my $idx = 1;
    foreach my $line (@lines) {
        chomp $line;
        if ($line =~ /^\s*$/) {
            push @options, [$idx, "", "", id_line($line), $line];
        } elsif ($line =~ /^\s*#+\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\.\/:;,'"\\\}\{\]\[\s-]+)?\s*$/) {
            my ($key, $value) = ($1, $2);
            print id_line($line).":$line\n";
            push @options, [$idx, $key, $value, id_line($line), $line];
        } elsif ($line =~ /^\s*#+\s*([0-9a-zA-Z_-]+)\s*$/) {
            my ($key, $value) = ($1, $2);
            print id_line($line).":$line\n";
            push @options, [$idx, $key, $value, id_line($line), $line];
        } elsif ($line =~ /^\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\.\/:;,\s-]+)?\s*$/) {
            my ($key, $value) = ($1, $2);
            print id_line($line).":$line\n";
            push @options, [$idx, $key, $value, id_line($line), $line];
        } elsif ($line =~ /^\s*([0-9a-zA-Z_-]+)\s*$/) {
            my ($key, $value) = ($1, $2);
            print id_line($line).":$line\n";
            push @options, [$idx, $key, "", id_line($line), $line];
        } elsif ($line =~ /^\s*#+/) {
            print id_line($line).":$line\n";
            push @options, [$idx, "#", "", id_line($line), $line];
        } else {
            print id_line($line).":$line\n";
            push @options, [$idx, "#", "", id_line($line), $line];
        }
        $idx += 1;
    }
    display_options();
}

# Display options on the GUI
sub display_options {
    clear_options_frame();  # Clear any existing options
    foreach my $option (@options) {
        my ($idx, $key, $value, $id, $original_line) = @$option;
        #print "$key, $is_on, $value, $original_line";
        if (!defined($original_line)){
          print 'UNDEFINED original_line';
        }
        print("(".caller().")".id_line($original_line).":[$key][$original_line]\n");
        if ($id eq "emt") {
        # empty or space only lines
        } elsif ($id eq "ioo") {
        # inactive option only line
            my $hbox = Gtk3::Box->new('horizontal', 5);
            my $cb = Gtk3::CheckButton->new("");
            $cb->set_active("0");
            $cb->signal_connect(toggled => sub { toggle_option($idx, \$id); });
            $hbox->pack_start($cb, 0, 0, 0);
            my $label = Gtk3::Label->new("$key");
            $hbox->pack_start($label, 0, 0, 0);
            $scrollable_frame->add($hbox);
        } elsif ($id eq "iov") {
        # inactive otion/value line
            my $hbox = Gtk3::Box->new('horizontal', 5);
            my $cb = Gtk3::CheckButton->new("");
            $cb->set_active("0");
            $cb->signal_connect(toggled => sub { toggle_option($idx, \$id); });
            $hbox->pack_start($cb, 0, 0, 0);
            my $label = Gtk3::Label->new("$key = ");
            $hbox->pack_start($label, 0, 0, 0);
            my $entry = Gtk3::Entry->new();# p
            if (defined($value)){
               $entry->set_text("$value");
            }else{
               $entry->set_text("");
            }
            $entry->signal_connect('focus-out-event' => sub { update_value($idx, $entry->get_text); });
            $hbox->pack_start($entry, 1, 1, 0);
            $scrollable_frame->add($hbox);
        } elsif ($id eq "aoo") {
        # active option line
            my $hbox = Gtk3::Box->new('horizontal', 5);
            my $cb = Gtk3::CheckButton->new("");
            $cb->set_active("1");
            $cb->signal_connect(toggled => sub { toggle_option($idx, \$id); });
            $hbox->pack_start($cb, 0, 0, 0);
            my $label = Gtk3::Label->new("$key");
            $hbox->pack_start($label, 0, 0, 0);
            $scrollable_frame->add($hbox);
        } elsif ( $id eq "aov") {
        # active option/value line
            my $hbox = Gtk3::Box->new('horizontal', 5);
            my $cb = Gtk3::CheckButton->new("");
            $cb->set_active("1");
            $cb->signal_connect(toggled => sub { toggle_option($idx, \$id); });
            $hbox->pack_start($cb, 0, 0, 0);
            my $label = Gtk3::Label->new("$key = ");
            $hbox->pack_start($label, 0, 0, 0);
            my $entry = Gtk3::Entry->new();
            if (defined($value)){
               $entry->set_text("$value");
            }else{
               $entry->set_text("");
            }
            $entry->signal_connect('focus-out-event' => sub { update_value($idx, $entry->get_text); });
            $hbox->pack_start($entry, 1, 1, 0);
            $scrollable_frame->add($hbox);
        } elsif ($id eq "com") {
        # Comment-only line
            my $escapelabel = encode_entities($original_line);
            my $label = Gtk3::Label->new($escapelabel);
            $label->set_markup("<span font='monospace'>$escapelabel</span>");
            # Enable markup
            $label->set_use_markup(1);
            # Set the label to wrap text
            $label->set_line_wrap(1);
            # Set alignment to left
            #$label->set_justify('left');          # Set text justification
            $label->set_halign('start');          # Align label horizontally to start (left)
            $label->set_valign('start');          # Align label vertically to top (optional)
            $scrollable_frame->add($label);
        } else { # un-matched line
                 # should not land here catchall
        }
    }
    $scrollable_frame->show_all();
}
sub id_line { #identify type of line
    my $input = shift;
    my $output = "und";
        if (!defined($input)) {
           $output = "und";
        } elsif ($input =~ /^\s*$/) { # empty line
           $output = "emt";
        } elsif ($input =~ /^\s*#+\s*([0-9a-zA-Z_-]+)\s*$/) { # inactive option only line
           $output = "ioo";
        } elsif ($input =~ /^\s*#+\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\.,\/:;'"\\\}\{\]\[\s-]+)?\s*$/) { # inactive otion/value line
            $output = "iov";
        } elsif ($input =~ /^\s*([0-9a-zA-Z_-]+)\s*$/) { # active option line
            $output = "aoo";
        } elsif ($input =~ /^\s*([0-9a-zA-Z_-]+)=([0-9a-zA-Z%_+\.,\/:;'"\\\}\{\]\[\s-]+)?\s*$/) { # active option/value line
            $output = "aov";
        } elsif ($input =~ /^\s*#+.*$/) { # Comment-only line
            $output = "com";
        } else { # should not land here catchall
            $output = "und";
        }
    return $output;
}
# Toggle option active state
sub toggle_option {
    my ($idx, $is_on_ref) = @_;
    foreach my $opt (@options) {
        if ($opt->[0] eq $idx) {
             my $bla = "NA";
             if (defined($opt->[2])){
                $bla = "[$opt->[2]]";
             } else {
                $bla = "";
             }
             if ($opt->[3] =~ /^a/){
                $opt->[3] =~ s/^a/i/g;
                print "toggled off/$ [$idx]:[$opt->[1]]${bla}[$opt->[3]]\n";
             }elsif ($opt->[3] =~ /^i/){
                $opt->[3] =~ s/^i/a/g;
                print "toggled on [$idx]:[$opt->[1]]${bla}[$opt->[3]]\n";
             }
        }
    }
    save_config();
}
# Update value
sub update_value {
    my ($idx, $new_value) = @_;
    foreach my $opt (@options) {
        if ("$opt->[0]" eq "$idx") {
            if (! defined($opt->[2])) {
               print "undefined value on [$idx]:[$opt->[1]]\n";
               return;
            } elsif ("$opt->[2]" eq "$new_value") {
               print "unchanged [$idx]:[$opt->[1]] is [$opt->[2]]\n";
               return;
            } else {
               $opt->[2] = $new_value;
               print "changed [$idx]:[$opt->[1]] to [$opt->[2]]\n";
            }
        }
    }
    save_config();
}
# Save the configuration back to the file, preserving comments and empty lines
sub save_config {
    return unless $file_path;

    open my $fh, '>', $file_path or die "Could not open file '$file_path': $!";
    foreach my $opt (@options) {
        my ($idx, $key, $value, $id, $original_line) = @$opt;
        if (!defined($original_line)){
           print 'UNDEFINED original_line while saving\n';
        }
        if (!defined($value)){
           $value = "";
        }
        #show full saved config interpretation#print(id_line($original_line).":saving:[$original_line]\n");
        if ($id eq "emt") { # empty or space only lines
           print $fh "$original_line\n";
        } elsif ($id eq "ioo") { # inactive option only line
           print $fh "# $key\n";
        } elsif ($id eq "iov") { # inactive otion/value line
           print $fh "# $key=$value\n";
        } elsif ($id eq "aoo") { # active option line
           print $fh "$key\n";
        } elsif ($id eq "aov") { # active option/value line
           print $fh "$key=$value\n";
        } elsif ($id eq "com") { # Comment-only line
           print $fh "$original_line\n";
        } else { # should not land here catchall
            print "# unmatched line: [$original_line]\n";
        }
    }
    close $fh;
    print "saved $file_path\n";
}

# Clear the options from the GUI
sub clear_options_frame {
    foreach ($scrollable_frame->get_children) {
        $_->destroy;
    }
}

# Reload the config file
sub reload_config {
    load_config() if $file_path;
}
sub new_config {
    $file_path = "";
    load_config();
}
# Show main window
$mw->show_all();
reload_config();
Gtk3->main();
