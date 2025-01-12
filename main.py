import requests
import random
import os
from dotenv import load_dotenv


def check_vk_response(response):
    if 'error' in response:
        raise Exception(
                f'VK API error: {response['error']['error_msg']}')


def post_image(access_token, group_id, file_path, text):
    try:
        params = {
            'access_token': access_token,
            'v': '5.199',
            'group_id': group_id
        }
        response = requests.get(
            'https://api.vk.ru/method/photos.getWallUploadServer',
            params=params
        )
        response.raise_for_status()
        response_json = response.json()
        check_vk_response(response_json)
        with open(file_path, 'rb') as file:
            url = response_json['response']['upload_url']
            files = {
                'photo': file,
            }
            response = requests.post(url, files=files)
            response.raise_for_status()
            response_json = response.json()
            check_vk_response(response_json)
        params = {
            'access_token': access_token,
            'photo': response_json['photo'],
            'server': response_json['server'],
            'hash': response_json['hash'],
            'v': '5.199'

        }
        response = requests.post(
            'https://api.vk.ru/method/photos.saveWallPhoto',
            params=params
        )
        response.raise_for_status()
        response_json = response.json()
        check_vk_response(response_json)
        owner_id = response_json['response'][0]['owner_id']
        image_id = response_json['response'][0]['id']
        params = {
            'access_token': access_token,
            'owner_id': owner_id,
            'message': text,
            "attachments": 'photo{}_{}'.format(owner_id, image_id),
            'v': '5.199'
        }
        response = requests.post(
            'https://api.vk.com/method/wall.post',
            params=params
        )
        response.raise_for_status()
        check_vk_response(response.json())
    except Exception as e:
        print(e)


def download_image(url, path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_random_xkcd():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    random_comics = random.randint(1, int(response.json()['num']))
    response = requests.get(f'https://xkcd.com/{random_comics}/info.0.json')
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    comics = get_random_xkcd()
    download_image(comics['img'], 'xkcd.png')
    acces_token = os.getenv("VK_ACCESS_TOKEN")
    group_id = os.getenv('VK_GROUP_ID')
    text = comics['alt']
    post_image(acces_token, group_id, 'xkcd.png', text)
    os.remove('xkcd.png')


if __name__ == "__main__":
    main()
