![Header](header.png)
=======

###### Pool your tmux sessions

------

I wanted tmux to manage my sessions for me - the result: Dux.

Dux is a wrapper for tmux which adds some nice features, including:

#### Session Pooling

All your sessions live in a pool - run Dux and it will search the pool for a disconnected session to reconnect to.

#### Session Creation and Naming

No available sessions open in the pool? No problem, Dux will start a new one with a random two word name. Warning: some are accidentally hilarious (my current session is `unfooled zalambdodonts` uh, what?)

#### Pool Blacklisting

Want to open a long-running session which should be left alone (e.g. daemon or vpn)? Ban them from your pool by renaming a tmux session with `:rename-sesion` to something that starts with `*`. Dux will ignore it when searching for disconnected sessions.

#### What do I need for Dux?

- tmux 2.X, 1.X is untested
- python 2
- `dux.py`

#### How do I run Dux?

- Clone repo `git clone https://github.com/csivanich/dux.git; cd dux`
- Run `./dux.py`

#### That's it?

Well, kinda. You'll probably want to kick of Dux when you start your shell - that's an excersize left to the reader, though. *Shameless plug alert* checkout my [dotfiles](https://github.com/csivanich/dotfiles) for an example which kicks it off on zsh's start.

#### So what's next?

 - Rule-based session auto-attaching
 - Better Tmux interaction (tmuxp)
 - Pool groups?

#### Special thanks:

- [github.com/atebits/Words](https://github.com/atebits/Words) - Word list to run session name generation. Licensed under CC0 Public Domain.
