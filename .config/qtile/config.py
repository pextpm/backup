# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

try:
    from typing import List  # noqa: F401
except ImportError:
    pass

mod = "mod4"
myTerm = "termite"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod, "control"], "c", lazy.spawn("vim ~/.config/qtile/config.py")), # it does not work
    
    # Volume configuration
    Key([mod], "Up", lazy.spawn("pulseaudio-ctl up")),
    Key([mod], "Down", lazy.spawn("pulseaudio-ctl down")),
    Key([mod, "control"], "m", lazy.spawn("pulseaudio-ctl mute")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

]

groups = [Group(i) for i in "asdfuiop"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.MonadTall(border_focus = "#6e8dd1")
]

colors = [["#292D3E", "#292D3E"],
          ["#373854","#373854"],
          ["#493267", "#493267"],
          ["#9e379f", "#9e379f"],
          ["#e86af0", "#e86af0"],
          ["#7bb3ff", "#7bb3ff"],
          ["#71c7ec", "#71c7ec"]]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    background = colors[0],
                    padding = 1.3,
                    fontsize = 15),
                widget.WindowName(
                    background = colors[0],
                    padding = 6),
                widget.TextBox(
                    padding = 6,
                    text = "",
                    background = colors[1],
                    fontsize = 18),
                widget.CurrentLayout(
                    background = colors[1],
                    fontsize = 15,
                    padding = 6),
                widget.TextBox(
                    background = colors[2],
                    text = "",
                    padding = 6,
                    fontsize = 18),
                widget.Memory(
                    background = colors[2],
                    padding = 6,
                    fontsize = 15,
                    update_interval = 5),
               widget.TextBox(
                   padding = 6,
                   text = "",
                   fontsize = 18,
                   background = colors[3]),
               widget.Volume(
                   fontsize = 15,
                   padding = 6,
                   background = colors[3]),
               widget.TextBox(
                    background = colors[3],
                    text = "",
                    fontsize = 18),
                widget.ThermalSensor(
                    background = colors[3],
                    fontsize = 15),
                widget.TextBox(
                    text ="",
                    background = colors[4],
                    fontsize = 18,
                    padding = 6),
                widget.Battery(
                    fontsize = 15,
                    background = colors[4]),
                widget.TextBox(
                    background = colors[5],
                    text = "",
                    fontsize = 18,
                    padding = 6),
                widget.Clock(
                    format = "%A, %B %d - %H:%M",
                    background = colors[5],
                    fontsize = 15,
                    padding = 6)
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
