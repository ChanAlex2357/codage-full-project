from codage.file import read_data, write_huffman_data, write_huffman_dico, load_huffman_data
from codage import  huffman_base, huffman_render, huffman_dico

print("Ceci est un projet d'evaluation des connaissances en codage")

## lecture du fichier text generer
# text_data = read_data(filepath="2434.txt")

## Codage de huffman
# M,S,P = huffman_base(text_data)
M,S,P = (load_huffman_data('input.txt'))
write_huffman_data('_huff_data.txt',M,S,P)

## Huffman dico/
C = huffman_render(M,S,P)
dico = huffman_dico(M,S,C)
write_huffman_dico('_huff_dico.txt',M,S,C)
