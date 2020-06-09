import unittest
import os
import shutil

from bin_cvs.base_work_with_files import create_file, write_file, read_file, rewrite_file
from bin_cvs.work_with_files import find_last_ver, add_deleted_files, find_all_files
from bin_cvs.classes import CVS, WorkingRep
from bin_cvs.functional import command_init, command_add, command_delete

current_directory = os.getcwd()
way_to_test_file = os.path.join(current_directory, 'test_file.txt')


class TestBaseWorkWithFile(unittest.TestCase):
    def test_create_file(self):
        create_file(way_to_test_file)
        self.assertTrue(os.path.exists(way_to_test_file))
        os.remove(way_to_test_file)

    def test_read_empty_file(self):
        open(way_to_test_file, 'w', encoding='utf-8').close()
        self.assertEqual(read_file(way_to_test_file), [])
        os.remove(way_to_test_file)

    def test_read_file_with_str(self):
        with open(way_to_test_file, 'w', encoding='utf-8') as f:
            f.write('Hello')
        self.assertEqual(read_file(way_to_test_file), ['Hello'])
        os.remove(way_to_test_file)

    def test_read_file_str_with_paragraph(self):
        with open(way_to_test_file, 'w', encoding='utf-8') as f:
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
        self.assertEqual(read_file(way_to_test_file), data)
        os.remove(way_to_test_file)

    def test_write_file_array_str_without_paragraph(self):
        data = ['Hello', 'World', '!']
        write_file(way_to_test_file, data, False)
        self.assertEqual(read_file(way_to_test_file), ['HelloWorld!'])
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
        self.assertEqual(read_file(way_to_test_file), ['Hello, World!'])
        os.remove(way_to_test_file)


class TestWorkWithFiles(unittest.TestCase):
    def test_find_last_ver_without_initialized_cvs(self):
        self.assertEqual(find_last_ver(current_directory), 0)

    def test_find_last_ver_second_ver(self):
        way_to_cvs = os.path.join(current_directory, '.cvs')
        os.mkdir(way_to_cvs)
        os.mkdir(os.path.join(way_to_cvs, 'prjVer'))
        os.mkdir(os.path.join(way_to_cvs, 'prjVer', '2'))
        self.assertEqual(find_last_ver(current_directory), 2)
        shutil.rmtree(way_to_cvs)

    def test_find_all_files_empty_dir(self):
        way_to_test_dir = os.path.join(current_directory, 'test_dir')
        os.mkdir(way_to_test_dir)
        self.assertEqual(find_all_files(way_to_test_dir), [])
        os.rmdir(way_to_test_dir)

    def test_find_all_files_without_files_only_dirs(self):
        way_to_test_dir = os.path.join(current_directory, 'test_dir')
        os.mkdir(way_to_test_dir)
        os.mkdir(os.path.join(way_to_test_dir, 'hello'))
        os.mkdir(os.path.join(way_to_test_dir, 'world'))
        self.assertEqual(find_all_files(way_to_test_dir), [])
        shutil.rmtree(way_to_test_dir)

    def test_find_all_files_with_base_files_and_base_ignore(self):
        self.assertEqual(find_all_files(current_directory), ['test.py'])

    def test_find_all_files_with_new_file(self):
        way_to_test_dir = os.path.join(current_directory, 'test_dir')
        os.mkdir(way_to_test_dir)
        open(os.path.join(way_to_test_dir, 'file'), 'w', encoding='utf-8').close()
        self.assertEqual(find_all_files(way_to_test_dir), ['file'])
        shutil.rmtree(way_to_test_dir)

    def test_find_all_files_with_new_files(self):
        way_to_test_dir = os.path.join(current_directory, 'test_dir')
        os.mkdir(way_to_test_dir)
        open(os.path.join(way_to_test_dir, 'file'), 'w', encoding='utf-8').close()
        open(os.path.join(way_to_test_dir, 'file1.txt'), 'w', encoding='utf-8').close()
        open(os.path.join(way_to_test_dir, 'file123.qwer'), 'w', encoding='utf-8').close()
        self.assertEqual(find_all_files(way_to_test_dir), ['file', 'file1.txt', 'file123.qwer'])
        shutil.rmtree(way_to_test_dir)


