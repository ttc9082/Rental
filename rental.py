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
    '/new/(.*)', 'new',
    '/new', 'new',
    '/del', 'delete',
    '/', 'index',
    '/index', 'index', 
    '/profile/(.*)', 'profile',
    '/show/(.*)', 'show'
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
            all_room = Room.show_all()
            print all_room
            titles = []
            des = []
            rid = []
            pics = []
            owner = []
            for room in all_room:
                titles.append(room[3])
                des.append(room[4])
                rid.append(room[0])
                s3 = AWS.AWSS3()
                tmp_bucket = s3.get_bucket(room[6])
                key = tmp_bucket.get_all_keys()
                pic = 'https://s3.amazonaws.com/' + tmp_bucket.name + '/' + key[0].name
                pics.append(pic)
                temp_name = User.find_by_id(room[1])[1]
                owner.append(temp_name)
            return render.index(userName, titles, rid, pics, owner)
        else:
            print 'not logged in'
            return render.login()

    def POST(self):
        name, passwd = web.input().user, web.input().passwd
        print name, passwd
        try:
            ps = User.validate_passwd(name)
            for p in ps:
                if hashlib.md5(passwd).hexdigest() == p[0]:
                    session.userId = p[1]
                    privilege = 1 # check privilege by name in DB
                    session.privilege = privilege
                    userName = User.find_by_id(session.userId)[1]

                    print "-----id-----"
                    print userName


                    if not logged():
                        print 'not logged in'
                    all_room = Room.show_all()
                    print all_room
                    titles = []
                    des = []
                    rid = []
                    pics = []
                    owner = []
                    for room in all_room:
                        titles.append(room[3])
                        des.append(room[4])
                        rid.append(room[0])
                        s3 = AWS.AWSS3()
                        tmp_bucket = s3.get_bucket(room[6])
                        key = tmp_bucket.get_all_keys()
                        pic = 'https://s3.amazonaws.com/' + tmp_bucket.name + '/' + key[0].name
                        pics.append(pic)
                        temp_name = User.find_by_id(room[1])[1]
                        owner.append(temp_name)

                    return render.index(userName, titles, rid, pics, owner)



        except:
            session.userId = 0
            session.privilege = 0
            return render.login_error()


class logout:
    def GET(self):
        uid = session.userId
        userName = User.find_by_id(session.userId)[1]
        session.userId = 0
        session.kill()
        return render.logout(userName)


class sign_up:
    def GET(self):
        errors = web.input(errors=None)
        print errors
        name=''
        if logged():
            logout()
            return render.sign_up(name,errors.errors)
        else:
            return render.sign_up(name,errors.errors)
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
            name=''
            return render.sign_up(name, error_message)
        else:
            return render.login()


class new:

    def GET(self, id=None):
        if logged():
            message = web.input(message=None).message
            print id
            if id == None:
                rid, bucket, title, des, price, location, status = None, None, None, None, None, None, None
            else:
                rid, uid, title, des, location, price, bucketname, status = Room.find_by_id(id)
                print Room.find_by_id(id)
                s3 = AWS.AWSS3()
                bucket = s3.get_bucket(bucketname)
            return render.new(message, rid, bucket, title, des, price, location, status)
        else:
            return render.login()

    def POST(self):
        S3 = AWS.AWSS3()

        uid = session.userId
        title = web.input().tit
        des = web.input().des
        price = web.input().price
        location = web.input().loc
        status = web.input().status
        rid = web.input().rid

        if not rid:
            num = 0
            while num < 10:
                try:
                    bname = 'rental_id_' + str(random.randint(1000, 9999))
                    S3.create_bucket(bname)
                    break
                except:
                    num += 1
                    pass
            room_data = [uid, title, des, location, price, bname, 0]
            print room_data
            Room.insert(room_data)
            rid = Room.find_my_id(bname)
        else:
            bname = Room.find_by_id(rid)[6]

        bucket_name = bname
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
            return render.new(errors, rid, bucket, title, des, price, location, status)
        s3_file = room_type + '/' + name
        saved = S3.saveFile(bucket=bucket, name=s3_file, file1=f.file2up.file)
        smessage = saved[4:] + ' has been saved!'
        return render.new([smessage], rid, bucket, title, des, price, location, status)


class delete:
    def POST(self):
        x = web.input()
        S3 = AWS.AWSS3()
        bucket = S3.get_bucket(x.bucketname)
        S3.delFile(x.keyname, x.bucketname)
        message = x.keyname + ' is Deleted'
        return render.new([message], x.rid, bucket, x.tit, x.des, x.price, x.location, x.status)

class show:
    def GET(self, rid):
        S3 = AWS.AWSS3()

        room = Room.find_by_id(rid)
        title = room[2]
        des = room[3]
        loc = room[4]
        price = room[5]
        bucket_name = room[6]
        bucket = S3.get_bucket(bucket_name)
        status = room[7]

        return render.show(title, des, loc, price, bucket, status)


class index:
    def GET(self):
        if not logged():
            print 'not logged in'
        all_room = Room.show_all()
        print all_room
        titles = []
        des = []
        rid = []
        pics = []
        owner = []
        for room in all_room:
            titles.append(room[3])
            des.append(room[4])
            rid.append(room[0])
            s3 = AWS.AWSS3()
            tmp_bucket = s3.get_bucket(room[6])
            key = tmp_bucket.get_all_keys()
            pic = 'https://s3.amazonaws.com/' + tmp_bucket.name + '/' + key[0].name
            pics.append(pic)
            temp_name = User.find_by_id(room[1])[1]
            owner.append(temp_name)
        if logged():
            userName = User.find_by_id(session.userId)[1]
        else:
            userName = ''
        print titles
        print des
        print rid
        print pics
        return render.index(userName, titles, rid, pics, owner)


class profile:
    def GET(self, id):
        my_room = Room.show_my_rooms(id)





if __name__ == "__main__":
    app.run()