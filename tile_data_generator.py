from PIL import Image
import numpy as np
import re
import uuid
from pathlib import Path
sample_fen = 'q1r1r1k1/pp1npppp/1p1ppn2/8/2PP4/1P1B1NN1/PB2QPPP/2R3K1'

import tile_splitter

def expand_fen(fen):
    fen = fen.replace('1', 'f')
    fen = fen.replace('2', 'ff')
    fen = fen.replace('3', 'fff')
    fen = fen.replace('4', 'ffff')
    fen = fen.replace('5', 'fffff')
    fen = fen.replace('6', 'ffffff')
    fen = fen.replace('7', 'fffffff')
    fen = fen.replace('8', 'ffffffff')
    fen = fen.replace('/', '')

    return fen



if __name__ == '__main__':
    # Path('./test/data/').rmdir(exist_ok =)

    img = Image.open('./img/example1.png').convert('RGB')
    img = img.resize((512,512))
    arr = np.asarray(img)
    tiles = tile_splitter.split_img(arr, 64, 64)
    fen = expand_fen(sample_fen)
    tiles = enumerate(tiles)
    
    
    for count, tile in tiles:
        tile_img = Image.fromarray(np.uint8(tile))
        fen_folder_name = f'./test/data/_{fen[count]}'
        Path(fen_folder_name).mkdir(parents=True, exist_ok=True)
        print(fen_folder_name)
        tile_img.save(f'{fen_folder_name}/{uuid.uuid4()}.jpg')