from steganographie import *
from codage import *
from codage.file import *

positions = list(range(100))
(data , header , fmt) = read_audio_data("assets/audio/remove/whistle-simple.wav")
wav_code = steg_decode_wav("assets/audio/remove/whistle-simple.wav" , positions)

dico = load_huffman_dico("assets/dico.txt")
decode = huffman_decode(wav_code,dico)
print(f"{decode}")