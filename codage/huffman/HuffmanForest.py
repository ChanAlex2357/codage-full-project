class HuffmanForest :
	def __init__(self,trees):
		self.set_trees(trees)
#Getteurs and Setteurs
	#trees
	def get_trees(self):
		return self._trees

	def set_trees(self,trees):
		self._trees=trees

