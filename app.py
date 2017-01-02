from flask import Flask, jsonify, render_template, request
from helper import Helper
import pandas
import requests
import json
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
    # print(csv_file)
    helper = Helper(user_videos,csv_file)
    # print("ps")
    interaction = helper.calc_user_interaction()
    # print(interaction)

    # Get tp cluster
    # print("Format for interaction")
    # print(interaction)
    data_json = json.dumps(interaction)
    headers = {'Content-type': 'application/json'}
    response = requests.post("https://hopenglish-tpc-classifier.herokuapp.com/processJson", data=data_json, headers=headers)
    tp_cluster = int(response.text.replace("C",""))
    # print("tp_cluster")
    # print(tp_cluster)
    # Get videos in that cluster
    videos = helper.get_videos_in_cluster(tp_cluster)

    # Creating result format
    result = { "cluster": tp_cluster , "videos": videos}
    # Get cluster of TP
    return jsonify(result)


if __name__ == '__main__':
    app.run()
