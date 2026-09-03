from pdf_information_extractor import PDFInformationExtractor

def main():
    
    while True:
        try:
            pdf_path = input("Enter the path of the PDF you want to open: ")
            
            if not pdf_path.strip():
                raise Exception("PDF path cannot be empty")
            
            pdf_information_extractor = PDFInformationExtractor(pdf_path)
            pdf_information_extractor.open_file()
            break
        
        except Exception as e:
            print(f"Error {e}")
        
    while True:
        try:
            
            operation = int(input(("Enter the operation you want to perform: \n1. Display total number of pages\n2. Extract text from the pages\n3. Search for a Keyword\n4. Generate Summary\n5. Exit\n")))
             
            if operation == 1:
                page_count = pdf_information_extractor.get_page_count()
                print(f"Total number of pages in the PDF are: {page_count}") 
                  
            elif operation == 2:
                extracted_text = pdf_information_extractor.extract_text()
                pdf_information_extractor.save_results()
                
                choice_to_view_results = input("Do you want to view the saved results? Y/N: ")
                
                if choice_to_view_results.upper() == "Y":
                    print(extracted_text)  
                                
            elif operation == 3:
                keyword = input("Enter the word that you want to search: ")
                
                if(pdf_information_extractor.search_keyword(keyword.strip())):
                    print(f"{keyword} found in the PDF do you also want to search the page where it is present? ", end = " ")
                    choice = input("Y/N: ")
                    
                    if choice.upper() == "Y":
                        pdf_information_extractor.get_matching_pages(keyword.strip())
                        
                else:
                    print("No such word found in the PDF")
                    
            elif operation == 4:
                pdf_information_extractor.generate_summary()
                
            elif operation == 5:
                print("Exit Successful!!")
                break
            
            else:
                print("Wrong option select again from the above given choices!!")
                
        except ValueError as e:
            print(f"Error {e}. Enter a valid value")
            
        except Exception as e:
            print(f"Error {e}. Try again!!")
            
if __name__ == "__main__":
    main()