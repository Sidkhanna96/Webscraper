import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from UFC_Webscraping import showTable
import matplotlib.style as style

def totalPPVBuys(c, numOfFighterToShow, startPoint):
    c.execute('''SELECT fighterName, SUM(ppvBuys)
    FROM fighterPPVBuys
    GROUP BY fighterName
    ORDER BY SUM(ppvBuys) DESC
    LIMIT ? OFFSET ?''', (numOfFighterToShow, startPoint))

def avgPPVBuys(c, numOfFighterToShow, startPoint):
    c.execute('''SELECT fighterName, AVG(ppvBuys)
    FROM fighterPPVBuys
    GROUP BY fighterName
    HAVING COUNT(fighterName) > 1
    ORDER BY AVG(ppvBuys) DESC
    LIMIT ? OFFSET ?''', (numOfFighterToShow, startPoint))


def main():
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#909090'
    plt.rcParams['axes.labelcolor']= '#909090'
    plt.rcParams['xtick.color'] = '#909090'
    plt.rcParams['ytick.color'] = '#909090'
    plt.rcParams['font.size']=8
    
    conn = sqlite3.connect('fighterPPV.db')
    c = conn.cursor()
    startPoint = 0
    numOfFighterToShow = 20

    if 'avg' in sys.argv:
        avgPPVBuys(c, numOfFighterToShow, startPoint)
    else:
        totalPPVBuys(c, numOfFighterToShow, startPoint)
    # numOfFighterToShow = input("Enter total number of fighters to show: ")
    fighterAndPpv = c.fetchall()
    fighter = []
    ppvBuys = []
    for elem in fighterAndPpv:
        fighter.append(elem[0])
        ppvBuys.append(elem[1])
    
    y_pos = np.arange(len(fighter))
    fighterList = []
    for eachFighter in fighter:
        fighterList.append(eachFighter.replace(' ', '\n'))
    
    plt.bar(y_pos, ppvBuys)
    plt.xticks(y_pos, fighterList)
    plt.xticks(rotation=70)

    plt.show()

if __name__ == "__main__":
    main()