from tempfile import TemporaryDirectory

from locust import User, between, run_single_user, task

from utils.config import git_config as config
from utils.git.local_repo import LocalRepository


class GitUser(User):
    wait_time = between(1, 5)

    def on_start(self):
        local_repo_original = LocalRepository(config.local_repo.location)
        temp_dir = TemporaryDirectory()
        local_repo_duplicate = local_repo_original.duplicate(str(temp_dir))
        self.local_repo: LocalRepository = local_repo_duplicate
        self.temp_dir: TemporaryDirectory = temp_dir

    @task
    def git_pull(self):
        self.local_repo.pull()
        self.local_repo.revert_pull()

    def on_stop(self):
        self.temp_dir.cleanup()


if __name__ == "__main__":
    run_single_user(GitUser)
