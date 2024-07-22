from typing import Union
from dlx import DLX_node,DLX

if __name__ == "__main__":
	sdk = DLX(board='003020600900305001001806400008102900700000008006708200002609500800203009005010300')
	curr = sdk.column_lookup['b8#0']
	succ = curr.bottom
	while succ is not curr:
		print(succ.name)
		succ = succ.bottom