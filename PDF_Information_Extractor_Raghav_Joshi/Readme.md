## PDF Information Extractor

## Project Description:

PDF Information Extractor is a Python-based application used to extract and analyze information from PDF files. The application provides a simple menu-driven interface through which users can view the number of pages, extract text, search for keywords, and generate a summary of the PDF.

## Implemented Features:

* Open and read PDF files.
* Display the total number of pages in a PDF.
* Extract text from all pages of a PDF.
* Save the extracted text to a text file.
* Search for a specific keyword in the PDF.
* Find the page numbers where a keyword is present.
* Generate a basic summary containing:

  * PDF title
  * Total number of pages
  * Total number of words
  * Longest word
  * Shortest word
* Handle invalid file paths and invalid input.
* Check whether the provided file has a `.pdf` extension.

Instructions to Run the Application

## 1. Install Python

Make sure Python is installed on your system.

## 2. Install the Required Package

Open the terminal in the project directory and run:

```bash
pip install pypdf
```

## 3. Run the Application

Run the following command:

```bash
python main.py
```

## 4. Enter the PDF Path

When prompted, enter the path of the PDF file you want to process.


After opening the PDF, select an operation from the menu.

## Known Limitations

* The application currently works with PDF files only.
* PDF's that are made using compiled images may not return any valid data
* The generated summary is displayed in the terminal and is not currently saved to a separate file.
* The summary provides basic information rather than a detailed natural-language summary.
