import os
import stat

class File():
    """A linux file"""
    def __init__(self, name, dir_path):
        if not os.path.isdir(dir_path):
            raise ValueError("Directory path not valid")
        self.name = name
        self.dir_path = dir_path
        self.mode = os.stat(os.path.join(self.dir_path, self.name)).st_mode     
                            
    def _get_permissions(self, r, w, x, s):
        """Private method that returns a three-char list of permissions for user,
        group or others"""
        permission_str = ['-', '-', '-']
        if r:
            permission_str[0] = 'r'
        if w:
            permission_str[1] = 'w'
        if x and s:
            permission_str[2] = 's'
        elif x:
            permission_str[2] = 'x'
        elif s:
            permission_str[2] = 'S'
        return permission_str

    def get_user_permissions(self):
        """
        Returns a three-char list for file user permissions
        1st char: 'r' or '-' 
        2nd char: 'w' or '-'
        3rd char: 'x', 's', 'S' or '-'
        """
        # permission is determined by performing a bitwise AND between mode and each constant
        r = self.mode & stat.S_IRUSR
        w = self.mode & stat.S_IWUSR
        x = self.mode & stat.S_IXUSR
        s = self.mode & stat.S_ISUID
        return self._get_permissions(r, w, x, s)
    
    def get_group_permissions(self):
        """
        Returns a three-char list for file group permissions
        1st char: 'r' or '-' 
        2nd char: 'w' or '-'
        3rd char: 'x', 's', 'S' or '-'
        """
        # permission is determined by performing a bitwise AND between mode and each constant
        r = self.mode & stat.S_IRGRP
        w = self.mode & stat.S_IWGRP
        x = self.mode & stat.S_IXGRP
        s = self.mode & stat.S_ISGID
        return self._get_permissions(r, w, x, s)
    
    def get_others_permissions(self):
        """
        Returns a three-char list for file group permissions
        1st char: 'r' or '-' 
        2nd char: 'w' or '-'
        3rd char: 'x' pr '-'
        """
        # permission is determined by performing a bitwise AND between mode and each constant
        r = self.mode & stat.S_IROTH
        w = self.mode & stat.S_IWOTH
        x = self.mode & stat.S_IXOTH
        return self._get_permissions(r, w, x, s=False)
    
    def __str__(self):
        return os.path.join(self.dir_path, self.name)