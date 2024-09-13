"""Load and parse the contents of a Nvidia audio2face NIM returned CSV file from the specified path.

Author: zhaoyafei0210@gmail.com
"""

import csv


def load_nv_a2f_csv(csv_path: str) -> dict:
    '''
    Load and parse the contents of a Nvidia audio2face NIM returned CSV file from the specified path.

    This function reads the CSV file, extracts the header row and all data rows.

    Parameters:
    csv_path (str): The path to the CSV file

    Returns:
    dict: A dictionary containing:
        - 'time_codes': List of time codes
        - 'blendshape_names': List of blendshape names
        - 'blendshape_frames': List of blendshape data rows
        - 'joint_names': List of joint names
        - 'joint_frames': List of joint data rows
    '''
    time_codes = []
    bs_names = []
    bs_frames = []
    joint_frames = []
    time_codes = []

    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        row = next(csv_reader)
        bs_names = [item.split('.')[-1] for item in row[2:-3]] # remove prefix "blendShapes."
        bs_names = [name[0].lower()+name[1:] for name in bs_names] # lower case the first letter
        joint_names = [item.split('.')[-1] for item in row[-3:]] # remove prefix "blendShapes."
        joint_names = [name[0].lower()+name[1:] for name in joint_names] # lower case the first letter

        for row in csv_reader:
            time_codes.append(row[1])
            bs_frames.append([float(item) for item in row[2:-3]])
            joint_frames.append([float(item) for item in row[-3:]])

    return {
        'time_codes': time_codes,
        'blendshape_names': bs_names,
        'blendshape_frames': bs_frames,
        'joint_names': joint_names,
        'joint_frames': joint_frames
    }


if __name__=='__main__':
    csv_path = r'/Users/zhaoyafei/work/NIM-audio2face-visualization/viz-threejs/assets/animation_frames.csv'
    loaded_data = load_nv_a2f_csv(csv_path)
    print('-' * 16)
    print(f"time_codes[:10]: {loaded_data['time_codes'][:10]}")
    print('-' * 16)
    print(f"blendshape_names: {loaded_data['blendshape_names']}")
    print(f"blendshape_frames[:2]: {loaded_data['blendshape_frames'][:2]}")
    print(f"blendshape_frames[-2:]: {loaded_data['blendshape_frames'][-2:]}")
    print('-' * 16)
    print(f"joint_names: {loaded_data['joint_names']}")
    print(f"joint_frames[:2]: {loaded_data['joint_frames'][:2]}")
    print(f"joint_frames[-2:]: {loaded_data['joint_frames'][-2:]}")
