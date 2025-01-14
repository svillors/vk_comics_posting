import requests
import random
import os
from dotenv import load_dotenv


class VkApiError(Exception):
    pass


def check_vk_response(response):
    if 'error' in response:
        raise VkApiError(
                f'VK API error: {response['error']['error_msg']}')


def get_upload_server(access_token, group_id):
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
    api_response = response.json()
    check_vk_response(api_response)
    return api_response


def upload_photo(response, file_path):
    with open(file_path, 'rb') as file:
        url = response['response']['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    api_response = response.json()
    check_vk_response(api_response)
    return api_response


def save_photo(response, access_token):
    params = {
        'access_token': access_token,
        'photo': response['photo'],
        'server': response['server'],
        'hash': response['hash'],
        'v': '5.199'
    }
    response = requests.post(
        'https://api.vk.ru/method/photos.saveWallPhoto',
        params=params
    )
    response.raise_for_status()
    api_response = response.json()
    check_vk_response(api_response)
    return api_response


def post_image(response, access_token, text):
    owner_id = response['response'][0]['owner_id']
    image_id = response['response'][0]['id']
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
    comics = get_random_xkcd()
    download_image(comics['img'], 'xkcd.png')
    try:
        load_dotenv()
        access_token = os.environ["VK_ACCESS_TOKEN"]
        group_id = os.environ['VK_GROUP_ID']
        text = comics['alt']
        upload_server_response = get_upload_server(access_token, group_id)
        upload_photo_response = upload_photo(upload_server_response,
                                             'xkcd.png')
        save_photo_response = save_photo(upload_photo_response, access_token)
        post_image(save_photo_response, access_token, text)
    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError:
        print('Environment variables are not set correctly.')
    except VkApiError as e:
        print(e)
    finally:
        if os.path.exists('xkcd.png'):
            os.remove('xkcd.png')


if __name__ == "__main__":
    main()
