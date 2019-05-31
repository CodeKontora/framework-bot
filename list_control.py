from telebot import types


def parse_list(shop_list):
    shop_list = shop_list['list'][0].split(', ')
    for item in range(len(shop_list)):
        shop_list[item] = shop_list[item].capitalize()

    return shop_list


def create_buttons(parsed_list):
    shop_list = types.InlineKeyboardMarkup()
    for item in parsed_list:
        button = types.InlineKeyboardButton(item, callback_data=item)
        shop_list.add(button)

    return shop_list


def list_to_file(parsed_list):
    file = open('shop_list.txt', 'w')

    for item in parsed_list:
        file.write(item + '\n')
    file.close()


def list_from_file():
    file = open('shop_list.txt', 'r')

    shop_list = [line.strip() for line in file]
    file.close()

    return shop_list
