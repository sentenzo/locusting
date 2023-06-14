from .local_repo import LocalRepository
from tempfile import TemporaryDirectory


class BufferIsEmpty(Exception):
    pass


class GitManager:
    def __init__(self, local_repo: LocalRepository, buffer_size=100) -> None:
        self.base_repo = local_repo
        self.storage = TemporaryDirectory()
        self.buffer_size = buffer_size
        self.buffer = []
        self.fill_buffer()

    def _prepare_repo(self):
        location = TemporaryDirectory(dir=self.storage.name).name
        new_repo = self.base_repo.duplicate(location)
        self.buffer.append(new_repo)

    def fill_buffer(self):
        while len(self.buffer) < self.buffer_size:
            self._prepare_repo()

    def __enter__(self):
        return self

    def _cleanup(self):
        self.storage.cleanup()

    def __exit__(self):
        self._cleanup()

    def get_new_repo(self):
        if self.buffer:
            return self.buffer.pop()
        raise BufferIsEmpty
