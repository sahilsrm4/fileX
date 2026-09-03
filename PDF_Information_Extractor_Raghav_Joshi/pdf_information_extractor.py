import pypdf
import re


class PDFInformationExtractor:
    
    def __init__(self, pdf_path = None):
        self.pdf_path = pdf_path
        self.text = None
        
        
    def open_file(self): #Funtion to open the file
        
        pattern = r"\.pdf$"
        if not re.search(pattern, self.pdf_path, re.IGNORECASE):
            raise Exception("Please upload a PDF file only")
        
        try:
            pdf_reader = pypdf.PdfReader(self.pdf_path)
            self.pdf_reader = pdf_reader
            print("File Opened Successfully!!")
            
        except FileNotFoundError:
            raise Exception("No such file found. Try again !!")
        
        except Exception as e:
            raise Exception("Invalid PDF file!!")
            
            
    def get_page_count(self): #Funtion to get total number of pages in PDF
        
        return len(self.pdf_reader.pages)
    
    
    def extract_text(self): #Function to extract text
        total_text = ""
        
        for p in range(len(self.pdf_reader.pages)):
            page = self.pdf_reader.get_page(p)
            total_text += page.extract_text() or ""
        self.text = total_text
        
        if not self.text.strip():
            raise Exception("PDF File is Empty!!")
        
        return self.text
    
    
    def save_results(self): #Function to save the extracted text
        
        with open("extracted_text_file.txt","w",encoding="utf-8") as extracted_text_file:
            extracted_text_file.write(self.text)
        
            
    def search_keyword(self,keyword): #Fncntion to search a keyword 
        
        if self.text is None or not self.text.strip():
            self.extract_text()
            
        if(not keyword.strip()):
            raise Exception("Keyword cannot be empty")
        
        elif(re.search(rf"\b{re.escape(keyword)}\b", self.text, re.IGNORECASE)):
            return True
        
        else:
            return False
        
        
    def get_matching_pages(self,keyword): #Funtion to get the page number where the keyword is present
        
        page_number = 1
        
        for page in self.pdf_reader.pages:
            page_text = page.extract_text() or ""
            if (re.search(rf"\b{re.escape(keyword)}\b", page_text, re.IGNORECASE)):
                print(f"{keyword} found on page number: {page_number}")
            page_number+=1
        
            
    def generate_summary(self): #Function to generate summary
        
        if self.text is None or not self.text.strip():
            self.extract_text()
            
        total_words = self.text.split()
        longest_word = ""
        shortest_word = total_words[0]
        
        for word in total_words:
            if len(word) >= len(longest_word):
                longest_word = word
            if len(word) <= len(shortest_word):
                shortest_word = word
                
        print(f"The title of this PDF is {self.pdf_reader.metadata.title}")
        print(f"Total number of pages in this PDF are {len(self.pdf_reader.pages)}")
        print(f"Total words in this PDF are {len(total_words)}")
        print(f"Longest word in this PDF is ({longest_word})")
        print(f"Shortest word in this PDF is ({shortest_word})")