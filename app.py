from flask import Flask, jsonify, render_template, request
from helper import Helper
import pandas
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/getClusterInteraction', methods=['POST'])
def calc_user_interaction():
    user_videos = request.get_json()
    csv_file = pandas.read_csv("data/clustersByWordLevel.csv",header=None)
    helper = Helper(user_videos,csv_file)
    interaction = helper.calc_user_interaction()
    print(interaction)
    return jsonify(interaction)

@app.route('/getTPVideos', methods=['POST'])
def getTPVideos():
    user_videos = request.get_json()
    csv_file = pandas.read_csv("data/clustersByWordLevel.csv",header=None)
    helper = Helper(user_videos,csv_file)
    interaction = helper.calc_user_interaction()
    print(interaction)

    # Get tp cluster
    #tp_cluster = requests.post('http://httpbin.org/post', data = interaction)
    tp_cluster = 0

    # Get videos in that cluster
    videos = helper.get_videos_in_cluster(0)

    # Creating result format
    result = { "cluster": tp_cluster , "videos": videos}
    # Get cluster of TP
    return jsonify(result)


if __name__ == '__main__':
    app.run()
