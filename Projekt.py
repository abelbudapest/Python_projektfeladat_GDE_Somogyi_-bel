import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt2 
import csv 
import operator
import numpy as np
from matplotlib.widgets import Slider
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import ttk, Tk, mainloop, TOP



def KettősVonaldiagramÉsLinRegresszió(fájl1, fájl2):

    fig, ax = plt.subplots()
    # a grafikon alsó vonalának beállítása az ábrán belül
    plt.subplots_adjust(bottom=0.25)

    # Tengelyek definiálása. 
    x = [] 
    y = []
    x2=[]
    y2=[]
    # ebből pedig a regresszió tesztelésekor a felugró ablakból lehet majd a települések adatait válogatni
    dataTuples=[]


    # a csv olvasót célszerű try blokkban megnyitni
    try:
        #https://www.geeksforgeeks.org/visualize-data-from-csv-file-in-python/ kódhoz felhasznált forrás
        
        with open(fájl1,'r', encoding='utf-8') as csvfile: 
            lines = csv.reader(csvfile, delimiter=';')

            #https://www.geeksforgeeks.org/how-to-sort-data-by-column-in-a-csv-file-in-python/ kódhoz felhasznált forrás
    
            lines = sorted(lines, key=operator.itemgetter(6))
            lines=lines[:-1]



            for li in lines:
                try:
                    # szükséges átváltás int-be
                    converted=int(li[6])
                    del li[6]
                    li[6]=converted
                except:
                    continue
            

            
            lines = sorted(lines, key=operator.itemgetter(6))

            # Azért kellett kétszer a sorted-dal sorba rendezni, mert az első után vált lehetségessé a stringes 
            # címsor törlése, minthogy akkor rakta utolsó helyre.
            
            for row in lines:

                try: 
                    # Az x2-n a települések sorrendje igazodni fog az x szerintihez, hiszen ugyanakkor "töltjük" fel.
                        x.append(row[1])
                        x2.append(row[0])
                        y.append(row[6])
                        dataTuples.append((row[1], row[0], row[6]))
                        
                except Exception as e1: print(f"e1: {e1}"); continue      
        
        # a vonaldiagram beállításai, külön try-ban
        try:
            plt.plot(x, y, color = 'g', linestyle = 'dashed', 
                    marker = 'o',label = "Lakásállomány ezer lakosra 2020-ban")
        
            plt.xticks(rotation = 25) 
            plt.xlabel('Település nevek') 
            plt.ylabel('Lakásállomány ezer lakosra') 

            plt.title('Lakásállomány ezer lakosra / Éves vízfogyasztás egy főre (2020)', fontsize = 20) 
            plt.axis([0, 20, 0, 3500])
            plt.legend()
        except Exception as e2: print(f"e2: {e2}")

    except Exception as e3: print(f"e3: {e3}")



    #https://stackoverflow.com/questions/31001713/plotting-the-data-with-scrollable-x-time-horizontal-axis-on-linux 
    # kódhoz felhasznált forrás
    # A csúsztatható szalag beállítása:

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor=axcolor)

    spos = Slider(axpos, 'Pozíció', 1, 3130.0)

    def update(val):
        pos = spos.val
        ax.axis([pos,pos+30,0,3500])
        fig.canvas.draw_idle()

    spos.on_changed(update)





    lilista=[] # ebbe lesznek kigyűjtve a másik csv sorai

    # a csv olvasót célszerű try blokkban megnyitni
    try:
        
        with open(fájl2,'r', encoding='utf-8') as csvfile: 
                    lines2 = csv.reader(csvfile, delimiter=';')

                    lilista=list(lines2)

        for element in x2:
            #(az x2 element[6]-jai között már nincs a csv címsorábol származó nemkívánatos str, a 31. sor miatt)
            # ez a beágyazott for ciklus olyan sorba rendezést végez, 
            # amely által az y2-beli értékek megfelelnek az x tengelyen
            # a települések sorrendjének, így mindkét értékábrázolás megfelelő lesz
            try:
                for line in lilista:
                        if line[0] == element:              
                            # szükséges átváltás int-be
                            u=int(line[6])
                            del line[6]
                            line[6]=u
                            y2.append(line[6])
                        else:
                            continue
                        

            except:
                continue
                

        try:
            # az y2 tengely beállításai

            ax2 = ax.twinx()
            ax2.plot(y2, color = 'b', linestyle = 'dashed', 
            marker = 'o')
            ax2.tick_params(axis='y', labelcolor='b')
            ax2.set_ylabel('Éves vízfogyasztás egy főre')
        except Exception as e4: print(f"ef: {e4}")

    except Exception as e5: print(f"e5: {e5}")
        
    try:
        plt.show()
    except Exception as e6: print(f"e6: {e6}")

    # lineáris regresszió ábrázolás >>
    # https://stackoverflow.com/questions/6148207/linear-regression-with-matplotlib-numpy#6148315 kódhoz felhasznált forrás

    try:
        x_linear_regres = y
        y_linear_regres=y2

        coef = np.polyfit(x_linear_regres,y_linear_regres,1)
        poly1d_fn = np.poly1d(coef) 
        

        plt2.plot(x_linear_regres,y_linear_regres, 'bo', x_linear_regres, poly1d_fn(x_linear_regres), '--k')
        plt2.xlabel('Lakásállomány ezer lakosra')
        plt2.ylabel('Éves vízfogyasztás egy főre')
        plt2.title('Lakásállomány ezer lakosra / Éves vízfogyasztás egy főre (2020)')
        plt2.show()
    except Exception as e7: print(f"e7: {e7}")

    # Most jön a scikit-learn használata lineáris regresszió számításokhoz

    try:

        x_linear_regresNdarray=np.array(x_linear_regres).reshape(-1,1)
        y_linear_regresNdarray=np.array(y_linear_regres)
        
        model = LinearRegression().fit(x_linear_regresNdarray, y_linear_regresNdarray)

        r_sq = model.score(x_linear_regresNdarray, y_linear_regres)
        print(f"Determinációs együttható: {r_sq}")
        print(f"Intercept: {model.intercept_}")
        print(f"Meredekség: {model.coef_}")

        for ii in range(4):
            # itt feljön egy ablak, amelyből könnyen ki lehet egy településre vonatkozó lakás adatot választani,
            # vagy helyette megadhatunk újat, amelyre a program prognózist ad
            tkinterAblak(dataTuples)
            Num=int(input("Add meg a számításhoz használandó lakásállomány számadatot: "))
            egyikTupleLista=[item for item in dataTuples if item[2] == Num]
            
            if len(egyikTupleLista) == 1:
                tenylegEgyikTuple=egyikTupleLista[0]
                indexIn_x2=dataTuples.index(tenylegEgyikTuple)
                y_pred = model.predict( x_linear_regresNdarray[[indexIn_x2]])
                print(f"A település neve és indexe: {tenylegEgyikTuple[0]}, {tenylegEgyikTuple[1]}")
                print(f"Előrejelzett érték: {y_pred}")
                print(f"Valódi érték: {y2[indexIn_x2]}.")

            elif len(egyikTupleLista) > 1:
                 # ez az elif azt kezeli le, amikor több településhez tartozik a megadottal azonos érték
                 print("""Több település szerepel ugyanezzel az adattal, válassza ki a lekérdezendőnek
                       az indexét.""")
                 for val in range(0,len(egyikTupleLista)):
                      print(f"{egyikTupleLista[val][0]} index: [{val}]")
                 valasztas=int(input("Választott index: "))
                 tenylegEgyikTuple=egyikTupleLista[valasztas]
                 indexIn_x2=dataTuples.index(tenylegEgyikTuple)
                 y_pred = model.predict( x_linear_regresNdarray[[indexIn_x2]])
                 print(f"A település neve és indexe: {tenylegEgyikTuple[0]}, {tenylegEgyikTuple[1]}")
                 print(f"Előrejelzett érték: {y_pred}")
                 print(f"Valódi érték: {y2[indexIn_x2]}.")

            else:
                toArr=[]
                toArr.append(Num)
                newNdarray=np.array(toArr).reshape(-1,1)       
                y_pred = model.predict(newNdarray[[0]])
                print(f"""Ilyen lakásszám-adattal település egyelőre nem létezik, de 
                kiszámoltuk az erre az x-re vonatkozó előrejelzett értéket: {y_pred}""")

    except Exception as e8: print(e8)
    

     




def tkinterAblak(listOfTuples):
        #https://www.pythontutorial.net/tkinter/tkinter-scrollbar/ kódhoz felhasznált forrás
        root = tk.Tk()
        root.resizable(True, True)
        root.title("Jegyezze meg egy település lakás változóját (2. szám) és zárja be!")
        root.geometry("") 



        # apply the grid layout
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # create the text widget
        text = tk.Text(root, height=40)
        text.grid(row=0, column=0, sticky=tk.EW)

        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(root, orient='vertical', command=text.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        #  communicate back to the scrollbar
        text['yscrollcommand'] = scrollbar.set

        position = f'1.0'
        for dt in listOfTuples:
             text.insert(position, dt)
             text.insert(position,"                  ")
        text.insert(position,f'Település        Index       Lakásállomány')

        root.mainloop()



# A funkció hívása:
KettősVonaldiagramÉsLinRegresszió('Lakásállomány ezer lakosra_2020_telepules.csv', 'Egy lakosra jutó éves vízfogyasztás_2020.csv')
