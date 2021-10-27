import os
import shutil

input_path = '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top/worktobe'
output_path = '/media/k/B4AC8B7FAC8B3ABE/aneuploidy fastq'

dir_contents = os.listdir(input_path)
dir_contents.sort()
for i in dir_contents:
    sub_contents = os.listdir(input_path + '/' + i)
    for j in sub_contents:
        shutil.move(input_path + '/' + i + '/' + j, output_path)


