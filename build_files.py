import os
import difflib
from ClassCVS import my_cvs
from functional import way_to


# Собирает файл с учётом изменений всех версий
def build_file(file_name, ver=my_cvs.last_project_version):
    first_ver = True

    builded_file = []

    for i in range(1, ver + 1):
        way_to_file = way_to(my_cvs.cur_dir + '\\.cvs\\prjVer\\' + str(i), file_name)
        if os.path.exists(way_to_file):
            if first_ver:
                with open(way_to_file, 'r', encoding='utf-8-sig') as f:
                    builded_file = f.read().splitlines()

                    first_ver = False
            else:
                if os.path.exists(way_to_file):
                    with open(way_to_file, 'r', encoding='utf-8-sig') as f:
                        changes_str = f.read().splitlines()
                        check_minus = 0

                        for change_str in changes_str:
                            change_str = change_str.split(' ', 1)
                            if change_str[0][-1] == '+':
                                builded_file.insert(int(change_str[0][0:-1]) - 1, change_str[1])
                            else:
                                builded_file.pop(int(change_str[0][0:-1]) - 1 - check_minus)
                                check_minus += 1
    return builded_file


# Заменяет файлы в основной директории
def make_file(file_name, ver=None):
    files = file_name
    way_to_file = way_to(my_cvs.cur_dir, file_name)

    if not ver:
        builded_file = build_file(files)
    else:
        builded_file = build_file(files, ver)

    with open(way_to_file, 'w', encoding='utf-8-sig') as f:
        for file_str in builded_file:
            f.write(file_str + '\n')


# Построчное сравнение двух файлов, если изменения были, то выводит True
def make_diff(file_name):
    check_diff = False
    way_to_f1 = way_to(my_cvs.cur_dir, file_name)

    f1 = open(way_to_f1, 'r', encoding='utf-8-sig')
    file1_text = f1.read().splitlines()
    file2_text = build_file(my_cvs.cur_dir, file_name)
    f1.close()

    d = difflib.Differ()
    diff = d.compare(file2_text, file1_text)
    count_str = 0
    way_to_finished_file = way_to(my_cvs.cur_dir + '\\.cvs\\prjVer\\' + str(my_cvs.last_project_version), file_name)
    finished_file = open(way_to_finished_file, 'w', encoding='utf-8-sig')

    for diff_str in diff:
        count_str += 1
        if diff_str[0] == '+' or diff_str[0] == '-':
            check_diff = True

            finished_file.write(str(count_str) + diff_str + '\n')

    finished_file.close()
    if not check_diff:
        way_to_remove_file = way_to(my_cvs.cur_dir + '\\.cvs\\prjVer\\' + str(my_cvs.last_project_version), file_name)
        os.remove(way_to_remove_file)
    return check_diff
