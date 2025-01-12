# Comics publisher

Script for posting random xkcd comics to your VK group
## Environment
### Requrements
you should install all dependencies using:
```
$ pip install -r requirements.txt
```
### Environment variables
first you should add some values ​​in `.env` file:
- VK_ACCESS_TOKEN - access token of your vk app
- VK_GROUP_ID - your VK group id
#### How to get
- Access token: to get acces token you have to create an app in VK and follow these instructions [dev.vk.com](https://dev.vk.com/ru/api/access-token/implicit-flow-user)
- Group id - to get group id you should use this service [regvk.com](https://regvk.com/id/)
## Run
to run script you should use:
```
$ python3 main.py
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).