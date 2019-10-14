# -*- coding: utf-8 -*- 
data_path = "../../data/dce/2014/"
import os
data = {}
def file_reader(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            f = open(data_path + str(file_name), encoding='utf-8', errors='ignore')
            tmpf = f.readlines()
            for items in tmpf:
                item = items.split(',')
                item_float = []
                for tmp in item:
                    item_float.append(float(str(tmp)))
                goodType = item[1][1:(len(item[1]) - 5)]
                if goodType not in data:
                    data[goodType] = []
                data[goodType].append(item_float)
    return True

file_reader(data_path)
# tmp = sorted(data["fb"], key=lambda x: x[2])
# sub_data = {}
# for i in tmp:
#     print(str(i[2]))
#     if str(i[2]) not in sub_data:
#         sub_data[str(i[2])] = []
#     sub_data[str(i[2])].append(i)

# for keys in sub_data:
#     tmp = sorted(sub_data[keys], key=lambda x: str(x[13]))
#     for i in tmp:
#         print(i)
#     print("================================================================================")
# for keys in data:
#     print(keys, len(data[keys][0]))
# for keys in data:
#     sorted_data_item = sorted(data[keys], key=lambda x: x[2])
#     sub_data = {}
#     for item in sorted_data_item:
#         if str(item[2]) not in sub_data:
#             sub_data[str(item[2])] = []
#         sub_data[str(item[2])].append(item)

#     for sub_keys in sub_data:
#         sorted_sub_data_item = sorted(sub_data[sub_keys], key=lambda y: str(y[-2]))
#         for i in sorted_sub_data_item:
#             print(i)
#         print("==============================================================================")
    
#     print("EEE   OOO   FFF")