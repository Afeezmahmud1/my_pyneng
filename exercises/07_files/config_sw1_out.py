from sys import argv
ig = ['alias','duplex','Current configuration']
with open (argv[1],'r') as src , open(argv[2],'a') as dst:
    for line in src:
        if line.rstrip().startswith('!'):
            continue
        elif ig[0] in line or ig[1] in line or ig[2] in line:
            continue
        else:
            dst.write(f"{line.rstrip()}\n")




