import argparse
import mapping
import readfiles

parser = argparse.ArgumentParser(
    prog="ReadOrganizer",
    description="Re-organize reads to improve sequence compression"
)

parser.add_argument("-i", "--input", required=True, help="input reads file")
parser.add_argument("-r", "--reference", required=True, help="reference genome file")
parser.add_argument("-k", type=int, help="seed size (only for seed-and-extend)")
parser.add_argument("-m", "--method", choices=["seed", "fast"], required=True, help="mapping method: 'seed' for seed-and-extend, 'fast' for faster")
parser.add_argument("-o", "--output", required=True, help="output file")

args = parser.parse_args()
# print(args)

ref = readfiles.read_ref(args.reference)
reads = readfiles.read_reads(args.input)

# print("REF=", ref)
# print("READS=", reads)

if args.method == "seed":
    mapper = mapping.MappingBest(ref, reads, k=args.k)
else:
    raise Exception("not implemented")

res = mapper.mapping()

#mapper = mapping.MappingBest(ref, [read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11], k=5)
# mapper = mapping.MappingBest(ref, reads, k=10)
# res = mapper.mapping()

#for pos, read in res.items():
    #for r in read:
        #print(r, "=>", r in reads)


res = dict(sorted(res.items(), key=lambda item: item[0]))

with open(args.output, 'a') as f:
    f.truncate(0)
    for pos, read in res.items():
        if (pos != -1):
            for r in read:
                f.write(r)
                f.write("\n")
            

    if -1 in res:
        for r in res.get(-1):
            f.write(r)
            f.write("\n")