class TestClasses(unittest.TestCase):
    work_rep = WorkingRep(current_directory, find_last_ver(current_directory))

    def test_cur_dir(self):
        self.assertEqual(self.work_rep.cur_dir, current_directory)

    def test_last_project_version(self):
        self.assertEqual(self.work_rep.last_project_version, find_last_ver(current_directory))

    def test_way_to_cvs(self):
        self.assertEqual(self.work_rep.way_to_cvs, os.path.join(current_directory, '.cvs'))

    def test_way_to_prj_ver(self):
        self.assertEqual(self.work_rep.way_to_prj_ver, os.path.join(current_directory, '.cvs', 'prjVer'))

    def test_way_to_cvs_data(self):
        self.assertEqual(self.work_rep.way_to_cvs_data, os.path.join(current_directory, '.cvs', 'cvsData'))

    def test_way_to_added_file(self):
        self.assertEqual(self.work_rep.way_to_added_file,
                         os.path.join(current_directory, '.cvs', 'prjVer', '.addedFiles'))

    def test_way_to_last_prj_ver(self):
        self.assertEqual(self.work_rep.way_to_last_prj_ver,
                         os.path.join(current_directory, '.cvs', 'prjVer', str(self.work_rep.last_project_version)))

    def test_way_to_track_files(self):
        self.assertEqual(self.work_rep.way_to_track_file,
                         os.path.join(current_directory, '.cvs', 'cvsData', 'trackFiles.txt'))

    def test_way_to_cvs_ignore(self):
        self.assertEqual(self.work_rep.way_to_cvs_ignore, os.path.join(current_directory, '.cvsignore.txt'))

    my_cvs = CVS

    def test_my_cvs_cur_dir(self):
        self.assertEqual(self.my_cvs.cur_dir, current_directory)

    def test_my_cvs_last_prj_ver(self):
        self.assertEqual(self.my_cvs.last_project_version, 0)

    def test_my_cvs_track_files(self):
        self.assertEqual(self.my_cvs.track_files, [])

    def test_my_cvs_added_files(self):
        self.assertEqual(self.my_cvs.added_files, [])

    def test_my_cvs_path(self):
        self.assertEqual(self.my_cvs.path.__class__,
                         WorkingRep(current_directory, find_last_ver(current_directory)).__class__)


class TestFunctional(unittest.TestCase):
    def test_command_init(self):
        self.assertTrue(command_init())
        self.assertTrue(os.path.exists(os.path.join(current_directory, '.cvs')))
        self.assertTrue(os.path.exists(os.path.join(current_directory, '.cvs', 'prjVer')))
        self.assertTrue(os.path.exists(os.path.join(current_directory, '.cvs', 'cvsData')))
        shutil.rmtree(os.path.join(current_directory, '.cvs'))

    def test_reinitialize_cvs(self):
        command_init()
        self.assertFalse(command_init())
        shutil.rmtree(os.path.join(current_directory, '.cvs'))

    def test_command_add(self):
        my_cvs = CVS
        command_init()
        open(way_to_test_file, 'w', encoding='utf-8').close()
        command_add('test_file.txt')
        self.assertEqual(read_file(my_cvs.path.way_to_track_file), ['test_file.txt'])
        os.remove(way_to_test_file)
        shutil.rmtree(os.path.join(current_directory, '.cvs'))

    def test_command_add_with_reg_exp_dot(self):
        my_cvs = CVS
        command_init()
        open(way_to_test_file, 'w', encoding='utf-8').close()
        open(os.path.join(current_directory, 'file.txt'), 'w', encoding='utf-8').close()
        command_add('.')

        for track_file in read_file(my_cvs.path.way_to_track_file):
            self.assertTrue(track_file in ['test.py', 'file.txt', 'test_file.txt'])

        os.remove(way_to_test_file)
        os.remove(os.path.join(current_directory, 'file.txt'))
        shutil.rmtree(os.path.join(current_directory, '.cvs'))

    def test_command_add_with_reg_exp_add_txt_files(self):
        my_cvs = CVS
        command_init()
        open(way_to_test_file, 'w', encoding='utf-8').close()
        open(os.path.join(current_directory, 'file.txt'), 'w', encoding='utf-8').close()
        command_add('*.txt')

        for track_file in read_file(my_cvs.path.way_to_track_file):
            self.assertTrue(track_file in ['file.txt', 'test_file.txt'])

        os.remove(way_to_test_file)
        os.remove(os.path.join(current_directory, 'file.txt'))
        shutil.rmtree(os.path.join(current_directory, '.cvs'))

    def test_command_delete(self):
        my_cvs = CVS
        command_init()
        rewrite_file(my_cvs.path.way_to_track_file, 'test_file.txt')
        command_delete('test_file.txt')
        self.assertEqual(read_file(my_cvs.path.way_to_track_file), [])
        shutil.rmtree(os.path.join(current_directory, '.cvs'))

    def test_command_delete_with_reg_exp_dot(self):
        my_cvs = CVS
        command_init()
        rewrite_file(my_cvs.path.way_to_track_file, ['test_file.txt', 'file1', 'file2.png'])
        command_delete('.')
        self.assertEqual(read_file(my_cvs.path.way_to_track_file), [])
        shutil.rmtree(os.path.join(current_directory, '.cvs'))
