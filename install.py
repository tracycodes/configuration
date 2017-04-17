#! /usr/local/bin/python3

# Install any tools that we need and move the dot files into the correct locations.

import os
import time
import sys
import inspect
import errno

class Constants:
    WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    HOME_DIRECTORY = os.path.expanduser('~')
    BIN_DIRECTORY = os.path.join(HOME_DIRECTORY, "bin/")
    DROPBOX_DIRECTORY = os.path.join(HOME_DIRECTORY, "Dropbox/")
    CLONES_PATH = os.path.join(HOME_DIRECTORY, "code/clones/")
    START_TIME = time.time()

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
        # TSL - The timestamp is negative zero for some reason
        print("[{0}] @ {1:.2f}: {2}".format(message_type, Constants.START_TIME - time.time(), message))


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
    def initialize_system(self):
        # TSL - Add functionality to setup a new structure on a system and clone down all of the frequently used repos
        pass

    def validate_system(self):
        if not os.path.isdir(Constants.HOME_DIRECTORY):
            CommandLine.fatal("Home directory does not exist at `{0}`".format(Constants.HOME_DIRECTORY))
        if not os.path.isdir(Constants.CLONES_PATH):
            CommandLine.fatal("Clone directory does not exist at `{0}`".format(Constants.CLONES_PATH))
        if not os.path.isdir(Constants.BIN_DIRECTORY):
            CommandLine.fatal("Binary directory does not exist at `{0}`".format(Constants.BIN_DIRECTORY))
        if not os.path.isdir(Constants.DROPBOX_DIRECTORY):
            CommandLine.fatal("Dropbox directory does not exist at `{0}`".format(Constants.DROPBOX_DIRECTORY))

    def install_all(self):
        installers = inspect.getmembers(Configurations)

        # Find and run all installer methods
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
    def install_tmuxinator():
        # Add tmuxinator completion
        tmuxinator_completion = Constants.CLONES_PATH + "tmuxinator/completion/tmuxinator.bash"
        if os.path.isfile(tmuxinator_completion):
            CommandLine.say("Symlinking `{0}` to `{1}`".format(tmuxinator_completion, Constants.BIN_DIRECTORY))
            Helpers.safe_link(tmuxinator_completion, Constants.BIN_DIRECTORY + "tmuxinator.bash")
        else:
            CommandLine.error("Unable to locate tmuxinator @ `{0}`. Tmuxinator was not installed.".format(tmuxinator_completion))

        # Add tmuxinator configuration
        tmuxinator_configuration = Constants.DROPBOX_DIRECTORY + "dotfiles/tmuxinator"
        symlink_path = os.path.join(Constants.HOME_DIRECTORY, ".tmuxinator")
        if os.path.isdir(tmuxinator_configuration):
            CommandLine.say("Symlinking `{0}` to `{1}`".format(tmuxinator_configuration, symlink_path))
            Helpers.safe_link(tmuxinator_configuration, symlink_path)
        else:
            CommandLine.warn("No tmuxinator configurations exist")
            return False

        CommandLine.say("Symlink in place. Add `source ~/bin/tmuxinator.bash` to your .bashrc if it's not already included")

        # TSL -  Add a generate component that is automatically appended to the bashrc (?)
        return True

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

    # TSL - install GNU tools

    # TSL - install rvm

    # TSL - install python, node, xcode tools

def main():
    installer = Installer()
    installer.validate_system()
    installer.install_all()

if __name__ == '__main__':
    main()
