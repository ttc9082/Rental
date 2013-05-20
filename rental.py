import web
import hashlib
import random
from tool import AWS
from rentaldb import *

web.config.debug = False

urls = (
    '/login', 'login',
    '/logout', 'logout',
    '/sign_up', 'sign_up',
    '/new', 'new',
    '/del', 'delete',
    '/', 'index',
    '/index', 'index', 
    '/profile/(.*)', 'show'
)

app = web.application(urls, locals())
store = web.session.DiskStore('session')
session = web.session.Session(app, store, initializer={'userId': 0, 'privilege': 0})

render = web.template.render('templates/')


def logged():
    if session.userId:
        return True
    else:
        return False

def cellphonecheck(number):
    return True

def validName(name):
    return True

class login:
    def GET(self):
        if logged():
            userName = User.find_by_id(session.userId)[1]
            return render.index(userName)
        else:
            return render.login()

    def POST(self):
        name, passwd = web.input().user, web.input().passwd
        userPassword = User.find_passwd(name)
        try:
            if hashlib.md5(passwd).hexdigest() in userPassword:
                session.userId = name
                privilege = 1 # check privilege by name in DB
                session.privilege = privilege
                userName = User.find_by_id(session.userId)[1]
                return render.login_ok(userName)
            else:
                session.userId = 0
                session.privilege = 0
                return render.login_error()
        except:
            session.userId = 0
            session.privilege = 0
            return render.login_error()


class logout:
    def GET(self):
        uid = session.userId
        session.userId = 0
        session.kill()
        return render.logout(uid)


class sign_up:
    def GET(self):
        errors = web.input(errors=None)
        print errors
        return render.sign_up(errors.errors)

    def POST(self):
        name = web.input().user 
        passwd = web.input().passwd
        passwdconf = web.input().passwdconf 
        encrypted_password = hashlib.md5(passwd).hexdigest()
        emailadd = web.input().email 
        emailaddconf = web.input().emailconf 
        cellphone = web.input().cellphone 
        privilege = 1
        user_data = [name, encrypted_password, emailadd, cellphone, privilege]
        User.insert(user_data)
        error_message = []
        try:
            if passwd != passwdconf:
                error_message.append('Password Confirmation is Wrong.')
            else:
                pass
            if emailadd != emailaddconf:
                error_message.append('Email Confirmation is Wrong. ')
            else:
                pass
            if not cellphonecheck(cellphone):
                error_message.append('Cellphone number format is Wrong.')
            else:
                pass
        except:
            error_message = ['Unknown Error!']
        if error_message:
            return render.sign_up(error_message)
        else:
            return render.index('good')

class new:

    def GET(self):
        message = web.input(message=None).message
        bucket = None
        postname = web.input(postname=None).postname
        return render.new(message, postname, bucket)

    def POST(self):
        S3 = AWS.AWSS3()
        postname = web.input(postname={}).postname
        alreadyHave = web.input(alreadyHave={})

        print postname
        print alreadyHave.alreadyHave

        if not alreadyHave.alreadyHave:
            num = 0
            while num < 10:
                try:
                    name = 'rental_id_' + str(random.randint(1000, 9999))
                    S3.create_bucket(name)
                    break
                except:
                    num += 1
                    pass
            # build a relationship between this bucket's name and the post's name here.


        #find bucket name in the table with the postname
        bucket_name = 'rental_id_7547'
        bucket = S3.get_bucket(bucket_name)
        f = web.input(file2up={})
        room_type = web.input().rooms
        print room_type
        filename = f.file2up.filename
        ext = filename.split('.')[-1]
        if validName(web.input().name):
            name = web.input().name + '.' + ext
        else:
            errors = ['name error.']
            return render.new(errors, postname, bucket)
        s3_file = room_type + '/' + name
        saved = S3.saveFile(bucket=bucket, name=s3_file, file1=f.file2up.file)
        smessage = saved[4:] + ' has been saved!'
        return render.new([smessage], postname, bucket)

class delete:
    def POST(self):
        x = web.input()
        S3 = AWS.AWSS3()
        bucket = S3.get_bucket(x.bucketname)
        S3.delFile(x.keyname, x.bucketname)
        message = x.keyname + ' is Deleted'
        return render.new([message], x.postname, bucket)


class index:
    def GET(self):
        if not logged():
            print 'not logged in'
        all_room = Room.show_all()
        return render.index('123')


class profile:
    def GET(self, id):
        my_room = Room.show_my_rooms(id)





if __name__ == "__main__":
    app.run()