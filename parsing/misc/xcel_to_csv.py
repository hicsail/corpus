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

    @staticmethod
    def filter_row(vals):

        ret = []

        for s in vals:
            if isinstance(s, str):
                ret.append(s.replace(",", ""))
            elif isinstance(s, float):
                ret.append(int(s))
            else:
                ret.append(s)

        return ret

    def convert_and_write(self):

        sheets = self.load_sheets()

        for s in sheets:

            with open("{0}/{1}.csv".format(self.output_path, s.name), 'w') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_ALL)

                for j in range(s.nrows):
                    wr.writerow(self.filter_row(s.row_values(j)[:7]))
