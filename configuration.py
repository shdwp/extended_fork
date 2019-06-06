import configparser
import os
import typing


class Configuration:
    class ConfigurationNotFoundException(Exception):
        pass

    class ConfigurationParseException(Exception):
        pass

    class ConfigurationInvalidException(Exception):
        pass

    def __init__(self, parent_repo_path: str, parent_base_commit: str, current_base_commit: str, directory_mapping: typing.Dict[str, str], file_mapping: typing.Dict[str, str]):
        self.parent_repo_path = os.path.expanduser(os.path.expandvars(parent_repo_path))
        self.parent_base_commit = parent_base_commit
        self.current_base_commit = current_base_commit

        self.directory_mapping = directory_mapping
        self.file_mapping = file_mapping

    @staticmethod
    def load(path: str):
        config = configparser.ConfigParser()

        if not os.path.exists(path):
            raise Configuration.ConfigurationNotFoundException()

        try:
            config.read("./.git_extended_fork")
        except:
            raise Configuration.ConfigurationParseException()

        try:
            return Configuration(config["parentRepo"]["path"],
                                 config["parentRepo"]["baseCommit"],
                                 config["currentRepo"]["baseCommit"],
                                 dict(config["directoryMapping"]),
                                 dict(config["fileMapping"]))
        except KeyError:
            raise Configuration.ConfigurationInvalidException()

