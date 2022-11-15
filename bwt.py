
# Créer suffixes avec positions
def creer_suffixes(seq):
    suff = []
    for i in range(len(seq)):
        suff.append((i, seq[i:]))
        
    return suff

# Trier les séq
def tri_suffixes(suff):
    suff.sort(key=lambda s: s[1])

# Création SA
def creer_sa(seq):
    suff = creer_suffixes(seq)
    tri_suffixes(suff)
    
    return [pos for (pos, _) in suff]

# BWT
def get_BWT(S, SA):
    BWT = []
    for i in SA:
        if i == 0:
            BWT.append('$')
        else:
            BWT.append(S[i-1])
            
    return BWT


def get_N(bwt):
    N = {}
    for c in bwt:
        if not c in N:
            N[c] = 1
        else:
            N[c] += 1
            
    return N

def get_R(BWT):
    R = []
    N = {}
    for i in BWT:
        if i not in N:
            N[i] = 0
        else:
            N[i] += 1
        R.append(N[i])
    return R

def LF(char, rank, N):
    if char == '$':
        return 0
    elif char == 'A':
        return N['$'] + rank
    elif char == 'C':
        return N['$'] + N['A'] + rank
    elif char == 'G':
        return N['$'] + N['A'] + N['C'] + rank
    elif char == 'T':
        return N['$'] + N['A'] + N['C'] + N['G'] + rank

def find_first(c, i, bwt):
    for idx in range(i, len(bwt)):
        if bwt[idx] == c:
            return idx
        
    return -1

def find_last(c, j, bwt):
    for idx in range(j, -1, -1):
        if bwt[idx] == c:
            return idx
    return -1

def P_in_S(P, bwt, N, R, sa):
    i = len(P) - 1
    c = P[i]
    
    borne_d = LF(c, 0, N)
    borne_f = borne_d + N[c] - 1
    
    l = 0
    f = 0
    while i > 0:
        i -= 1
        f = find_first(P[i], borne_d, bwt)
        l = find_last(P[i], borne_f, bwt)

        c = P[i]
        borne_d = LF(c, R[f], N)
        borne_f = LF(c, R[l], N)
    
    #print(l ,f)
    if l < f:
        return []
    
    return sa[borne_d : borne_f+1]

