import os


def rename_files_in_directory(directory_path):
    """
    Rename all files in the given directory to 1.obj, 2.obj, and so on.

    Args:
        directory_path (str): The path to the directory containing the files to be renamed.
    """
    files = sorted([f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])

    for idx, filename in enumerate(files, 1):
        old_path = os.path.join(directory_path, filename)
        new_path = os.path.join(directory_path, f"{idx}.obj")
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")


if __name__ == "__main__":
    dir_path = input("Enter the directory path: ")
    rename_files_in_directory(dir_path)
