import math
import random
import matplotlib.pyplot as plt

K = 200
elo_buffer = .1
provisionals = 10

def Probability(rating1, rating2): 
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 

def newVideo(videos):
    title = input("Enter the title of the movie: ")
    genre = input("Enter the genre of the movie: ")
    elo = 1000
    video = {"title":title, "genre":genre, "elo":elo}

    for _ in range(provisionals):
        index = random.randint(0, len(videos)-1)
        match(video, videos[index])
    
    videos.append(video)

def match(a, b):
    print("\nWhich movie was better to watch?")
    print(a["title"], "(1)")
    print(b["title"], "(2)")
    result = input("Enter (1) or (2): ")
    if result == "1":
        matches = getAdjustments(b["elo"], a["elo"])
        b["elo"] = matches[0]
        a["elo"] = matches[1]
    else:
        matches = getAdjustments(a["elo"], b["elo"])
        b["elo"] = matches[1]
        a["elo"] = matches[0]
    print("New elo:")
    print(a["title"], a["elo"])
    print(b["title"], b["elo"])

def randomMatch(videos):
    a = random.randint(0, len(videos)-1)
    b = random.randint(0, len(videos)-1)
    while a == b:
        b = random.randint(0, len(videos)-1)
    
    match(videos[a], videos[b])

def search(videos, movie):
    movies = sorted(videos, key=lambda x: x["elo"],reverse=True)
    for i in range(len(movies)):
        if movies[i]["title"] == movie:
            print("\n", movie, "is present at rank", i+1, "perentile", int(100*(1-(i+1)/len(movies))), "with elo score of", movies[i]["elo"], "\n")
            return
    print(movie, "is not present")
    return

def genreRankings(videos, category):
    movies = sorted(videos, key=lambda x: x["elo"],reverse=True)
    count = 1
    for movie in movies:
        if category in movie["genre"].split("/"):
            print(count, movie["title"])
            count += 1
    return 

def rankedMatch(videos):
    K = int(elo_buffer*len(videos))
    videos = sorted(videos, key=lambda x: x["elo"], reverse=True)
    a = random.randint(0, len(videos)-1)
    b = a
    while a == b:
        b = random.randint(max(0, a-K), min(len(videos)-1, a+K))
    match(videos[a], videos[b])

def getAdjustments(loserElo, winnerElo):
    wp = Probability(loserElo, winnerElo)
    lp = Probability(winnerElo, loserElo)
    newLoser = loserElo + K * (0 - lp)
    newWinner = winnerElo + K * (1 - wp)
    return (int(newLoser), int(newWinner))

def printRankings(videos):
    print("\n")
    videos = sorted(videos, key= lambda k: k["elo"], reverse=True)
    for vid in videos:
        print(vid["title"], vid["genre"], vid["elo"])

def kmeans(clusters, videos):
    means = sorted([videos[i]["elo"] for i in range(0, len(videos), len(videos)//clusters)])
    avg = lambda x: sum(x) / len(x)
    lst = sorted(videos, key=lambda x: x["elo"])

    for _ in range(50):
        cluster = [[] for _ in range(len(means))]
        for point in lst:
            mindex = 0
            for i in range(1, len(means)):
                if abs(point["elo"]-means[i]) < abs(point["elo"]-means[mindex]):
                    mindex = i
            cluster[mindex].append(point)
        means = [avg([y["elo"] for y in x]) for x in cluster]
        edges = [max([y["elo"] for y in x]) for x in cluster]

    return edges, means, cluster

videos = []

with open("movies.txt", "r") as vidFile:
    for line in vidFile:
        data = line.split(",")
        videos.append({"title":data[0], "genre":data[1], "elo":int(data[2])})

while True:
    decision = input("Would you like to quit(0), enter a new movie(1), do a random match(2), see the rankings(3), \ndo a ranked match(4), get partial rankings(5), plot elo(6), or search(7): ")
    if decision == "1":
        newVideo(videos)
    elif decision == "2": 
        n = input("How many random matches do you want to do: ")
        for _ in range(int(n)):
            randomMatch(videos)
    elif decision == "3":
        printRankings(videos)
    elif decision == "4":
        n = input("How many ranked matches do you want to do: ")
        for _ in range(int(n)):
            rankedMatch(videos)
    elif decision == "5":
        cat = input("What category would you like: ")
        genreRankings(videos, cat)
    elif decision == "6":
        x = [vid["elo"] for vid in videos]
        plt.scatter(range(len(x)), sorted(x[::-1]))
        edges, means, clusters = kmeans(5, videos)
        for i in range(6):
            print("Top of Tier {0}: {1}".format(i, clusters[~i][~0]["title"]))
            print("Bottom of Tier {0}: {1}".format(i, clusters[~i][0]["title"]))
        for edge in edges:
            plt.axhline(y=edge, color='b', linestyle='-')
        plt.show()
    elif decision == "7":
        movie = input("What movie are you looking for: ")
        search(videos, movie)
    else:
        break

with open("movies.txt", "w") as vidFile:
    movies = sorted(videos, key=lambda x: x["elo"],reverse=True)
    for video in movies:
        vidFile.write(video["title"] + "," + video["genre"] + "," + str(video["elo"]) + "\n")