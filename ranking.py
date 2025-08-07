import math
import random
import matplotlib.pyplot as plt
import sys

K = 200
TOTAL_MATCHES = 0
elo_buffer = .15
provisionals = 10

def Probability(rating1, rating2): 
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 

def fair_matches(items):
    item_matches_ratio = [1-(x["W"]+x["L"])/(2*TOTAL_MATCHES) for x in items]
    normalizer = sum(item_matches_ratio)
    item_matches_ratio = list(map(lambda x: x/normalizer, item_matches_ratio))
    for i in range(1, len(item_matches_ratio)):
        item_matches_ratio[i] += item_matches_ratio[i-1]
    selection = random.random()
    for i in range(len(item_matches_ratio)):
        if selection < item_matches_ratio[i]:
            return i

def newItem(items, headers):
    item = {header: input(f"Enter the {header} of the item: ") if header not in ["elo", "W", "L"] else 1000 for header in headers}
    if "W" in headers:
        item["W"] = 0
    if "L" in headers:
        item["L"] = 0
    if "year" in headers:
        item["year"] = int(item["year"])

    for _ in range(provisionals):
        index = random.randint(0, len(items)-1)
        match(item, items[index])
    
    items.append(item)

def match(a, b):
    global TOTAL_MATCHES 
    TOTAL_MATCHES += 1
    print("\nWhich item do you prefer?")
    print(a["title"], "(1)")
    print(b["title"], "(2)")
    result = input("Enter (1) or (2): ")
    if result == "1":
        matches = getAdjustments(b["elo"], a["elo"])
        b["elo"] = matches[0]
        b["L"] += 1
        a["elo"] = matches[1]
        a["W"] += 1
    else:
        matches = getAdjustments(a["elo"], b["elo"])
        b["elo"] = matches[1]
        b["W"] += 1
        a["elo"] = matches[0]
        a["L"] += 1
    print("New elo:")
    print(a["title"], a["elo"])
    print(b["title"], b["elo"])

def randomMatch(items):
    a = random.randint(0, len(items)-1)
    b = random.randint(0, len(items)-1)
    while a == b:
        b = random.randint(0, len(items)-1)
    
    match(items[a], items[b])

def search(videos, movie):
    movies = sorted(videos, key=lambda x: x["elo"],reverse=True)
    for i in range(len(movies)):
        if movies[i]["title"] == movie:
            print("\n", movie, "is present at rank", i+1, "perentile", int(100*(1-(i+1)/len(movies))), "with elo score of", movies[i]["elo"], "\n")
            return
    print(movie, "is not present")
    return

def genreRankings(items, category):
    items = sorted(items, key=lambda x: x["elo"],reverse=True)
    count = 1
    for item in items:
        if category in item["genre"].split("/"):
            print(count, item["title"])
            count += 1
    return 

def rankedMatch(items):
    K = int(elo_buffer*len(items))
    items = sorted(items, key=lambda x: x["elo"], reverse=True)
    a = fair_matches(items)
    b = a
    while a == b:
        b = random.randint(max(0, a-K), min(len(items)-1, a+K))
    match(items[a], items[b])

def getAdjustments(loserElo, winnerElo):
    wp = Probability(loserElo, winnerElo)
    lp = Probability(winnerElo, loserElo)
    newLoser = loserElo + K * (0 - lp)
    newWinner = winnerElo + K * (1 - wp)
    return (int(newLoser), int(newWinner))

def printRankings(items):
    print("\n")
    items = sorted(items, key= lambda k: k["elo"], reverse=True)
    for vid in items:
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

def get_from_title(items, title):
    for i in range(len(items)):
        if items[i]["title"] == title:
            return i
    return -1

ranklist = []
if len(sys.argv) < 2:
    raise Exception("Filename of ranking file must be provided as command line argument")

filename = sys.argv[1]
with open(filename, "r") as file:
    headers = list(map(lambda x: x.strip(), file.readline().split(",")))
    if "elo" not in headers:
        raise Exception("'elo' must be provided as a header")
    if "title" not in headers:
        raise Exception("'title' must be provided as a header")
    
    for line in file:
        data = line.split(",")
        ranklist.append({headers[i]:data[i] for i in range(len(headers))})
        ranklist[~0]["elo"] = int(ranklist[~0]["elo"])
        ranklist[~0]["W"] = int(ranklist[~0]["W"])
        ranklist[~0]["L"] = int(ranklist[~0]["L"])
        TOTAL_MATCHES += ranklist[~0]["W"]
        if "year" in headers:
            ranklist[~0]["year"] = int(ranklist[~0]["year"])

while True:
    decision = input("Would you like to quit(0), enter a new item(1), do a random match(2), see the rankings(3), \ndo a ranked match(4), get partial rankings(5), plot elo(6), search(7), or choose a match(8): ")
    if decision == "1":
        newItem(ranklist, headers)
    elif decision == "2": 
        n = input("How many random matches do you want to do: ")
        for _ in range(int(n)):
            randomMatch(ranklist)
    elif decision == "3":
        printRankings(ranklist)
    elif decision == "4":
        n = input("How many ranked matches do you want to do: ")
        for _ in range(int(n)):
            rankedMatch(ranklist)
    elif decision == "5":
        cat = input("What category would you like: ")
        genreRankings(ranklist, cat)
    elif decision == "6":
        x = [item["elo"] for item in ranklist]
        plt.scatter(range(len(x)), sorted(x[::-1]))
        edges, means, clusters = kmeans(5, ranklist)
        tiers = ["S", "A", "B", "C", "D", "F"]
        for i in range(6):
            print("Top of {0} Tier: {1}".format(tiers[i], clusters[~i][~0]["title"]))
            print("Bottom of {0} Tier: {1}".format(tiers[i], clusters[~i][0]["title"]))
        for edge in edges:
            plt.axhline(y=edge, color='b', linestyle='-')
        plt.show()
    elif decision == "7":
        item = input("What item are you looking for: ")
        search(ranklist, item)
    elif decision == "8":
        a, b = -1, -1
        while a == -1:
            title = input("Enter the title of the first item you want: ")
            a = get_from_title(ranklist, title)
            if a == -1:
                print("That item was not found, please try again")
        while b == -1:
            title = input("Enter the title of the second item you want: ")
            b = get_from_title(ranklist, title)
            if b == -1:
                print("That item was not found, please try again")
        
        match(ranklist[a], ranklist[b])
        
    else:
        break

with open(filename, "w") as file:
    ranklist = sorted(ranklist, key=lambda x: x["elo"],reverse=True)
    file.write(",".join(headers) + "\n")
    for item in ranklist:
        file.write(",".join(map(str, [item[header] for header in headers])) + "\n")