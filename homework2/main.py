def hash(salt, password):
    x = 0
    for i, c in enumerate(password):
        x += ord(c) * 10 ** ((5 - i) * 2)
    x += salt * 10 ** 12
    left = int(x / 10 ** 7)
    right = x % 10 ** 7
    hashValue = ((243 * left) + right) % 85767489
    return hashValue

def findPassword(hashValue, dictionary):
    count = 1
    for k, v in dictionary.items():
        for key, value in v.items():
            if hashValue == value:
                return k, str(key).zfill(3), count
            count += 1
    return '******', '***', len(dictionary) * 1000

if __name__ == '__main__':
    dictionary = dict() 
    fin = open(input('Please enter the name of password file: '))
    # fin = open('password.txt')
    for line in fin:
        temp = dict()
        line = line.strip() 
        for i in range(1000):
            temp[i] = hash(i, line)
        dictionary[line] = temp
    fin.close()

    fout = open('Dictionary.txt', 'w')
    for password, v in dictionary.items():
        for key, value in v.items():
            fout.write(f'{password} {key:-03d} {value}\n')
    fout.close()

    hashValue = int(input('Please enter a hash value: '))
    password, salt, entry = findPassword(hashValue, dictionary)
    if (password, salt, entry) != ('******', '***', len(dictionary) * 1000):
        print(f'Find out the password!!\n\tPassword: {password}\n\tSalt value: {salt}\n\tNumber of entries has been searched: {entry}')
    else:
        print(f'Recover the password unsuccessfully. {entry} entries have been searched.')

    # Read list_pa2.txt and generate results_pa2.txt.
    # //////////////////////////////////////
    # hashValues = []
    # fin = open('list_pa2.txt')
    # for line in fin:
    #     hashValues.append(int(line.strip()))
    # fin.close()
    
    # fout = open('results_pa2.txt', 'w')
    # for i in hashValues:
    #     password, salt, entry = findPassword(i, dictionary)
    #     fout.write(f'{i} {password} {salt} {entry}\n')
    # fout.close()