import os


# Создает файл
def create_file(way):
    if not os.path.exists(way):
        open(way, 'w', encoding='utf-8-sig').close()
        return True
    return False


def write_file(way, data, make_paragraph=True):
    paragraph = ''
    if make_paragraph:
        paragraph = '\n'

    with open(way, 'a', encoding='utf-8-sig') as f:
        if isinstance(data, str):
            f.write(data + paragraph)
        else:
            for string in data:
                f.write(string + paragraph)


def rewrite_file(way, data, make_paragraph=True):
    paragraph = ''
    if make_paragraph:
        paragraph = '\n'

    with open(way, 'w', encoding='utf-8-sig') as f:
        if isinstance(data, str):
            f.write(data + paragraph)
        else:
            for string in data:
                f.write(string + paragraph)


def read_file(way):
    if os.path.exists(way):
        with open(way, 'r', encoding='utf-8-sig') as f:
            return f.read().splitlines()

    return []
