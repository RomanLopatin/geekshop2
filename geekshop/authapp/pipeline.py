from datetime import datetime

import requests
import social_core.backends.vk
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    fields_for_requests = ['bdate', 'sex', 'about', 'photo_200']

    base_url = 'https://api.vk.com/method/users.get/'
    params = {
        'fields': ','.join(fields_for_requests),
        'access_token': response['access_token'],
        'v': settings.API_VERSION
    }

    api_response = requests.get(base_url, params=params)
    print(api_response)

    if api_response.status_code != 200:
        return

    api_data = api_response.json()['response'][0]
    print(api_data)

    if api_data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if api_data['sex'] == 2 else ShopUserProfile.FEMALE

    if api_data['about']:
        user.shopuserprofile.aboutMe = api_data['about']

    if api_data['bdate']:
        bdate = datetime.strptime(api_data['bdate'], '%d.%m.%Y').date()
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden(social_core.backends.vk.VKOAuth2)
        user.age = age

    if api_data['photo_200']:
        avatar_url = api_data['photo_200']
        avatar_obj = requests.get(avatar_url)
        avatar_path = f'{settings.MEDIA_ROOT}/users/{user.pk}.jpg'
        with open(avatar_path, 'wb') as avatar_file:
            avatar_file.write(avatar_obj.content)
            user.avatar = f'/users/{user.pk}.jpg'
    user.save()
