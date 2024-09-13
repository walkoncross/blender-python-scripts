import csv


def load_livelinkface_csv(csv_path: str) -> dict:
    '''
    Load and parse the contents of a LiveLinkFace CSV file from the specified path.

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
        bs_names = row[2:-9]
        joint_names = row[-9:]


        for row in csv_reader:
            time_codes.append(row[0])
            bs_frames.append([float(item) for item in row[2:-9]])
            joint_frames.append([float(item) for item in row[-9:]])

    return {
        'time_codes': time_codes,
        'blendshape_names': bs_names,
        'blendshape_frames': bs_frames,
        'joint_names': joint_names,
        'joint_frames': joint_frames
    }


if __name__=='__main__':
    csv_path = r'/Users/zhaoyafei/dl-bk/LiveLinkFace_data/20210129_MySlate_3/MySlate_3_JAMESs_iPhone12Pro.csv'
    loaded_data = load_livelinkface_csv(csv_path)
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
