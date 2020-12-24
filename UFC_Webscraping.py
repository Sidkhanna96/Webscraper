import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import webbrowser
import sys
import sqlite3
import time

def getHtmlData(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def openBrowser(ppvTable, isEditor=False):
    if isEditor:
        path = os.path.abspath('temp.txt')
    else:
        path = os.path.abspath('temp.html')
    url = 'file://' + path
    with open(path, 'w') as htmlContent:
        htmlContent.write(ppvTable)
    webbrowser.open(url, new=2)

def checkArg(ppvTable, c):
    for elem in sys.argv:
        if '-ob' == elem:
            openBrowser(str(ppvTable))
        if '-of' == elem:
            openBrowser(str(ppvTable), True)
        if '-st' == elem:
            showTable(c)

def showTable(c):
    rows = c.fetchall()
    for rows in rows:
        print(rows)

def createFighterDatabase(listFight, ppvBuys, c):
    for fighter in listFight:
        c.execute('''INSERT INTO fighterPPVBuys(fighterName, ppvBuys) VALUES(?, ?)''', (fighter, ppvBuys))

def getFighters(ppvTable, c):
    specificPPVLink = ''
    ppvBuys = 0
    currentPPVBuys = 0
    
    for tableRow in ppvTable.findAll('tr'):
        tableHead = tableRow.findAll('th')
        if not tableHead:
            tableArray = tableRow.findAll('td')
            if len(tableArray) > 0:
                specificPPVLink = "https://www.tapology.com" + tableArray[0].findAll('a')[0]['href']
                ppvBuys = int(tableArray[6].contents[0].replace('\n','').replace(',',''))
            fighterNames = (getHtmlData(specificPPVLink).findAll('ul')[6].find('li').find('div').findAll('div'))
            fightWinner = fighterNames[4].find('a').string
            fightLoser = fighterNames[11].find('a').string
            listFight = []
            listFight.append(fightLoser)
            listFight.append(fightWinner)
            createFighterDatabase(listFight, ppvBuys, c)
        showTable(c)
        time.sleep(3)

def createDataBaseFighter(c):
    c.execute('DROP TABLE IF EXISTS fighterPPVBuys')
    c.execute('CREATE TABLE fighterPPVBuys(id integer PRIMARY KEY AUTOINCREMENT,fighterName text, ppvBuys integer)')

def main():
    conn = sqlite3.connect('fighterPPV.db')
    c = conn.cursor()
    
    createDataBaseFighter(c)

    siteHtml = getHtmlData('https://www.tapology.com/search/mma-event-figures/ppv-pay-per-view-buys-buyrate')
    ppvTable = siteHtml.find('table')
    getFighters(ppvTable, c)

    conn.commit()
    checkArg(ppvTable, c)
    conn.close()
            

if __name__ == "__main__":
    start_time =time.time()
    main()
    print("Time = ", (time.time()-start_time)/60 + " mins")


