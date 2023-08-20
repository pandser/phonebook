import json
from os import path
from typing import Dict, List


def create_contact(
        phonebook: Dict[str, str],
        id: str,
        data: Dict[str, str]
        ) -> Dict[str, str]:
    '''Добавление, обновление контакта в справочнике.'''
    phonebook['contacts'][id] = data
    return phonebook


def search(find: str, data: Dict[str, str]) -> List[str]:
    '''
    Возвращает список id контактов в полях которых встречается 
    искомая строка.
    '''
    return [k for k, v in data.get('contacts').items() for key, value in v.items() if find.lower() in value.lower()]


def paginator(data: Dict[str, str], step: int=1) -> None:
    '''Постраничный вывод справочника.'''
    start: int = 0
    end: int = step
    while True:
        for i in data[start:end]:
            print(json.dumps(i, indent=2))
        key: str = input(
            'n - следующая страница \n'
            'p - предыдущая страница \n'
            'q - выход \n'
            ).lower()
        if key == 'n':
            start = end
            end += step
        elif key == 'p':
            end = start
            start -= step
        elif key == 'q':
            break


def input_contact() -> Dict[str, str]:
    '''Ввод данных контакта.'''
    contact = {}
    contact['first_name']: str = input('first_name \n')
    contact['surname']: str = input('surname \n')
    contact['last_name']: str = input('last_name \n')
    contact['organization']: str = input('organization \n')
    contact['phone']: str = input('phone \n')
    contact['mobile_phone']: str = input('mobile_phone \n')
    return contact


def write_file(id: str, data: Dict[str, str]) -> None:
    '''Запись данных в файл.'''
    with open('phonebook.json', 'w') as file:
        json.dump(create_contact(data, id, input_contact()),file)


if __name__ == '__main__':
    if not path.exists('phonebook.json'):
        with open('phonebook.json', 'w') as file:
            json.dump({'contacts': {}}, file)
    print(
        'Команды справочника: \n'
        'Показать контакты - start \n'
        'Добавить контакт - add \n'
        'Редактировать контакт - update \n'
        'Поиск контактов - search \n'
        'Выход exit \n'
        )
    while True:
        cmd: str = input('введите команду '
                    '(start, add, update, search, exit) \n').lower()
        print()
        with open('phonebook.json', 'r') as read_file:
            data: Dict[str, str] = json.load(read_file)
        if cmd == 'start':
            step = input('Укажите количество контактов на странице. \n')
            if step:
                paginator(
                    [(k, v) for k, v in data.get('contacts').items()],
                    int(step)
                    )
            else:
                paginator(
                    [(k, v) for k, v in data.get('contacts').items()],
                    )
        elif cmd == 'add':
            write_file(len(data.get('contacts')) + 1, data)
        elif cmd == 'update':
            write_file(input('введите id контакта \n'), data)
        elif cmd == 'search':
            result: List[str] = search(input('введите запрос \n'), data)
            print()
            if not result:
                print('Совпадений не найдено')
                continue
            for i in result:
                print(f'"{i}",\n '
                      f'{json.dumps(data.get("contacts")[i], indent=2)}')
                print()
            if input('Изменить контакт? y/n \n').lower() == 'y':
                write_file(i, data)
        elif cmd == 'exit':
            break
        else:
            print('неизвестная команда')
            