import hug
from os import walk, path
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from random import shuffle
import smtplib
from email.mime.text import MIMEText
import config

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
	if len(files) > limit:
		files = files[:limit]
	return files

@hug.startup()
def thumbPics(api): # Check pics folder, make thumbs
	thumbs = getFiles('static/thumbs', 'jpg')
	pics = getFiles('static/pics', 'jpg')
	for pic in (p for p in pics if p not in thumbs):
		im = Image.open(path.join(pic[0], pic[1]))
		im.thumbnail((100, 100), Image.ANTIALIAS)
		im.save(path.join('static/thumbs', pic[1]))

@hug.local()
@hug.get('/', output=hug.output_format.html)
def home():
	songs = getFiles('static/audio', 'mp3')
	pics = getFiles('static/pics', 'jpg', 20)
	shuffle(songs)
	shuffle(pics)
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

def sendMail(message):
	try:
		s=smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT)
		s.set_debuglevel(1)
		#s.ehlo()
		s.starttls()
		s.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
		s.sendmail(message['From'], config.MAIL_SENDTO, message.as_string())
		s.quit()
		return True
	except Exception:
		return False


@hug.static('/static')
def static():
	return('static',)
