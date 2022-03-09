import os
def index_gen(foldername):
    presetlist = os.listdir(foldername)
    n = 0
    file_index = []
    print (f'Total file found: {len(presetlist)}')
    for i in presetlist:
        print(f'{n} -- {i}')
        file_index.append(i)
        n += 1
    print (f'Index Finished')
    return preset
