from flask import Flask, Response, request
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello World!</h1>"

@app.route("/api/entryphone", methods = ['GET', 'POST'])
def entryphone_api():
    url_args = request.args
    ring = 'ring' in url_args.keys()
    ring = ring and int(url_args['ring'].strip()) == 1
    
    return '{"status" : "ok", "ring" : %s}' % int(ring)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
