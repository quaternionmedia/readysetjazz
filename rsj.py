import hug
from os import walk, path
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from random import shuffle
env = Environment(loader=FileSystemLoader('templates'))

#api = hug.get(output=hug.output_format.html, on_invalid=hug.redirect.not_found, )

@hug.startup()
def thumbPics(api): # Check pics folder, make thumbs
	thumbs = []
	for dirpath, dirname, filenames in walk('thumbs'): #list all thumbs
		for t in filenames:
			if t.endswith('.jpg'):
				thumbs.append(t)

	for dirpath, dirname, filenames in walk('pics'):
		for p in filenames:
			if p.endswith('.jpg') and p not in thumbs: # convert it
				im = Image.open(path.join(dirpath, p))
				im.thumbnail((100, 100), Image.ANTIALIAS)
				im.save(path.join('thumbs', p))
#	return

@hug.local()
@hug.get()
def songlist():
	songs = []
	limit = 10
	for dirpath, dirname, filenames in walk('audio'):
		for f in filenames:
			if f.endswith('.mp3') and len(songs) <= limit:
				songs.append(f)
	shuffle(songs)
	return songs

def piclist():
	pics = []
	limit = 10
	for dirpath, dirname, filenames in walk('pics'):
		for f in filenames:
			if f.endswith('.jpg') and len(pics) <= limit:
				pics.append(f)
	shuffle(pics)
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
def audio():
	return('audio',)
@hug.static('/thumbs')
def thumbs():
	return('thumbs',)
@hug.static('/css')
def css():
	return('css',)
@hug.static('/js')
def js():
	return('js',)
@hug.static('/images')
def images():
	return('images',)
@hug.static('/img')
def img():
	return('img',)
