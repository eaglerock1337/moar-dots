# moar-dots
A Python utility for managing dotfiles and system configuration files

## setup

### install pip3

```
sudo apt install pip3
sudo pip3 install --upgrade pip
```

### install pipenv

```
sudo pip3 install pipenv
```

### run setup script

From this directory:
```
pipenv install
pipenv run python setup.py
```

### usage

TBD

## everything

TBD

## ideas
* dotfiles are processed by tags
* dot class to handle placement or removal of dotfiles as needed
* .local dotfiles which are added to the main dotfile thru a call
* tags processed by OS, hostname, and other metrics
* tags are processed in a hierarchical order (always processed in order)
* errors are handled through a function that says a funny comment
* errors are tracked in 50DKP-minuses which are displayed when the command is run
