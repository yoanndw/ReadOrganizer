def creer_suffixes(seq):
    """Create all the suffixes of seq, and return the position for each suffix"""
    suff = []
    for i in range(len(seq)):
        suff.append((i, seq[i:]))
        
    return suff

def tri_suffixes(suff):
    """Sort the suffixes in lexicographical order"""
    suff.sort(key=lambda s: s[1])

def creer_sa(seq):
    """Create the suffix array from a sequence seq"""
    suff = creer_suffixes(seq)
    tri_suffixes(suff)
    
    return [pos for (pos, _) in suff]

# BWT
def get_BWT(S, SA):
    """Create the BWT array from the suffix array SA and the sequence S"""
    BWT = []
    for i in SA:
        if i == 0:
            BWT.append('$')
        else:
            BWT.append(S[i-1])
            
    return BWT


def get_N(bwt):
    """Return the count of occurrences of each character.
    
    Return: dict{character : count}
    """
    N = {}
    for c in bwt:
        if not c in N:
            N[c] = 1
        else:
            N[c] += 1
            
    return N

def get_R(BWT):
    """Return the rank of each character in BWT.
    
    If BWT[i] = A_3 : in Python: BWT[i] = 'A', and R[i] = 3
    """
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
    """Return the position in F of the character `char` of rank `rank`"""
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
    """Return the first position of c in bwt, starting at index i"""
    for idx in range(i, len(bwt)):
        if bwt[idx] == c:
            return idx
        
    return -1

def find_last(c, j, bwt):
    """Return the last position of c in bwt, from 0 to j"""
    for idx in range(j, -1, -1):
        if bwt[idx] == c:
            return idx
    return -1

def P_in_S(P, bwt, N, R, sa):
    """Find the pattern P in a sequence, and return the positions of all occurrences
    
    Params:
        - P: pattern to search
        - bwt: BWT
        - N: number of occurrences (see get_N())
        - R: ranks (see get_R())
        - sa: suffix array
        
    Return:
        List of positions of all occurrences
    """
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
        if f == -1 or l == -1:
            return []


        c = P[i]
        borne_d = LF(c, R[f], N)
        borne_f = LF(c, R[l], N)
    
    if l < f:
        return []
    
    return sa[borne_d : borne_f+1]

