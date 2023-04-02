from sys import argv

from models.directory import Directory


class FilePermissionsMonitor():
    """Monitor of file permissions in a directory"""
    def __init__(self, dir_path):
        directory = Directory(dir_path)
        self.files = directory.all_files
        self.read_denied_dirs = directory.read_denied_dirs
        self.setuid_files = set()
        self.setgid_files = set()
        self.group_x_files = set()
        self.others_x_files = set()
        self._populate_filters()

    def _populate_filters(self):
        """Loops over files and populate filters"""
        for file in self.files:
            user_permissions = file.get_user_permissions()
            group_permissions = file.get_group_permissions()
            others_permissions = file.get_others_permissions()

            if user_permissions[2] == 's':
                self.setuid_files.add(file)
            if group_permissions[2] == 's':
                self.setgid_files.add(file)
            elif group_permissions[2] == 'x':
                self.group_x_files.add(file)
            if others_permissions[2] == 'x':
                self.others_x_files.add(file)

    def _print_file_set(self, header, file_set):
        if not file_set:
            return
        print('\n' + '-' * 80)
        print(header + '\n')
        for file in file_set:
            print(file)

    def print_report(self):
        """Reports files with permissions for potential exploitations"""
        print('\n\n' + '#' * 44 + '  FILE PERMISSIONS REPORT  ' + '#' * 44 + '\n')

        self._print_file_set(
            header='List of files that are EXECUTABLE by OTHERS and have the SetUID bit:',
            file_set=self.setuid_files.intersection(self.others_x_files)
            )
        self._print_file_set(
            header='List of files that are EXECUTABLE by OTHERS and have the SetGID bit:',
            file_set=self.setgid_files.intersection(self.others_x_files)
            )
        self._print_file_set(
            header='List of remaining files that are EXECUTABLE by OTHERS:',
            file_set=self.others_x_files - self.setuid_files - self.setgid_files
        )
        self._print_file_set(
            header='List of files that are EXECUTABLE by GROUP and have the SetUID bit:',
            file_set=self.setuid_files.intersection(self.group_x_files)
            )
        self._print_file_set(
            header='List of remaining files that are EXECUTABLE by GROUP:',
            file_set=self.group_x_files - self.setuid_files
        )
        self._print_file_set(
            header='List of directories that couldn\'t be read:',
            file_set=set(self.read_denied_dirs)
        )


if __name__ == "__main__":
    if len(argv) != 2:
        raise Exception("Incorrect number of arguments.")
    path = argv[1]
    monitor = FilePermissionsMonitor(path)
    monitor.print_report()