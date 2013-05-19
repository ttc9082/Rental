import web
import hashlib
import random
from tool import AWS

web.config.debug = False

urls = (
    '/login', 'login',
    '/reset', 'reset',
    '/sign_in', 'sign_in',
    '/new', 'new',
    '/del', 'delete'
)
app = web.application(urls, locals())
store = web.session.DiskStore('session')
session = web.session.Session(app, store, initializer={'userName': 0, 'privilege': 0})

render = web.template.render('templates/')


def logged():
    if session.userName:
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
            return render.index(session.userName)
        else:
            return render.login()

    def POST(self):
        name, passwd = web.input().user, web.input().passwd
        userPassword = '07f793d559d19bba6263b082cf20703d' # check password by name in DB (encoded in MD5)
        try:
            if hashlib.md5(passwd).hexdigest() == userPassword:
                session.userName = name
                privilege = 1 # check privilege by name in DB
                session.privilege = privilege
                return render.login_ok(session.userName)
            else:
                session.userName = 0
                session.privilege = 0
                return render.login_error()
        except:
            session.userName = 0
            session.privilege = 0
            return render.login_error()


class reset:
    def GET(self):
        name = session.userName
        session.userName = 0
        session.kill()
        return render.logout(name)


class sign_in:
    def GET(self):
        errors = web.input(errors=None)
        print errors
        return render.sign_in(errors.errors)

    def POST(self):
        name = web.input().user
        passwd = web.input().passwd
        passwdconf = web.input().passwdconf
        emailadd = web.input().email
        emailaddconf = web.input().emailconf
        cellphone = web.input().cellphone
        privilege = 1
        # write these in DB here.
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
            return render.sign_in(error_message)
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
        filename = f.file2up.filename
        ext = filename.split('.')[-1]
        if validName(web.input().name):
            name = web.input().name + '.' + ext
        else:
            errors = ['name error.']
            return render.new(errors, postname, bucket)
        saved = S3.saveFile(bucket=bucket, name=name, file1=f.file2up.file)
        smessage = saved + ' has been saved!'
        return render.new([smessage], postname, bucket)

class delete:
    def POST(self):
        x = web.input()
        S3 = AWS.AWSS3()
        bucket = S3.get_bucket(x.bucketname)
        S3.delFile(x.keyname, x.bucketname)
        message = x.keyname + ' is Deleted'
        return render.new([message], x.postname, bucket)




if __name__ == "__main__":
    app.run()