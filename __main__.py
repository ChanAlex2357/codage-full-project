from codage.file import read_data, write_huffman_data
from codage import  huffman_base

print("Ceci est un projet d'evaluation des connaissances en codage")

## lecture du fichier text generer
text_data = read_data(filepath="2434.txt")
## Codage de huffman
M,S,P = huffman_base(text_data)
write_huffman_data('_huff_data.txt',M,S,P)

