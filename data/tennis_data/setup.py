import os
import shutil
from subprocess import call


WEBSITE = 'http://tennis-data.co.uk/alldata.php'

DIRS = [d for d in os.listdir('.') if os.path.isdir(d)]

def unzip_directories(directories):
    for d in directories:
        is_wtp = 'w' in d
        d += '/'
        print('Unzipping ' + d)
        os.chdir(d)
        file_name = d[:4]
        fix_file_name(file_name) # Some folders like 2016w have bad file names
        call(['unzip', file_name])
        
        move_file_and_rename(file_name, is_wtp)

        os.chdir('..')

        # remove directory
        shutil.rmtree(d)
    print('finished')

def move_file_and_rename(file_name, is_wtp):
    final_name = file_name if not is_wtp else file_name +'w'
    print(file_name)
    if os.path.isfile(file_name + '.xls'):
        call(['mv', file_name + '.xls', '../' + final_name + '.xls'])
    elif os.path.isfile(file_name + '.xlsx'):
        call(['mv', file_name + '.xlsx', '../' + final_name + '.xlsx'])

def fix_file_name(file_name):
    if '.zip' not in os.listdir('.')[0]:
        call(['mv', file_name +'zip', file_name +'.zip'])

def download_all_zip_files_from_page(site):
    print('downloading tennis data from ' + site)
    call(['wget', '-r', '-np' ,'-l 1' ,'-A' ,'zip' ,site])

download_all_zip_files_from_page(WEBSITE)
os.chdir('tennis-data.co.uk/')
unzip_directories([d for d in os.listdir('.') if os.path.isdir(d)])
# move all files one level up
[call(['mv', f, '..']) for f in os.listdir('.')]
os.chdir('..')
shutil.rmtree('tennis-data.co.uk')
os.remove('robots.txt')
