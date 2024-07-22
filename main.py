from typing import Union
from dlx import DLX_node,DLX

if __name__ == "__main__":
	sdk = DLX()
	sdk.cover(sdk.head.next)
	print(sdk.column_lookup['r0#1'].size)