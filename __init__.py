import os
import subprocess
import shutil

from configuration import Configuration
from git import Repo


class ExtendedFork():
    def __init__(self, config: Configuration):
        self.config = config
        self.parent_repo = Repo(config.parent_repo_path)
        self.current_repo = Repo(".")

    def execute(self):
        current_commit = self._find_commit(self.config.current_base_commit, self.current_repo)
        branch = self.current_repo.create_head("extrebase", current_commit)
        branch.checkout()

        for relative_path in subprocess.check_output(["git", "ls-files"]).decode("utf-8").splitlines():
            current_path = os.path.join(".", relative_path)
            main_path = self._main_path(current_path)

            if main_path:
                shutil.copy(main_path, current_path)
                self.current_repo.index.add([relative_path])

        #self.current_repo.git.commit("--amend", "--no-edit")

    def _find_commit(self, shortsha: str, repo: Repo):
        for commit in repo.iter_commits():
            if commit.name_rev.startswith(shortsha):
                return commit

        return None

    def _current_path(self, path: str):
        return os.path.join(".", path)

    def _main_path(self, path: str):
        for f, t in self.config.directory_mapping.items():
            if path.startswith(f):
                main_relative_path = os.path.join(t, path[len(f)+1:])
                main_path = os.path.join(self.config.parent_repo_path, main_relative_path)
                if os.path.exists(main_path):
                    return main_path

        for f, t in self.config.file_mapping.items():
            if path.endswith(f):
                if os.path.exists(t):
                    return t

        return None


#current_repo.head.reset(config.current_base_commit)
config = Configuration.load("./.git_extended_fork")
ExtendedFork(config).execute()
