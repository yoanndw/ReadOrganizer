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
        return bwt.P_in_S(pattern, self.bwt, self.N, self.R, self.sa)

    def find_seeds_for_one_read(self, read):
        res = []

        for i in range(len(read) - self.k):
            w = read[i : i + self.k]
            pos = self.find_with_bwt(w)
            for p in pos:
                res.append((i, p))

                # TODO: liste tested pour éviter de tester plusieurs fois la meme chose

        return res

    def extend(self, read, positions_pair):
        (pos_in_read, pos_in_ref) = positions_pair
        pos_ref_to_cmp = pos_in_ref - pos_in_read

        # Si dépasse ref sur la gauche
        if pos_ref_to_cmp < 0:
            return None

        ref_to_cmp = self.ref[pos_ref_to_cmp : pos_ref_to_cmp + len(read)]

        return (pos_ref_to_cmp, utils.score(ref_to_cmp, read))

    def mapping(self):
        result = {}
        for read in self.reads_lst:
            seeds = self.find_seeds_for_one_read(read)
            
            l = []
            for seed in seeds:
                score_normal = self.extend(read, seed)
                score_revcomp = self.extend(utils.revcomp(read), seed)

                if score_normal is None:
                    best = score_revcomp
                elif score_revcomp is None:
                    best = score_normal
                elif score_normal[1] < score_revcomp[1]:
                    best = score_normal
                elif score_normal[1] > score_revcomp[1]:
                    best = score_revcomp

                if best is not None:
                    l.append(best)

            if len(l) > 0:
                min_score_seed = min(l, key=lambda pos_score: pos_score[1])
                #print(min_score_seed)
                result[min_score_seed[0]] = read

        return result