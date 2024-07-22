from typing import Union, Iterator

# Reference: http://web.archive.org/web/20171112064626/http://garethrees.org/2007/06/10/zendoku-generation/#section-4

class DLX_node:
	def __init__(self) -> None:
		self.col: str = ''
		self.size: int = 0
		self.is_column: bool = False
		self.name: str = ''
		self.next   : Union[None,DLX_node] = self
		self.prev   : Union[None,DLX_node] = self
		self.top    : Union[None,DLX_node] = self
		self.bottom : Union[None,DLX_node] = self

class DLX():
	def __init__(self,board: Union[str,None] = None) -> None:
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
					succ.col = f's{row*9 + col}'
					curr = s1
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s1 = succ
					# Row
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					succ.col = f'r{row}#{i}'
					curr = s2
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s2 = succ
					# Col
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					succ.col = f'c{col}#{i}'
					curr = s3
					succ.top = curr.top
					curr.top = succ
					succ.top.bottom = succ
					succ.bottom = curr
					s3 = succ
					# Box
					succ: DLX_node = DLX_node()
					succ.name = f'r{row}c{col}#{i}'
					succ.col = f'b{(col // 3) + (row // 3)*3}#{i}'
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
		
		# Parse board
		self.board = []
		if board is not None:
			if len(board) != 81:
				raise Exception('Invalid board!')
			board_arr = [(ord(i)-ord('1')) if (ord('1') <= ord(i) <= ord('9')) else -1 for i in board]
			self.board = board_arr
			for i in range(9):
				for j in range(9):
					if board_arr[i*9+j] == -1: continue
					curr = self.column_lookup[f's{i*9 + j}'].bottom
					while not curr.is_column and not curr.name == f'r{i}c{j}#{board_arr[i*9+j]}':
						curr = curr.bottom
					if curr.name == f'r{i}c{j}#{board_arr[i*9+j]}':
						temp = curr
						curr = curr.next
						while curr is not temp:
							self.cover(self.column_lookup[curr.col])
							curr = curr.next

	
	def cover(self, c: DLX_node) -> None:
		if not c.is_column:
			return
		
		c.prev.next = c.next
		c.next.prev = c.prev
		n = c.bottom
		while n is not c:
			r = n.next
			while r is not n:
				r.top.bottom = r.bottom
				r.bottom.top = r.top
				self.column_lookup[r.col].size -= 1
				r = r.next
			n = n.bottom
	
	def uncover(self, c: DLX_node) -> None:
		if not c.is_column:
			return
		
		u = c.top
		while u is not c:
			p = u.prev
			while p is not u:
				self.column_lookup[p.col].size += 1
				p.top.bottom = p
				p.bottom.top = p
				p = p.prev
			u = u.top
		c.prev.next = c
		c.next.prev = c

	def search(self,limit: int) -> Iterator[Union[str,None]]:
		if limit == 0: # Limit how many solutions do we want
			yield None
			# "".join([chr(i+ord('1')) if 1 <= i <= 9 else ' ' for i in self.board])
		curr = self.head.next
		if curr is self.head: # We've found a solution
			limit -= 1
			yield "".join([chr(i+ord('1')) if 1 <= i <= 9 else ' ' for i in self.board])
		minsize = 100
		mincol = curr
		while curr is not self.head:
			if curr.size < minsize:
				minsize = min(curr.size, minsize)
				mincol = curr
			curr = curr.next
		if minsize == 0: # This column have nothing to cover => contradiction
			yield None
		self.cover(mincol)
		r = curr.bottom
		while r is not curr:
			# o = r
			j = r.next
			while j is not r:
				self.cover(self.column_lookup[j.col])
				j = j.next
			_,u,_,v,_,w = [ord(i)-ord('0') for i in r.name]
			self.board[u*9+v] = w
			yield from self.search(limit)
			j = r.prev
			while j is not r:
				self.uncover(self.column_lookup[j.col])
				j = j.prev
			self.board[u*9+v] = -1
			r = r.bottom
		self.uncover(mincol)