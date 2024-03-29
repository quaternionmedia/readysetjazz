import hug
import pymongo
from os import walk, path
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from random import shuffle
from smtplib import SMTP
from email.mime.text import MIMEText
import config
from pprint import pprint
import json
import csv
import io
import cal


hug.API(__name__).http.output_format = hug.output_format.html


client = pymongo.MongoClient(config.DB_URL, connect=False)
db = client.rsj

store = cal.Storage(path.join('cred', 'cred.json'))
credentials = store.get()

env = Environment(loader=FileSystemLoader('templates'))

def getFiles(directory, ext=None, limit=10): # returns [(dir, file),]
	files = []
	for dirpath, dirname, filenames in walk(directory):
		for f in filenames:
			if ext:
				if f.endswith(ext):
					files.append((dirpath, f))
			else:
				files.append((dirpath, f))
	if (limit is not 0) and (len(files) > limit):
		shuffle(files)
		files = files[:limit]
	return files

def sendMail(message):
	try:
		s=SMTP(config.MAIL_SERVER, config.MAIL_PORT)
		s.set_debuglevel(1)
		#s.ehlo()
		s.starttls()
		s.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
		s.sendmail(message['From'], message['To'], message.as_string())
		s.quit()
		return True
	except Exception:
		return False

def compare(reference, source): # check database query against files
	refs = []
	for r in db.media.find(reference):
		#print(r)
		refs.append(r['name'])
	#print('refs = ', refs)
	#print('count = ', len(refs))
	src = getFiles(source, ext=reference['type'], limit=0)
	srcs = [] # names of db items
	for s in src:
		srcs.append(s[1])
	new = []
	for q in (s for s in src if s[1] not in refs):
		new.append({'name':q[1], 'type':q[1][1 + q[1].rfind('.'):].lower(), 'path':source})
	if len(new) > 0:
		print('about to insert ', new)
		db.media.insert_many(new)
	old = []
	for q in (r for r in refs if r not in srcs):
		old.append(q)
	if len(old) > 0:
		print('about to delete media not found in database', old)
		db.media.remove({'name':{'$in':old}})

def randQuery(fields=None, limit=10):
	if limit == 0:
		x = [ d for d in db.media.find(fields) ]
		shuffle(x)
		return x
	return [ d for d in db.media.aggregate( [ {'$match': fields}, { '$sample': {'size': limit }} ])]



@hug.startup()
def checkFiles(api): # Check pics folder, make thumbs
	thumbs = getFiles('static/thumbs', 'jpg', limit=0)
	pics = getFiles('static/pics', 'jpg', limit=0)
	music = getFiles('static/audio', 'mp3', limit=0)
	# compare with db
	compare({'type': 'mp3'}, 'static/audio')
	compare({'type': 'jpg'}, 'static/pics')
	thumb = [t[1] for t in thumbs]
	#convert thumbs
	for pic in (p for p in pics if p[1] not in thumb):
		print('converting thumbnail ', pic)
		im = Image.open(path.join(pic[0], pic[1]))
		im.thumbnail((100, 100), Image.ANTIALIAS)
		im.save(path.join(pic[0], '..', 'thumbs', pic[1]))



@hug.local()
@hug.get('/')
def home():
	# songs = query('static/audio', 'mp3')
	# pics = getFiles('static/pics', 'jpg', 20)
	songs = randQuery({'type':'mp3'})
	pics = randQuery({'type':'jpg'}, limit=0)
	bios = [m for m in db.musicians.find()]
	videos =  [m for m in db.videos.find()]

	gigs = cal.get_events(credentials, config.CALENDAR_ID)
	# print(gigs)
	# print('bios = ', bios)
	# print('songs = ', songs)
	# print('pics = ', pics)
	return env.get_template('player.html').render(songs=songs, pics=pics, gig=gigs[0], gigs=gigs, bios=bios, videos=videos, mapsAPIKey=config.MAPS_API_KEY)

@hug.local()
@hug.post('/contact')
def contact(name=None, email=None, message=None):
	#print('got a message!', name, email, message)
	msg = MIMEText(message)
	msg['From'] = config.MAIL_DEFAULT_SENDER
	msg['To'] = config.MAIL_SENDTO
	msg['Subject'] = 'rsj form from: %s, %s' % (name, email)
	if sendMail(msg):
		hug.redirect.to('/thanks')
	else:
		hug.redirect.to('/error')
	#return hug.redirect.to('/')

@hug.local()
@hug.get('/thanks')
def thanks():
	return 'Thanks! Your email is sent! You will be redirected back in just a moment. <meta http-equiv="refresh" content="2;url=/"/>'

@hug.static('/static')
def static():
	return('static',)

@hug.local()
@hug.get('/upload', output=hug.output_format.html)
def uploader():
	return env.get_template('uploader.html')

@hug.post('/upload')#,versions=1)
def upload_file(body,request,response):
	# """Receives a stream of bytes and writes them to a file."""
	#pprint((request.env['wsgi.input'].fileno))
	print(request.stream.stream.read(20))
	print('stream = ', stream)
	n = len(body['files'])
	for f in body['files']:
		#with open(path.join('static', f), 'wb') as o:
		#	o.write(body['stream'][n])
		n += 1
	#pprint(dir(response))
	#pprint(dir(request.env['wsgi.file_wrapper']))
	pprint((request.stream.stream.read))

	#print(request.env['CONTENT_TYPE'])
	#print(vars(request.env['wsgi.file_wrapper']))
	#print(i)
	#print(vars(request.env['wsgi.file_wrapper']))
	#pprint(dir(response))
	# #print(body)
	# for f in body['files[]']:
	# 	print(len(f))
		#print(dir(f))
		#print(dir(f.title))
		#print(f.title.__name__)
	#fileame = body['files[]'][0]
	#filebody = body['files[]'][1]
	#print(filebody)

	return

@hug.local()
@hug.get('/success')
def win():
	return 'Upload success! You will return in just a moment. <meta http-equiv="refresh" content="2;url=/"/>'
