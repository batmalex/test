import gitlab
import cfg

gl = gitlab.Gitlab('https://gitlab.gitlab.bcs.ru', cfg.token, api_version=4)
gl.auth()


def get_group_name():
    group = False
    attempt = 0
    while not group and attempt < 4:
        group_name = input('Укажите наименование группы или GroupID из Gitlab: ')
        # Если выбор непустой
        if group_name:
            search_list = check_group_name(group_name)
            if search_list[1] == 0:
                print('Не найдено ни одной группы по заданным условиям')
            elif search_list[1] > 1:
                print('Надено несколько вариантов: \n\n{0:^10} {1:^25} {2:^30}'.format('GroupID', 'NAME', 'FULL PATH'))
                for item in search_list[0]:
                    print('{0:<10} {1:.<35} {2:.<55}'.format(item.id, item.name, item.full_path))
                print(' \n Для конкретизации укажите GroupID!! \n{0:.<100}'.format('.'))
            elif search_list[1] == 1:
                # group = gl.groups.get(search_list[0].id)
                group = search_list[0]
                print('Выбрана группа: {0}'.format(search_list[0].name))
        attempt += 1
    return group


def check_group_name(group_name):
    # Если строка валидная
    try:
        if len(group_name) < 100:
            # Если указали ID
            if group_name.isdigit():
                group = gl.groups.get(id=group_name)
                if group:
                    search_group_count = 1
            # Если указали наименовение
            elif group_name:
                group = gl.groups.list(search=group_name)
                search_group_count = len(group)
                if search_group_count == 1:
                    group = gl.groups.get(group[0].id)
        else:
            group = False
            search_group_count = 0
    except Exception:
        group = False
        search_group_count = 0
    return group, search_group_count


def get_tag_name():
    tag_name = input('\nУкажите номер тега в формате "1.1.1": ').strip()
    try:
        if tag_name:
            for item in tag_name:
                if not (item.isdigit() or item == '.'):
                    tag_name = False

    except Exception:
        return False
    return tag_name


def get_tag_message():
    tag_message = input('Укажите описание к тегу (message): ').strip()
    try:
        if len(tag_message) > 100:
            tag_message = tag_message[0:99]
    except():
        return ''
    return tag_message


def print_all_tags():
    try:
        answer = input('Вывести текущий список тегов по всем проектам для группы? (y/n): ').strip().lower()
        if answer == 'y' or answer == 'yes':
            print('\n{0:<10}{1:<45}  {2}'.format('PPJ ID', 'PROJECT NAME', 'TAGS'))
            for item in projects:
                project = gl.projects.get(item.id)
                tags = project.tags.list()
                print('{0:.<10}{1:.<45} {2}'.format(item.id, item.name, tags))
    except Exception:
        print('..возникло исключение...')


def set_tag(tag_name, tag_message, projects):
    project_id = input(
        'Укажите номер проекта (Prj_Id) либо нажмите (enter) для пометки всех проектов: ').strip().lower()
    if project_id:
        project = gl.projects.get(project_id)
        tag_finded = project.tags.get(str(tag_name), '')
        if not tag_finded:
            tag = project.tags.create({'tag_name': tag_name, 'ref': 'master', 'message': tag_message})
            print('Для проекта {0:.<40}, тег {1} добавлен'.format(project.name, tag))
        else:
            print('Для проекта {0:.<40}, тег {1:<12} был установлен ранее;'.format(project.name, tag_name))
    else:
        for item in projects:
            project = gl.projects.get(item.id)
            if not project.tags.get(str(tag_name)):
                project.tags.create({'tag_name': tag_name, 'ref': 'master', 'message': tag_message})
                print('Для проекта {0:.<40}, тег {1:<12} добавлен; {2}'.format(tag_name, item.name, tag_message))
            else:
                print('Для проекта {0:.<40}, тег {1:<12} был установлен ранее;'.format(tag_name, item.name))


if __name__ == "__main__":
    group = get_group_name()

    if group:
        projects = group.projects.list(all=True, order_by='name', sort='asc')
        print('Всего проектов в группе {1}: {0} '.format(len(projects), group.name))
        print_all_tags()
        tag_name = get_tag_name()
        tag_message = get_tag_message()

        if tag_name:
            set_tag(tag_name, tag_message, projects)
        else:
            print('Указаны некорректные данные для tagname')
            
def get_hosts(file_path):
    hosts = []
    with open(file_path, 'r') as f:
        db_list = json.loads(f.read())
        print(db_list)
        for host in db_list:
            if db_list[host]['dumping'] == "True":
                hosts.append(host)
        print(hosts)
    return hosts
