import os


if __name__ == "__main__":
    for filename in os.listdir("./COCO"):
        with open(os.path.join('./COCO', filename), 'r') as f:
            lines = f.readlines()
        with open(os.path.join('./COCO', filename), 'w') as f:
            for line in lines:
                if line.strip("\n")[0] == "0":
                    f.write(line)
