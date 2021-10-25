#Votes transfer matrix
class VTMatrix:
	initial = []
	final = []
	matrix = []
	
	def __init__(self, initial: list, final: list, matrix: list):
		#Check everything is alright
		if (len(matrix) != len(initial)) or (len(matrix[0]) != len(final)):
			raise Exception('Matrix isn\'t regular, {0} initial, {1} final, values are {2} initial and {3} final'.format(initial, final, len(matrix), len(matrix[0])))
		for i in range(1,len(matrix)):
			if len(matrix[i]) != len(matrix[i-1]):
				raise Exception('Matrix isn\'t uniform, row {0} has length {1} but previous row has length {2}'.format(i, len(matrix[i]), len(matrix[i-1])))
		#If everything is alright
		self.initial = initial
		self.final = final
		self.matrix = matrix
	
	def getCol(self, name: str) -> list:
		if name not in self.final:
			raise Exception('{0} not found in list in finals'.format(name))
		
		return [x[self.final.index(name)] for x in self.matrix]
	
	def getColDict(self, name: str) -> dict:
		if name not in self.final:
			raise Exception('{0} not found in list in finals'.format(name))
		
		return dict(zip(self.initial, [x[self.final.index(name)] for x in self.matrix]))