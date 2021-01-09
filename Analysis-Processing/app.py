from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename
import os
import requests
import urllib.request
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from flask import send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]




app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt'])

analyseFileUrl = "https://us-central1-gold-hybrid-283915.cloudfunctions.net/predictCluster"

def preprocessLine(line):
    return line

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyse(content):
  result = "Not found"
  data = json.dumps({
        'title': content
    })
  result =requests.post(analyseFileUrl,data=data,headers={"Content-Type":"application/json"})
  if result:
    cluster_name = json.loads(result.text)
    return cluster_name
  return result
  
@app.route('/')
def upload_form():
  return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
  file_array = []
  if request.method == 'POST':
    if 'files[]' not in request.files:
      flash('No file part')
      return redirect(request.url)
  files = request.files.getlist('files[]')
  for file in files:
    files_c = {}
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      # print(file.read())
      cluster = analyse(str(file.read()))
      files_c["filename"] = filename
      files_c["cluster"] = cluster
    file_array.append(files_c)
  flash('File(s) successfully uploaded')
  print(file_array)
  return render_template('upload.html',files=file_array)

@app.route('/processData',methods=['POST'])
def wordCloudGenerator():
    f = request.files['file']
    json_array = {}
    filename = secure_filename(f.filename)
    line = f.read().decode('utf-8')
    line = preprocessLine(line)
    line = line.strip('\n\r')
    words = line.split()
    for w in words:
      if ((w[0].isupper()) and (w.lower() not in stop_words)):
        if (w in json_array):
          json_array[w]+=1
        else:
          json_array[w]=1
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=json_array)
    wordcloud.to_file("first_review.png")
    return send_file("first_review.png",as_attachment=True)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5000, debug=True)