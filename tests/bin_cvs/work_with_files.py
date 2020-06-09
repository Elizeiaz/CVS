import os
import re

from bin_cvs.base_work_with_files import read_file, rewrite_file


# Ищет номер последнего коммита
def find_last_ver(directory):
    if os.path.exists(os.path.join(directory, '.cvs', 'prjVer')):
        folders = os.listdir(os.path.join(directory, '.cvs', 'prjVer'))
        last_ver = int(0)

        for folder in folders:
            if os.path.isdir(os.path.join(os.path.join(directory, '.cvs', 'prjVer'), folder)):
                try:
                    if int(last_ver) < int(folder):
                        last_ver = folder
                except ValueError:
                    pass
        return int(last_ver)
    return 0


# Удаляет "лишние" отслеживаемые файлы, возвращает True, если такие файлы имеются
def add_deleted_files(func):
    directory = os.getcwd()
    if os.path.exists(os.path.join(os.getcwd(), '.cvs', 'cvsData', 'trackFiles.txt')):
        files = find_all_files(directory)
        way_to_track_files = os.path.join(directory, '.cvs', 'cvsData', 'trackFiles.txt')
        track_files = read_file(way_to_track_files)
        deleted_files = []
        cur_track_files = []

        for t_file in track_files:
            if t_file not in files:
                deleted_files.append(t_file)
            else:
                cur_track_files.append(t_file)

        rewrite_file(way_to_track_files, cur_track_files)

        return func


# Функция ищет все файлы в dir, которых нет в .cvsignore.txt
def find_all_files(directory):
    ignore_files = ['.cvs', '.cvsignore.txt', 'CVS_prog.py', 'bin_cvs']
    all_files = []
    remove_files = []

    if os.path.exists(os.path.join(directory, '.cvsignore.txt')):
        ignore_files += read_file(os.path.join(directory, '.cvsignore.txt'))

    for cur_file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, cur_file)):
            all_files.append(cur_file)

    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir not in ignore_files:
                for n_root, n_dirs, n_files in os.walk(dir):
                    for n_file in n_files:
                        all_files.append(os.path.join(dir, n_file))

    for ignore_file in ignore_files:
        if ignore_file[0] == '*':
            ignore_file = '.' + ignore_file + '$'
            for all_file in all_files:
                re_find_file = re.findall(ignore_file, all_file)
                if re_find_file:
                    remove_files.append(re_find_file[0])
        else:
            remove_files.append(ignore_file)

    for remove_file in remove_files:
        if remove_file in all_files:
            all_files.remove(remove_file)

    return all_files
