import os
import shutil

print('print path to folder FROM which folders should be moved')
input_path = input() # '/media/k/B4AC8B7FAC8B3ABE/aneuploidyFastq'
print('###')
print('print path to folder TO which folders should be moved')
output_path = input()  # '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top/worktobe'
print('###')
dir_contents = os.listdir(input_path)
# sort list to correct bug with random(?) files coming on first position of the list
dir_contents.sort()

for directory in dir_contents:
    shutil.move(input_path + '/' + directory, output_path)

