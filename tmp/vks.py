import vk_api#, vkontakte

vk_session = vk_api.VkApi('hamster197@mail.ru', 'polina2016')
try:
    vk_session.auth()
    vk_session = vk_api.VkApi('hamster197@mail.ru', token=vk_session.token['access_token'])
    vk_session.auth()
    vk = vk_session.get_api()
    my = vk.account.getProfileInfo()
    fr = vk.friends.get()['items']#[:5]
    print(my['first_name'], my['last_name'], my['home_town'], my['bdate'])
    ch = 0
    for f in fr:
        frn = vk.users.get(user_ids=f)
        if not frn[0]["first_name"] == 'DELETED':
            if ch < 5:
                ch = ch + 1
                n = frn[0]["first_name"]
                n = n + ' ' + frn[0]["last_name"]
                print(n)

except:
    print('no')


