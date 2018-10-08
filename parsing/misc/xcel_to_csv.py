import xlrd
import csv


class XcelToCsv:
    """
    Converts xlsx to csv because I hate using xlrd
    """

    def __init__(self, input_path, output_path="/tmp"):

        self.input_path = input_path
        self.output_path = output_path

    def load_sheets(self):

        wb = xlrd.open_workbook(self.input_path)

        return wb.sheets()

    def convert_and_write(self):

        sheets = self.load_sheets()

        for s in sheets:

            with open("{0}/{1}.csv".format(self.output_path, s.name), 'w') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_ALL)

                for j in range(s.nrows):
                    wr.writerow(s.row_values(j)[:7])
