# FileX — Command-Line File Automation Utility

FileX is a command-line file automation utility written in Python. It provides a simple interface for performing common file and directory operations such as listing files, searching files, retrieving file information, copying and renaming files, generating directory summaries, and generating reports.

The tool can be used directly through Python or as a standalone executable.

---

## Features

FileX currently provides the following functionality:

* List files in a directory
* Search files by name or extension
* Search recursively through directories
* Display file information
* Copy files to another directory
* Rename files
* Generate directory summaries
* Generate reports
* Maintain command execution logs
* Automatically create a log directory
* Command-line executable support

---

## Available Commands

| Command   | Description                           |
| --------- | ------------------------------------- |
| `lsfile`  | List files in a directory             |
| `dirs`    | Generate a directory summary          |
| `info`    | Display information about a file      |
| `search`  | Search for files by name or extension |
| `copyf`   | Copy a file to another directory      |
| `renamef` | Rename a file                         |
| `help`    | Display available commands            |

---

# Installation

## Option 1 — Run using Python

To run FileX using Python, Python must be installed on your system.

Clone or download the project and navigate to the project directory:

```bash
cd path/to/fileX
```

Run the tool using:

```bash
python fileX.py <command> <arguments>
```

For example:

```bash
python fileX.py lsfile
```

> **Requirement:** Python must be installed and available from your command line.

You can verify your Python installation with:

```bash
python --version
```

---

## Option 2 — Run using `fileX.exe`

FileX also provides a standalone executable:

```text
fileX.exe
```
`fileX.exe` is present in the fileX folder of the github repositry you can download `fileX.exe` from there

You can add the directory containing `fileX.exe` to your system's `PATH` environment variable.

After adding it to `PATH`, FileX can be executed directly from the command line:

```bash
fileX <command> <arguments>
```

For example:

```bash
fileX lsfile
```

This allows you to use FileX as a normal command-line utility without explicitly running:

```bash
python fileX.py
```

---

# Command Usage

## 1. `lsfile`

Lists files in a directory.

### Usage

```bash
python fileX.py lsfile [directory]
```

or, if `fileX.exe` is in your `PATH`:

```bash
fileX lsfile [directory]
```

### Arguments

```text
0 or 1
```

If no directory is provided, the tool uses the default/current directory.

### Examples

```bash
fileX lsfile
```

```bash
fileX lsfile C:\Users\dell\Documents
```

---

# 2. `dirs`

Generates a summary of a directory.

### Usage

```bash
python fileX.py dirs [directory]
```

### Arguments

```text
0 or 1
```

### Examples

```bash
fileX dirs
```

```bash
fileX dirs C:\Users\dell\Documents
```

### Recursive Summary

The `dirs` command supports recursive processing.

Use:

```bash
-r
```

or:

```bash
--recursive
```

to include files and directories inside subdirectories.

### Example

```bash
fileX dirs C:\Users\dell\Documents -r
```

or:

```bash
fileX dirs C:\Users\dell\Documents --recursive
```

Without the recursive option, only the specified directory is processed.

---

# 3. `info`

Displays information about a file.

### Usage

```bash
python fileX.py info <file> [directory]
```

### Arguments

```text
1 or 2
```

### Example

```bash
fileX info rocket.obj
```

The command can be used to retrieve information and metadata associated with the specified file.

---

# 4. `search`

Searches for files by name or extension.

### Usage

```bash
python fileX.py search <pattern/file> [directory] [-r | --recursive ]
```

### Arguments

```text
1 or 2
```

### Examples

Search for a specific filename:

```bash
fileX search rocket.obj C:\Users\dell\Documents
```

Search using a file extension or pattern:

```bash
fileX search .txt C:\Users\dell\Documents
```

### Recursive Search

The `search` command supports recursive searching.

Use:

```bash
-r
```

or:

```bash
--recursive
```

### Example

```bash
fileX search rocket.obj C:\Users\dell\Documents -r
```

or:

```bash
fileX search .txt C:\Users\dell\Documents --recursive
```

When recursive mode is enabled, FileX searches the specified directory and its subdirectories.

---

# 5. `copyf`

Copies a file to another location.

### Usage

```bash
python fileX.py copyf <source> <destination>
```

### Arguments

```text
2
```

### Example

```bash
fileX copyf C:\Users\dell\Documents\rocket.obj C:\Users\dell\Desktop
```

The source file is copied to the specified destination.

---

# 6. `renamef`

Renames a file.

### Usage

```bash
python fileX.py renamef <old_name> <new_name>
```

### Arguments

```text
2
```

### Example

```bash
fileX renamef old_name.txt new_name.txt
```

The file:

```text
old_name.txt
```

will be renamed to:

```text
new_name.txt
```

---

# 7. `help`

Displays the available commands and their usage.

