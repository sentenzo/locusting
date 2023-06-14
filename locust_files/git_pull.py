from tempfile import TemporaryDirectory

from locust import User, between, events, run_single_user, task

from git_.config import config
from git_.local_repo import LocalRepository
from git_.git_manager import GitManager, BufferIsEmpty
from utils.locust_helpers import self_firing

git_manager: GitManager | None = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global git_manager

    local_repo_original = LocalRepository(
        config.local_repo.location,
        config.remote_repo.clone_url,
    )
    git_manager = GitManager(local_repo_original, buffer_size=200)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    git_manager._cleanup()


class GitUser(User):
    wait_time = between(0.1, 1.0)

    def on_start(self):
        ...

    @task
    @self_firing(request_type="git", name="git_pull")
    def git_pull(self):
        try:
            local_repo = git_manager.get_new_repo()
            local_repo.pull()
            del local_repo
        except BufferIsEmpty:
            self.environment.reached_end = True
            self.environment.runner.quit()

    def on_stop(self):
        ...


if __name__ == "__main__":
    run_single_user(GitUser)
