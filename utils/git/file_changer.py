class FileChangerError(Exception):
    pass


def change_files(path, confurmation=None):
    if confurmation != (
        "Yes, I know this action will irreversibly delete my files "
        "on the path specified."
    ):
        raise FileChangerError("Please provide a suitable confurmation.")
