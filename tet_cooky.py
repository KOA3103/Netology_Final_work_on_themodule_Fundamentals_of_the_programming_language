from pprint import pprint
import datetime
import os
import json

path_or_file = r'C:\Users/source_cooky.txt'
json_list = []
with open(os.path.join(os.getcwd(), path_or_file), 'r') as cooky_file:
    a = True
    while a:
        dict_item = {}
        cooky = cooky_file.readline()
        cooky_list = cooky.split()
        list_pare = []
        for word in cooky_list:
            list_word = []
            for letter in word:
                if letter != '[' and letter != ']' and letter != "'" and letter != '"' \
                        and letter != '{' and letter != '}' and letter != ':' and letter != ',':
                    list_word.append(letter)

            list_word = "".join(list_word)
            list_pare.append(list_word)
        if cooky == '':
            break
        try:
            dict_item[list_pare[0]] = list_pare[1]
        except IndexError:
            pass
        try:
            dict_item[list_pare[2]] = list_pare[3]
        except IndexError:
            pass
        try:
            dict_item[list_pare[4]] = list_pare[5]
        except IndexError:
            pass
        try:
            dict_item[list_pare[6]] = list_pare[7]
        except IndexError:
            pass
        try:
            dict_item[list_pare[8]] = list_pare[9]
        except IndexError:
            pass
        try:
            dict_item[list_pare[10]] = list_pare[11]
        except IndexError:
            pass
        try:
            dict_item[list_pare[12]] = list_pare[13]
        except IndexError:
            pass
        try:
            dict_item[list_pare[14]] = list_pare[15]
        except IndexError:
            pass
        try:
            dict_item[list_pare[16]] = list_pare[17]
        except IndexError:
            pass
        try:
            dict_item[list_pare[18]] = list_pare[19]
        except IndexError:
            pass
        json_list.append(dict_item)
for i in json_list:
    try:
        a = i["expiry"]
    except:
        pass
    time_bc = datetime.datetime.fromtimestamp(int(a))
    b = str(time_bc.strftime('%d.%m.%Y-%H.%M.%S'))
    print("expiry:", b)

print("\n", json.dumps(json_list))

with open("data_files_uploded.json", "w") as write_file:
    json.dump(json_list, write_file)

