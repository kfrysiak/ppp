# ppp-run

`ppp` is a simple script/alias runner for Python - akin to `npm run` in javascript world.

## Installation

```sh
uv add --dev ppp-run
```

## Usage

### CLI

`ppp` has only 2 commands

- `ppp run {script}` - run a script (where `{script}` is a script defined in pyproject.toml)
- `ppp list` - list available scripts along with their descriptions

### Defining scripts

Define your scripts/aliases in `pyproject.toml` in `[tool.ppp.scripts]`.

You can use comments to specify command or argument descriptions.

#### Example

```toml
[tool.ppp.scripts]
# Run a docker image with http server
"docker-up" = "docker run -it -v bob:the_builder nvm" # [start|stop]
"type" = "echo"                                       # any text
```

Will result in

![List result](documentation/list.png)
