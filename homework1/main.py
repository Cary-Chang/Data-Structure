import numpy as np

def PageRank(page, d, DIFF):
    N = len(page)
    PR = np.ones(N) / N
    while True:
        diff = 0
        PRold = PR.copy()
        for i in range(N):
            PRbefore = PRold[i]
            sum = 0
            for j in range(N):
                if i in page[j]:
                    sum += PRold[j] / len(page[j])
            PR[i] = (1 - d) / N + d * sum 
            diff += abs(PRbefore - PR[i])
        if diff < DIFF:
            return PR 

def ReverseIndex(pageStr):
    pageStrReverse = dict()
    for k, v in pageStr.items():
        v = list(set(v))
        for i in range(len(v)):
            if v[i] in pageStrReverse:
                pageStrReverse[v[i]].append(k)
            else:
                pageStrReverse[v[i]] = [k]
    return pageStrReverse

def SearchEngine(words, PR, pageStrReverse):
    search = dict()
    for i in words:
        if len(i) == 1:
            if i[0] in pageStrReverse.keys():
                pageStrReverse[i[0]] = sorted(pageStrReverse[i[0]], reverse = True, key = lambda j: PR[j])
                search[i[0]] = pageStrReverse[i[0]][:10]
            else:
                search[i[0]] = [-1]
        else:
            tempDict = dict()
            if i[0] in pageStrReverse.keys():
                tempSet_and = set(pageStrReverse[i[0]])
                for j in i[1:]:
                    if j not in pageStrReverse.keys():
                        tempSet_and.clear()
                        break
                    else:
                        tempSet_and &= set(pageStrReverse[j])
                if len(tempSet_and) > 0:
                    tempList = list(tempSet_and)
                    tempList = sorted(tempList, reverse = True, key = lambda k: PR[k])
                    tempDict[0] = tempList[:10]
                else:
                    tempDict[0] = [-1]
            else:
                tempDict[0] = [-1]
            if i[0] in pageStrReverse.keys():
                tempSet_or = set(pageStrReverse[i[0]])
            else:
                tempSet_or = set()
            for j in i[1:]:
                if j in pageStrReverse.keys():
                    tempSet_or |= set(pageStrReverse[j])
            if len(tempSet_or) > 0:
                tempList = list(tempSet_or)
                tempList = sorted(tempList, reverse = True, key = lambda k: PR[k])
                tempDict[1] = tempList[:10]
            else:
                tempDict[1] = [-1]
            search[" ".join(i)] = tempDict
    return search

if __name__ == '__main__':
    page = dict()
    pageStr = dict()
    N = 500
    PRArray = np.empty((4, 3, 501))

    for i in range(N):
        fin = open(f'web-search-files2/page{i}')
        page[i] = []
        isStr = False
        for line in fin:
            if line.strip() != '---------------------' and not isStr:
                page[i].append(int(line.lstrip('page').split()[0]))
            elif isStr:
                pageStr[i] = line.strip().split()
            else:
                isStr = True
        fin.close()
    page[N] = []
 
    for i in range(4):
        for j in range(3):
            PRArray[i][j] = PageRank(page, 0.25 + 0.2 * i, 0.001 * 10 ** j)
            fout = open(f'output/pr_{int(100 * (0.25 + 0.2 * i))}_{int(1000 * (0.001 * 10 ** j)):03d}.txt', 'w')
            pageOutput = dict()
            for k in range(N + 1):
                pageOutput[PRArray[i][j][k]] = k
            for k in sorted(pageOutput.keys(), reverse = True):
                fout.write(f'page{pageOutput[k]:-3d}  {len(page[pageOutput[k]]):-3d}   .{round(k * 10 ** 7):07d}\n')
            fout.close()

    pageStrReverse = ReverseIndex(pageStr)
    fout = open('output/reverseindex.txt', 'w')
    for i in sorted(pageStrReverse):
        fout.write(f'{i:20s}  ')
        for j in pageStrReverse[i]:
            fout.write(f'page{j} ')
        fout.write('\n')
    fout.close()

    fin = open('list.txt')
    words = []
    for line in fin:
        words.append(line.strip().split())
    fin.close()

    for i in range(4):
        for j in range(3):
            search = SearchEngine(words, PRArray[i][j], pageStrReverse)
            fout = open(f'output/result_{int(100 * (0.25 + 0.2 * i))}_{int(1000 * (0.001 * 10 ** j)):03d}.txt', 'w')
            for value in search.values():
                if type(value) == list:
                    for k in value:
                        if k != -1:
                            fout.write(f'page{k} ')
                        else:
                            fout.write('none')
                else:
                    fout.write('AND ')
                    for k in value[0]:
                        if k != -1:
                            fout.write(f'page{k} ')
                        else:
                            fout.write('none')
                    fout.write('\nOR ')
                    for k in value[1]:
                        if k != -1:
                            fout.write(f'page{k} ')
                        else:
                            fout.write('none')
                fout.write('\n')
            fout.close()