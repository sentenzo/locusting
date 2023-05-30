from tempfile import TemporaryDirectory
import time
from functools import wraps

from locust import User, HttpUser, between, run_single_user, task, events

from utils.config import git_config as config
from utils.git.local_repo import LocalRepository


def self_firing(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        start_time = time.time()
        exception = None
        result = None
        try:
            result = func(*args, **kwds)
        except Exception as ex:
            exception = ex
        events.request.fire(
            request_type="git",
            name="git_pull",
            response_length=0,
            start_time=start_time,
            response_time=time.time() - start_time,
            exception=exception,
        )
        return result

    return wrapper


class GitUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        local_repo_original = LocalRepository(
            config.local_repo.location,
            config.remote_repo.clone_url,
        )
        temp_dir = TemporaryDirectory()
        local_repo_duplicate = local_repo_original.duplicate(temp_dir.name)
        self.local_repo: LocalRepository = local_repo_duplicate
        self.temp_dir: TemporaryDirectory = temp_dir
        # pass

    @task
    @self_firing
    def git_pull(self):
        self.local_repo.pull()
        self.local_repo.revert_pull()
        # time.sleep(1)
        # raise IndexError

    def on_stop(self):
        self.temp_dir.cleanup()
        # pass


if __name__ == "__main__":
    run_single_user(GitUser)
