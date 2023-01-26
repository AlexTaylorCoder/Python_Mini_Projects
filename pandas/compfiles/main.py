

with open("file1.txt") as file:
    file1 = [file.readlines()]

with open("file2.txt") as file:
    common = [int(line.strip()) for line in file.readlines() if line in file1[0]]
    print(common)
