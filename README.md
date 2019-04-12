# TrollSSH #

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

![](./demo.gif)

## Description ##
Stub ssh server in Python using the excellent [paramiko](http://www.paramiko.org/)
package.

Will blindly accept any connection and print out some nonsense on the
client's terminal.

## Installation ##

Using `python 3.7` only.

```
$ pipenv --python 3.7
$ pipenv sync
$ pipenv run server
```

The Python package `cryptography` is held back to version `2.4.2` to
avoid deprecation warnings. Fixes are pending release in Paramiko's
master.

## Configuration ##

Configured through environmental variables. Pipenv optionally reads a
`.env` in the root of the project directory.
