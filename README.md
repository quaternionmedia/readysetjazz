# readysetjazz.com
a full stack website, written (mostly) in python! Designed to keep all media continuously updated with the files available to the system at any moment.

Live version available at https://readysetjazz.com

### Quickstart
`docker-compose up`

### The Stack
##### Traefik
Reverse proxy, designed for microservices. https://traefik.io/

##### MongoDB
Straightforward mongo backend https://www.mongodb.com/

##### FastAPI
Modern asynchronous python api creation. Does what it says on the tin. Fast to write, faster to execute. https://fastapi.tiangolo.com

### Optional dependencies

##### Jinja2
Pythonic templating. This time, it's not jinja1! https://jinja.palletsprojects.com

##### Pillow
For image processing. Needs to be complied on some systems, including alpine/raspbian. See [Dockerfile](Dockerfile) for instructions.

##### google-api-python-client
Used to integrate web components with Calendars, Maps, etc.


### Design

##### Init
Create the file `rsj/config.py` and populate it with the necessary configurations:
`MAIL_SERVER = 'your.mail.server'
MAIL_PORT = 587
MAIL_USERNAME = 'your@email.address'
MAIL_PASSWORD = 'Your3mailP@ssw4rd'
MAIL_DEFAULT_SENDER = 'your@email.address'
MAIL_SENDTO = 'your@email.address'
CALENDAR_ID = 'YourCalendarID@group.calendar.google.com'
DB_URL = 'mongodb://mongo:27017'
MAPS_API_KEY = 'YourGoogleMapsAPIKey'`

Sample database entries are provided as [bios.csv](rsj/bios.csv) and [videos.csv](rsj/videos.csv). If the database is not already seeded, they will need to be added to enable their respective components.

##### Startup
With a traefik image and a mongo image running, (rsj.py)[rsj/rsj.py] starts and creates the necessary objects for operation. In this case:
- db connection
- google credentials
- jinja template Environment
- `getFiles()` function to search for local media
- `sendMail()` to send emails. (requires separate mail server, not included here. See https://mailinabox.email/ if you need one)
- `compare()` check the database against the actual files, modify database to match.
- `randQuery()` grab a random selection from the database [within search parameters].

On server startup, the `/static/` folders are scanned for media (pictures and audio) and compared against the database. Old entries are removed, and new files are added to the db. Also, thumbnails are created for any new photos found, to speed up client renderings.

##### Home
On requests to `/`, a random selection of songs and pictures are drawn from the database, as well as all the bios, videos, and calendar events. Each of these objects are passed into the Jinja template engine, and rendered in their respective components.
- audio
- photos
- videos
- bios
- event list
- event map
Finally, the entire string is served to the client as an `HTMLResponse()`.

##### Contact
When a client submits the contact form, after the fields are validated, a `POST` method is sent to `/contact`, which accepts the fields `name`, `email`, and `message`. This is wrapped into an email and sent to the `config.MAIL_SENDTO` address.

If the email was sent successfully, the client is redirected to the `/thanks` page. Otherwise, they are redirected to the `/error` page.
