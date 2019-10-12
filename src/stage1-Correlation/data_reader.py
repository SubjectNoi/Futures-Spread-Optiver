# -*- coding: utf-8 -*- 
data_path = "../../data/dce/2018/"
import os
data = {}
def file_reader(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            print(data_path + str(file_name))
            f = open(data_path + str(file_name), errors='ignore')
            tmpf = f.readlines()
            for item in tmpf:
                print(item)

file_reader(data_path)