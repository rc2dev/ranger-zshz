import ranger.api
from os import getenv
from subprocess import Popen, PIPE

hook_init_prev = ranger.api.hook_init
zshz_src = getenv("ZSHZ_SRC")


def hook_init(fm):
    def z_add(signal):
        cmd = f"source {zshz_src} && zshz --add '{signal.new.path}'"
        Popen(["zsh", "-c", cmd])

    fm.signal_bind("cd", z_add)
    return hook_init_prev(fm)


ranger.api.hook_init = hook_init


class z(ranger.api.commands.Command):
    """
    :z

    Jump directories with zsh-z.
    """

    def execute(self):
        cmd = f"source {zshz_src} && zshz -e {' '.join(self.args[1:])}"
        proc = Popen(["zsh", "-c", cmd], stdout=PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:  # not found
            return None

        dir = stdout.decode("utf-8").strip()
        self.fm.cd(dir)
