# ranger-zshz

A plugin to integrate [zsh-z](https://github.com/agkozak/zsh-z) into [ranger](https://github.com/ranger/ranger).

## How it works

- Every directory you visit in ranger is automatically added to your zsh-z database.
- Type `:z foobar` to jump to directory matching `foobar`. Use `TAB` to cycle completions.

## Installation

- Set an environment variable `ZSHZ_SRC` to `zsh-z.plugin.zsh` path.
- Clone this repo to `~/.config/ranger/plugins`.
- Optionally, bind a key:

```conf
# ~/.config/ranger/rc.conf

...

map gz console z%space
```

## License

Licensed under [GPLv3](LICENSE)

Copyright (C) 2022 [Rafael Cavalcanti](https://rafaelc.org/dev)
