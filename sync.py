import subprocess
import time
import os
import yaml

path = '/home/JDWorkSpace/xxx/ctxmnt/xxx/'

def load_watchlist(path):
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)

def is_git_updated():
    process = subprocess.Popen(["git", "pull", 'origin', 'dev'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # process = subprocess.Popen(["git", "pull", 'origin', 'master'])
    output = str(process.communicate()[0])
    # print(1)
    print(output)
    return output.find('file changed') >= -1


def get_mtime(filename):
    statbuf = os.stat(filename)
    return statbuf.st_mtime

def get_watchlist_time(watchlist):
    watchlist_time = []
    for i in watchlist:
        watchlist_time.append(get_mtime(path + i))
    return watchlist_time

def copy_file(file):
    subprocess.run(['cp', '-f', path + file, file])

print('start')

watchlist = load_watchlist('watchlist.yml')
watchlist_time = get_watchlist_time(watchlist)

for i in watchlist:
    copy_file(i)


while(True):
    time.sleep(0.5)
    for i,file in enumerate(watchlist):
        time.sleep(0.2)
        if watchlist_time[i] != get_mtime(path+file):
            print('------------start '+ file + '-------------')
            watchlist_time[i] = get_mtime(path+file)
            copy_file(file)

            if(file == 'watchlist.yml'):
                watchlist = load_watchlist('watchlist.yml')
                watchlist_time = get_watchlist_time(watchlist)

            else:
                subprocess.run(['python', file])
            print('-------------finish--------------')

