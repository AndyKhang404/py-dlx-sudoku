from typing import Union

# Reference: http://web.archive.org/web/20171112064626/http://garethrees.org/2007/06/10/zendoku-generation/#section-4

class DLX_node:
	def __init__(self) -> None:
		self.value: int = 0
		self.size: int = 0
		self.is_column: bool = False
		self.name: str = ''
		self.next   : Union[None,DLX_node] = self
		self.prev   : Union[None,DLX_node] = self
		self.top    : Union[None,DLX_node] = self
		self.bottom : Union[None,DLX_node] = self

class DLX():
	def __init__(self) -> None:
		self.head: DLX_node = DLX_node()
		self.head.name = 'head'
		curr: DLX_node = self.head
		self.column_lookup: dict[str,DLX_node] = {}

		# Only one number in each square
		for row in range(9):
			for col in range(9):
				succ: DLX_node = DLX_node() # successor
				succ.name = f's{row*9 + col}'
				succ.is_column = True
				self.column_lookup[succ.name] = succ
				curr.next = succ
				succ.prev = curr
				curr = succ
				self.head.size += 1
		
		# Only one number from 1-9 in each row
		for row in range(9):
			for i in range(9):
				succ: DLX_node = DLX_node()
				succ.name = f'r{row}#{i}'
				succ.is_column = True
				self.column_lookup[succ.name] = succ
				curr.next = succ
				succ.prev = curr
				curr = succ
				self.head.size += 1
		
		# Only one number from 1-9 in each col
		for col in range(9):
			for i in range(9):
				succ: DLX_node = DLX_node()
				succ.name = f'c{col}#{i}'
				succ.is_column = True
				self.column_lookup[succ.name] = succ
				curr.next = succ
				succ.prev = curr
				curr = succ
				self.head.size += 1
		
		# Only one number from 1-9 in each box
		for box in range(9):
			for i in range(9):
				succ: DLX_node = DLX_node()
				succ.name = f'b{box}#{i}'
				succ.is_column = True
				self.column_lookup[succ.name] = succ
				curr.next = succ
				succ.prev = curr
				curr = succ
				self.head.size += 1
		
		# Loop around
		curr.next = self.head
		self.head.prev = curr
		# Each candidate number
		for row in range(9):
			for col in range(9):
				for i in range(9):
					s1 = self.column_lookup[f's{row*9 + col}']
					s2 = self.column_lookup[f'r{row}#{i}']
					s3 = self.column_lookup[f'c{col}#{i}']
					s4 = self.column_lookup[f'b{(col // 3) + (row // 3)*3}#{i}']
					# Square
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					curr = s1
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s1 = succ
					# Row
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					curr = s2
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s2 = succ
					# Col
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					curr = s3
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s3 = succ
					# Box
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					curr = s4
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s4 = succ
					# Connect these four to make a row (candidate)
					s1.next = s2
					s2.next = s3
					s3.next = s4
					s4.next = s1
					# ...and reverse
					s1.prev = s4
					s2.prev = s1
					s3.prev = s2
					s4.prev = s3
					# Count increment
					s1.bottom.size += 1
					s2.bottom.size += 1
					s3.bottom.size += 1
					s4.bottom.size += 1