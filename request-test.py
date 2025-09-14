import requests
import json
import pprint

def get_the_smartest_superhero() -> str:

    url = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'

    list_hero = ['Hulk', 'Captain' 'America', 'Thanos']

    response = requests.get(url)
    all_hero = json.loads(response.content)


    hero_info = []

    for hero in all_hero:
        if hero['name'] in list_hero:
            hero_info.append((hero['name'],hero['powerstats']['intelligence']))

    hero_sort = sorted(hero_info, key=lambda x: x[1])


    smartest_hero = hero_sort[-1][0]

    return smartest_hero

print(get_the_smartest_superhero())

def get_the_smartest_superhero() -> str:
    base_url = "https://akabab.github.io/superhero-api/api"
    hulk = 332
    captain_america = 149
    thanos = 655
    max_intelligence = 0
    the_smartest_superhero = ''
    for superhero_id in (hulk, captain_america, thanos):
        url = base_url + f"/id/{superhero_id}.json"
        response = requests.get(url)
        info = response.json()
        intelligence = info['powerstats']['intelligence']
        if intelligence > max_intelligence:
            max_intelligence = intelligence
            the_smartest_superhero = info['name']
    return the_smartest_superhero


if __name__ == '__main__':
    assert get_the_smartest_superhero() == 'Thanos'