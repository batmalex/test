import gitlab
import cfg
import json

gl = gitlab.Gitlab('https://gitlab.gitlab.bcs.ru', cfg.token, api_version=4)
gl.auth()

def get_working_mode():
    working_mode = input('Для выбора диалогового режима нажмите Enter или укажите "f" для загрузки конфигураци из файла :')
    if working_mode.lower() == 'f':
        user_mode = False
    else:
        user_mode = True
    return user_mode


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


def set_tag(tag_name, tag_message, project):
    tag_finded = project.tags.get(str(tag_name))
    if not tag_finded:
        tag = project.tags.create({'tag_name': tag_name, 'ref': 'master', 'message': tag_message})
        print('Для проекта {0:.<40}, тег {1} добавлен'.format(project.name, tag))
    else:
        print('Для проекта {0:.<40}, тег {1:<12} был установлен ранее;'.format(project.name, tag_name))


def get_projects(file_path):
    project_list = []
    with open(file_path, 'r') as f:
        parced_file = json.loads(f.read())
        print(parced_file)
        for item in parced_file['projects']:
            if item['tagging'].lower() == "true":
                project_list.append(item.get('project_id'))
        # group_name = parced_file['group_name']
        print(project_list)
    return project_list

# def set_tag(tag_name, tag_message, projects):
#     project_id = input(
#         'Укажите номер проекта (Prj_Id) либо нажмите (enter) для пометки всех проектов: ').strip().lower()
#     if project_id:
#         project = gl.projects.get(project_id)
#         tag_finded = project.tags.get(str(tag_name), '')
#         if not tag_finded:
#             tag = project.tags.create({'tag_name': tag_name, 'ref': 'master', 'message': tag_message})
#             print('Для проекта {0:.<40}, тег {1} добавлен'.format(project.name, tag))
#         else:
#             print('Для проекта {0:.<40}, тег {1:<12} был установлен ранее;'.format(project.name, tag_name))
#     else:
#         for item in projects:
#             project = gl.projects.get(item.id)
#             if not project.tags.get(str(tag_name)):
#                 project.tags.create({'tag_name': tag_name, 'ref': 'master', 'message': tag_message})
#                 print('Для проекта {0:.<40}, тег {1:<12} добавлен; {2}'.format(tag_name, item.name, tag_message))
#             else:
#                 print('Для проекта {0:.<40}, тег {1:<12} был установлен ранее;'.format(tag_name, item.name))


if __name__ == "__main__":
    user_mode = get_working_mode()

    if not user_mode:
        tag_name = get_tag_name()
        tag_message = get_tag_message()
        project_list = get_projects('./project_list.json')
        for project_id in project_list:
            project = gl.projects.get(project_id)
            set_tag(tag_name, tag_message, project)
    else:
        group = get_group_name()
        if group:
            projects = group.projects.list(all=True, order_by='name', sort='asc')
            print('Всего проектов в группе {1}: {0} '.format(len(projects), group.name))
            print_all_tags()

            # tag_name = get_tag_name()
            # tag_message = get_tag_message()
            #
            # if tag_name:
            #     set_tag(tag_name, tag_message, project)
            # else:
            #     print('Указаны некорректные данные для tagname')

#
# prj_list = [{'project_name': 4, 'tagging': "true", 'project_id': prj_id} for prj_id in 'qwe']
#
# print(prj_list)
#
# {
#   "group_name": "perseus",
#   "working_mode": "deatached",
#   "projects": [
#     {
#       "project_name": "adminer",
#       "project_id": "12",
#       "tagging": "true"
#     },
#     {
#       "project_name": "gui",
#       "project_id": "15",
#       "tagging": "false"
#     },
#     {
#       "project_name": "web",
#       "project_id": "100500",
#       "tagging": "true"
#     }
#   ]
# }

