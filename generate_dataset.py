import glob, os
from subprocess import check_output, run, Popen, PIPE, CalledProcessError

with open("dataset", "r") as dataset:
    lignes = dataset.readlines()
    for i, l in enumerate(lignes):
        if l[0] != "#":
        #print(f"python3 test2.py ./my_dataset/raw/{l[:-1]}")
            run(f"python test2.py ./my_dataset/raw/{l[:-1]}", shell=True, check=True)
            print(f"Traité {i} / 677")

