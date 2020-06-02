import os
import difflib

from binCVS.ClassCVS import my_cvs
from binCVS.base_work_with_files import write_file, rewrite_file, read_file


# Собирает файл с учётом изменений всех версий
def build_file(file_name, ver):
    first_ver = True

    builded_file = []

    for i in range(1, int(ver) + 1):
        way_to_file = os.path.join(my_cvs.way_to_prj_ver, str(i), file_name)
        if os.path.exists(way_to_file):
            if first_ver:
                builded_file = read_file(way_to_file)
                first_ver = False
            else:
                if os.path.exists(way_to_file):
                    changed_str = read_file(way_to_file)
                    check_minus = 0

                    for change_str in changed_str:
                        change_str = change_str.split(' ', 1)
                        if change_str[0][-1] == '+':
                            builded_file.insert(int(change_str[0][0:-1]) - 1, change_str[1])
                        else:
                            builded_file.pop(int(change_str[0][0:-1]) - 1 - check_minus)
                            check_minus += 1
    return builded_file


# Заменяет файлы в основной директории
def make_file(file_name, ver=None):
    way_to_file = make_subdirectory(my_cvs.cur_dir, file_name)

    if not ver:
        builded_file = build_file(file_name, my_cvs.last_project_version)
    else:
        builded_file = build_file(file_name, ver)

    rewrite_file(way_to_file, builded_file)


# Построчное сравнение двух файлов, если изменения были, то выводит True
def make_diff(file_name):
    file1_text = read_file(os.path.join(my_cvs.cur_dir, file_name))
    file2_text = build_file(file_name, my_cvs.last_project_version)

    d = difflib.Differ()
    diff = d.compare(file2_text, file1_text)

    differences = []
    count_str = 0

    for diff_str in diff:
        count_str += 1
        if diff_str[0] == '+' or diff_str[0] == '-':
            differences.append(str(count_str) + diff_str + '\n')

    if len(differences) > 0:
        way_to_finished_file = make_subdirectory(
            os.path.join(my_cvs.cur_dir, '.cvs', 'prjVer', str(my_cvs.last_project_version + 1)), file_name)
        write_file(way_to_finished_file, differences, False)
        return file_name
    return ''


# Обрабатывает название файла на поддиректории, создаёт их и выводит путь к файлу
def make_subdirectory(way_dir, file_name):
    splited_dir = os.path.split(way_dir)

    if not splited_dir[0]:
        return os.path.join(way_dir, file_name)

    if not os.path.exists(os.path.join(way_dir, splited_dir[0])):
        os.mkdir(os.path.join(way_dir, splited_dir[0]))

    return os.path.join(way_dir, file_name)
