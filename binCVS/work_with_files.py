import os


# Возвращает отслеживаемые файлы
def return_track_files(directory):
    if os.path.exists(os.path.join(directory, '.cvs', 'cvsData', 'trackFiles.txt')):
        with open(os.path.join(directory, '.cvs', 'cvsData', 'trackFiles.txt'), 'r', encoding='utf-8-sig') as f:
            track_files = f.read().splitlines()
            return track_files
    return []


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
def add_deleted_files(directory):
    files = find_all_files(directory)
    way_to_track_files = os.path.join(directory, '.cvs', 'cvsData', 'trackFiles.txt')

    f = open(way_to_track_files, 'w', encoding='utf-8-sig')
    count = 0

    for t_file in way_to_track_files:
        if t_file not in files:
            print('    - ' + t_file)
            count += 1
        else:
            f.write(t_file + '\n')
    f.close()

    if count < 1:
        return False
    return True

# Функция ищет все файлы в dir, которых нет в .cvsignore.txt
def find_all_files(directory):
    files = os.listdir(directory)
    ignore_files = ['.cvs', '.cvsignore.txt', 'CVS.py', 'functional.py']
    return_files = []

    if os.path.exists(os.path.join(directory, '.cvsignore.txt')):  # Херня какая-то
        with open(os.path.join(directory, '.cvsignore.txt'), encoding='utf-8-sig') as ignore:
            ignore_files += ignore.read().splitlines()

    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            if file not in ignore_files:
                return_files.append(file)
        elif file not in ignore_files:
            other_files = find_all_files(os.path.join(directory, file))
            for f in other_files:
                if f not in ignore_files:
                    return_files.append(os.path.join(file, f))

    return return_files