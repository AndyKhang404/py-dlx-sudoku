import sys
from dlx import SudokuSolver

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class SudokuGUI:
	def __init__(self, solver: SudokuSolver) -> None:
		self._root = tk.Tk()
		self._root.title("Sudoku Solver")
		self._root.geometry("700x600")
		self._root.resizable(False,False)
		self._solver = solver
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
		self._import_entry = ttk.Entry(self._import_frame, width=85)
		self._import_label = ttk.Label(self._import_frame,text="Input a 81-character string representing the board:")
		self._import_label.pack(side=tk.TOP)
		self._import_entry.pack(side=tk.LEFT)
		self._import_btn = ttk.Button(self._import_frame,text="Import",command=self._import_board)
		self._import_btn.pack(side=tk.RIGHT)
	
	def _solve_sudoku(self) -> None:
		str = ''
		for i in range(9):
			for j in range(9):
				c = self._buttons[i][j].get()
				str += c if c else '.'
		if not ('.' in str):
			tk.messagebox.showinfo("Solved","Board already solved!")
			return
		self._solutions = self._solver.solve(str,2)
		if len(self._solutions) == 0:
			tk.messagebox.showinfo("No Solutions","No solutions found!")
			return
		if len(self._solutions) > 1:
			tk.messagebox.showinfo("Multiple Solutions","Board has multiple solutions!")
		for i in range(9):
			for j in range(9):
				if self._buttons[i][j].get() != '': 
					self._buttons[i][j].config(state="readonly")
					continue
				self._buttons[i][j].config(validate="none", fg="red")
				self._buttons[i][j].delete(0,tk.END)
				self._buttons[i][j].insert(0,self._solutions[0][i*9+j])
				self._buttons[i][j].config(validate="key")
				self._buttons[i][j].config(state="readonly")
		self._solve.config(state="disabled")
	
	def _clear_board(self) -> None:
		for i in range(9):
			for j in range(9):
				self._buttons[i][j].config(validate="none", fg="black", state="normal")
				self._buttons[i][j].delete(0,tk.END)
				self._buttons[i][j].config(validate="key")
		self._solve.config(state="normal")
		self._board = []
		self._solutions = []
	
	def _import_board(self) -> None:
		str = self._import_entry.get()
		if len(str) != 81:
			tk.messagebox.showerror("Invalid Board","Invalid board string!")
			return
		for i in range(9):
			for j in range(9):
				self._buttons[i][j].config(validate="none")
				self._buttons[i][j].delete(0,tk.END)
				if 1 <= ord(str[i*9+j])-ord('0') <= 9:
					self._buttons[i][j].insert(0,str[i*9+j])
				self._buttons[i][j].config(validate="key")
		self._board = [int(i)-1 if i.isdigit() else -1 for i in str]
	
	def _export_board(self) -> None:
		str = ''
		for i in range(9):
			for j in range(9):
				c = self._buttons[i][j].get()
				str += c if c else '.'
		self._root.clipboard_clear()
		self._root.clipboard_append(str)
		self._root.update()
		tk.messagebox.showinfo("Exported","Board copied to clipboard!")

if __name__ == "__main__":
	sdk = SudokuSolver()
	args = sys.argv[1:]
	if len(args) == 0 or args[0] == "-h":
		print("Usage:")
		print("    Solve:    python main.py <board> [-n <max_solutions>]")
		print("    GUI mode: python main.py -g")
		print("	   Help:     python main.py -h")
		if '-h' in args: exit(0)
		exit(1)
	if args[0] == "-g":
		gui = SudokuGUI(sdk)
		gui._root.mainloop()
		exit(0)
	if "-n" in args:
		n = args[args.index("-n")+1]
		args.remove("-n")
		args.remove(n)
		solutions = sdk.solve(args[0],int(n))
		if len(solutions) == 0:
			print("No solutions found!")
		else:
			for i in solutions:
				print(i)
	else:
		solutions = sdk.solve(args[0],2)
		if len(solutions) == 0:
			print("No solutions found!")
		else:
			for i in solutions:
				print(i)