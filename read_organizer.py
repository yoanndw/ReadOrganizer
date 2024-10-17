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
parser.add_argument("-m", "--method", choices=["seed", "fast", "1", "2"], required=True, help="mapping method: 'seed' or 1 for seed-and-extend, 'fast' or 2 for faster")
parser.add_argument("-o", "--output", required=True, help="output file")

args = parser.parse_args()
# print(args)

ref = readfiles.read_ref(args.reference)
reads = readfiles.read_reads(args.input)

# print("REF=", ref)
# print("READS=", reads)

if args.method in ["seed", "1"]:
    mapper = mapping.MappingBest(ref, reads, args.k)
else:
    mapper = mapping.MappingFast(ref, reads, args.k)

res = mapper.mapping()
res_normal, res_rev = res

for pos, read in res_normal.items():
    for r in read:
        print(r, "=>", r in reads)

print("---- REV-----")
for pos, read in res_rev.items():
    for r in read:
        print(r, "=>", r in reads)

with open(args.output, 'a') as f:
    f.truncate(0)
    for pos in sorted(res_normal.keys()):
        read = res_normal[pos]
        if (pos != -1):
            for r in read:
                f.write(r)
                f.write("\n")

    for pos in sorted(res_rev.keys()):
        read = res_rev[pos]
        if (pos != -1):
            for r in read:
                f.write(r)
                f.write("\n")
            

    if -1 in res_normal:
        for r in res_normal.get(-1):
            f.write(r)
            f.write("\n")

    if -1 in res_rev:
        for r in res_rev.get(-1):
            f.write(r)
            f.write("\n")