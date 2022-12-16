import ranger.api
from os import getenv
from os.path import isfile
from subprocess import Popen, PIPE

hook_init_prev = ranger.api.hook_init
zshz_src = getenv("ZSHZ_SRC", "")


def hook_init(fm):
    def z_add(signal):
        cmd = f"source {zshz_src} && zshz --add '{signal.new.path}'"
        Popen(["zsh", "-c", cmd])

    fm.signal_bind("cd", z_add)

    return hook_init_prev(fm)


if isfile(zshz_src):
    ranger.api.hook_init = hook_init


class z(ranger.api.commands.Command):
    """
    :z

    Jump directories with zsh-z.
    """

    def execute(self):
        if not isfile(zshz_src):
            self.fm.notify("Can't find ZSHZ_SRC.", bad=True)
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