### Usage

```bash
fileX help
```

or:

```bash
python fileX.py help
```

Example output:

```text
Command-Line File Automation Utility
=============================================

Available commands:

lsfile
  List files in a directory.
  Usage: python mytool.py lsfile [directory]
  Arguments: 0 or 1

dirs
  Generate a summary of a directory.
  Usage: python mytool.py dirs [directory]
  Arguments: 0 or 1

info
  Display information about a file.
  Usage: python mytool.py info <file> [option]
  Arguments: 1 or 2

search
  Search for files by name or extension.
  Usage: python mytool.py search <directory> [pattern]
  Arguments: 1 or 2

copyf
  Copy a file to another directory.
  Usage: python mytool.py copyf <source> <destination>
  Arguments: 2

renamef
  Rename a file.
  Usage: python mytool.py renamef <old_name> <new_name>
  Arguments: 2

help
  Display this help message.
  Usage: python mytool.py help
  Arguments: 0
```

---

# Logging

FileX maintains a history of command execution through log files.

A directory named:

```text
log_folder
```

is automatically created in the directory from which FileX is executed.

For example:

```text
fileX/
│
├── fileX.py
├── ...
└── log_folder/
```

The log directory is created automatically when required.

Each command's execution history is stored in the `log_folder`.

Log files contain a date and time timestamp in their filename, allowing command executions to be identified chronologically.

Example:

```text
log_folder/
├── log_2026-09-01_10-30-15.log
├── log_2026-09-01_11-15-42.log
└── log_2026-09-02_09-20-11.log
```

This makes it possible to review previous FileX operations and troubleshoot command execution.

---

# Project Structure

A typical FileX project structure looks like:

```text
FileX/
│
├── fileX.py
├── list_file.py
├── search_file.py
├── info.py
├── copy_file.py
├── rename_file.py
├── directory_summary.py
├── report_gen.py
|__ exceptions.py
│
└── log_folder/
```

The main functionality is separated into individual Python modules.

| Module                 | Responsibility                              |
| ---------------------- | ------------------------------------------- |
| `fileX.py`             | Command-line interface and command handling |
| `list_file.py`         | File/directory listing                      |
| `search_file.py`       | File searching                              |
| `info.py`              | File information                            |
| `copy_file.py`         | File copying                                |
| `rename_file.py`       | File renaming                               |
| `directory_summary.py` | Directory summaries                         |
| `report_gen.py`        | Report generation class                     |
| `exceptions.py`        | Keep all the custom exceptions and errors   |
| `log_folder/`          | Command execution logs                      |

---

# Error Handling

FileX validates command arguments and handles common filesystem errors.

For example, operations may fail when:

* A specified file does not exist
* A directory does not exist
* The user does not have permission to access a location
* A destination already exists
* An invalid command is supplied
* An incorrect number of arguments is provided
* Source Path not Exist
* Destination Path Not Exist
* Not a file path
* Not a directory path
* Exact file Not exist
* Not string 
* Not supported option
* Path length greater than 260


Protected Windows directories may also return permission errors. FileX should handle these errors gracefully rather than terminating unexpectedly.

---

# Examples

### List current directory

```bash
fileX lsfile
```

### List a specific directory

```bash
fileX lsfile C:\Users\dell\Documents
```

### Generate directory summary

```bash
fileX dirs C:\Users\dell\Documents
```

### Generate recursive directory summary

```bash
fileX dirs C:\Users\dell\Documents -r
```

### Search for a file

```bash
fileX search rocket.obj C:\Users\dell\Documents
```

### Recursively search for a file

```bash
fileX search rocket.obj C:\Users\dell\Documents --recursive
```

### Get file information

```bash
fileX info C:\Users\dell\Documents\rocket.obj
```

### Copy a file

```bash
fileX copyf C:\Users\dell\Documents\rocket.obj C:\Users\dell\Desktop
```

### Rename a file

```bash
fileX renamef old.txt new.txt
```

### Display help

```bash
fileX help
```

---

# Command Overview

```text
fileX lsfile [directory]

fileX dirs [directory] [-r | --recursive]

fileX info <file> [option]

fileX search [pattern] <directory> [-r | --recursive]

fileX copyf <source> <destination>

fileX renamef <old_name> <new_name>

fileX help
```

---

# Technologies

FileX is implemented using Python and its built-in standard library.

No third-party Python packages are required for the core functionality.

---

# Future Improvements

Possible future enhancements include:

* More advanced file pattern matching
* Improved recursive search
* File filtering by size and date
* Additional file metadata
* Configurable logging
* Improved report formats
* Command aliases
* Better error reporting
* Progress indicators for large operations
* Configuration files
* More advanced command-line argument parsing

---

 

## Author

**Sahil**

FileX — Command-Line File Automation Utility
