Web Remote MPlayer
==================

This is a web-based remote control for
[MPlayer](http://www.mplayerhq.hu/design7/news.html).

Imagine this use-case:

You have a small GNU/Linux computer attached to a TV screen (with HDMI cable,
perhaps). In order to playback motion pictures, you login into the Linux
computer from your laptop, sat in the couch, through SSH and launch MPlayer.

That's cool for you, but it's not for your special-other. They might prefer to
use a graphical user interface from their mobile. Well, these bytes solve that
problem.

Using [Flask](http://flask.pocoo.org/), a microframework for Python for web
development, a web application, within its own web server, is launched. This
web application shows the motion pictures stored in a configured directory
(~/Downloads by the default) in a UI mobile friendly, but also it allows to
control the playback using the
[slave mode](http://www.mplayerhq.hu/DOCS/tech/slave.txt) of MPlayer.

Not only that, but it also offers, through
[subliminal](http://pythonhosted.org//subliminal/), the possibility to
download the subtitles of a specific motion picture, with a simple click.

Anyway, this is project is still very homebrew: no fancy configurations,
service control nor elegant error handling. You must deal with Python, HTML5
(jQuery), etc.
