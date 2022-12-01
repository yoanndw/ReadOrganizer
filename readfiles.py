def read_ref(filename):
    with open(filename, "r") as f:
        return f.read()

def read_reads(filename):
    lines = []
    with open(filename, "r") as f:
        for l in f.readlines():
            lines.append(l.strip())

    return lines