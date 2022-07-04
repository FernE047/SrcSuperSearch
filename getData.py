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

STOPPED = 534074
begin = time() - (STOPPED*1.1)
TOTAL = 662266
API = "https://www.speedrun.com/api/v1/"
ALPHA = ['_','-','+','.','|','@', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
allIDS = []
with open("allRunners.csv",'r',newline = "") as file:
    reader = csv.reader(file,delimiter = ";")
    for i in reader:
        allIDS.append(i[0])
if True:
    with open("allRunnersDataUTF.csv","a",newline = "", encoding = "UTF-8") as csvOutput:
        output = csv.writer(csvOutput, delimiter = ";")
        #output.writerow(['id','name','pronouns','area','area Label',
        #          'power Level','color 1','color 2','color Animated?',
        #          'signup Date','has donated','donated','coin',
        #          'supporter End Date','boost End Date','is a Game Moderator',
        #          'is Translator','is Supporter','is Boosted','runs ILs',
        #          'runs FGs','runs','categories ILs','categories FGs',
        #          'categories','games ILs','games FGs','games',
        #          'platforms ILs','platforms FGs','platforms','wrs ILs',
        #          'wrs FGs','wrs','podiums ILs','podiums FGs','podiums',
        #          'obsoletes ILs','obsoletes FGs','obsoletes',
        #          'Games with at least 1 wrs','categoriesMisc','levels'])
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
            v = [0,0,0]
            for run in ALL['runs']:
                if "levelId" in run:
                    v[0] += 1
                else:
                    v[1] += 1
                v[2] += 1
            user += v
            for cat in ['category','game','platform']:
                v = [set(),set(),0]
                for run in ALL['runs']:
                    if cat+'Id' not in run:
                        continue
                    if "levelId" in run:
                        v[0].add(run[cat+'Id'])
                    else:
                        v[1].add(run[cat+'Id'])
                v[0] = len(v[0])
                v[1] = len(v[1])
                v[2] = v[0] + v[1]
                user += v
            wrs = [0,0,0]
            podiums = [0,0,0]
            obsoletes = [0,0,0]
            gamesWithAWr = set()
            for run in ALL['runs']:
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
            user += wrs + podiums + obsoletes
            user.append(len(gamesWithAWr))
            user.append(len([a for a in ALL['categories'] if a['isMisc']]))
            user.append(len(ALL['levels']))
            output.writerow(user)
            if lenght % 100 == 0:
                end = time()
                duration = (end - begin)/lenght
                print(f"{lenght} : {eT(end - begin)} : {eT(duration)} : {eT(duration * (TOTAL - lenght))}")
else:
    print("interrompido")
end = time()
duration = (end - begin)/lenght
print(f"{lenght} : {eT(end - begin)} : {eT(duration)} : {eT(duration * (TOTAL - lenght))}")
