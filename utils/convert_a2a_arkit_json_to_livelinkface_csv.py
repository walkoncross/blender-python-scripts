import os
import os.path as osp

import json
import csv

import base64
from io import BytesIO
import wave


first_2_cols_in_livelinkface = [
    "Timecode",
    "BlendShapeCount",
]

arkit_bs_keys_in_livelinkface = [
    'eyeBlinkRight',
    'eyeLookDownRight',
    'eyeLookInRight',
    'eyeLookOutRight',
    'eyeLookUpRight',
    'eyeSquintRight',
    'eyeWideRight',
    'eyeBlinkLeft',
    'eyeLookDownLeft',
    'eyeLookInLeft',
    'eyeLookOutLeft',
    'eyeLookUpLeft',
    'eyeSquintLeft',
    'eyeWideLeft',
    'jawForward',
    'jawRight',
    'jawLeft',
    'jawOpen',
    'mouthClose', # jawOpenMouthClose
    'mouthFunnel',
    'mouthPucker',
    'mouthRight',
    'mouthLeft',
    'mouthSmileRight',
    'mouthSmileLeft',
    'mouthFrownRight',
    'mouthFrownLeft',
    'mouthDimpleRight',
    'mouthDimpleLeft',
    'mouthStretchRight',
    'mouthStretchLeft',
    'mouthRollLower',
    'mouthRollUpper',
    'mouthShrugLower',
    'mouthShrugUpper',
    'mouthPressRight',
    'mouthPressLeft',
    'mouthLowerDownRight',
    'mouthLowerDownLeft',
    'mouthUpperUpRight',
    'mouthUpperUpLeft',
    'browDownRight',
    'browDownLeft',
    'browInnerUp',
    'browOuterUpRight',
    'browOuterUpLeft',
    'cheekPuff',
    'cheekSquintRight',
    'cheekSquintLeft',
    'noseSneerRight',
    'noseSneerLeft',
    # 'tongueOut',
    # 'HeadYaw',
    # 'HeadPitch',
    # 'HeadRoll',
    # 'LeftEyeYaw',
    # 'LeftEyePitch',
    # 'LeftEyeRoll',
    # 'RightEyeYaw',
    # 'RightEyePitch',
    # 'RightEyeRoll'
]

def convert_a2a_json_to_livelinkface_csv(
    a2a_json_path, 
    save_dir='./converted_livelinkface_csv'
):
    """convert_a2a_json_to_livelinkface_csv

    Args:
        a2a_json_path (_type_): input json path
        save_dir (str, optional): where to save output .wav and .csv files. Defaults to './converted_livelinkface_csv'.
    """
    base_name_root = osp.splitext(osp.basename(a2a_json_path))[0]

    fp = open(a2a_json_path, 'r')
    a2a_frames = json.load(fp)
    fp.close()

    if not save_dir:
        save_dir = './output'

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    combined_wav_fn = osp.join(save_dir, base_name_root + '.combined.wav')
    combined_wav_fp = wave.open(combined_wav_fn, 'wb')

    output_arkit_bs_path = osp.join(save_dir, base_name_root + '.arkit_bs.csv')

    csv_fp = open(output_arkit_bs_path, 'w')
    csv_writer = csv.writer(csv_fp)
    csv_writer.writerow(first_2_cols_in_livelinkface + arkit_bs_keys_in_livelinkface)

    for ii, frame_data in enumerate(a2a_frames):
        print('===> a2a frame #', ii)

        # deal with audio
        audio_enc = frame_data["frame"]["animation"]["agent"]["audio"]
        audio_dec = base64.b64decode(audio_enc)

        ff = BytesIO(audio_dec)
        wav_handle = wave.open(ff, 'rb')

        if ii==0:
            print('-' * 16 + ' audio info:')
            print('     nchanenels: ', wav_handle.getnchannels())
            print('     sampwidth: ', wav_handle.getsampwidth())
            print('     framerate: ', wav_handle.getframerate())
            print('     nframes', wav_handle.getnframes())
            combined_wav_fp.setparams(wav_handle.getparams())
        
        combined_wav_fp.writeframes(wav_handle.readframes(wav_handle.getnframes()))

        wav_handle.close()

        # deal with bs values
        arkit_bs = frame_data["frame"]["animation"]["agent"]["values"]
        # print('--> arkit_bs: \n', arkit_bs)
    
        write_list = [ii, 51]

        for kk in arkit_bs_keys_in_livelinkface:
            val = arkit_bs[kk]
            write_list.append(val)
        
        csv_writer.writerow(write_list)

    combined_wav_fp.close()
    
    csv_fp.close()


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Convert a2a-arkit json into LiveLinkFace format .csv file,'
                                      'and combine audio clips into one .wav file.')
    parser.add_argument(
        'json_path',
        default='/Users/zhaoyafei/Downloads/a2a-dimo-arkit/ar_dimo.json',
        nargs='?',
        type=str,
        help='path to input text file'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        default='./converted_livelinkface_csv',
        type=str,
        help='where to save converted .wav and .csv files'
    )

    args = parser.parse_args()
    print('=' * 32)
    print('Input args: ')
    print(args)

    convert_a2a_json_to_livelinkface_csv(
        args.json_path,
        args.output_dir
    )
