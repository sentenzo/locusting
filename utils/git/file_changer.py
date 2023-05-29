import os
import random
import string
from uuid import uuid4


class FileChangerError(Exception):
    pass


class FileChanger:
    FILE_EXTANTIONS = ["", ".qw", ".we", ".er", ".rt", ".ty"]
    SYMBOLS = string.ascii_letters + string.digits + ".,;:()+-*/" + " " * 50
    MAX_LINE_LENGTH = 120
    MAX_LINES = 160

    @staticmethod
    def _get_random_line():
        line = random.choices(
            FileChanger.SYMBOLS,
            k=random.randint(0, FileChanger.MAX_LINE_LENGTH),
        )
        return "".join(line)

    @staticmethod
    def _get_random_file_name():
        return uuid4().hex() + random.choice(FileChanger.FILE_EXTANTIONS)

    def __init__(self, path, average_file_count=10):
        self.path = path
        self.average_file_count = average_file_count

    def _add_one_new_file(self, new_file_path=None):
        if not new_file_path:
            new_file_name = FileChanger._get_random_file_name()
            new_file_path = os.path.join(self.path, new_file_name)
        with open(new_file_path, "w") as new_file:
            for _ in range(random.randint(0, FileChanger.MAX_LINES)):
                line = FileChanger._get_random_line()
                new_file.write(line)
                new_file.write("\n\r")

    def _delete_one_file(self, delete_file_path=None):
        if not delete_file_path:
            files = self.get_file_list()
            name, delete_file_path = random.choice(files)
        os.remove(delete_file_path)

    def _rename_one_file(self):
        files = self.get_file_list()
        name, full_path = random.choice(files)
        new_name = FileChanger._get_random_file_name()
        new_full_path = os.path.join(self.path, new_name)
        os.rename(full_path, new_full_path)

    def _modefy_one_file(self):
        files = self.get_file_list()
        name, full_path = random.choice(files)
        self._delete_one_file(full_path)
        self._add_one_new_file(full_path)

    def _choose_action(self):
        files = self.get_file_list()
        file_count = len(files)
        if file_count == 0:
            return self._add_one_new_file
        if random.random() > 0.5:
            if file_count > self.average_file_count:
                return self._delete_one_file
            else:
                return self._add_one_new_file
        else:
            return random.choice(
                [self._modefy_one_file, self._rename_one_file]
            )

    def get_file_list(self):
        file_list = []
        obj_names_in_path = next(os.walk())[1]
        for name in obj_names_in_path:
            full_path = os.path.join(self.path, name)
            if os.path.isfile(full_path):
                file_list.append((name, full_path))
        return file_list

    def change_files(self, confurmation=None, times=3):
        if confurmation != (
            "Yes, I know this action will irreversibly delete my files "
            "on the path specified."
        ):
            raise FileChangerError("Please provide a suitable confurmation.")
        for _ in range(times):
            self._choose_action()()
