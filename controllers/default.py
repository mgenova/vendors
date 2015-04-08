# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
db.feedback.rating.widget = rating_widget



#import time
#from datetime import date
#created_date = date.fromtimestamp(time.time())

def test():
    return dict()

def login():
    return dict(form=auth.login())

def index():
    return redirect(URL('default', 'category/Art'))

    links = []
    links.append(A('Star rating',_href=URL(r=request,f=star_rating)))
    return dict(widgets=links)


    #form = SQLFORM(db.feedback)
    #return dict(form = form)

def list(): 
    vendors = db().select(db.vendor.ALL, orderby=db.vendor.name )
    return dict(vendors=vendors)

def category():
    category = request.args(0)
    #rows = db((db.vendor.id==db.category.vendor_id) & (db.category.name == category)).select()
    rows = db(db.category.name==category).select()
    return dict(category=category, rows=rows)


@auth.requires_login()
def create():
    """creates a new empty vendor page"""
    form = SQLFORM(db.vendor).process(next=URL('index'))
    return dict(form=form)



@auth.requires_login()
def view():
    """shows a vendor page"""
    if request.args(1):
        category = request.args(1)
    else:
        category =''

    vendor = db.vendor(request.args(0))

    comments = db(db.feedback.vendor_id==vendor.id).select()

    categories = db(db.category.vendor_id==vendor.id).select()
    db.feedback.vendor_id.default = vendor
    
  
    num_of_ratings = len(comments)
    all_ratings = 0
    rating = 0
    for comment in comments:
        all_ratings = all_ratings + comment.rating #adds all ratings 1-5   
    try:
        rating = all_ratings/num_of_ratings
    except ZeroDivisionError:
        response.flash = 'There is no rating for this vendor'


    form = SQLFORM(db.feedback, _class='rate')
    if form.process().accepted:
        session.flash = 'Thank you for your feedback!'
        redirect(URL('default', 'view', args=request.args(0, cast=int)))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        #response.flash = 'please fill the form'
        pass 
    #if(db.feedback.anonymous and value == True)    
        

    return dict(vendor=vendor, comments=comments, rating=rating, form=form, categories=categories, category=category)









def avg_rating():
    num_of_ratings = len(comments)
    all_ratings = 0
    rating = 0
    for comment in comments:
        all_ratings = all_ratings + comment.rating #adds all ratings 1-5   
    try:
        rating = all_ratings/num_of_ratings
    except ZeroDivisionError:
        response.flash = 'There is no rating for this vendor'
    return dict(avg_rating=avg_rating)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)






@auth.requires_login()
def edit():
    """edit an existing vendor page"""
    this_vendor = db.vendor(request.args(0,cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.vendor, this_vendor).process(
            next = URL('view', args=request.args))
    return dict(form=form)



def search():
    """an ajax vendor search page"""
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
        _onkeyup="ajax('callback', ['keyword'], 'target');")),
        target_div=DIV(_id='target'))





def callback():
     """an ajax callback that returns a <ul> of links to vendors"""
     query = db.vendor.name.contains(request.vars.keyword)
     vendorpages = db(query).select(orderby=db.vendor.name)
     links = [A(v.name, _href=URL('view',args=v.id)) for v in vendorpages]
     return UL(*links)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
