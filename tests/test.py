import unittest
import os

from binCVS.base_work_with_files import create_file, write_file, read_file, rewrite_file
from binCVS.classes import CVS, WorkingRep

current_directory = os.getcwd()
way_to_test_file = os.path.join(current_directory, 'test_file.txt')


class TestBaseWorkWithFile(unittest.TestCase):
    def test_create_file(self):
        create_file(way_to_test_file)
        self.assertTrue(os.path.exists(way_to_test_file))
        os.remove(way_to_test_file)

    def test_read_empty_file(self):
        f = open(way_to_test_file, 'w', encoding='utf-8').close()
        self.assertEqual(read_file(way_to_test_file), '')
        os.remove(way_to_test_file)

    def test_read_file_with_str(self):
        with open('textfile_1.txt', 'tw', encoding='utf-8') as f:
            f.write('Hello')
        self.assertEqual(read_file(way_to_test_file), 'Hello')
        os.remove(way_to_test_file)

    def test_read_file_str_with_paragraph(self):
        with open('textfile_1.txt', 'tw', encoding='utf-8') as f:
            f.write('Hello\nWorld')
        self.assertEqual(read_file(way_to_test_file), ['Hello', 'World'])
        os.remove(way_to_test_file)

    def test_write_file_str(self):
        data = 'Hello'
        write_file(way_to_test_file, data)
        self.assertEqual(read_file(way_to_test_file), [data])
        os.remove(way_to_test_file)

    def test_write_file_array_str_with_paragraph(self):
        data = ['Hello', 'World', '!']
        write_file(way_to_test_file, data)
        self.assertEqual(read_file(way_to_test_file), [data])
        os.remove(way_to_test_file)

    def test_write_file_array_str_without_paragraph(self):
        data = ['Hello', 'World', '!']
        write_file(way_to_test_file, data)
        self.assertEqual(read_file(way_to_test_file), 'HelloWorld!')
        os.remove(way_to_test_file)

    def test_write_file_few_times(self):
        data = 'Hello'
        for i in range(3):
            write_file(way_to_test_file, data)
        self.assertEqual(read_file(way_to_test_file), ['Hello', 'Hello', 'Hello'])
        os.remove(way_to_test_file)

    def test_rewrite_file(self):
        data = 'Hello'
        write_file(way_to_test_file, data)
        rewrite_file(way_to_test_file, 'Hello, World!')
        self.assertEqual(read_file(way_to_test_file), 'Hello, World!')
        os.remove(way_to_test_file)


class TestClasses(unittest.TestCase):
    pass
