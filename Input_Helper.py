import os.path


# raise exception if the path does not finish with a '/'
def check_if_path_is_dir(the_input_path):
    # os.path.split(home/some/path/)[1] outputs ''
    # os.path.split(home/some/path)[1] outputs 'path'
    if not os.path.split(the_input_path)[1] == '':
        raise OSError("Path is not a directory.\nPlease recheck the parameter file, all 'paths' should end with a '/' character.")


def main():
    with open("./Input_SINS_Pipeline.par", 'r') as inF:
        for line in inF:
            if 'PATH_TO_' in line:
                if line.split()[0] != '#':
                    path_to_a_folder = line.split()[2]
                    print path_to_a_folder
                    check_if_path_is_dir(path_to_a_folder)
