#! /usr/local/bin/python

import subprocess

def main():

    defaults = {
        "Prevent DS store files from being written on network drives":
            "defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true",

        "Disable reply animation in mail":
            "defaults write com.apple.Mail DisableReplyAnimations -bool YES",

        "Disable swoosh send animation in mail":
            "defaults write com.apple.Mail DisableSendAnimations -bool YES",

        "Always use list view":
            "defaults write com.apple.Finder FXPreferredViewStyle Nlsv",

        "Disable dashboard":
            "defaults write com.apple.dashboard mcx-disabled -boolean true",

        "Instant dropdown of overlays":
            "defaults write NSGlobalDomain NSWindowResizeTime .001",

        "Copy email addresses as `foo@example.com` instead of `Foo Bar <foo@example.com>` in Mail.app":
            "defaults write com.apple.mail AddressesIncludeNameOnPasteboard -bool false",

        "Expand save panel in save dialog by default":
            "defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true",

        "Expand save panel in save dialog by default":
            "defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true",

        "Save to disk, not iCloud by default":
            "defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false",

        "Automatically quit the printer app when printing is complete":
            'defaults write com.apple.print.PrintingPrefs "Quit When Finished" -bool true',

        "Check for software updates daily, not weekly":
            "defaults write com.apple.SoftwareUpdate ScheduleFrequency -int 1",

        "Enable tap to click for current user and on login screen":
            [
                "defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true",
                "defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1",
                "defaults write NSGlobalDomain com.apple.mouse.tapBehavior -int 1"
            ],

        "Enable tab in modal dialogs":
            "defaults write NSGlobalDomain AppleKeyboardUIMode -int 3",

        "Automatically enable backlit keyboard in lowlight":
            "defaults write com.apple.BezelServices kDim -bool true",

        "Disable keyboard illumination after 5 minutes of inactivity":
            "defaults write com.apple.BezelServices kDimTime -int 300",

        "Save screenshot in PNG":
            'defaults write com.apple.screencapture type -string "png"',

        "Disable shadows in screenshots":
            "defaults write com.apple.screencapture disable-shadow -bool true",

        "Enable subpixel font rendering on non-Apple LCDs":
            "defaults write NSGlobalDomain AppleFontSmoothing -int 2",

        "Disable window animations and Get Info animations":
            "defaults write com.apple.finder DisableAllAnimations -bool true",

        "Speed up animation in finder":
            "defaults write NSGlobalDomain NSWindowResizeTime .001",

        "Disable window open / close animations in finder":
            "defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false",

        "Show path bar in finder":
            "defaults write com.apple.finder ShowPathbar -bool true",

        "Enable text selection in quick look":
            "defaults write com.apple.finder QLEnableTextSelection -bool true",

        "When doing a search, search the current folder by default":
            'defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"',

        "Remove warning when modifying the file extension":
            "defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false",

        "Speed up mission control animations":
            "defaults write com.apple.dock expose-animation-duration -float 0.1",

        #### Dock

        "Don't animate opening animations from the Dock":
            "defaults write com.apple.dock launchanim -bool false",

        "Remove auto-hide Dock delay":
            "defaults write com.apple.dock autohide-delay -float 0",

        "Remove Dock hide/show animation":
            "defaults write com.apple.dock autohide-time-modifier -float 0",

        "Make Dock icons transparent":
            "defaults write com.apple.dock showhidden -bool true",

        #### Safari

        "Set Safari's home page to `about:blank` for faster loading":
            'defaults write com.apple.Safari HomePage -string "about:blank"',

        "Allow hitting the Backspace key to go to the previous page in history":
            "defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2BackspaceKeyNavigationEnabled -bool true",

        "Add a context menu item for showing the Web Inspector in web views":
            "defaults write NSGlobalDomain WebKitDeveloperExtras -bool true",

        "Remove icons from Safari's bookmarks bar":
            'defaults write com.apple.Safari ProxiesInBookmarksBar "()"',

        "Enable the Develop menu and the Web Inspector in Safari": [
            "defaults write com.apple.Safari IncludeDevelopMenu -bool true",
            "defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true",
            "defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled -bool true"
        ]
    }

    kill = [
        "Dock",
        "Finder",
        "Dashboard",
        "Mail",
        "Safari",
        "SystemUIServer",
        "Terminal"
    ]

    for description, default in defaults.items():
        print(description)

        if type(default) == list:
            for value in default:
                subprocess.call(value.split(' '))
        else:
            subprocess.call(default.split(' '))


    for process in kill:
        print("Killing %s" % process)
        subprocess.call(['killall', process])

if __name__ == '__main__':
    main()