import requests
from pprint import pprint
import datetime
import os
import json

"""Работа с классами на примере API VK"""

def get_tokens_from_file(token_name, file_name ="requiremеnts.txt"):
    # Чтения токенов пользователя по умолчанию из файла requiremеnts.txt
    list_of_tokens = {}
    with open(os.path.join(os.getcwd(), file_name), 'r') as token_file:
        a = True
        while a:
            line_token = token_file.readline()
            if line_token == '':
                break
            else:
                split_line_token = line_token.split()
                key = split_line_token[0]
                key = key[:-1]
                value = split_line_token[1]
                list_of_tokens[key] = value
    TOKEN = list_of_tokens[token_name]
    return TOKEN


class VK:

    def __init__(self, TOKEN, version='5.131'):
        self.token = TOKEN
        # self.id = user_id_VK
        self.version = version
        self.params = {'list_of_tokens': self.token, 'v': self.version}

    def get_photos_info(self):
        url = "https://api.vk.com/method/photos.get"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "album_id": "profile",
            "extended": 1,
        }
        response = requests.get(url, params=params)
        response_json = response.json()["response"]["items"]
        list_of_links_avatar_photo = list()
        for photo in response_json:
            sorted(photo)
            list_of_sizes_avatar_photo = list()
            for sizes in photo['sizes']:
                list_of_sizes_avatar_photo.append(
                    (photo['likes']['count'], photo['date'], sizes["width"], sizes["type"], sizes["url"]))
            list_of_sizes_avatar_photo = sorted(list_of_sizes_avatar_photo, key=lambda type: type[2])
            list_of_links_avatar_photo.append(list_of_sizes_avatar_photo[-1])
        # Naming of files by attaching extention JPG to Like or Date.
        list_of_photos = []
        # Поиск повторяющихся элементов в списке (множестве) по индексу во всех списках (множествах).
        for item in list_of_links_avatar_photo:
            a = item[0]  # Выбор искомого индекса.
            # Checking name for repeating.
            list_of_photo = []
            counter = 0
            for i in list_of_links_avatar_photo:
                if i[0] == a:
                    counter += 1
            if counter == 1:
                # Name is not repeated, it's naming by quantities of Likes.
                list_of_photo.append(str(item[0]) + ".jpg")
                list_of_photo.append(item[1])
                list_of_photo.append(item[2])
                list_of_photo.append(item[3])
                list_of_photo.append(item[4])
                list_of_photos.append(list_of_photo)
            else:  # Name is repeated, it's naming by Date.
                time_bc = datetime.datetime.fromtimestamp(item[1])
                list_of_photo.append(str(time_bc.strftime('%d.%m.%Y-%H.%M.%S')) + ".jpg")
                list_of_photo.append(item[0])
                list_of_photo.append(item[2])
                list_of_photo.append(item[3])
                list_of_photo.append(item[4])
                list_of_photos.append(list_of_photo)
        return list_of_photos

class YaUploader:
    URL_FILES_LIST: str = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    URL_FILES_RESOURCES: str = 'https://cloud-api.yandex.net/v1/disk/resources'
    URL_UPLOAD_LINK: str = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def __init__(self, TOKEN: str):
        self.token = TOKEN

    def create_folder_into_YaDisk(self):
        """Создание папки. \n path: Путь к создаваемой папке."""
        folder_path_to_y = input("Введите название папки: ")
        headers = {"Content-Type": "application/json", "Authorization": f"OAuth {self.token}"}
        target_folder = requests.put(f'{self.URL_FILES_RESOURCES}?path={folder_path_to_y}', headers=headers)
        if target_folder.status_code == 201:
            print(f"Папка {folder_path_to_y} создана! Статус {target_folder.status_code}")
        else:
            print(f'{target_folder.json().get("message")}! Статус {target_folder.status_code}.\n'
                  f' Загрузка будет выполнена в эту папку!')
        return folder_path_to_y


    def upload(self, replace=False):

        """Метод загружает файлы по списку file_list на яндекс диск"""
        headers = {"Content-Type": "application/json", "Authorization": f"OAuth {self.token}"}
        file_path_to_y = self.create_folder_into_YaDisk()
        count = 0
        josn_file =[]
        for i in vk.get_photos_info():
            file_name = str(i[0])
            file_name_with_path = (f'{file_path_to_y}/{file_name}')
            params = {'path': file_name_with_path,  # <- savefile куда сохраняем на Я.Д.
                      'url': i[-1],  # <- ссылка из ВК.
                      'overwrite': 'false'}
            res = requests.get(self.URL_FILES_RESOURCES, headers=headers, params=params).json()
            try:
                up_file = requests.post(self.URL_UPLOAD_LINK, headers=headers, params=params)
                requests_json = requests.get(self.URL_UPLOAD_LINK, headers=headers, params=params).json()
                if up_file.status_code == 202:
                    print(f'Файл {file_name} загружен на Яндекс.Диск')
                    count += 1
                    josn_file.append({"file_name": file_name, "size": i[-2]})
            except KeyError:
                pprint(res)
        pprint(f'Всего: {count}')
        with open("data_files_uploded.json", "w") as write_file:
            json.dump(josn_file, write_file)
        pprint(f"Файл data_files_uploded.json создан.\n {josn_file}")



# Инициализация токенов из файла requiremеnts.txt по ключам токунов TOKEN_VK:  и token_y: .
vk = VK(get_tokens_from_file('TOKEN_VK'))
y_uploader = YaUploader(get_tokens_from_file('token_y'))


if __name__ == '__main__':


    # Получаем список [(Likes, Date, Type, URL), (....), (....)].
    # pprint(vk.get_photos_info())

    # Создаёт папку на Яндекс.Диске.
    # y_uploader.create_folder_into_YaDisk()

    # Загружает все аватарки из профиля ВК на Ян.Ди.
    y_uploader.upload()