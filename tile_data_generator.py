from PIL import Image
import numpy as np
import re
import uuid
from pathlib import Path


import tile_splitter
import utils


def expand_fen(fen):
    # def my_replace(m):
    #     my_list = ['f' ]
    fen = fen.replace('1', 'f')
    fen = fen.replace('2', 'ff')
    fen = fen.replace('3', 'fff')
    fen = fen.replace('4', 'ffff')
    fen = fen.replace('5', 'fffff')
    fen = fen.replace('6', 'ffffff')
    fen = fen.replace('7', 'fffffff')
    fen = fen.replace('8', 'ffffffff')
    fen = fen.replace('/', '')
    fen = fen.replace('\n', '')

    return fen


def start_from_dir():
    chessboards_dir = '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/cb_sample_300/'
    chessboard_images = utils.get_filenames_from_dir(chessboards_dir)
    chessboard_images.sort(key=utils.alphanum_key)

    fen_list = utils.get_lines_from_file('./sample_data/fen-201-300.txt')
    print(chessboard_images)
    for i in range(len(chessboard_images)):

        img_path = Path(chessboards_dir).joinpath(chessboard_images[i])
        img = Image.open(img_path)
        img = img.resize((512, 512))
        arr = np.asarray(img)
        tiles = tile_splitter.split_img(arr, 64, 64)
        fen = expand_fen(fen_list[i])
        tiles = enumerate(tiles)
        print(i, chessboard_images[i], fen_list[i])

        for count, tile in tiles:
            tile_img = Image.fromarray(np.uint8(tile))
            fen_folder_name = f'./test/data/_{fen[count]}'
            Path(fen_folder_name).mkdir(parents=True, exist_ok=True)
            tile_img.save(
                f'{fen_folder_name}/{chessboard_images[i]}-{count}.jpg')


def start_from_single_img():
    # G:/Documents/Chess/1001 Chess Exercises for Club Players/output/chessboard
    img = Image.open(
        '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/chessboard/Image-1.jpg')
    sample_fen = 'k2r3r/p1Rp4/1p4p1/n3R2p/3P1B2/1q4P1/5P1P/3Q2K1'
    img = img.resize((512, 512))
    arr = np.asarray(img)
    tiles = tile_splitter.split_img(arr, 64, 64)
    fen = expand_fen(sample_fen)
    tiles = enumerate(tiles)

    for count, tile in tiles:
        tile_img = Image.fromarray(np.uint8(tile))
        fen_folder_name = f'./test/data/_{fen[count]}'
        Path(fen_folder_name).mkdir(parents=True, exist_ok=True)
        tile_img.save(f'{fen_folder_name}/{uuid.uuid4()}.jpg')


if __name__ == '__main__':
    start_from_dir()
    # start_from_single_img()
