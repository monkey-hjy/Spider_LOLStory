import requests
import pandas as pd


def get_json(url):
    headers = {'user-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf8'
    d_json = response.json()
    return d_json


def get_city_info(city_url):
    city_json = get_json(city_url)
    city_name = []
    city_slug = []
    city_context = []
    for i in range(len(city_json['factions'])):
        city_name.append(city_json['factions'][i]['name'])
        city_slug.append(city_json['factions'][i]['slug'])
        the_url = 'https://yz.lol.qq.com/v1/zh_cn/factions/{}/index.json'.format(city_json['factions'][i]['slug'])
        the_json = get_json(the_url)
        city_context.append(the_json['faction']['overview']['short'].replace('<p>', '').replace('</p>', '\n'))
    info = pd.DataFrame({'city_name': city_name,
                         'city_slug': city_slug,
                         'city_context': city_context})
    return info


def city_info_write(city_info):
    for i in range(len(city_info)):
        with open('f://SpiderData//lol故事.txt', 'a', encoding='utf8') as f:
            f.write('地区:' + city_info['city_name'][i] + '\n')
            f.write('地区简介:' + city_info['city_context'][i] + '\n\n')


if __name__ == "__main__":
    city_url = 'https://yz.lol.qq.com/v1/zh_cn/faction-browse/index.json'
    city_info = get_city_info(city_url)
    city_info_write(city_info)
    url = 'https://yz.lol.qq.com/v1/zh_cn/search/index.json'
    data_json = get_json(url)
    for i in range(len(data_json['champions'])):
        name = data_json['champions'][i]['name']
        slug = data_json['champions'][i]['slug']
        city_other_name = data_json['champions'][i]['associated-faction-slug']
        if city_other_name == 'unaffiliated':
            city_name = '符文之地'
        elif city_other_name == 'runeterra':
            city_name = '未定'
        else:
            city_index = list(city_info['city_slug']).index(city_other_name)
            city_name = city_info['city_name'][city_index]
        url = 'https://yz.lol.qq.com/v1/zh_cn/champions/{}/index.json'.format(slug)
        the_json = get_json(url)
        other_name = the_json['champion']['title']
        context = the_json['champion']['biography']['full'].replace('<p>', '').replace('</p>', '\n')
        with open('f://SpiderData//lol故事.txt', 'a', encoding='utf8') as f:
            f.write('名字1: ' + name + '\n')
            f.write('名字2:' + other_name + '\n')
            f.write('所属地区:' + city_name + '\n')
            f.write('故事:' + context + '\n\n')
            print(name + ':' + other_name)
