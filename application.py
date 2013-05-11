import web
from tool import SQL
from tool import AWS
import random
import os

urls = ('/', 'index',
        '/new', 'new',
        '/show', 'show',
        '/test', 'test'
        )

render = web.template.render('templates/')

class index:
    def GET(self):
        db = SQL.SQLtools()
        table = db.lookup('rooms')
        return render.index(table)

class add:
    def POST(self):
        i = web.input()
        S3 = AWS.AWSS3()
        db = SQL.SQLtools()
        try:
            S3.create_bucket(name=i.name)
        except:
            return render.wrong('Can not Use This Name.')
        if 'front' in i:
            download, stream = S3.create_cloudfront(i.name)
            db.insert('front', 'bucket', value=i.name)
            db.insert('front', 'bucket', value=i.name+'str')
            db.update('front', 'dis_id', value=download.id, where='bucket', name=i.name)
            db.update('front', 'dom_name', value=download.domain_name, where='bucket', name=i.name)
            db.update('front', 'dis_id', value=stream.id, where='bucket', name=i.name+'str')
            db.update('front', 'dom_name', value=stream.domain_name, where='bucket', name=i.name+'str')
            print 'added'
        raise web.seeother('/upload')

class favicon:
    def GET(self):
        return web.seeother('/static/favicon.ico')

class new:
    def GET(self):
        S3 = AWS.AWSS3()
        buckets = S3.get_all_buckets()
        return render.upload(buckets)

    def POST(self):
        b = web.input(bucket={})
        db = SQL.SQLtools()
        S3 = AWS.AWSS3()
        x = web.input(video={})
        if x.video.filename == '':
            return render.wrong('You did not choose a file~!')
        d = web.input(videoDes={})
        if d.videoDes == '':
            d.videoDes = 'This gay left nothing to describe his video.'
        i = web.input(videoName={})
        if i.videoName == '':
            return render.wrong('You video must have a Name~ right?')

        web.debug(x['video'].filename)
        #web.debug(x['video'].value)
        web.debug(i.videoName)
        web.debug(x.video.filename)
        filedir = '/home/ec2-user/uploads' #'Users/TTc9082/uploads'#' change this to the directory you want to store the file in.

        if 'video' in x: # to check if the file-object is created
            filepath=x.video.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1]
            ext = filename.split('.')[-1]
            filenoext = filename.split('.')[0]
            fout = open(filedir + '/' + filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.video.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        if ext not in ['mp3', 'mp4', 'flv', 'MOV', 'avi', 'wma']:
            e = "The extension is not legal.(legal extensions:['mp3', 'mp4', 'flv', 'MOV', 'avi', 'wma']"
            return render.wrong(e)
        finalfile = filedir + '/' + filename
        finalflv = filedir + '/' + filenoext + '.flv'
        os.system('ffmpeg -i "%s" -ar 44100 -ab 96 -f flv "%s"' % (finalfile, finalflv))
        keyname1 = i.videoName + str(random.randint(1000, 9999)) + '.flv'
        keyname2 = i.videoName + str(random.randint(1000, 9999)) + '.' + ext
        S3 = AWS.AWSS3()
        db = SQL.SQLtools()
        db.insert('videos', 'name', value=i.videoName)
        S3.save_string(bucket=b.bucket, name=(i.videoName + '.txt'), value=d.videoDes)
        flvName = S3.saveFile(bucket=b.bucket, name=keyname1, filename=finalflv)
        mp4Name = S3.saveFile(bucket=b.bucket, name=keyname2, filename=finalfile)
        os.remove(filedir + '/' + filename)
        os.remove(filedir + '/' + filenoext + '.flv')
        db.update('videos', 'key', value=keyname1, where='name', name=i.videoName)
        db.update('videos', 'hd', value=keyname2, where='name', name=i.videoName)
        db.update('videos', 'bucket', value=b.bucket, where='name', name=i.videoName)
        db.update('videos', 'des', value=(i.videoName + '.txt'), where= 'name', name=i.videoName)
        return web.redirect('/sort')

class sort:
    def GET(self):
        url = 'NULL'
        db = SQL.SQLtools()
        table = db.sortdb()
        return render.index(table, url)

class delete:
    def GET(self, name):
        S3 = AWS.AWSS3()
        db = SQL.SQLtools()
        hdfilename = db.lookup(table='videos', which='hd', where='key', name=name)[0][0]
        desfilename = db.lookup(table='videos', which='des', where='key', name=name)[0][0]
        bucketname = db.lookup(table='videos', which='bucket', where='key', name=name)[0][0]
        web.debug(hdfilename)
        web.debug(bucketname)
        S3.delFile(name=name, bucket=bucketname)
        S3.delFile(name=hdfilename, bucket=bucketname)
        S3.delFile(name=desfilename, bucket=bucketname)
        db.delraw(name)
        return web.redirect('/')

class video:
    def GET(self, name):
        if name.split('.')[-1] != 'flv':
            what = 'hd'
        else:
            what = 'key'
        db = SQL.SQLtools()
        S3 = AWS.AWSS3()
        rate = float(db.lookup(table='videos', which='rate', where=what, name=name)[0][0])
        desc = db.lookup(table='videos', which='des', where=what, name=name)[0][0]
        Name = db.lookup(table='videos', which='name', where=what, name=name)[0][0]
        bucketname = db.lookup(table='videos', which='bucket', where=what, name=name)[0][0]
        des = S3.get_string(bucket=bucketname, name=desc)
        try:
            down = db.lookup(table='front', which='dom_name', where='bucket', name=bucketname)[0][0]
            stream = db.lookup(table='front', which='dom_name', where='bucket', name=bucketname+'str')[0][0]
            url = 'http://' + stream + '/' + name
            urld = 'http://' + down + '/' + name
        except:
            url = 'https://s3.amazonaws.com/' + bucketname + '/' + name
            urld = 'https://s3.amazonaws.com/' + bucketname + '/' + name
        return render.video(url,urld, Name, des, rate)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()