import requests
import json
from datetime import datetime
from pprint import pprint
import configparser
from tqdm import tqdm


congig = configparser.ConfigParser()
congig.read('settings.ini')
access_token = congig['Tokens']['vk_token']
#token_yd = congig['Tokens']['yd_token']


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v':
            self.version}


    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params,
                                            **params})
        return response.json()

    def get_photos(self, count=5):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'count': count,
            'album_id': 'profile',
            'extended': 1
        }
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()

    def search_max_size(self,sizes): #функция возращает максимальный размер фото и его url
        max_size = 0
        d = {}
        sorted_sizes = {
            's': 1,
            'm': 2,
            'o': 3,
            'p': 4,
            'q': 5,
            'r': 6,
            'x': 7,
            'y': 8,
            'z': 9,
            'w': 10
        }
        for s in sizes:
            if sorted_sizes[s['type']] > max_size:
                max_size = sorted_sizes[s['type']]
                d['size'] = s['type']
                d['url'] = s['url']

        return d

    def get_format_photo(self, data):
        formats = ['.jpg','.png','.gif']
        if data['url'][-4:] not in formats:
            for f in formats:
                if f in data['url']:
                    return f
        else:
            return data['url'][-4:]


    def make_data(self, photos):
        cur = sorted(photos['response']['items'], key=lambda d:d['likes']['count'])
        t0 = int(cur[0]['date'])
        d = self.search_max_size(cur[0]['sizes'])
        data = [
            {
                'name': str(cur[0]['likes']['count']),
                'size': d['size'],
                'url' : d['url']
            }
        ]

        for i in (range(1, len(cur))):

            t = int(cur[i]['date'])
            t = datetime.fromtimestamp(t0).strftime('%Y-%m-%d_%H-%M-%S')

            if cur[i]['likes']['count'] == cur[i - 1]['likes']['count']:
                name_photo = str(cur[i]['likes']['count']) + '_' + t
            else:
                name_photo = str(cur[i]['likes']['count'])

            d = {}
            d['name'] = name_photo
            d['size'] = cur[i]['sizes'][-1]['type']
            d['url'] = cur[i]['sizes'][-1]['url']
            data.append(d)

        return data

def create_folder(folder, token):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        'path': folder
    }
    headers = {
        'Authorization': f'OAuth {token}'
    }
    response = requests.put(url, params=params, headers=headers)
    return response.json()

def upload_folder(folder_name, name, token, url_photo):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params = {
        'path': '/'+folder_name+'/'+name,
        'url': url_photo
    }
    headers = {
        'Authorization': f'OAuth {token}'
    }
    response = requests.post(url, params=params, headers=headers)
    return response.json()

#user_id = '1725906'
user_id = input('Введите id пользователя VK: ')  # ввод идентификатор пользователя vk
token_yd = input('Введите токен: ') # ввод токена с Полигона Яндекс.Диска
vk = VK(access_token, user_id)
#pprint(vk.get_photos())
dat = vk.make_data(vk.get_photos())
#pprint(dat)

create_folder('photos_vk', token_yd)

list_files = []

for i in tqdm(dat):

    upload_folder('photos_vk', i['name'], token_yd, i['url'])
    d = {}
    d['file_name'] = i['name']+vk.get_format_photo(i)
    d['size'] = i['size']
    list_files.append(d)

pprint(list_files)

file = open('photos_info.json', 'w', encoding='utf8')
json.dump(list_files, file, ensure_ascii=False, indent=4)
file.close()


