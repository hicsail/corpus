import xlrd


def to_list(row):

    ret = []

    for cell in row:
        ret.append(cell.value)

    return ret


def is_ht(row):

    if row[7] == 'N/A' or row[7] == "" or row[7] == "HT ID":
        return False
    else:
        return True


def is_lit_banken(row):
    tmp = row[10].split()

    for t in tmp:
        if t.strip()[0:11] == 'https://lit':
            return True

    return False

def has_link(row):
    tmp = row[10].split()

    for t in tmp:
        if t.strip()[0:4] == 'http':
            return True

    return False


def format_ht(row):

    ret = []

    ret.append(row[7])
    ret.append(row[0])
    ret.append(row[1])
    ret.append(' '.join([row[5], row[6]]))

    return ret


def format_banken(row):

    ret = []

    tmp = row[10].split()
    link = ''
    for t in tmp:
        if t.strip()[0:5] == 'https':
            link = t.strip()

    ret.append(link)
    ret.append(row[0])
    ret.append(row[1])
    ret.append(' '.join([row[5], row[6]]))

    return ret

def format_other(row):

    ret = []

    tmp = row[10].split()
    link = ''

    for t in tmp:
        if t.strip()[0:4] == 'http':
            link = t.strip()

    ret.append(link)
    ret.append(row[0])
    ret.append(row[1])
    ret.append(' '.join([row[5], row[6]]))

    return ret


if __name__ == '__main__':

    vols = xlrd.open_workbook('/Users/ben/Downloads/swedish.xlsx')
    sh = vols.sheet_by_index(0)

    all_recs = []

    for row in sh.get_rows():
        all_recs.append(to_list(row))

    ht_recs = []
    banken = []
    others = []

    for row in all_recs:
        if is_ht(row):
            ht_recs.append(format_ht(row))
        elif is_lit_banken(row):
            banken.append(format_banken(row))
        elif has_link(row):
            others.append(format_other(row))

    with open('/Users/ben/Desktop/swedish_ht.csv', 'w') as ht_out:
        for rec in ht_recs:
            ht_out.write(','.join(str(i) for i in rec))
            ht_out.write('\n')

    with open('/Users/ben/Desktop/swedish_banken.csv', 'w') as banken_out:
        for rec in banken:
            banken_out.write(','.join(str(i) for i in rec))
            banken_out.write('\n')

    with open('/Users/ben/Desktop/swedish_other.csv', 'w') as other_out:
        for rec in others:
            other_out.write(','.join(str(i) for i in rec))
            other_out.write('\n')
