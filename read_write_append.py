import os
import exceptions
from report_gen import Report_Gen
from helpers.collections.output import Output


report = Report_Gen()


def read_file(args: list = [], options: list = []):
    """
    Read the contents of a file.

    args[0] -> file name/path
    options -> initially empty
    """

    try:
        # Parse arguments
        if len(args) == 1:
            file = args[0]
        else:
            raise exceptions.ArgumentError(
                "read_file",
                ["file"],
                args
            )

        # Check whether path exists
        if not os.path.exists(file):
            raise exceptions.FileNotExist(file)

        # Check whether the path is actually a file
        if not os.path.isfile(file):
            raise exceptions.NotAFilePath(file)

        # Read file
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        # Store output in custom Output object
        output_obj = Output()

        print(content, file=output_obj)

        report.write_log(
            f"File successfully read -> {file}\n"
        )

        return output_obj

    except Exception as e:
        print(e)
        report.write_log(str(e) + "\n")


def write_file(args: list = [], options: list = []):
    """
    Write content to a file.

    args[0] -> file name/path
    args[1] -> content
    options -> initially empty

    If the file already exists, its content will be overwritten.
    """

    try:
        # Parse arguments
        if len(args) == 2:
            file = args[0]
            content = args[1]
        else:
            raise exceptions.ArgumentError(
                "write_file",
                ["file", "content"],
                args
            )

        # Validate parent directory if a directory is explicitly provided
        parent_directory = os.path.dirname(os.path.abspath(file))

        if not os.path.exists(parent_directory):
            raise exceptions.PathNotExist(parent_directory)

        # Check that existing path is not a directory
        if os.path.exists(file) and not os.path.isfile(file):
            raise exceptions.NotAFilePath(file)

        # Write content
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

        report.write_log(
            f"File successfully written -> {file}\n"
        )

        output_obj = Output()

        print(
            f"File successfully written -> {file}",
            file=output_obj
        )

        return output_obj

    except Exception as e:
        print(e)
        report.write_log(str(e) + "\n")


def append_file(args: list = [], options: list = []):
    """
    Append content to a file.

    args[0] -> file name/path
    args[1] -> content
    options -> initially empty
    """

    try:
        # Parse arguments
        if len(args) == 2:
            file = args[0]
            content = args[1]
        else:
            raise exceptions.ArgumentError(
                "append_file",
                ["file", "content"],
                args
            )

        # Check whether file exists
        if not os.path.exists(file):
            raise exceptions.FileNotExist(file)

        # Check whether path is actually a file
        if not os.path.isfile(file):
            raise exceptions.NotAFilePath(file)

        # Append content
        with open(file, "a", encoding="utf-8") as f:
            f.write(content)

        report.write_log(
            f"Content successfully appended -> {file}\n"
        )

        output_obj = Output()

        print(
            f"Content successfully appended -> {file}",
            file=output_obj
        )

        return output_obj

    except Exception as e:
        print(e)
        report.write_log(str(e) + "\n")


if __name__ == "__main__":

    result = read_file(
        args=["test1.txt"]
    )

    print(result)

