from PIL import Image
import numpy as np

#split image
#split fen
#map image to fen
#create uuid filename for image
#save the image to the specified fen label

def split_img(img, width, length):

    img_width = img.shape[0]
    img_length = img.shape[1]
        
    tiles = []
    for x in range(0, img_width, width): 
        for y in range(0, img_length, length):
            cropped = img[x:x+width, y:y+length]
            tiles.append(cropped)
    
    return tiles

def sample_diff_func():
    return None

if __name__ == '__main__':
    img = Image.open('./img/example1.png').convert('RGB')
    img = img.resize((512,512))
    arr = np.asarray(img)
    tiles = split_img(arr, 64, 64)
    print()

    tiles = enumerate(tiles)
    

    for count, tile in tiles:
        tile_img = Image.fromarray(np.uint8(tile))
        tile_img.save(f'./test/Image-{count}.jpg')
    