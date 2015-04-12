#!/usr/bin/env python3

from flask import Flask, render_template, g,\
    redirect, url_for, session, request, json, make_response
from functools import wraps
import os
import mplayer
import re
import logging
try:
    import subliminal
    have_subliminal = True
except ImportError:
    have_subliminal = False

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.user_home = os.path.expanduser("~")
app.secret_key = "ASD"


@app.before_request
def get_mplayer():
    g.mplayer = mplayer.Mplayer()
    g.extensions = ('.avi', '.mp4', '.m4a', '.mov', '.mpg', '.mpeg',
                    '.ogg', '.flac', '.mkv')


def check_running(endpoint='controls', on_stop=False):
    def outer(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not g.mplayer.check_fifo():
                if on_stop:
                    return redirect(url_for(endpoint))
                return f(*args, **kwargs)

            if on_stop:
                return f(*args, **kwargs)
            return redirect(url_for(endpoint))
        return inner
    return outer


@app.route('/', defaults={"path": "Downloads"})
@app.route('/explore/<path:path>')
@check_running()
def explore(path):
    directories = []
    files = []
    internal_path = os.path.join(app.user_home, path)
    for content in os.listdir(internal_path):
        fullpath = os.path.join(internal_path, content)
        if os.path.isdir(fullpath) and not content.startswith('.'):
            directories.append((os.path.join(path, content), content))
        else:
            ext = os.path.splitext(content)[-1].lower()
            if ext in g.extensions:
                filepath = (os.path.join(path, content))
                sub_exists = os.path.exists(os.path.join(
                    internal_path, content.replace(ext, '.srt')))
                files.append((filepath, content, sub_exists))

    parent = list(os.path.split(path))
    parent.pop()
    parent = os.path.join(*parent)
    parent = (parent, os.path.basename(parent))
    directories.sort(key=natural_key)
    files.sort(key=natural_key)
    return render_template('listing.html', files=files,
                           directories=directories, title=parent)


def natural_key(string_):
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',
                                                           string_[0])]


@app.route('/play/<path:path>')
@check_running()
def play(path):
    full_path = os.path.join(app.user_home, path)
    if not g.mplayer.check_fifo():
        session['filename'] = full_path
        g.mplayer.load_file(full_path)
        g.mplayer.start()
    return redirect(url_for('controls'))


@app.route('/sub/<path:path>')
def sub(path):
    full_path = unicode(os.path.join(app.user_home, path))
    if not have_subliminal:
        return 'subliminal is required for this.\
                please try "# pip install subliminal"'

    with subliminal.Pool(8) as pool:
        results = pool.download_subtitles([full_path], ['es'],
                                          cache_dir='/tmp/', force=True)

    if results:
        return 'subtitle downloaded for %s, now play it %s'\
            % (path, url_for('play', path=path))
    else:
        return 'no subtitles'


@app.route('/controls')
@check_running('explore', on_stop=True)
def controls():
    return render_template('controls.html')


@app.route('/command/', methods=['POST'])
def command():
    cmd = request.form['cmd']
    g.mplayer.send_cmd(cmd)
    redirect = False
    if cmd == 'quit':
        redirect = url_for('explore')
    return json.dumps({"redirect": redirect})

def cleanup(fifo_path='/tmp/mplayer-fifo.sock'):
    try:
        os.unlink(fifo_path)
    except OSError:
        pass

if __name__ == "__main__":
    cleanup()
    app.run(debug=True, host='0.0.0.0')
