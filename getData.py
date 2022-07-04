import csv
from time import time
import requests

def eT(tempo):
    minutos=int(tempo/60)
    segundos=tempo-60*minutos
    horas=int(minutos/60)
    minutos=minutos-60*horas
    dias=int(horas/24)
    horas=horas-24*dias
    retorno=""
    if(dias>0):
        retorno+=str(dias)+" day"+("s, " if dias>1 else ", ")
    if(horas>0):
        retorno+=str(horas)+" hour"+("s, " if horas>1 else ", ")
    if(minutos>0):
        retorno+=str(minutos)+" minute"+("s, " if minutos>1 else ", ")
    retorno+=str(segundos)+" seconds"
    return(retorno)

def anyRequests(text):
    while True:
        try:
            return requests.get(text).json()
        except:
            print("connection")

begin = time()
allIDS = []
with open("allIDs.csv",'r',newline = "") as file:
    reader = csv.reader(file,delimiter = ";")
    for i in reader:
        allIDS.append(i[0])
TOTAL = len(allIDS)
with open("allRunnersData.csv","w",newline = "", encoding = "UTF-8") as csvOutput:
    output = csv.writer(csvOutput, delimiter = ";")
    output.writerow(['id','name','pronouns','area','area Label',
              'power Level','color 1','color 2','color Animated?',
              'signup Date','has donated','donated','coin',
              'supporter End Date','boost End Date','is a Game Moderator',
              'is Translator','is Supporter','is Boosted','runs ILs',
              'runs FGs','runs','categories ILs','categories FGs',
              'categories','games ILs','games FGs','games',
              'platforms ILs','platforms FGs','platforms','wrs ILs',
              'wrs FGs','wrs','podiums ILs','podiums FGs','podiums',
              'obsoletes ILs','obsoletes FGs','obsoletes',
              'Games with at least 1 wrs','categoriesMisc','levels'])
    lenght = 0
    for idd in allIDS:
        lenght +=1
        if lenght < STOPPED:
            continue
        ALL = anyRequests(f"https://www.speedrun.com/_fedata/user/runs?userId={idd}&vary=1654385324&ver=4")
        if 'error' in ALL:
            print(idd)
            continue
        data = ALL['user']
        user = []
        user.append(data['id'])
        user.append(data['name'])
        user.append(data['pronouns'])
        if 'areas' in data:
            user.append(data['areas'][0]['name'])
            user.append(data['areas'][0]['label'])
        else:
            user.append("None")
            user.append("None")
        user.append(data['powerLevel'])
        if data['color1']:
            user.append(data['color1']['name'])
        else:
            user.append("None")
        if data['color2']:
            user.append(data['color2']['name'])
        else:
            user.append("None")
        user.append(data['colorAnimate'])
        user.append(data['signupDate'])
        user.append(data['hasDonated'])
        user.append(data['donated'])
        user.append(data['coin'])
        user.append(data['supporterEndDate'])
        user.append(data['boostEndDate'])
        user.append(data['isGameModerator'])
        user.append(data['isTranslator'])
        user.append(data['isSupporter'])
        user.append(data['isBoosted'])
        runs = [0,0,0]
        categories = [set(),set(),0]
        games = [set(),set(),set()]
        platforms = [set(),set(),set()]
        wrs = [0,0,0]
        podiums = [0,0,0]
        obsoletes = [0,0,0]
        gamesWithAWr = set()
        for run in ALL['runs']:
            if "levelId" in run:
                runs[0] += 1
            else:
                runs[1] += 1
            runs[2] += 1
            if 'categoryId' in run:
                if "levelId" in run:
                    categories[0].add(run['categoryId'])
                else:
                    categories[1].add(run['categoryId'])
            if 'gameId' in run:
                if "levelId" in run:
                    games[0].add(run['gameId'])
                else:
                    games[1].add(run['gameId'])
                games[2].add(run['gameId'])
            if 'platformId' in run:
                if "levelId" in run:
                    platforms[0].add(run['platformId'])
                else:
                    platforms[1].add(run['platformId'])
                platforms[2].add(run['platformId'])
            if 'place' in run:
                if run['place'] == 1:
                    if "levelId" in run:
                        wrs[0] += 1
                    else:
                        wrs[1] += 1
                    wrs[2] += 1
                    gamesWithAWr.add(run['gameId'])
                if run['place'] in (1,2,3):
                    if "levelId" in run:
                        podiums[0] += 1
                    else:
                        podiums[1] += 1
                    podiums[2] += 1
            else:
                if "levelId" in run:
                    obsoletes[0] += 1
                else:
                    obsoletes[1] += 1
                obsoletes[2] += 1
        categories[2] = categories[0] + categories[1]
        games[2] = len(games[2])
        platforms[2] = len(platforms[2])
        user += runs + categores + games + platforms + wrs + podiums + obsoletes
        user.append(len(gamesWithAWr))
        user.append(len([a for a in ALL['categories'] if a['isMisc']]))
        user.append(len(ALL['levels']))
        output.writerow(user)
        if lenght % 100 == 0:
            end = time()
            duration = (end - begin)/lenght
            print(f"{lenght} : {eT(end - begin)} : {eT(duration)} : {eT(duration * (TOTAL - lenght))}")
end = time()
duration = (end - begin)/lenght
print(f"{lenght} : {eT(end - begin)} : {eT(duration)} : {eT(duration * (TOTAL - lenght))}")
