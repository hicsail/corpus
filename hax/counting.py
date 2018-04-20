


with open('/Users/ben/Desktop/swedish_banken.csv', 'r') as rfile:
    reader = rfile.read()

    ret = []

    for l in reader.split('\n'):
        recs = l.split(',')
        if recs[0].split('/')[-1].strip() == 'faksimil':
            ret.append(l)


with open('/Users/ben/Desktop/omitted_lb.csv', 'w') as ofile:

    ofile.write('\n'.join(ret))

