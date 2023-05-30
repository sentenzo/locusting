from tempfile import TemporaryDirectory

from locust import User, between, events, run_single_user, task

from utils.config import git_config as config
from utils.git.local_repo import LocalRepository
from utils.locust_helpers import self_firing


class GitUser(User):
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
    @self_firing(request_type="git", name="git_pull")
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
