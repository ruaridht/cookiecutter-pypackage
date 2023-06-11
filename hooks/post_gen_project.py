#!/usr/bin/env python
import os
import shutil
import subprocess
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_path(filepath):
    try:
        path_to_remove = os.path.join(PROJECT_DIRECTORY, filepath)
        if os.path.isdir(path_to_remove):
            shutil.rmtree(path_to_remove)
        else:
            os.remove(path_to_remove)
    except FileNotFoundError:
        pass


def execute(*args, supress_exception = False, cwd=None):
    cur_dir = os.getcwd()

    try:
        if cwd:
            os.chdir(cwd)

        proc = subprocess.Popen(args, stdout = subprocess.PIPE, stderr= subprocess.PIPE)

        out, err = proc.communicate()
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        if err and not supress_exception:
            raise Exception(err)
        else:
            return out
    finally:
        os.chdir(cur_dir)


def init_git():
    # workaround for issue #1
    if not os.path.exists(os.path.join(PROJECT_DIRECTORY, ".git")):
        execute("git", "config", "--global", "init.defaultBranch", "main", cwd = PROJECT_DIRECTORY)
        execute("git", "init", cwd=PROJECT_DIRECTORY)


def install_pre_commit_hooks():
    execute(sys.executable, "-m", "pip", "install", "pre-commit==2.12.0")
    execute(sys.executable, "-m", "pre_commit", "install")


if __name__ == '__main__':

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.pkg_name }}', 'cli.py')
        remove_path(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_path('LICENSE')

    if "n" == "{{ cookiecutter.use_vscode_devcontainer }}":
        remove_path(".devcontainer")

    if "n" == "{{ cookiecutter.use_github_workflows }}":
        remove_path(".github/workflows")

    try:
        init_git()
    except Exception as e:
        print(e)

    if '{{ cookiecutter.install_precommit_hooks }}' == 'y':
        try:
            install_pre_commit_hooks()
        except Exception as e:
            print(str(e))
            print("Failed to install pre-commit hooks. Please run `pre-commit install` by your self. For more on pre-commit, please refer to https://pre-commit.com")
