def score(s1, s2):
    subs = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            subs += 1

    return subs

def revcomp(s):
    rev = ""
    for c in reversed(s):
        if c == 'A':
            nc = 'T'
        elif c == 'C':
            nc = 'G'
        elif c == 'G':
            nc = 'C'
        elif c == 'T':
            nc = 'A'

        rev += nc

    return rev

if __name__ == "__main__":
    print(revcomp("ACCTTGGA"))