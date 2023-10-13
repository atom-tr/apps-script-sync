from os import makedirs, environ
from os.path import dirname, join
from shutil import copy, rmtree

environ["GIT_PYTHON_REFRESH"] = "quiet"
from git import Repo
from github import Github, AuthenticatedUser, Repository

from manager_environment import EnvironmentManager as EM


class GitHubManager:
    USER: AuthenticatedUser
    REPO: Repo
    REMOTE: Repository

    _REMOTE_NAME: str
    _REMOTE_PATH: str
    _SINGLE_COMMIT_BRANCH = "latest_branch"

    @classmethod
    def prepare_github_env(cls):
        """
        Download and store for future use:
        - Current GitHub user.
        - Named repo of the user [username]/[username].
        - Clone of the named repo.
        """
        github = Github(EM.GH_TOKEN)
        clone_path = "repo"
        cls.USER = github.get_user()
        rmtree(clone_path, ignore_errors=True)

        cls._REMOTE_NAME = f"{cls.USER.login}/{EM.GITHUB_REPOSITORY}"
        cls._REPO_PATH = f"https://{EM.GH_TOKEN}@github.com/{cls._REMOTE_NAME}.git"

        cls.REMOTE = github.get_repo(cls._REMOTE_NAME)
        cls.REPO = Repo.clone_from(cls._REPO_PATH, to_path=clone_path)

    @classmethod
    def branch(cls, requested_branch: str) -> str:
        """
        Gets requested branch name or the default branch name if requested branch wasn't found.
        The default branch name is regularly, 'main' or 'master'.

        :param requested_branch: Requested branch name.
        :returns: Commit author.
        """
        return cls.REMOTE.default_branch if requested_branch == "" else requested_branch

    @staticmethod
    def _copy_file_and_add_to_repo(src_path: str):
        """
        Copies file to repository folder, creating path if needed and adds file to git.
        The copied file relative to repository root path will be equal the source file
        relative to work directory path.

        :param src_path: Source file path.
        """
        dst_path = join(GitHubManager.REPO.working_tree_dir, src_path)
        makedirs(dirname(dst_path), exist_ok=True)
        copy(src_path, dst_path)
        GitHubManager.REPO.git.add(dst_path)
