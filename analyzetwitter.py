import csv
import re
import matplotlib.pyplot as plt

def gettweets():
    tweetinfo = []
    with open('tweets.csv', 'r') as tweetfile:
        tweetfile.readline()
        tweetreader = csv.reader(tweetfile, delimiter=",")
        for row in tweetreader:
            tweetinfo.append([row[1], row[3], row[5], row[6]])
       
    return tweetinfo 

def analyzeHourOfDay():
    hourDict = {}
    tweetinfo = gettweets()
    for tweet in tweetinfo:
        #Subtract four to account for timezone (CST)
        hour = (int(tweet[1].split()[1].split(":")[0]) - 4) % 24
        if hour not in hourDict.keys():
            hourDict[hour] = 1
        else:
            hourDict[hour] = hourDict[hour] + 1
    return hourDict

def analyzeWordFreq():
    wordDict = {}
    tweetinfo = gettweets()
    for tweet in tweetinfo:
        #disregard the tweet if it is a retweet (tweet[3] is not empty)
        if not tweet[3]:
            text = tweet[2]
            words = text.split()
            for word in words:
                word = re.sub(r'[^A-Za-z]+', '', word)
                if word not in wordDict.keys():
                    wordDict[word] = 1
                else:
                    wordDict[word] = wordDict[word] + 1
    sortedWordsByFreq = sorted(wordDict, key=wordDict.get, reverse=True)
    print(sortedWordsByFreq[0:250])

def analyzeRetweets():
    retweetHandles = {}
    tweetinfo = gettweets()
    for tweet in tweetinfo:
        if tweet[3]:
            text = tweet[2]
            m = re.search(r'RT @(?P<handle>.+?):', text)
            handle = m.group('handle')
            if handle not in retweetHandles.keys():
                retweetHandles[handle] = 1
            else:
                retweetHandles[handle] = retweetHandles[handle] + 1
    sortedRT = sorted(retweetHandles, key=retweetHandles.get, reverse=True)
    print("You have retweeted someone for {0} out of {1} tweets".format(\
                len(sortedRT), len(tweetinfo)))
    print("which is {0}% of your tweets".format((len(sortedRT) /\
                                          len(tweetinfo)) * 100))
    topten = sortedRT[0:10]
    for key in topten:
        print(key, retweetHandles[key])

def analyzeTweetAt():
    handleDict = {}
    tweetinfo = gettweets()
    for tweet in tweetinfo:
        if not tweet[3]:
            text = tweet[2]
            words = text.split()
            for word in words:
                word = re.sub(r'[^A-Za-z0-9_@]', '', word)
                if "@" in word:
                    #for better analysis, should check if actually valid handle
                    handle = word.replace("@", "")
                    if handle not in handleDict:
                        handleDict[handle] = 1
                    else:
                        handleDict[handle] = handleDict[handle] + 1
    sortedHandlesByFreq = sorted(handleDict, key=handleDict.get, reverse=True)
    print("You have mentioned someone in {0} out of {1} tweets".format(\
                len(sortedHandlesByFreq), len(tweetinfo)))
    print("which is {0}% of your tweets".format((len(sortedHandlesByFreq) /\
                                          len(tweetinfo)) * 100))
    topfifteen = sortedHandlesByFreq[0:15]
    for w in topfifteen:
       print(w,handleDict[w])

def graphHours(hourDict):
    times = []
    for i in range(2):
        if i == 0:
            times.append("12 AM")
        else:
            times.append("12 PM")
        for j in range(1,12):
            if i == 0:
                times.append("{0} AM".format(j))
            else:
                times.append("{0} PM".format(j))
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.bar(range(len(times)),hourDict.values())
    ax.set_xticks([i for i in range(24)])
    ax.set_xticklabels(times, rotation = 45)
    plt.title("Tweets per Hour")
    plt.show()

if __name__ == "__main__":
    analyzeWordFreq()
