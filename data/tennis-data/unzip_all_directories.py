import os
from subprocess import call

dirs = [d for d in os.listdir('.') if os.path.isdir(d) ]

for d in dirs:
    d += '/'
    print('Unzipping ' + d)
    os.chdir(d)
    call(['unzip', d[:4]])
    os.chdir('..')
print('finished')
