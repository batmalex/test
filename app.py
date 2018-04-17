#!/usr/bin/env python3

def get_name():
    name = input("Введите имя: ")
    if name:
        print('правильно')
    else:
        print('неправильне')
    return name

def get_secondname():
    secondname = input("Введите фамилию: ")
    return secondname

if __name__ == '__main__':
    name = get_name()
    second = get_secondname()
    print('Вы указали имя {0}'.format(name))
    print('Вы указали фамилию {0}'.format(second))