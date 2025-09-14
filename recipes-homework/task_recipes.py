from pprint import pprint

def makeListFromFile(file: str):

    f = open(file, encoding="utf-8")
    list_recipes = f.readlines()
    f.close()
    return list_recipes


def inDictFromList(s: str):

    dict_ingredient = {}
    dict_ingredient['ingredient_name'] = s[0]
    dict_ingredient['quantity'] = int(s[1])
    dict_ingredient['measure'] = s[2]
    return dict_ingredient


def makeCookBook(list_recipes: list[str]):

    cook_book = {}

    for i in range(len(list_recipes)):

        item = list_recipes[i]
        str_item = item.split('\n')[0]
        if str_item.isdigit() == False:
            continue

        count_ing = int(str_item)
        name_recipe = list_recipes[i-1].split('\n')[0]
        list_ingredients = []

        for k in range(i+1, i+count_ing+1):

            cur_list = list_recipes[k].split('\n')[0].split('|')
            list_ingredients.append(inDictFromList(cur_list))

        cook_book[name_recipe] = list_ingredients

    return cook_book

def getShopListByDishes(dishes: list[str], person_count: int):

    dict_ingredients = {}
    cook_book = makeCookBook(makeListFromFile('recipes.txt'))

    for dish in dishes:

        for ingredient in cook_book[dish]:

            if ingredient['ingredient_name'] in dict_ingredients:
                dict_ingredients[ingredient['ingredient_name']['quantity']] += person_count*ingredient['quantity']

            else:
                dict_ingredients[ingredient['ingredient_name']] = {'measure': ingredient['measure'],
                                                                   'quantity': person_count*ingredient['quantity']}

    return dict_ingredients


def sortedNewFile(file1: str, file2: str, file3: str):
    f1 = makeListFromFile(file1)
    f2 = makeListFromFile(file2)
    f3 = makeListFromFile(file3)

    len1 = len(f1)
    len2 = len(f2)
    len3 = len(f3)

    sorted_len = sorted([len1, len2, len3])
    dict_files = {len1: [file1, f1], len2: [file2, f2], len3: [file3, f3]}
    my_file = open("UnionFile.txt", "w+", encoding="utf-8")

    for n in sorted_len:
        my_file.write(f'{dict_files[n][0]}\n{str(n)}\n')
        for i in dict_files[n][1]:
            my_file.write(i)
        my_file.write('\n')

    my_file.close()

    return

#задача №1
res1 = makeCookBook(makeListFromFile("recipes.txt"))
pprint(res1)

#задача №2
res2 = getShopListByDishes(['Запеченный картофель', 'Омлет'], 2)
pprint(res2)

#задача №3
sortedNewFile("1.txt", "2.txt", "3.txt")
