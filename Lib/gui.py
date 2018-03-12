# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Project: -/Lib/gui.py -> Manages the curses gui for the simulation

import curses
from curses.textpad import Textbox, rectangle

message = ""

def main(stdscr):
    stdscr.addstr(0, 0, "Enter Parameters: (hit Ctrl-G to send)")
    curses.noecho()
    editwin = curses.newwin(5,30, 2,1)
    rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
    stdscr.refresh()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()