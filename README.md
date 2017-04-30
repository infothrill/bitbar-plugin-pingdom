# bitbar-plugin-pingdom

This is a plugin for [Bitbar](https://github.com/matryer/bitbar) that hooks up
with the API of [pingdom](https://pingdom.com) to show a summary of currently
problematic checks.

## Installation

Since this is a python script with some dependencies, a convenience shell
script wrapper is provided:

```bash
git clone https://github.com/infothrill/bitbar-plugin-pingdom.git

cd YOUR_BITBAR_PLUGIN_FOLDER

ln -s YOUR_CLONE/bitbar-pingdom.60s.sh .
```

This wrapper will install dependencies into a virtual environment inside the
cloned repository.

## Configuration

Copy the example config `bitbar_pingdom_sample.conf` to `bitbar_pingdom.conf`
and fill in your credentials.
