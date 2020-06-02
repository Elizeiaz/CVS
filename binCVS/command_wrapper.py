from binCVS.ClassCVS import my_cvs
from binCVS.functional import command_init, command_add, command_commit, command_reset, \
    command_delete, command_log, command_track


def command_init_wrapper():
    if command_init():
        print('.cvs успешно инициализирован')
    else:
        print('.cvs уже инициализирован')


def command_add_wrapper(file_name):
    new_track_files = command_add(file_name)

    if new_track_files:
        print(' Файл(ы) добавлен(ы):\n')

        if isinstance(new_track_files, str):
            print(new_track_files)
        else:
            for t_file in new_track_files:
                print(t_file)
    else:
        print(' Ни один файл не был добавлен')


def command_commit_wrapper(comment):
    commited_files = command_commit(comment)

    if commited_files:
        print(' Сохранен(ы) файл(ы):')

        if isinstance(commited_files, str):
            print(commited_files)
        else:
            for commited_file in commited_files:
                print(commited_file)
    else:
        print(' Ни одно изменение не было найдено')


def command_reset_wrapper(version=my_cvs.last_project_version, file_name=None):
    prj_ver = command_reset(version, file_name)
    print(' Переход к версии ' + prj_ver)


def command_delete_wrapper(file_name):
    deleted_files = command_delete(file_name)

    if deleted_files:
        print(' Удалённые файлы:\n')
        for deleted_file in deleted_files:
            print(deleted_file)
    else:
        print('Ни один файл не был удалён')

def command_track_wrapper():
    tracked_files = command_track()
    print(' Отслеживаемые файлы:')
    if isinstance(tracked_files, str):
        print(tracked_files)
    else:
        for tracked_file in tracked_files:
            print(tracked_file)


def command_log_wrapped():
    log = command_log()
    print(log)
