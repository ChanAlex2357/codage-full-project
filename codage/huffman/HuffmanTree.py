class HuffmanTree :
	def __init__(self,libelle,probabilite,arret=None,tree1=None,tree2=None,code=''):
		self.set_arret(arret)
		self.set_tree1(tree1)
		self.set_tree2(tree2)
		self.set_libelle(libelle)
		self.set_probabilite(probabilite)
		self.set_code(code)
#Getteurs and Setteurs
	#arret
	def get_arret(self):
		return self._arret

	def set_arret(self,arret):
		self._arret=arret

	#tree1
	def get_tree1(self):
		return self._tree1

	def set_tree1(self,tree1):
		self._tree1=tree1

	#tree2
	def get_tree2(self):
		return self._tree2

	def set_tree2(self,tree2):
		self._tree2=tree2

	#libelle
	def get_libelle(self):
		return self._libelle

	def set_libelle(self,libelle):
		self._libelle=libelle

	#probabilite
	def get_probabilite(self):
		return self._probabilite

	def set_probabilite(self,probabilite):
		self._probabilite=probabilite

	#code
	def get_code(self):
		return self._code

	def set_code(self,code):
		self._code=code

