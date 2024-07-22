from typing import Union
from dlx import DLX_node,DLX,SudokuSolver

import tkinter as tk
from tkinter import ttk

class SudokuGUI:
	def __init__(self) -> None:
		self._root = tk.Tk()
		self._root.title("Sudoku Solver")
		self._root.geometry("700x600")
		self._root.resizable(False,False)
		self._sudoku = SudokuSolver()
		self._solutions = []
		self._board = []
		self._create_widgets()
		self._root.mainloop()
	
	def _create_widgets(self) -> None:
		self._frame = ttk.Frame(self._root)
		self._frame.pack()
		self._input_frame = ttk.Frame(self._frame)
		self._input_frame.pack(pady=10)
		self._buttons = []
		for i in range(9):
			row = []
			for j in range(9):
				btn = tk.Entry(self._input_frame,width=3, font=('System',24), justify="center", validate="key",validatecommand=(self._root.register(lambda x: (x.isdigit() and 1 <= int(x) <= 9) or x == ''),"%P"))
				btn.grid(row=i,column=j,pady=3)
				row.append(btn)
			self._buttons.append(row)
		self._control_frame = ttk.Frame(self._frame)
		self._control_frame.pack(pady=10)
		self._solve = ttk.Button(self._control_frame,text="Solve",command=self._solve_sudoku)
		self._solve.pack(side=tk.LEFT,padx=5)
		self._clear = ttk.Button(self._control_frame,text="Clear",command=self._clear_board)
		self._clear.pack(side=tk.RIGHT,padx=5)
		self._export = ttk.Button(self._control_frame,text="Export",command=self._export_board)
		self._export.pack(side=tk.RIGHT,padx=5)
		self._import_frame = ttk.Frame(self._frame)
		self._import_frame.pack()
		self._import_entry = ttk.Entry(self._import_frame, width=81)
		self._import_label = ttk.Label(self._import_frame,text="Input a 81-character string representing the board:")
		self._import_label.pack(side=tk.TOP)
		self._import_entry.pack(side=tk.LEFT)
		self._import_btn = ttk.Button(self._import_frame,text="Import",command=self._import_board)
		self._import_btn.pack(side=tk.RIGHT)
	
	def _solve_sudoku(self) -> None:
		...
	
	def _clear_board(self) -> None:
		for i in range(9):
			for j in range(9):
				self._buttons[i][j].config(validate="none",fg="red")
				self._buttons[i][j].delete(0,tk.END)
				self._buttons[i][j].config(validate="key")
		self._board = []
		self._solutions = []
	
	def _import_board(self) -> None:
		...
	
	def _export_board(self) -> None:
		str = ''
		for i in range(9):
			for j in range(9):
				c = self._buttons[i][j].get()
				str += c if c else '.'
		self._root.clipboard_clear()
		self._root.clipboard_append(str)

if __name__ == "__main__":
	# sdk = SudokuSolver()
	# sols = sdk.solve('.................................................................................',2)
	# print(sols)
	gui = SudokuGUI()
	gui._root.mainloop()