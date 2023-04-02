import os

from .file import File


class Directory():
    """A linux directory"""
    def __init__(self, dir_path):
        print(f'analyzing {dir_path}')
        if not os.path.isdir(dir_path):
            raise ValueError("Directory path not valid")
        self.dir_path = dir_path
        self.files = []
        self.subdirs = []
        self.all_files = []
        self.read_denied_dirs = []
        self._create_tree()

    def _create_tree(self):
        """Finds files and sub-directories in directory and
        updates files and sub_dirs attributes"""
        files = []
        subdirs = []
        all_files = []
        read_denied_dirs = []

        try:
            for name in os.listdir(self.dir_path):
                file_path = os.path.join(self.dir_path, name)
                if os.path.isfile(file_path):
                    file = File(name, self.dir_path)
                    files.append(file)
                elif os.path.isdir(file_path):
                    subdir = Directory(os.path.join(self.dir_path, name))
                    subdirs.append(subdir)
                    all_files += subdir.all_files
                    read_denied_dirs += subdir.read_denied_dirs

            self.files = files
            self.subdirs = subdirs
            self.all_files = files + all_files
            self.read_denied_dirs = read_denied_dirs
        except PermissionError:
            self.read_denied_dirs.append(self)

    def __str__(self):
        return self.dir_path