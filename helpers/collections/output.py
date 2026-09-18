class Output:
    def __init__(self):
        self.output_list = []

    def write(self, data: object):
        data_str = str(data)

        if not data_str:
            return

        lines = data_str.split("\n")

        if self.output_list:
            self.output_list[-1] += lines[0]
        else:
            self.output_list.append(lines[0])

        self.output_list.extend(lines[1:])

    def __str__(self):
        return "\n".join(self.output_list)