import os, shutil
import os
import shutil
from subprocess import call


def copy_dir(src_path, dest_path):
    try:
        print("Copying", src_path, "to", dest_path)
        call(['cp', '-rp', src_path, dest_path])
    except Exception as e:
        print("Exception:", e)
        return e


def clean_dir(dir_path, exclude=[]):
    print("Cleaning the contents of", dir_path)
    for folder in os.listdir(dir_path):
        if folder in exclude:
            continue
        folder_path = os.path.join(dir_path, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        else:
            os.remove(folder_path)


def retrieve_archive(filename, extract_dir, archive_format):
    try:
        shutil.unpack_archive(filename, extract_dir, archive_format)
    except Exception as e:
        print("Exception:", e)
        return e


def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

make_archive('/path/to/folder', '/path/to/folder.zip')  