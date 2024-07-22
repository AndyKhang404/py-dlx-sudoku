# py-dlx-sudoku

This project was made for the [Hack Club Arcade(2024)](https://hackclub.com/arcade/) and is a follow up to my [sudoku solver website](https://github.com/AndyKhang404/sudoku-solver) project

A python sudoku solver implementing Donald Knuth's DLX algorithm. You can read more about his paper [here](http://web.archive.org/web/20171105084810/http://lanl.arxiv.org/pdf/cs/0011047) or read this [Zendoku article](http://web.archive.org/web/20171112064626/http://garethrees.org/2007/06/10/zendoku-generation/#section-4) first to get some insights.

### How to use
```
Usage:
    Solve:    python main.py <board> [-n <max_solutions>]
    GUI mode: python main.py -g
	Help:     python main.py -h
```
**Note:** In case of tkinter clipboard doesn't work, try installing pyperclip with:
```
pip install pyperclip
```
