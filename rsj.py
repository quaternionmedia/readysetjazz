import hug
from os import walk
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

html = hug.get(output=hug.output_format.html)

@hug.local()
@hug.get()
def songlist():
	songs = {}
	limit = 10
	for dirpath, dirname, filenames in walk('audio'):
		for f in filenames:
			if f.endswith('.mp3') and len(songs) <= limit:
				songs[f] = 'audio/%s' % f
	return songs

def piclist():
	pics = {}
	limit = 10
	for dirpath, dirname, filenames in walk('pics'):
		for f in filenames:
			if f.endswith('.jpg') and len(pics) <= limit:
				pics[f] = 'audio/%s' % f
	return pics

#@html
@hug.local()
@hug.get('/', output=hug.output_format.html)
def home():
	songs = songlist()
	pics = piclist()
	return env.get_template('player.html').render(songs=songs, pics=pics)

# @hug.static()
# def static():
# 	return ('',)
@hug.static('/pics')
def pics():
	return('pics',)
@hug.static('/audio')
def pics():
	return('audio',)
@hug.static('/thumbs')
def pics():
	return('thumbs',)
@hug.static('/css')
def pics():
	return('css',)
@hug.static('/js')
def pics():
	return('js',)
@hug.static('/images')
def pics():
	return('images',)
@hug.static('/img')
def pics():
	return('img',)
