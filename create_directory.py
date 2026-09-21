import os
import exceptions
from report_gen import Report_Gen

report = Report_Gen()


def create_directory(args: list = [], options: list = []):
    """
    Create a directory.

    The first argument is the directory name to create.
    The second argument is the parent path where the directory will be created.
    If the parent path is not provided, the current working directory is used.
    """
    try:
        if len(args) == 0:
            raise ValueError("Directory name is required")

        if len(args) > 2:
            raise ValueError("Expected directory name and optional parent path")

        directory_name = args[0]
        parent_path = args[1] if len(args) == 2 else os.getcwd()

        if not os.path.exists(parent_path):
            raise exceptions.PathNotExist(parent_path)

        if not os.path.isdir(parent_path):
            raise exceptions.PathNotExist(parent_path)

        directory_path = os.path.join(parent_path, directory_name)

        if os.path.exists(directory_path):
            raise FileExistsError(f"Directory already exists: {directory_path}")

        os.makedirs(directory_path)
        report.write_log(f"Directory successfully created: {directory_path}\n")
        print(f"Directory successfully created: {directory_path}")
        return directory_path

    except Exception as e:
        print(e)
        report.write_log(str(e) + "\n")
        return None


if __name__ == "__main__":
    create_directory(args=["new_directory"])
