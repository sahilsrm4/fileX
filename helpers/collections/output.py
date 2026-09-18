class Output():
    def __init__(self):
        self.output_list = []
    
    def write(self,data:str):
        if "\n" in data:
            data_list = data.split("\n")
            self.output_list.extend(data_list)
        else:
            self.output_list.append(data)
    
    def __str__(self):
        output_for_print = "\n".join(self.output_list)
        return output_for_print