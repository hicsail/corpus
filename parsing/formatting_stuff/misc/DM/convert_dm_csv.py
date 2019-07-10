import sys
import csv

all_recs = [["id of xml file", "Author", "Title", "Date"]]


def filter_date(d):
    try:
        return int(d)
    except ValueError:
        if d[0] == "c":
            return int(d[-4:])
        else:
            return int(d.split('-')[0])


with open(sys.argv[1], 'r', encoding='utf-8') as unparsed:
    read_csv = csv.reader(unparsed, delimiter=',')
    for row in read_csv:
        if row[0] != "Date":
            new_rec = []

            # id, author, title, date

            if row[6] != "":
                new_rec.append(row[6])
            else:
                continue

            new_rec.append(row[1])
            new_rec.append(row[2])

            if row[0] != "":
                new_rec.append(filter_date(row[0]))
            else:
                continue

            all_recs.append(new_rec)


with open(sys.argv[2], 'w', encoding='utf-8') as parsed:
    wr = csv.writer(parsed, quoting=csv.QUOTE_ALL)

    sorted_recs = all_recs.sort(key=lambda x: x[0])

    for r in all_recs:
        wr.writerow(r)
