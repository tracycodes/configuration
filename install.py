#! /usr/local/bin/python

# Install any tools that we need and move the dot files into the correct locations.

import os
import time
import sys
import inspect
import errno

class Constants:
    HOME_DIRECTORY = os.path.expanduser('~')
    BIN_DIRECTORY = os.path.join(HOME_DIRECTORY, "bin/")
    CLONES_PATH = os.path.join(HOME_DIRECTORY, "code/clones/")
    START_TIME = time.time()

class Helpers:
    @staticmethod
    def safe_link(source, link_name):
        try:
            os.symlink(source, link_name)
            return True
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
            CommandLine.warn("Symlink already exists. Attempted to link `{0}` to `{1}".format(source, link_name))
            return False

class CommandLine:
    @staticmethod
    def say(message, message_type='info'):
        # TSL - The timestamp is negative zero for some reason
        print "[{0}] @ {1:.2f}: {2}".format(message_type, Constants.START_TIME - time.time(), message)


    @staticmethod
    def warn(message):
        CommandLine.say(message, 'error')

    @staticmethod
    def error(message):
        CommandLine.say(message, 'error')

    @staticmethod
    def fatal(message):
        CommandLine.say(message, 'fatal')
        sys.exit()

class Installer:
    def validate_system(self):
        if not os.path.exists(Constants.HOME_DIRECTORY):
            CommandLine.fatal("Home directory does not exist at `{0}`", Constants.HOME_DIRECTORY)
        if not os.path.exists(Constants.CLONES_PATH):
            CommandLine.fatal("Clone directory does not exist at `{0}`", Constants.CLONES_PATH)
        if not os.path.exists(Constants.BIN_DIRECTORY):
            CommandLine.fatal("Binary directory does not exist at `{0}`", Constants.BIN_DIRECTORY)


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
        tmuxinator_path = Constants.CLONES_PATH + "tmuxinator/completion/tmuxinator.bash"

        if os.path.isfile(tmuxinator_path):
            CommandLine.say("Symlinking `{0}` to `{1}`".format(tmuxinator_path, Constants.HOME_DIRECTORY))
            if not Helpers.safe_link(tmuxinator_path, Constants.BIN_DIRECTORY + "tmuxinator.bash"):
                return False
        else:
            CommandLine.error("Unable to locate tmuxinator @ `{0}`. Tmuxinator was not installed.".format(tmuxinator_path))

        CommandLine.say("Symlink in place. Add `source ~/bin/tmuxinator.bash` to your .bashrc if it's not already included")
        return True

def main():
    Installer().install_all()

if __name__ == '__main__':
    main()
