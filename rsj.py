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
import mimetypes

from falcon_multipart.middleware import MultipartMiddleware

#import cgi
#import cgitb
#cgitb.enable()


hug.API(__name__).http.output_format = hug.output_format.html
mid = MultipartMiddleware()
#__hug__.http.add_middleware(mid)
#hug.API(__name__).http.add_middleware(middleware=mid)


client = pymongo.MongoClient()
db = client.media

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
	shuffle(files)
	if len(files) > limit:
		files = files[:limit]
	return files

def sendMail(message):
	try:
		s=SMTP(config.MAIL_SERVER, config.MAIL_PORT)
		s.set_debuglevel(1)
		#s.ehlo()
		s.starttls()
		s.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
		s.sendmail(message['From'], config.MAIL_SENDTO, message.as_string())
		s.quit()
		return True
	except Exception:
		return False

@hug.startup()
def checkFiles(api): # Check pics folder, make thumbs
	thumbs = getFiles('static/thumbs', 'jpg')
	pics = getFiles('static/pics', 'jpg')
	music = getFiles('static/audio', 'mp3')
	for pic in (p for p in pics if p not in thumbs):
		im = Image.open(path.join(pic[0], pic[1]))
		im.thumbnail((100, 100), Image.ANTIALIAS)
		im.save(path.join(pic[0], '..', 'thumbs', pic[1]))
	# compare with db

@hug.local()
@hug.get('/', output=hug.output_format.html)
def home():
	songs = getFiles('static/audio', 'mp3')
	pics = getFiles('static/pics', 'jpg', 20)
	return env.get_template('player.html').render(songs=songs, pics=pics)

@hug.local()
@hug.post('/contact')
def contact(name=None, email=None, message=None):
	#print('got a message!', name, email, message)
	msg = MIMEText(message)
	msg['From'] = config.MAIL_DEFAULT_SENDER
	msg['Subject'] = 'rsj form from: %s, %s' % (name, email)
	if sendMail(msg):
		hug.redirect.to('/thanks')
	else:
		hug.redirect.to('/error')
	#return hug.redirect.to('/')

@hug.local()
@hug.get('/thanks', output=hug.output_format.html)
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
	# print(len(body['files[]']))
	#pprint(vars(body))
	#pprint()
	#pprint(dict(body))
	print(dir(request))
	print(dict(request.headers))
	#print(mimetypes.guess_all_extensions(body['files'][0]))
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

	#with open(filename,'wb') as f:
		# chunksize = 4096
		# while True:
		# 	chunk = filebody.read(chunksize)
		# 	if not chunk:
		# 		break
		# 	f.write(chunk)
	return

# @hug.local()
# @hug.post('/upload')#,versions=1)
# def upload(body,request,response):
# 	"""Receives a stream of bytes and writes them to a file."""
# 	#print(body)
# 	c = 0
# 	#print(list(body.keys()).pop()) #, dir(body.items))
# 	#print(body['files[]']['name'])
# 	files = []
# 	# for n in body['files[]'][0]:
# 	# 	files.append(n)
# 	# 	c += 1
# 	#print(dir(request.headers.keys))
# 	env = request.env
# 	env.setdefault('QUERY_STRING', '')
# 	#ct = request.get_header('content-type')
# 	#postvars = cgi.parse_multipart(fp=request.stream, pdict=ct)
# 	#print(postvars.keys())
# 	#form = cgi.FieldStorage(fp=request.stream, environ=request.env, headers=request.headers)
# 	form = cgi.FieldStorage(fp=body, environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':'MULTIPART/FORM-DATA'})
# 	print(dir(form))
# 	#print(form.file, form.filename, form.name, form.type)
# 	#print(request.stream.fileno())
# 	#print(dir(request.get_param()))
# 	#print(dict(body))
# 	#print(response.content)
# 	# filename = body['files[]'][0]
# 	# filebody = body['files[]'][1]
# 	#print(filebody)
# 	c = 0
# 	for f in files:
# 		with open('%s.jpg' % c,'wb') as out:
# 			out.write(f)
# 			c += 1
# 	return hug.redirect.to('/success')

@hug.local()
@hug.get('/success')
def win():
	return 'Upload success! You will return in just a moment. <meta http-equiv="refresh" content="2;url=/"/>'

# @hug.local()
# @hug.post('/upload', output=hug.output_format.html)
# def upload(body):
# 	print('body: ', body)
# 	#for f in filename
# 	return {'filename': list(body.keys()).pop(), 'filesize ': len(list(body.values()).pop()),
# 	'keys':list(body.keys())}
