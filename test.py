result = []

with open("proof.txt", "r") as f:
    for idx, line in enumerate(f):
        if line.startswith("commit"):
            continue
        if line.startswith("Author: Saad"):
            result.append("Author: satifi\n")
            continue
        if line.startswith("Author: otahiri"):
            result.append("Author: otahiri-\n")
            continue
        if line.startswith("Date: "):
            result.append(line[0 : line.index("+")])
            result.append("\n")

            continue
        if line.startswith("    "):
            result.append(line.strip())
            result.append("\n\n")

            continue
        # result.append("\n")
# result.reverse()
with open("ss.txt", "w") as f:
    for line in result:
        f.write(line)
