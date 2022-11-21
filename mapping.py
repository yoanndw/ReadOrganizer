import bwt
import utils

class Mapping:
    def __init__(self, ref, reads_lst, k):
        self.ref = ref
        self.reads_lst = reads_lst
        self.k = k

class MappingBest(Mapping):
    def __init__(self, ref, reads_lst, k):
        Mapping.__init__(self, ref, reads_lst, k)

        self.sa = bwt.creer_sa(self.ref)
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

                # TODO: liste tested pour éviter de tester plusieurs fois la meme chose

        return res

    def extend(self, read, positions_pair):
        """Extend of the seed.
        
        Params: positions_pair: result of find_seeds_for_one_read
        
        Return: (position in ref, read content)
        """
        (pos_in_read, pos_in_ref) = positions_pair
        pos_ref_to_cmp = pos_in_ref - pos_in_read

        # Si dépasse ref sur la gauche
        if pos_ref_to_cmp < 0:
            return None

        ref_to_cmp = self.ref[pos_ref_to_cmp : pos_ref_to_cmp + len(read)]

        return (pos_ref_to_cmp, utils.score(ref_to_cmp, read))

    def align(self, w):
        """Seed-and-extend on a specific string. Used to seed-and-extend both read and its reverse-complement.

        Return: result of extend()
        """
        seeds = self.find_seeds_for_one_read(w)
        
        l = []
        for seed in seeds:
            score = self.extend(w, seed)

            l.append(score)

        if len(l) > 0:
            min_score_seed = min(l, key=lambda pos_score: pos_score[1])
            return min_score_seed

        return None


    def mapping(self):
        """Map each read of the list in the reference

        Return: dict{position in the reference : reads found at this position (list)}
            Where each read found is the read or its reverse-complement
        """
        result = {}
        for read in self.reads_lst:
            score_normal = self.align(read)
            score_rev = self.align(utils.revcomp(read))

            if score_normal is None:
                best = score_rev
            elif score_rev is None:
                best = score_normal
            else:
                best = min(score_normal, score_rev, key=lambda pos_score: pos_score[1])
            
            if best is None: # Not found
                continue

            pos = best[0]
            if pos not in result:
                result[pos] = []

            if best == score_normal:
                found_in_ref = read
            else:
                found_in_ref = utils.revcomp(read)
            result[pos].append(found_in_ref)

        return result