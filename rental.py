import web
import hashlib

web.config.debug = False

urls = (
    '/login', 'login',
    '/reset', 'reset',
    '/sign_in', 'sign_in'
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


if __name__ == "__main__":
    app.run()