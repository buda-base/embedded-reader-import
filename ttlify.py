
file = "collections/W0CJ001.txt"

col = []
longest = 0


def addIndex(col):
    maxRowLen = len(max(col, key=len))

    collection = []

    for row in col:
        # clear empty rows and add empty index
        if not all(v is '' for v in row):
            collection.append([[0, i] for i in row])
    
    # pad lists
    for row in collection:
        rowTemplate = [[0, ''] for _ in range(maxRowLen)]
        rowTemplate[:len(row)] = row
        row[:] = rowTemplate
    
    print('ha', collection)
    
    # populate index

    i = 0
    prev = [[0, ''] * maxRowLen]

    while i < maxRowLen:
        for row in collection:
                if row[i][1] != '':
                    row[i][0] = prev[i][0] + 1
                    # i += 1
                else:
                    row[i][0] = prev[i][0]
                    row[i][1] = prev[i][1]
                print(row)
                prev = row
                # print(prev)
        i += 1

    # print(collection)
    return collection







def splitRows(f):
    collection = []
    for line in f:
        ln = line.replace('\r', '').replace('\n', '').split("\t")
        collection.append(ln)
    return collection


with open(file, 'r') as f:
    col = splitRows(f)
    addIndex(col)


