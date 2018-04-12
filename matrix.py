from bs4 import BeautifulSoup
import requests
import json
from urllib.request import urlopen
#import urllib2 cant work in 3.7
from google.colab import files
import csv
from numpy import mean

w = [0]*48 #Width of the table  (16 seeds x 3 row for each + seed # column)
h = [0]*16 #Height of the table (16 seeds)

for x in range(len(h)): # adds each seed # in list h
  if(x < 9) :
    h[x] = ("Seed "+str(x+1)+" ")
  else:
    h[x] = ("Seed "+str(x+1))

# Setup for our Score matrix.
# S[Row][Column] to insert
S = [ [0 for j in range(len(w))] for i in range(len(h)) ]

#print (len(S))
#print (len(S[0]))

#Prints our matrix nicely
def printS():
    print(end= "           ") #Gap of space in the beginning
    count = 0
    
    for l in range(int(len(h))): #Prints W, T, or % over each column
      if count == 0:
        print('W |',end="  ")
        count = count +1 
        
      if count == 1:
        print('T |',end="  ")
        count = count + 1
        
      if count == 2:
        print('% |',end="  ")
        count = 0
        
      if l >= len(w):
        break
        
    print()
    for i in range(len(h)):  #prints A seed name and its data
        print(h[i]+'|', end=' ')
        for j in range(len(w)):
          print(end="%3d " % S[i][j] +'|')
        print()


#updates the score matrix when the high seed wins
def recordHSWin(hs,ls):
  S[(int(hs)-1)][((int(ls)-1)*3)]+=1

#updates total games and percentage of a given matchup
def recalcPercent(hs,ls):
  S[int(hs)-1][(((int(ls))-1)*3)+1]+=1 # this adds a game to the total column
  S[int(hs)-1][(int(ls)*3)-1] = 100*(float(S[(int(hs)-1)][((int(ls)-1)*3)])/float(S[int(hs)-1][(((int(ls))-1)*3)+1])) #recalcs win percentage after a game

page = urlopen("http://apps.washingtonpost.com/sports/apps/live-updating-mens-ncaa-basketball-bracket/search/?from=1985&game_type=7&opp_bid_type=&opp_coach=&opp_conference=&opp_power_conference=&opp_school_id=&opp_seed_from=1&opp_seed_to=16&pri_bid_type=&pri_coach=&pri_conference=&pri_power_conference=&pri_school_id=&pri_seed_from=1&pri_seed_to=16&submit=&to=2018")
soup = BeautifulSoup(page, 'html.parser')
tableRows = soup.find("table", {"class": "search-results"}).find("tbody").findAll("tr")


hwins = 0 #high seed wins
lwins = 0 #lowseed wins
twins = 0 #total wins (total games)

champWinScores = []
champLoseScores = []
#Notes: [3:-2] has been changed to [2:-2] after moving from python 2 to 3
for tr in tableRows:
  tds = tr.findAll("td")
  if len(tds)==8:
    if((str(tds[4].contents)[2:-2])!="TBD"):
      highSeed  = str(tds[2].contents)[2:-2]      #highseed #
      lowSeed   = str(tds[5].contents)[2:-2]      #lowseed #
      highScore = int(str(tds[4].contents)[2:-2]) #highseed score
      lowScore  = int(str(tds[7].contents)[2:-2]) #highseed score
      if(int(highSeed)>int(lowSeed)):
        temp = lowSeed
        lowSeed = highSeed
        highSeed = temp
        temp = lowScore
        lowScore = highScore
        highScore = temp
      result =  highScore - lowScore # determine which seed won
      if((str(tds[1].contents)).find("National Championship") != -1):
        if(highScore > lowScore):
          champWinScores.append(highScore)
          champLoseScores.append(lowScore)
        else:
          champLoseScores.append(highScore)
          champWinScores.append(lowScore)
      if highSeed != lowSeed:
        if result > 0: #if high seed won
          recordHSWin(highSeed,lowSeed)
          hwins = hwins + 1
        else: 
          lwins = lwins +1
        recalcPercent(highSeed,lowSeed)
        twins+=1
      else:
        recordHSWin(highSeed, lowSeed)
        recalcPercent(highSeed, lowSeed)
        twins+=1

   
  
printS()
sum = 0
for row in range (len(h)):
  col = 1;
  while(col < 48):
    sum = sum + S[row][col]
    col+=3
print("Highseed wins:"+str(hwins)," Lowseed wins:"+str(lwins), " Same seed games:"+str(twins-hwins-lwins), " Total games:"+str(twins))
print("Does the Score board show all games played?",sum == twins)

print()
print("Winning scores of championships: ",champWinScores)
print("Average winning score: ",mean(champWinScores))
print("Losing scores of championships: ",champLoseScores)
print("Average losing score: ",mean(champLoseScores))
