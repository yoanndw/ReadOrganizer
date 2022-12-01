def read_ref(filename):
    with open(filename, "r") as f:
        ref = f.readline()
        while '>' in  ref:
            ref = f.readline()
        return ref.strip()

def read_reads(filename):
    lines = []
    with open(filename, "r") as f:
        for l in f.readlines():
            lines.append(l.strip())

    return lines