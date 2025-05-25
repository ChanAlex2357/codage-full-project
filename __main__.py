from codage.file import *
from codage.huffman import  *
from codage.language_analyser import *

# ===================== Traitement du fichier texte de baase ===================

print("Ceci est un projet d'evaluation des connaissances en codage")

## lecture du fichier text generer
text_data = read_data(filepath="2434.txt")

## Codage de huffman
M,S,P = huffman_base(text_data)
# M,S,P = (load_huffman_data('input.txt'))
write_huffman_data('_huff_data.txt',M,S,P)

## Huffman dico/
C = huffman_render(M,S,P)
dico = huffman_dico(M,S,C)
write_huffman_dico('_huff_dico.txt',M,S,C)


# =================== Verification code par sardinas pattersons ======================
L = C
print(f'L >> {L}')
print("\nEst-ce un code ? >> ", is_code_language(L))

# ================== Fonction Recurcive ===============================
def u(n:int,a,b) :
    if n == 1:
        return 1
    return a * u(n-1) + b

def generate_positions(indexes:List[int], a=2, b=4):
    positions = List()

    for n in indexes:
        positions.append(u(n),a,b)

    return positions
