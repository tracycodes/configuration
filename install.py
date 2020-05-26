#! /usr/local/bin/python3

# Install any tools that we need and move the dot files into the correct locations.

import os
from datetime import datetime
import sys
import inspect
import errno
import requests
import subprocess

class Constants:
    WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    HOME_DIRECTORY = os.path.expanduser('~')
    DROPBOX_DIRECTORY = os.path.join(HOME_DIRECTORY, "Dropbox/")
    CLONES_PATH = os.path.join(HOME_DIRECTORY, "code/clones/")
    VIM_PLUG_FILE = os.path.join(HOME_DIRECTORY, ".vim/autoload/plug.vim")
    START_TIME = datetime.now()
    VIM_PLUG_URL = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    VIM_COLOR_REPO = "git@github.com:altercation/vim-colors-solarized.git"
    VIM_COLOR_INSTALL_PATH = os.path.join(HOME_DIRECTORY, ".vim/colors/")
    VIM_COLOR_FILE = 'solarized.vim'
    VIM_COLOR_CLONE_PATH = os.path.join(CLONES_PATH, 'vim-colors-solarized/colors')
    SSH_KEY_PATH = os.path.join(HOME_DIRECTORY, ".ssh/macbook-work")

class Helpers:
    @staticmethod
    def safe_link(source, link_name):
        try:
            os.symlink(source, link_name)
            return True
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            CommandLine.warn("Symlink already exists. Attempted to link `{0}` to `{1}".format(source, link_name))
            return False


class CommandLine:
    @staticmethod
    def say(message, message_type='info'):
        print("[{0}] {1}: {2}".format(message_type, datetime.now(), message))

    @staticmethod
    def warn(message):
        CommandLine.say(message, 'warn')

    @staticmethod
    def error(message):
        CommandLine.say(message, 'error')

    @staticmethod
    def fatal(message):
        CommandLine.say(message, 'fatal')
        sys.exit()


class Installer:
    def validate_system(self):
        if not os.path.isdir(Constants.HOME_DIRECTORY):
            CommandLine.fatal("Home directory does not exist at `{0}`".format(Constants.HOME_DIRECTORY))
        if not os.path.isdir(Constants.CLONES_PATH):
            CommandLine.fatal("Clone directory does not exist at `{0}`".format(Constants.CLONES_PATH))
        if not os.path.isdir(Constants.DROPBOX_DIRECTORY):
            CommandLine.fatal("Dropbox directory does not exist at `{0}`".format(Constants.DROPBOX_DIRECTORY))

    def install_all(self):
        installers = inspect.getmembers(Configurations)

        for installer in installers:
            installer_method = installer[0]
            if installer_method.find('install_') == 0:
                CommandLine.say('Running installer `{0}`'.format(installer_method))
                if getattr(Configurations, installer_method)():
                    CommandLine.say('Installer completed successfully.')
                else:
                    CommandLine.warn('Installer failed to complete.')

class Configurations:
    @staticmethod
    def install_dotfiles():
        dotfiles = os.path.join(Constants.WORKING_DIRECTORY, "dotfiles")

        symlinked_files = 0
        for dotfile in os.listdir(dotfiles):
            dotfile_path = os.path.join(dotfiles, dotfile)
            if os.path.isfile(dotfile_path):
                symlink_path = os.path.join(Constants.HOME_DIRECTORY, dotfile)
                CommandLine.say("Symlinking `{0}` to `{1}`".format(dotfile_path, symlink_path))
                if Helpers.safe_link(dotfile_path, symlink_path):
                    symlinked_files += 1


        if symlinked_files == 0:
            CommandLine.say("All dotfiles already symlinked")
        else:
            CommandLine.say("Installed {0} dotfiles".format(symlinked_files))

        return True

    # TSL - Add osx defaults writes
    @staticmethod
    def install_osx_configuration():
        pass

    @staticmethod
    def install_ssh():
        ssh_keys = Constants.DROPBOX_DIRECTORY + "dotfiles/ssh"
        symlink_path = os.path.join(Constants.HOME_DIRECTORY, ".ssh")
        if os.path.isdir(ssh_keys):
            CommandLine.say("Symlinking `{0}` to `{1}`".format(ssh_keys, symlink_path))
            Helpers.safe_link(ssh_keys, symlink_path)
        else:
            CommandLine.warn("No ssh keys directory exists")
            return False

        return True


    @staticmethod
    def install_vim():
        # Install vim.plug
        if not os.path.isfile(Constants.VIM_PLUG_FILE):
            plug_script = requests.get(Constants.VIM_PLUG_URL)
            with open(Constants.VIM_PLUG_FILE, "w+") as fd:
                written = fd.write(plug_script.text)
                CommandLine.say("Wrote vim plug. Bytes written: {}".format(written))
        else:
            CommandLine.say("Vim plug already installed")

        # Clone colors repository
        colors_path = os.path.join(Constants.CLONES_PATH, 'vim-colors-solarized')
        if not os.path.isdir(colors_path):
            CommandLine.say("Cloning colors repository")
            ssh_create_agent = ['ssh-agent']
            ssh_add_key = ['ssh-add {}'.format(Constants.SSH_KEY_PATH)]
            clone_colors_repo = ['git clone {} {}'.format(Constants.VIM_COLOR_REPO, colors_path)]

            for i in [ssh_create_agent, ssh_add_key, clone_colors_repo]:
                process = subprocess.Popen(i,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True)

                CommandLine.say("Running Subprocess command: {}".format(i))
                stdout, stderr = process.communicate()
                if len(stdout):
                    CommandLine.say("Subprocess: stdout - {}".format(stdout))
                if len(stderr):
                    CommandLine.say("Subprocess: stderr - {}".format(stderr))
                if process.returncode > 0:
                    CommandLine.fatal("Error running process, code: {}".format(process.returncode))
        else:
            CommandLine.say("Colors repository already exists")

        if not os.path.isdir(Constants.VIM_COLOR_INSTALL_PATH):
            os.mkdir(Constants.VIM_COLOR_INSTALL_PATH)

        # Install links
        vim_color_link = os.path.join(Constants.VIM_COLOR_INSTALL_PATH, Constants.VIM_COLOR_FILE)
        vim_color_clone_file = os.path.join(Constants.VIM_COLOR_CLONE_PATH, Constants.VIM_COLOR_FILE)
        CommandLine.say("Symlinking `{0}` to `{1}`".format(vim_color_clone_file, vim_color_link))
        Helpers.safe_link(vim_color_clone_file, vim_color_link)


    # TSL - install GNU tools

    # TSL - install rvm

    # TSL - install python, node, xcode tools

def main():
    installer = Installer()
    installer.validate_system()
    # installer.install_all()
    Configurations.install_ssh()
    Configurations.install_dotfiles()
    Configurations.install_vim()

if __name__ == '__main__':
    main()
