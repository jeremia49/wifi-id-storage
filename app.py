import flask
from flask import request, jsonify, Response, abort, render_template, flash, redirect
from werkzeug.utils import secure_filename
import time
import tempfile
import subprocess
import os
import json
import time
import requests
import urllib.parse


class wifiidstorage:
    def __init__(self):
        self.ma="ceea823af07a4dca9e1f43e88b98c401"                                  #mountbit-auth
        self.ak="15ee82f543953d38316c34abed4bdc01fd1acf79101703312041c81d8d829f2d"   #api-Key
        self.url_createfile="https://api.obscloud.mobilecloud.co.id/api/2/files/create/"
        self.useragent="android-client (5.1.1; SM-N950N) v1.1.38"
        self.deviceid = "1f594fb6610b0104"

    def create_file(self,file):
        url = self.url_createfile
        payload = "{\n    \"created\": 1552970625000,\n    \"device_id\": \"%s\",\n    \"device_reference\": \"/storage/emulated/0/Storage/%s\",\n    \"multipart\": true,\n    \"modified\": 1552970625000,\n    \"overwrite\": true,\n    \"path\": \"/apistorage/%s\",\n    \"size\": %s,\n    \"version\": 0\n}"%(self.deviceid,file,file,os.path.getsize(file))
        headers = {
          'Host': 'api.obscloud.mobilecloud.co.id',
          'Connection': 'Keep-Alive',
          'Accept-Encoding': 'gzip',
          'User-Agent': self.useragent,
          'Mountbit-Auth': self.ma,
          'Content-Type': 'application/json; charset=UTF-8'
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        response = response.json()
        urlupload = response['url']
        urlconfirm = response ['confirm_url']
        return urlupload, urlconfirm

    def put_file(self,file,url):
        payload=open(file,'rb')
        headers = {
          'Connection': 'Keep-Alive',
          'Accept-Encoding': 'gzip',
          'User-Agent': self.useragent,
          'content-type': 'application/octet-stream'
        }

        response = requests.request("PUT", url, headers=headers, data = payload)
    def confirm_file(self,url):
        payload = {}
        headers = {
          'Connection': 'Keep-Alive',
          'Accept-Encoding': 'gzip',
          'User-Agent': self.useragent,
          'Mountbit-Auth': self.ma
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        print ("sukses")
    def get_item_data(self,path):
        url = "https://api.obscloud.mobilecloud.co.id/api/2/files/get/%s/?for_view=true"%(path)
        payload = {}
        headers = {
          'Mountbit-Auth': self.ma,
          'User-Agent': self.useragent,
          'Connection': 'Keep-Alive',
          'Accept-Encoding': 'gzip'
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        response=response.json()
        a=response['url']
        return a

#Config File
def upload(namafile):
    path = "/apistorage/%s"%(namafile)
    ws=wifiidstorage()
    print("Inisiasi Berhasil\n get url file to upload ... ")
    try:
        urlupload, urlconfirm = ws.create_file(namafile)
        print("Berhasil mendapatkan link\n memulai upload file ... ")
        try:
            ws.put_file(namafile,urlupload)
            print("Berhasil mengupload file ! , mengkorfirmasi file ...")
            try:
                ws.confirm_file(urlconfirm)
                print("File Berhasil di upload ..")
                params = {'path': path}
                pathencode=urllib.parse.urlencode(params)
                return("https://api.jeremia.live/wifiidstoragefinder.php?%s"%(pathencode))
            except Exception as e:
                print("Gagal mengkorfirmasi URL, Error : %s"%(e))
        except Exception as e :
            print("Gagal meletakkan file !, Error : %s"%(e))
    except Exception as e:
        print("Gagal Mendapatkan Link !, Error : %s"%(e))


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return """Hello !"""

@app.route('/backup', methods=['GET','POST'])
def cloudmax():
  if request.method == 'POST':
    time_start=time.time()
    if not request.files:
        time_end=time.time()
        exe_time=time_end-time_start
        e= "No Files Uploaded/Selected"
        output_json={"status": 400, "error":e,"execution_time":exe_time }
        return jsonify(output_json)
    else:
        files=request.files['file']
        try:
          files.save(secure_filename(files.filename))
        except:
          e= "Failed to save temporary file"
          time_end=time.time()
          exe_time=time_end-time_start
          output_json={"status": 400, "error":e,"execution_time":exe_time }
          return jsonify(output_json)
        try:
          hasil=upload(files.filename)
        except:
          e ="Failed to upload files"
          time_end=time.time()
          exe_time=time_end-time_start
          output_json={"status": 400, "error":e,"execution_time":exe_time }
          return jsonify(output_json)
        try:
          time_end=time.time()
          exe_time=time_end-time_start
          output_json={"status": 200, "error": "no error occured", "url": hasil,"Copyright (c)": 2019, "credits": "Jeremia M ","execution_time": exe_time}
          #return Response(output_json, mimetype='application/json')
          return jsonify(output_json)
        except:
          return """Something Error when parsing final json"""
        try:
          os.remove(secure_filename(files.filename))
        except Exception as e:
          print(e)
  elif request.method == 'GET':
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <meta name="viewport" content="initial-scale=1">
    <content>
    <form method=post action='' enctype=multipart/form-data>
      <input type="file" required name="file">
      <input type="submit" value="Upload">
    </form>
    </content>
    '''

#----------------------End Main Program----------------------------
if __name__ == "__main__":
  #flask run --host=0.0.0.0 --port=8080
  app.run(host="0.0.0.0",port="8080")