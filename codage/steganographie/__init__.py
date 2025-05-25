from typing import List, Tuple
import numpy as np
import cv2
import struct


def read_wav_header(file_path):
    """
    Lit et interprète les 44 premiers octets d'un fichier WAV pour en extraire les métadonnées.
    """
    with open(file_path, 'rb') as f:
        header = f.read(44)  # Les 44 premiers octets contiennent l'en-tête WAV

        # Décompacte les métadonnées du fichier WAV
        (
            chunk_id, chunk_size, format,
            subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate,
            block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        ) = struct.unpack('<4sI4s4sIHHIIHH4sI', header)

        # Convertit les données binaires en un dictionnaire lisible
        header_info = {
            'chunk_id': chunk_id.decode('ascii'),
            'chunk_size': chunk_size,
            'format': format.decode('ascii'),
            'subchunk1_id': subchunk1_id.decode('ascii'),
            'subchunk1_size': subchunk1_size,
            'audio_format': audio_format,
            'num_channels': num_channels,
            'sample_rate': sample_rate,
            'byte_rate': byte_rate,
            'block_align': block_align,
            'bits_per_sample': bits_per_sample,
            'subchunk2_id': subchunk2_id.decode('ascii'),
            'subchunk2_size': subchunk2_size
        }

        return header_info


def read_gray_image_file(filepath: str) -> Tuple[np.ndarray, dict]:
    """
        Lit une image en niveaux de gris et retourne l'image sous forme de matrice ainsi que ses métadonnées.
    """
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Impossible de charger l'image: {filepath}")

    # Construction des métadonnées
    metadata = {
        'width': img.shape[1],
        'height': img.shape[0],
        'channels': 1,
        'dtype': str(img.dtype)
    }
    return img, metadata

def convert_rgb_to_grayscale(image_path: str, output_path: str = None) -> np.ndarray:
    """
    Convertit une image RGB en niveaux de gris (noir et blanc).
    
    Args:
        image_path (str): Chemin vers l'image RGB à convertir.
        output_path (str, optional): Chemin pour sauvegarder l'image convertie. 
                                     Si None, l'image ne sera pas sauvegardée.
    
    Returns:
        np.ndarray: Image convertie en niveaux de gris.
    """
    # Charger l'image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Impossible de charger l'image: {image_path}")
    
    # Vérifie si l'image est déjà en niveaux de gris
    if len(image.shape) == 2 or image.shape[2] == 1:
        gray_image = image  # Déjà en niveaux de gris
    else:
        # Conversion en niveaux de gris
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Sauvegarde facultative
    if output_path:
        cv2.imwrite(output_path, gray_image)
    
    return gray_image


def get_lsb_bits_from_positions(img_array: np.ndarray, positions: List[Tuple[int, int]]) -> List[int]:
    """
    Extrait les bits LSB des pixels aux positions spécifiées dans une image en niveaux de gris.
    Affiche aussi la valeur binaire complète de chaque pixel.

    Args:
        img_array: Image chargée sous forme de tableau numpy 2D.
        positions: Liste de tuples (row, col) représentant les coordonnées à lire.

    Returns:
        Liste des bits LSB extraits dans l'ordre.
    """
    bits = []
    height, width = img_array.shape

    for row, col in positions:
        if row >= height or col >= width:
            raise ValueError(f"Position invalide: ({row}, {col}) - Taille image: {height}x{width}")

        pixel_value = img_array[row, col]
        binary_str = format(pixel_value, '08b')  # Représentation binaire sur 8 bits
        lsb = pixel_value & 1  # Extraction du LSB
        bits.append(lsb)

        # # Affichage de debug
        # print(f"Position ({row}, {col})")
        # print(f"Valeur décimale: {pixel_value}")
        # print(f"Valeur binaire: {binary_str} (LSB: {binary_str[7]})")
        # print("-" * 30)

    return bits


def bits_to_bytes_str(bits: List[int]) -> bytes:
    """
    Transforme une liste de bits en une chaîne de caractères binaire (bytes sous forme de string).
    """
    return ''.join([f'{i}' for i in bits])


def bits_to_bytes(bits: List[int]) -> bytes:
    """
    Convertit une liste de bits (0 ou 1) en données binaires (bytes).

    Args:
        bits: Liste de bits

    Returns:
        Objet bytes représentant les données binaires.
    """
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits += [0] * (8 - len(byte_bits))  # Complète à 8 bits si besoin
        byte = sum(bit << pos for pos, bit in enumerate(byte_bits))  # Reconstruit l'octet
        byte_array.append(byte)
    return bytes(byte_array)


def steg_decode_gray_image_file(filepath: str, positions: List[Tuple[int, int]]) -> bytes:
    """
    Extrait un message caché dans une image en niveaux de gris.

    Args:
        filepath: Chemin de l'image.
        positions: Liste des coordonnées des pixels contenant les LSB à extraire.

    Returns:
        Message décodé sous forme de bytes (sous forme de chaîne binaire).
    """
    img_array, _ = read_gray_image_file(filepath)
    bits = get_lsb_bits_from_positions(img_array, positions)
    decoded_data = bits_to_bytes_str(bits)
    return decoded_data


def read_audio_data(file_path):
    """
    Lit les données audio d'un fichier WAV, retourne l'audio brut, l'en-tête et le format.

    Args:
        file_path: Chemin du fichier audio.

    Returns:
        Tuple contenant la liste des échantillons audio, l'en-tête, et la chaîne de format struct.
    """
    with open(file_path, 'rb') as f:
        header = f.read(44)  # En-tête WAV
        data = f.read()      # Données audio brutes

    header_info = read_wav_header(file_path)
    bits_per_sample = header_info['bits_per_sample']

    # Détermine le format de décodage des échantillons selon leur taille
    if bits_per_sample == 16:
        fmt = '<' + 'h' * (len(data) // 2)
    elif bits_per_sample == 8:
        fmt = '<' + 'b' * len(data)
    else:
        raise ValueError(f"Unsupported bit depth: {bits_per_sample}")

    audio_data = struct.unpack(fmt, data)

    return audio_data, header, fmt


def steg_decode_wav(filepath: str, positions: List[int]) -> bytes:
    """
    Extrait un message caché dans un fichier audio WAV en utilisant les LSB de certains échantillons.

    Args:
        filepath: Chemin du fichier .wav
        positions: Indices des échantillons à lire pour extraire les LSB

    Returns:
        Message décodé sous forme de chaîne binaire (bytes)
    """
    audio_data, header, fmt = read_audio_data(filepath)
    bits = []

    for pos in positions:
        if pos >= len(audio_data):
            raise ValueError(f"Position invalide: {pos} - Taille audio: {len(audio_data)}")

        sample = audio_data[pos]

        if isinstance(sample, int):
            lsb = sample & 1  # Extrait le LSB
            bits.append(lsb)
            print(f"Pos {pos} | Valeur: {sample} | LSB: {lsb}")
        else:
            raise ValueError("Format inattendu dans les données audio")

    return bits_to_bytes_str(bits)
