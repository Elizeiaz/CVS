import os

from ClassCVS import my_cvs


# Возвращает отслеживаемые файлы
def return_track_files(cur_dir):
    if os.path.exists(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
        with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'r', encoding='utf-8-sig') as f:
            track_files = f.read().splitlines()
            return track_files
    return []


# Ищет номер последнего коммита
def find_last_ver():
    way_to_prj_ver = my_cvs.cur_dir + '\\.cvs\\prjVer'
    folders = os.listdir(way_to_prj_ver)
    last_ver = int(0)

    for folder in folders:
        if os.path.isdir(way_to_prj_ver + '\\' + folder):
            try:
                if int(last_ver) < int(folder):
                    last_ver = folder
            except ValueError:
                pass
    return int(last_ver)


# Функция ищет все файлы в dir, которых нет в .cvsignore.txt
def find_all_files(directory):
    files = os.listdir(directory)
    ignore_files = ['.cvs', '.cvsignore.txt', 'CVS.py', 'functional.py']
    return_files = []

    if os.path.exists(my_cvs.cur_dir + '\\.cvsignore.txt'):  # Херня какая-то
        with open(my_cvs.cur_dir + '\\.cvsignore.txt', encoding='utf-8-sig') as ignore:
            ignore_files += ignore.read().splitlines()

    for file in files:
        if os.path.isfile(directory + '\\' + file):
            if file not in ignore_files:
                return_files.append(file)
        elif file not in ignore_files:
            other_files = find_all_files(directory + '\\' + file)
            for f in other_files:
                if f not in ignore_files:
                    return_files.append(file + '\\' + f)

    return return_files


# Создаёт новую директорию для commit
def create_new_prj_ver_dir():
    way_to_prj_ver = my_cvs.cur_dir + '\\.cvs\\prjVer'
    files = os.listdir(way_to_prj_ver)
    folders = []
    for file in files:
        if os.path.isdir(way_to_prj_ver + '\\' + file):
            folders.append(file)

    os.makedirs(way_to_prj_ver + '\\' + str(my_cvs.last_project_version + 1))


# Добавляет файл(ы) в отслеживаемые
def add_track_files(files):
    added_files = []

    way_to_track_files = my_cvs.cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'

    if not os.path.exists(way_to_track_files):
        open(way_to_track_files, 'w+', encoding='utf-8-sig').close()

    for new_file in files:
        if new_file not in my_cvs.track_files:
            added_files.append(new_file)

    with open(way_to_track_files, 'a', encoding='utf-8-sig') as f:
        for new_file in added_files:
            f.write(new_file + '\n')


# Удаляет "лишние" отслеживаемые файлы, возвращает True, если такие файлы имеются
def add_deleted_files(cur_dir):
    files = find_all_files(cur_dir)
    track_files = return_track_files(cur_dir)

    f = open(my_cvs.cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'w', encoding='utf-8-sig')
    count = 0

    for t_file in track_files:
        if t_file not in files:
            print('    - ' + t_file)
            count += 1
        else:
            f.write(t_file + '\n')
    f.close()

    if count < 1:
        return False
    return True
