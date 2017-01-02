from flask import Flask, jsonify, render_template, request
from helper import Helper
import pandas
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

    result = { "cluster": 0 , "videos": [1231,34235,12335,5345345,123123]}
    # Get cluster of TP
    return jsonify(result)


if __name__ == '__main__':
    app.run()
