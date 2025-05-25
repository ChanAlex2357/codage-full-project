from .HuffmanTree import HuffmanTree
from .HuffmanForest import HuffmanForest
from typing import List, Dict, Tuple
import heapq
from collections import Counter
import re
import itertools

counter = itertools.count()  # global or within the function


## Build the huffman tree
def build_huffman_forest(m: int, S: List[str], P: List[float]) -> HuffmanForest:
    """Construit une forêt d'arbres de Huffman optimisée."""
    return HuffmanForest([HuffmanTree(S[i], P[i]) for i in range(m)])

def build_huffman_tree(Si: str, Pi: float) -> HuffmanTree:
    """Construit un arbre de Huffman simple optimisé."""
    return HuffmanTree(Si, Pi)

def merge_trees(trees: List[HuffmanTree], m: int) -> List[HuffmanTree]:
    """Fusionne les arbres de manière optimisée avec complexité O(m log m)."""
    if m == 1:
        return trees
    
    # Utilisation d'un tas min pour une meilleure performance
    heap = [(tree.get_probabilite(), idx, tree) for idx, tree in enumerate(trees)]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        prob1, idx1, temp1 = heapq.heappop(heap)
        prob2, idx2, temp2 = heapq.heappop(heap)

        # Ensure t1 has the higher prob, or lower idx if equal
        if (prob1 > prob2) or (prob1 == prob2 and idx1 < idx2):
            t1, t2 = temp1, temp2
            p1, p2 = prob1, prob2
        else:
            t1, t2 = temp2, temp1
            p1, p2 = prob2, prob1

        merged = HuffmanTree(
            libelle=t1.get_libelle() + t2.get_libelle(),
            probabilite=p1 + p2,
            tree1=t1,
            tree2=t2
        )

        heapq.heappush(heap, (merged.get_probabilite(), len(trees) + next(counter), merged))

    # Reconstruction des codes de manière optimale
    final_tree = heap[0][2]
    nodes = [final_tree]
    codes = []
    
    while nodes:
        node = nodes.pop()
        if node.get_tree1() is None and node.get_tree2() is None:
            codes.append(node)
            continue
            
        if node.get_tree1():
            node.get_tree1().set_code(node.get_code() + '1')
            nodes.append(node.get_tree1())
            
        if node.get_tree2():
            node.get_tree2().set_code(node.get_code() + '0')
            nodes.append(node.get_tree2())
    
    return codes

## Methodes de conversion binaires
def get_binaries(encoded: bytes) -> List[str]:
    """
        Conversion bytes -> binaire optimisée.
        012010212 -> 08b binaire 8 bits
    """
    return [f'{byte:08b}' for byte in encoded]

def get_binaries_str(encoded: bytes) -> str:
    """
        Conversion bytes -> chaîne binaire optimisée.
        012010212 ->
    """
    return ''.join(get_binaries(encoded))

def render_forest(forest: HuffmanForest, m: int) -> None:
    """Rendu optimisé de la forêt."""
    trees = forest.get_trees()
    merge_trees(trees, m)

def huffman_render(m: int, S: List[str], P: List[float]) -> List[str]:
    """Génération des codes Huffman optimisée."""
    forest = build_huffman_forest(m, S, P)
    render_forest(forest, m)
    return [tree.get_code() for tree in forest.get_trees()]

def huffman_decode(encoded: str, dico: Dict[str, str]) -> str:
    """Décodage optimisé avec lookup direct."""
    reverse_dict = {v: k for k, v in dico.items()}
    decoded = []
    current = []
    
    for bit in encoded:
        current.append(bit)
        code = ''.join(current)
        if code in reverse_dict:
            decoded.append(reverse_dict[code])
            current = []
    
    if current:
        raise ValueError("Encodage invalide - bits restants")
    
    return ''.join(decoded)

def huffman_encode_word(mot: str, huffman_dict: Dict[str, str]) -> str:
    """Encodage d'un mot optimisé."""
    return ''.join(huffman_dict.get(char, '') for char in mot)

def huffman_encode(sentence: str, huffman_dict: Dict[str, str]) -> str:
    """Encodage d'une phrase optimisé."""
    return ''.join(huffman_encode_word(mot, huffman_dict) for mot in sentence)

def huffman_dico(m: int, s: List[str], c: List[str]) -> Dict[str, str]:
    """Création du dictionnaire optimisée."""
    return {s[i]: c[i] for i in range(m)}

def huffman_base(text: str, keep_spaces: bool = True, ingnore_case=False) -> Tuple[int, List[str], List[float]]:
    """Analyse de fréquence optimisée."""
    if keep_spaces:
        text = re.sub(r'\s+', ' ', text).strip()
    else:
        text = re.sub(r'[^\w]', '', text)

    if ingnore_case:
        text = text.lower()
    
    if not text:
        return 0, [], []
    
    freq = Counter(text)
    chars = sorted(freq.keys())
    probs = [freq[char] for char in chars]
    
    return len(chars), chars, probs