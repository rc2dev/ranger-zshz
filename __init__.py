import ranger.api
from ranger.ext.get_executables import get_executables
from os import getenv
from os.path import isfile, expanduser
from subprocess import Popen, PIPE

hook_init_prev = ranger.api.hook_init
# Fallback to ohmyzsh's plugins path as it's a popular framework.
zshz_src = expanduser(getenv("ZSHZ_SRC", "~/.oh-my-zsh/plugins/z/z.plugin.zsh"))


def get_missing_dep():
    if "zsh" not in get_executables():
        return "zsh"

    if not isfile(zshz_src):
        return "ZSHZ_SRC"

    return None


def hook_init(fm):
    def z_add(signal):
        cmd = f"source {zshz_src} && zshz --add '{signal.new.path}'"
        Popen(["zsh", "-c", cmd])

    fm.signal_bind("cd", z_add)

    return hook_init_prev(fm)


if get_missing_dep() is None:
    ranger.api.hook_init = hook_init


class z(ranger.api.commands.Command):
    """
    :z

    Jump directories with zsh-z.
    """

    def execute(self):
        dep = get_missing_dep()
        if dep is not None:
            self.fm.notify(f"Can't find {dep}.", bad=True)
            return None

        cmd = f"source {zshz_src} && zshz -e {' '.join(self.args[1:])}"
        proc = Popen(["zsh", "-c", cmd], stdout=PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:  # not found
            return None

        dir = stdout.decode("utf-8").strip()
        self.fm.cd(dir)

    def tab(self, tabnum):
        if not isfile(zshz_src):
            return None

        cmd = f"source {zshz_src} && zshz --complete {' '.join(self.args[1:])}"
        proc = Popen(["zsh", "-c", cmd], stdout=PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:  # not found
            return None

        paths = stdout.decode("utf-8").strip().splitlines()
        return [f"z {path}" for path in paths]
