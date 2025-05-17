def read_data(filepath,mode='r'):
    with open(filepath, mode) as f:
        data = f.read().strip()
    return data

# Fonction pour lire depuis un fichier binaire
def read_binary_file(filename: str):
    '''
        Lit un fichier binaire et renvoie les donnees sous forme de chaine binaire
        Params :
            - filename : le nom du fichier
        Returns :
            - binary_str : la chaine binaire
    '''
    with open(filename, 'rb') as f:
        padding = f.read(1)[0]  # Lire le premier byte (padding)
        byte_data = f.read()
    
    binary_str = ''.join(f'{byte:08b}' for byte in byte_data)
    
    # Retirer le padding
    if padding > 0:
        binary_str = binary_str[:-padding]
    
    return binary_str

def load_huffman_data(filepath):
    '''
        Recupere les donnee necessaire (M,S,P) pour etablir l'arbre de huffman
        M: le nombre de mot
        S: la liste des mots
        P: Probabilite de chaque mot

        Params : 
            - filepath : le chemin vers le fichier contenant les donnees
        Returns :
            M , S , P
    '''
    with open(filepath, 'r') as f:
        lines = f.read().strip().splitlines()
    if len(lines) < 3:
        raise ValueError("File format incorrect. Expected at least 3 lines.")
    m = int(lines[0].strip())
    alphabets = lines[1].strip().split()
    probabilities = list(map(float, lines[2].strip().split()))
    if len(alphabets) != m or len(probabilities) != m:
        raise ValueError("Mismatch between declared size and provided data.")
    return m , alphabets, probabilities

def write_huffman_dico(filePath,m,S,C):
    '''
        Ecrit le dictionnaire de huffman dans un fichier
        Params :
            - filePath : le chemin vers le fichier
            - m : le nombre de mot
            - S : la liste des mots
            - C : la liste des codes de huffman

    '''
    with open(filePath, 'w') as f:
        for i in range(m):
            f.write(f'{S[i]}:{C[i]}\n')

def load_huffman_dico(filePath):
    '''
        Charge le dictionnaire de huffman depuis un fichier
        Params :
            - filePath : le chemin vers le fichier
        Returns :
            - huffDico : le dictionnaire de huffman
    '''
    huffDico = dict()
    with open(filePath,'r') as f:
        lines = f.read().strip().splitlines()
    for line in lines:
        [k,v] = line.strip().split(':')
        huffDico.__setitem__(k,v)
    return huffDico

def write_compressed_binary(encoded_data: str, filename: str):
    """
    Écrit les données binaires compressées (sans header) dans un fichier.
    
    Args:
        encoded_data (str): Données encodées en binaire (suite de '0' et '1')
        filename (str): Nom du fichier de sortie (.bin)
    """
    # Ajout du padding et conversion en bytes
    padding = (8 - len(encoded_data) % 8) % 8
    padded_data = encoded_data + '0' * padding
    
    # Conversion en bytes
    byte_array = bytearray()
    for i in range(0, len(padded_data), 8):
        byte = padded_data[i:i+8]
        byte_array.append(int(byte, 2))
    
    # Écriture dans le fichier (1er byte = padding)
    with open(filename, 'wb') as f:
        f.write(padding.to_bytes(1, 'big'))  # Stocke le padding (1 byte)
        f.write(byte_array)  # Stocke les données

def write_huffman_data(filepath, M, S, P):
    '''
        Écrit les données dans un fichier
        Params :
            - filepath : le chemin vers le fichier
            - M : un entier ou string
            - S : liste de chaînes (symboles)
            - P : liste de floats (probabilités ou fréquences)
    '''
    with open(filepath, 'w') as f:
        f.write(f"{M}\n")
        f.write(" ".join(S) + "\n")
        f.write(" ".join(map(str, P)) + "\n")
