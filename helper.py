# Generate Users Profile File
import json
import pandas
# This method return a mapping of video(key)
# and and array of scores(value)
class Helper:
    def parse_video_scores(self,scores_object):
        result = {}
        for score in scores_object:
            if score['postId'] not in result:
                result[score['postId']] = []
            result[score['postId']].append(score['score'])
        return result

    def parse_video_words(self,words_object):
        result = {}
        for word in words_object:
            if word['postId'] not in result:
                result[word['postId']] = []
            result[word['postId']].append(word['word'])
        return result

    def parse_csv_file(self,csv_file):
        result = {}
        for index in range(1,len(csv_file[0])):
            result[csv_file[0][index]] = int(csv_file[1][index])
        return result

    def get_cluster_cardinality(self,videos_cluster):
        result = {}
        for video in videos_cluster:
            if videos_cluster[video] in result:
                # Increase
                result[videos_cluster[video]] += 1
            else:
                result[videos_cluster[video]] = 1
        return result


    def calc_skipping_ratio(self,scores):
        countSkipped = 0
        for score in scores:
            if score < 0:
                countSkipped += 1
        return round(countSkipped*1.0/len(scores)*1.0,2)

    def calc_avg_score(self,scores):
        countSkipped = 0
        sumScores = 0
        for score in scores:
            if score < 0:
                countSkipped += 1
            else:
                sumScores += score

        if countSkipped > 0:
            return 0
        else:
            return round(sumScores*1.0/(len(scores)*1.0-countSkipped*1.0),2)

    def calc_user_interaction(self):
        video_to_cluster = self.parse_csv_file(self.clusterData)
        cardinality = self.get_cluster_cardinality(video_to_cluster)
        video_sequence = self.in_user_videos
        users_scores = self.in_user_scores
        clusterSequence = []
        for video in video_sequence:
            # ClusterSequece
            clusterSequence.append(video_to_cluster[str(video)])

        # Calculate Interaction
        # Sum scores by cluster
        scores_by_cluster = {}
        for c_index in range(len(clusterSequence)):
            cluster = clusterSequence[c_index]
            if cluster in scores_by_cluster:
                scores_by_cluster[cluster] += self.calc_avg_score(users_scores[video_sequence[c_index]])
            else:
                scores_by_cluster[cluster] = self.calc_avg_score(users_scores[video_sequence[c_index]])
        # Add cluster with no interaction
        for cluster in cardinality:
            if cluster not in scores_by_cluster:
                scores_by_cluster[cluster] = 0
        # Divide sum by cardinality of the cluster
        for cluster in scores_by_cluster:
            scores_by_cluster[cluster] = round((scores_by_cluster[cluster]*1.0) / (cardinality[cluster] * 1.0),2)

        return scores_by_cluster

    def calc_user_profile(self):
        lenStudentBehavior = self.user_videos
        usersProfilesJsonWithIndexes = {}
        video_to_cluster = parse_csv_file(self.clusterData)
        cardinality = get_cluster_cardinality(video_to_cluster)
        print(cardinality)
        for index in range(lenStudentBehavior):
            memberId = studentBehavior[index]["memberId"]
            if memberId not in usersProfilesJsonWithIndexes:
                studentProfile                          = {}
                studentProfile["memberId"]              = memberId
                studentProfile["videoSequence"]         = []
                studentProfile["skippingRatioSequence"] = []
                studentProfile["avgScoreSequence"]         = []
                studentProfile["dictionarySequence"]    = []
                studentProfile["skippingIndex"]         = -1
                studentProfile["clusterSequence"]       = []
                studentProfile["scores"]                = []
                studentProfile["interaction"]           = {}
                usersProfilesJsonWithIndexes[memberId] = studentProfile

            # Addid values for every key
            # Video Sequence
            usersProfilesJsonWithIndexes[memberId]["videoSequence"].extend(studentBehavior[index]["chosenVideo"])

            videos_scores = parse_video_scores(studentBehavior[index]["listenScore"])
            video_words = parse_video_words(studentBehavior[index]["vocabularyList"])

            # SkippingRationSequence
            for video in studentBehavior[index]["chosenVideo"]:
                scores = videos_scores[video]
                usersProfilesJsonWithIndexes[memberId]["scores"].append(scores)
                usersProfilesJsonWithIndexes[memberId]["skippingRatioSequence"].append(calc_skipping_ratio(scores))
                # Average Score Sequence
                avg = calc_avg_score(scores)
                usersProfilesJsonWithIndexes[memberId]["avgScoreSequence"].append(avg)

                # DictionarySequence
                if str(video) in video_words:
                    words = video_words[str(video)]
                    usersProfilesJsonWithIndexes[memberId]["dictionarySequence"].append(len(words))
                else:
                    usersProfilesJsonWithIndexes[memberId]["dictionarySequence"].append(0)

                # ClusterSequece
                usersProfilesJsonWithIndexes[memberId]["clusterSequence"].append(video_to_cluster[str(video)])


            # skippingIndex
            skip_index = [ n for n,i in enumerate(usersProfilesJsonWithIndexes[memberId]["skippingRatioSequence"]) if i>0.0 ][0]
            usersProfilesJsonWithIndexes[memberId]["skippingIndex"] = skip_index
            # Add cluster turning point
            usersProfilesJsonWithIndexes[memberId]["tp"] = usersProfilesJsonWithIndexes[memberId]["clusterSequence"][skip_index]

            # Calculate Interaction
            # Sum scores by cluster
            scores_by_cluster = {}
            for c_index in range(len(usersProfilesJsonWithIndexes[memberId]["clusterSequence"])):
                cluster = usersProfilesJsonWithIndexes[memberId]["clusterSequence"][c_index]
                if cluster in scores_by_cluster:
                    scores_by_cluster[cluster] += usersProfilesJsonWithIndexes[memberId]["avgScoreSequence"][c_index]
                else:
                    scores_by_cluster[cluster] = usersProfilesJsonWithIndexes[memberId]["avgScoreSequence"][c_index]
            # Add cluster with no interaction
            for cluster in cardinality:
                if cluster not in scores_by_cluster:
                    scores_by_cluster[cluster] = 0
            # Divide sum by cardinality of the cluster
            for cluster in scores_by_cluster:
                scores_by_cluster[cluster] = round((scores_by_cluster[cluster]*1.0) / (cardinality[cluster] * 1.0),2)

            usersProfilesJsonWithIndexes[memberId]["interaction"] = scores_by_cluster
            return scores_by_cluster

    def parse_cluster_videos(self,clusterData):
        result = {}
        for index in range(1,len(csv_file[0])):
            cluster_number = int(csv_file[1][index])
            if cluster_number not in result:
                result[cluster_number] = []
            result[cluster_number].append(csv_file[0][index])
        return result

    def get_videos_in_cluster(self,cluster):
        return self.cluster_videos[cluster]
        
    def __init__(self,users_videos,clusterData):
        self.in_user_scores = self.parse_video_scores(users_videos["listenScore"])
        self.in_user_videos = users_videos["chosenVideo"]
        self.clusterData = clusterData
        self.cluster_videos = self.parse_cluster_videos(clusterData)

with open("data/studentBehaviorExample.json") as data_file:
    user_videos = json.load(data_file)
csv_file = pandas.read_csv("data/clustersByWordLevel.csv",header=None)
helper = Helper(user_videos,csv_file)
interaction = helper.calc_user_interaction()
print(interaction)
