import os
import shutil

# edit
input_path = '/mnt/storage/home/knostroverkhii/=results/aneuploidyFastq' # '/media/k/B4AC8B7FAC8B3ABE/aneuploidy fastq'
# edit
output_path_general = '/mnt/storage/home/knostroverkhii/temp'  # '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top/worktobe'
# /pycharmProjects/project1/out_gen'
dir_contents = os.listdir(input_path)
# sort list to correct bug with random(?) files coming on first position of the list
dir_contents.sort()
for i in range(0, len(dir_contents)-1, 2):
    # get new folder name
    output_path_specific = output_path_general + '/' + dir_contents[i][:dir_contents[i].find('_001') - 3]
    # create new folder
    os.mkdir(output_path_specific)
    # get fastq folder name in new folder
    output_path_specific = output_path_specific + '/' + 'fastq'
    # create new folder
    os.mkdir(output_path_specific)
    # send files to new folder
    pair_to_move = [dir_contents[i],  dir_contents[i+1]]
    shutil.move(input_path + '/' + dir_contents[i], output_path_specific)
    shutil.move(input_path + '/' + dir_contents[i+1], output_path_specific)

