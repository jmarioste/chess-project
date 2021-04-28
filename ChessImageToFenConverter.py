from os import path

import json
import ChessVisionWrapper as cvw
import constants as const
import utils

class ChessImageToFenConverter:
    def __init__(self, chess_vision_wrapper):
        print('init ChessImageToFenConverter')
        self.wrapper = chess_vision_wrapper
        pass
    
    def construct_json_data(self, base64str):
        data = {
            'image': base64str,
            'flip': False
        }

        return json.dumps(data)

    def invoke_lambda(self, data):
        return self.wrapper.invoke_lambda_fn(const.AWS_FUNCTION_NAME, data)


    def get_fen_from_file(self, file_path):
        base64str = utils.img_to_base64(file_path)
        data = self.construct_json_data(base64str)
        response_data = self.invoke_lambda(data)
        fen = response_data['FEN']
        print(fen)

        return fen

    def get_fens_from_dir(self, file_dir):
        # chessboards_dir = '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/cb_sample_300/'
        filenames = utils.get_filenames_from_dir(file_dir)
        filenames.sort(key=utils.alphanum_key)
        fens = []
        
        for filename in filenames:
            file_path = path.join(file_dir, filename)
            fen = self.get_fen_from_file(file_path)
            fens.append(fen)
        
        print(len(fens))

        return fens


if __name__ == '__main__':
    wrapper = cvw.ChessVisionWrapper(
            const.AWS_IDENTITY_POOL_ID,
            const.AWS_REGION_NAME)
    converter = ChessImageToFenConverter(wrapper)
    # converter.get_fen_from_file('./img/Image-2.jpg')
    converter.get_fens_from_dir('./img')