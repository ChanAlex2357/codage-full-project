from steganographie import *
from codage import *
from codage.file import *
# Positions où les données sont cachées (doivent correspondre à l'encodage)
positions = [
    (0, 0),  # Premier byte, LSB
    (0, 1),  # Premier byte, 2e bit
    (1, 0),  # Deuxième byte, LSB
]
# CONVERSION TN N&B
# gray_img = convert_to_grayscale('assets/img/baobab.jpg', method='luminosity', output_path='assets/img/baobab-1.jpg')

# READ IMAGE DATA
# image_data,metadata = read_image_file("assets/img/baobab-1.jpg")
# if image_data is not None:
#     print("Image loaded successfully!")
#     print(f"Dimensions: {metadata['width']}x{metadata['height']}")
#     print(f"Channels: {metadata['channels']}")
#     print(f"Data type: {image_data.dtype}")
    
#     # For grayscale images (2D array)
#     if len(image_data.shape) == 2:
#         print(f"Pixel at (0,0): {image_data[0,0]}")
#     # For color images (3D array)
#     else:
#         print(f"Pixel at (0,0): {image_data[0,0,:]}")

img_code = steg_decode_gray_image_file("assets/img/baobab-1.jpg",positions)
print(img_code)

dico = load_huffman_dico("assets/dico.txt")
decode = huffman_decode(img_code,dico)
print(f"{decode}")


gray_img = convert_rgb_to_grayscale("assets/img/baobab.jpg","assets/img/gray.jpg")
img_code = steg_decode_gray_image_file("assets/img/baobab-2.jpg",positions)
print(img_code)

decode = huffman_decode(img_code,dico)
print(f"{decode}")