import os

def create_index(foldername):
    presetlist = os.listdir("stringer_data")
    n = 0
    print ('Enter the preset #')
    for i in presetlist:
        print(f'{n} -- {i}')
        n += 1
    n = int(input())
    with open (f'Data files/{str(presetlist[n])}', 'r') as f:
        preset = []
        for line in f:
            if floatcheck(line):
                line = line.strip('\n')
                preset.append(line)

    return preset
