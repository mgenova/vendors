# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

#auth.settings.extra_fields['auth_user']= [Field('anonymous', label=T('anonymous'))]
#auth.settings.extra_fields['auth_user']=[Field('created_by',compute=lambda r: "%(first_name)s %(last_name)s" % r)]


## create all tables needed by auth if not custom tables
auth.define_tables(username=False,signature=False)


## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)



db.define_table('vendor',
    Field('name', 'string', unique=True),
    Field('website', 'string'),
    Field('note', 'string'),
    auth.signature,
    format = '%(name)s'
    )

db.define_table('category_name',
    Field('name', 'string'), 
    format = '%(name)s')

db.define_table('category',
    Field('vendor_id', 'reference vendor'),
    Field('name', 'string'), 
    format = '%(name)s')

db.define_table('feedback',
    Field('vendor_id', 'reference vendor', readable=False, writable=False),
    Field('rating', 'decimal(2,0)', default=0),
    Field('grade_level', requires=IS_IN_SET(['K','1','2','3','4','5','6'])),
    Field('created_on', 'datetime', default=request.now),
    #Field('created_by', compute=lambda r: "%(first_name)s %(last_name)s" % r, writable=False, readable=False),
    Field('comments', 'text', requires=IS_NOT_EMPTY()),
    Field('product_name', 'string', requires=IS_NOT_EMPTY()),
    Field('product_url', 'string'),
    Field('product_category', 'reference category_name'),
    Field('anonymous','boolean', label=T('anonymous'), default=False, writable=True, readable=True), auth.signature)




db.define_table('average_rating',
    Field('avg_rating', 'double'))




db.vendor.name.requires = IS_NOT_IN_DB(db, db.vendor.name)
db.vendor.website.requires = IS_NOT_IN_DB(db, db.vendor.website)
db.feedback.vendor_id.requires = IS_IN_DB(db, db.vendor.id, '%(name)s')
db.feedback.comments.requires = IS_NOT_EMPTY()
db.feedback.rating.requires = IS_IN_SET(range(0, 6))
db.feedback.created_on.readable = db.feedback.created_on.writable = False


