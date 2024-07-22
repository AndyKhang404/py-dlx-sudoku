from typing import Union
from dlx import DLX_node,DLX,SudokuSolver

if __name__ == "__main__":
	sdk = SudokuSolver()
	sols = sdk.solve('003020600900305001001806400008102900700000008006708200002609500800203009005010300',2)
	print(sols)