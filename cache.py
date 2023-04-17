#!/usr/bin/python3

import requests
from datetime import datetime
import os

history=168
data_path='data'

def gen_filename():
    now = datetime.now()
    filename = now.strftime("%Y%m%d%H%M.csv")
    print(" file:    " + filename)
    return filename

def stash_data(path,data):
    filename = gen_filename()
    with open(os.path.join(path,filename), 'w', encoding="utf-8") as stash:
        stash.write(data)
    return filename

def update_link(filename):
    os.remove(os.path.join(data_path,"latest.csv"))
    os.symlink(filename,os.path.join(data_path,"latest.csv"))

def get_files(path):
    a = [s for s in os.listdir(path) if os.path.isfile(os.path.join(path, s)) and s.endswith('.csv')]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(path,s)))
    return a

def maintain_history(path,count):
    remove = get_files(path)[:-1*(count+1)]
    for file in remove:
        os.remove(os.path.join(path,file))
        print(" removed: " + file)

def main():
    print("request:")
    r = requests.get("https://rest.fnar.net/csv/prices")
    if r.status_code == 200:
        filename = stash_data(data_path,r.text)
        update_link(filename)
        print(" .. success")
    else:
        print(" .. failure")
    maintain_history(data_path,history)
    print("done")

if __name__ == "__main__":
    main()
