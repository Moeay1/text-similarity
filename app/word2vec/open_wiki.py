import opencc

op = opencc.OpenCC()

with open("../../data/dataset/wiki.zh.simple.txt", mode="w") as write_f:
    with open("../../data/dataset/wiki.zh.text", mode="r") as read_f:
        i = 0
        for line in read_f:
            write_f.write(op.convert(line) + "\n")
            i += 1
            if i % 1000 == 0:
                print("convert: {} rows".format(i))
