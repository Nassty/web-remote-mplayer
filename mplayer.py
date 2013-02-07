import subprocess
import os


class Mplayer(object):

    def __init__(self, filename=False, fifo_path='/tmp/mplayer-fifo.sock',
                 binary='mplayer'):

        self.filename = filename
        self.p = None
        self.fifo_path = fifo_path
        self.arguments = [
            binary,
            '-really-quiet',
            '-noconsolecontrols',
            '-fs',
            '-slave',
            '-input',
            'file=%s' % self.fifo_path,
        ]

    def load_file(self, filename):
        self.filename = filename
        return self

    def check_fifo(self):
        return os.path.exists(self.fifo_path)

    def remove_fifo(self):
        try:
            os.unlink(self.fifo_path)
        except OSError:
            pass

    def start(self):
        self.remove_fifo()
        os.mkfifo(self.fifo_path)
        self.p = subprocess.Popen(self.arguments + [self.filename])
        return self

    def send_cmd(self, *args):
        with open(self.fifo_path, 'w') as sock:
            cmd = " ".join(args)
            sock.write("%s\n" % cmd)
            sock.flush()
            if cmd == 'quit':
                self.remove_fifo()
        return self

    def kill(self):
        self.p.kill()
        return self
