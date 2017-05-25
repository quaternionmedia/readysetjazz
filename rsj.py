import hug
from os import walk, path
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from random import shuffle

env = Environment(loader=FileSystemLoader('templates'))

def getFiles(path, ext=None, limit=10):
	files = []
	for dirpath, dirname, filenames in walk(path):
		for f in filenames:
			if ext:
				if f.endswith(ext):
					files.append(f)
			else:
				files.append(f)
	if len(files) > limit:
		files = files[:limit]
	return files

@hug.startup()
def thumbPics(api): # Check pics folder, make thumbs
	thumbs = getFiles('static/thumbs', 'jpg')
	pics = getFiles('static/pics', 'jpg')
	for pic in (p for p in pics if p not in thumbs):
		im = Image.open(path.join(dirpath, pic))
		im.thumbnail((100, 100), Image.ANTIALIAS)
		im.save(path.join('thumbs', pic))

@hug.local()
@hug.get('/', output=hug.output_format.html)
def home():
	songs = getFiles('static/audio', 'mp3')
	pics = getFiles('static/pics', 'jpg', 20)
	return env.get_template('player.html').render(songs=songs, pics=pics)

@hug.static('/static')
def pics():
	return('static',)
