import bwt
import utils
import kark

class Mapping:
    def __init__(self, ref, reads_lst, k):
        self.ref = ref
        self.reads_lst = reads_lst
        self.k = k

class MappingBest(Mapping):
    def __init__(self, ref, reads_lst, k):
        Mapping.__init__(self, ref, reads_lst, k)

        self.sa = kark.simple_kark_sort(ref)
        self.bwt = bwt.get_BWT(self.ref, self.sa)
        self.N = bwt.get_N(self.bwt)
        self.R = bwt.get_R(self.bwt)
    
    def find_with_bwt(self, pattern):
        """Search pattern in reference"""
        return bwt.P_in_S(pattern, self.bwt, self.N, self.R, self.sa)

    def find_seeds_for_one_read(self, read):
        """Return seeds of size self.k which are in reference
        
        Return: (position of the seed in read, position of the seed in ref)
        """
        res = []

        for i in range(len(read) - self.k):
            w = read[i : i + self.k]
            pos = self.find_with_bwt(w)
            for p in pos:
                res.append((i, p))

        return res

    def extend(self, read, positions_pair):
        """Extend of the seed.
        
        Params: positions_pair: result of find_seeds_for_one_read
        
        Return: (position in ref, score)
        """
        (pos_in_read, pos_in_ref) = positions_pair
        pos_ref_to_cmp = pos_in_ref - pos_in_read

        # If overflows ref on the left
        if pos_ref_to_cmp < 0:
            return None

        ref_to_cmp = self.ref[pos_ref_to_cmp : pos_ref_to_cmp + len(read)]

        return (pos_ref_to_cmp, utils.score(ref_to_cmp, read))

    def align(self, w):
        """Seed-and-extend on a specific string. Used to seed-and-extend both read and its reverse-complement.

        Return: result of extend()
        """
        seeds = self.find_seeds_for_one_read(w)
        for i, s in enumerate(seeds):
            #print("------")
            #print(i, ":", s, w[s[0] : s[0] + self.k], self.ref[s[1] : s[1] + self.k])
            pass
        
        tested_seeds = []
        
        l = []
        for seed in seeds:
            start_pos_in_ref = seed[0] - seed[1]

            if start_pos_in_ref in tested_seeds:
                continue # don't execute extend if already computed

            tested_seeds.append(start_pos_in_ref)

            score = self.extend(w, seed)

            if score is not None:
                l.append(score)

        if len(l) > 0:
            min_score_seed = min(l, key=lambda pos_score: pos_score[1])
            return min_score_seed

        return None

    def test(self):
        #p = self.find_with_bwt("TCTGATGTAA")
        p = self.find_with_bwt("TTACATCAGA")
        print("TEST:", p)


    def mapping(self):
        """Map each read of the list in the reference

        Return two dictionaries with this format:
            position in the reference : reads found at this position (list)

            The first dictionary contains the reads
            The second one contains the reverse-complements

        Return: tuple of two dictionaries, with the reads and the reverse-complements
        """
        result_normal = {}
        result_rev = {}
        for read in self.reads_lst:
            score_normal = self.align(read)
            score_rev = self.align(utils.revcomp(read))

            if score_normal is None:
                best = score_rev
            elif score_rev is None:
                best = score_normal
            else:
                best = min(score_normal, score_rev, key=lambda pos_score: pos_score[1])
            
            if best is None: # Not found => add at the end of the output, which is result_rev
                if -1 not in result_rev:
                    result_rev[-1] = []

                result_rev[-1].append(read)
                continue

            pos = best[0]
            if best == score_normal:
                if pos not in result_normal:
                    result_normal[pos] = []

                result_normal[pos].append(read) #always append read, even if the revcomp was found
            else:
                if pos not in result_rev:
                    result_rev[pos] = []

                result_rev[pos].append(read) #always append read, even if the revcomp was found


        return result_normal, result_rev


class MappingFast(Mapping):
    def __init__(self, ref, reads_lst, k):
        super().__init__(ref, reads_lst, k)

        self.sa = kark.simple_kark_sort(ref)
        self.bwt = bwt.get_BWT(self.ref, self.sa)
        self.N = bwt.get_N(self.bwt)
        self.R = bwt.get_R(self.bwt)

    def find_with_bwt(self, pattern):
        """Search pattern in reference
        
        Return: List of all the found positions 
        """
        return bwt.P_in_S(pattern, self.bwt, self.N, self.R, self.sa)

    def find_first_seed_for_read(self, read):
        seed = read[:self.k]
        pos = self.find_with_bwt(seed)

        if len(pos) == 0:
            return None

        return pos[0]

    def extend(self, read, pos_in_ref):
        """Extend of the seed.
        
        Params: pos_in_ref: result of find_first_seed_for_read
        
        Return: (position in ref, score)
        """
        ref_to_cmp = self.ref[pos_in_ref : pos_in_ref + len(read)]

        return (pos_in_ref, utils.score(ref_to_cmp, read))

    def align(self, w):
        """Seed-and-extend on a specific string. Used to seed-and-extend both read and its reverse-complement.

        Return: result of extend()
        """
        seed = self.find_first_seed_for_read(w)
        if seed is None:
            return None

        #print("------")
        #print(i, ":", s, w[s[0] : s[0] + self.k], self.ref[s[1] : s[1] + self.k])
        
        tested_seeds = []
        
        l = []
        #start_pos_in_ref = seed[0] - seed[1]

        #if start_pos_in_ref in tested_seeds:
        #    continue # don't execute extend if already computed

        #tested_seeds.append(start_pos_in_ref)

        score = self.extend(w, seed)

        if score is not None:
            l.append(score)

        if len(l) > 0:
            min_score_seed = min(l, key=lambda pos_score: pos_score[1])
            return min_score_seed

        return None

    def mapping(self):
        """Map each read of the list in the reference

        Return two dictionaries with this format:
            position in the reference : reads found at this position (list)

            The first dictionary contains the reads
            The second one contains the reverse-complements

        Return: tuple of two dictionaries, with the reads and the reverse-complements
        """
        result_normal = {}
        result_rev = {}
        for read in self.reads_lst:
            score_normal = self.align(read)
            score_rev = self.align(utils.revcomp(read))

            if score_normal is None:
                best = score_rev
            elif score_rev is None:
                best = score_normal
            else:
                best = min(score_normal, score_rev, key=lambda pos_score: pos_score[1])
            
            if best is None: # Not found => add at the end of the output, which is result_rev
                if -1 not in result_rev:
                    result_rev[-1] = []

                result_rev[-1].append(read)
                continue

            pos = best[0]
            if best == score_normal:
                if pos not in result_normal:
                    result_normal[pos] = []

                result_normal[pos].append(read) #always append read, even if the revcomp was found
            else:
                if pos not in result_rev:
                    result_rev[pos] = []

                result_rev[pos].append(read) #always append read, even if the revcomp was found


        return result_normal, result_rev