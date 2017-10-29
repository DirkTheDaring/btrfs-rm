# btrfs-rm
remove directories which contain(s) btrfs snapshot(s) recursively.
Works with python 2 and 3

# Install
On Centos/Fedora the following packages need to be installed:
* python
* util-linux   
* coreutils
* btrfs-progs

# How to use
    # Dry run (-t flag) - does not delete anything
    sudo ./btrfs-rm -t DIRECTORY


    # Delete for real (See Risk!)
    sudo ./btrfs-rm DIRECTORY


# RISKS
Use at your own risk. No warranty!

