import os
import getpass
import vk


if __name__ == '__main__':
    app_id = os.environ['VK_API_APP_ID']
    login = input('VK login: ')
    password = getpass.getpass('Password: ')
    session = vk.AuthSession(user_login=login, user_password=password, 
                             app_id=app_id)
    api = vk.API(session)
    print(api.groups.search(q='Python', type='page'))
