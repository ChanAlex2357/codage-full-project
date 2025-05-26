from codage.file import *
from codage.huffman import  *
from codage.language_analyser import *
from codage.steganographie import *

# ===================== Traitement du fichier texte de baase ===================

print("Ceci est un projet d'evaluation des connaissances en codage")

## lecture du fichier text generer
text_data = read_data(filepath="docs/2434.txt")

## Codage de huffman
M,S,P = huffman_base(text_data, ingnore_case=True)
# M,S,P = (load_huffman_data('input.txt'))
write_huffman_data('docs/_huff_data.txt',M,S,P)

## Huffman dico/
C = huffman_render(M,S,P)
dico = huffman_dico(M,S,C)
write_huffman_dico('docs/_huff_dico.txt',M,S,C)


# =================== Verification code par sardinas pattersons ======================
L = read_data("docs/_language.txt").splitlines()
print(f'L >> {L}')
print("\nEst-ce un code ? >> ", is_code_language(L))

# ================== Fonction Recurcive ===============================
def u(n:int,a,b) :
    if n == 0:
        return 1
    return a * u(n-1,a,b) + b

def generate_positions(indexes:List[int], a=2, b=4):
    positions = []

    for n in indexes:
        positions.append(u(n,a,b))

    return positions

# ================== Generere les positions =========================

u_steps = [0,2,2,3,1,4]
a = 2
b = 4
img_indexes = audio_indexes = generate_positions(u_steps, a, b)

# ================== Decodage Steganographie Image =========================

img_data , metadata = read_gray_image_file("assets/img/baobab-2.jpg")
print(f"Image data: {img_data}")


# ================== Decodage Steganographie Audio =========================
