import SerialHandler
import threading
import sys

import time
import cv2
import numpy as np
from benzi import Banda
from Observer import DeplasareMasina
from StopAndPark import stopOrPark


global serialHandler
DEBUG_ALL_DATA = False
ESTE_PE_MASINA = False
VIDEO_RECORD = False
AMPARCAT=False

## VARIABILE
cap = cv2.VideoCapture('cameraE.avi')
latimeSus = np.zeros(0)
latimeJos = np.zeros(0)
vectorLatimiMedii=np.array([-1, -1])
distantaFataDeAx = 0
centruRelativ = 0


#CentruImaginar = 0
EroareCentrare = 30
#DistanteBenzi = np.zeros(0)
#mijlocCalculat=0
pasAdaptare = 0
pozitieMijlocAnterior = -1
counter = 0
masina = DeplasareMasina()
## END OF VARIABLE



if VIDEO_RECORD:
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('cameraJ.avi', fourcc, 20,(640, 480))



class Indicator:
    STOP = 1
    PARCARE = 2
    Eroare = 3


class TwoLanes:
    def __init__(self, Sectiune):
        self.Sectiune = Sectiune
        self.MedDistanta=0
    def draw(self):
        global DiferentaFataDeMijloc

        for centru in self.Sectiune.centreSectiuniCompletat:
            cv2.putText(img, str(centru), (int(centru - 20), int(inaltimeCadru * 2.0 / 3)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        self.nrBenzi, self_ = self.Sectiune.nrBenziDetectate()
        if self.nrBenzi > 1:
            cv2.arrowedLine(img, (int(lungimeCadru / 2), 300), (int(centruRelativ), 300), (255, 255, 125), 2)
            cv2.putText(img, "Dist: " + str(distantaFataDeAx), (int(lungimeCadru / 2 + 50), 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 0, 60), 1)
            cv2.line(img, (int(centruRelativ), 0), (int(centruRelativ), inaltimeCadru), (255, 125, 125), 5)



class OneLane:
    def __init__(self, Sectiune):
        self.Sectiune = Sectiune
        self.CentruImaginar = 0
        self.Referinta = 0
        global MedDistanta
        if 'MedDistanta' not in globals():
            MedDistanta=350

        #if self.Sectiune.centre.size == 1:  # cazul in care nu ai 2 benzi
        self.nrBenzi, self.partea = Sectiune.nrBenziDetectate()
        if self.nrBenzi == 1:
            if self.partea == "stanga":
                #self.Referinta = self.Sectiune.centre[0]
                #self.CentruImaginar = self.Referinta + (MedDistanta / 2)

                print("Avem o banda pe stanga")
                #print("Nu exista banda pe partea dreapta, pozitia ei aproximata este " + str(self.CentruImaginar))
                #cv2.putText(img, "Pozitie Relativa Mijloc Imaginar: " + str(self.CentruImaginar), (10, 420),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            else:
                #self.Referinta = self.Sectiune.centre[0]
                #self.CentruImaginar = self.Referinta - (MedDistanta / 2)
                print("Avem o banda pe dreapta")
                #print("Nu exista banda pe partea stanga, pozitia ei aproximata este " + str(self.CentruImaginar))
                #cv2.putText(img, "Pozitie Relativa Mijloc Imaginar: " + str(self.CentruImaginar), (10, 420),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        #for centru in self.Sectiune.centre:
            #    cv2.putText(img, str(centru), (int(centru - 20), int(LatimeCadru * 2.0 / 3)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def draw(self):
        global MijlocCamera
        if self.Sectiune.nrBenziDetectate == 1:  # cazul in care nu ai 2 benzi
            cv2.line(img, (int(centruRelativ), 0), (int(centruRelativ), inaltimeCadru), (125, 125, 0), 5)
            cv2.arrowedLine(img, (int(lungimeCadru / 2), 300), (int(centruRelativ), 300), (255, 255, 125), 2)
            cv2.putText(img, "Avem Mijloc Imaginar", (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(img, "Dist: " + str(abs(int(MijlocCamera - centruRelativ))), (int(lungimeCadru / 2 + 50), 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 0, 60), 1)

def PutLines():
    inaltimeCadru, lungimeCadru, _ = frame.shape
    cv2.line(img, (int(0.1*lungimeCadru), int(inaltimeCadru * 1.0 / 2)), (int(0.9*lungimeCadru), int(inaltimeCadru * 1.0 / 2)), (255, 255, 0), 2)
    cv2.line(img, (0, int(inaltimeCadru * 0.65)), (lungimeCadru, int(inaltimeCadru * 0.65)), (255, 255, 0), 2)
    cv2.line(img, (int(lungimeCadru / 2), 0), (int(lungimeCadru / 2), inaltimeCadru), (255, 255, 255), 2) # linia verticala

def calculLatimeBanda(centreSectiuni):
    vectorLatimiBanda = [-1, -1]
    if centreSectiuni[0][1] != -1 and centreSectiuni[0][0] != -1:
        vectorLatimiBanda[0] = int(centreSectiuni[0][1] - centreSectiuni[0][0]) # latime sus
    if centreSectiuni[1][1] != -1 and centreSectiuni[1][0] != -1:
        vectorLatimiBanda[1] = int(centreSectiuni[1][1] - centreSectiuni[1][0])
    print("### vectorLatimiBanda", vectorLatimiBanda)
    return vectorLatimiBanda

def completareCentre(centreSectiuni, vectorLatimiMedii): # completeaza centrele nedetectate din matricea centrelor cu ajutorul vectorLatimiBanda
    centreSectiuniCompletat = np.copy(centreSectiuni)

    if centreSectiuni[0][0] == -1 and centreSectiuni[0][1] != -1: # completare sectiuni sus
        centreSectiuniCompletat[0][0] = centreSectiuni[0][1] - vectorLatimiMedii[0]
        centreSectiuniCompletat[0][1] = centreSectiuni[0][1]
    elif centreSectiuni[0][0] != -1 and centreSectiuni[0][1] == -1:
        centreSectiuniCompletat[0][0] = centreSectiuni[0][0]
        centreSectiuniCompletat[0][1] = centreSectiuni[0][0] + vectorLatimiMedii[0]

    if centreSectiuni[1][0] == -1 and centreSectiuni[1][1] != -1:
        centreSectiuniCompletat[1][0] = centreSectiuni[1][1] - vectorLatimiMedii[1]
        centreSectiuniCompletat[1][1] = centreSectiuni[1][1]
    elif centreSectiuni[1][0] != -1 and centreSectiuni[1][1] == -1:
        centreSectiuniCompletat[1][0] = centreSectiuni[1][0]
        centreSectiuniCompletat[1][1] = centreSectiuni[1][0] + vectorLatimiMedii[1]
    print("### centreSectiuniCompletat ", centreSectiuniCompletat)
    return centreSectiuniCompletat





counterStop=0
contorDistMedBenzi = 0 # calculam distanda medie intre benzi in primele 3 cade ale videoului

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        break
    img = frame

    EsteStop, EsteParcare = stopOrPark(frame, AMPARCAT)

    counter = counter + 1
    if counter < 5 :
        continue
    if VIDEO_RECORD:
        out.write(frame)
    if not ESTE_PE_MASINA:
        cv2.putText(img, "Cadrul: " + str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (250, 250, 250), 2)

    print("\n ----------- FRAME ", counter, " --------------")

    if EsteStop :
        print("avem stop")
        print(str(masina.current_state))
        if (masina.current_state == masina.initializare) :  # verific ca sunt in starea initiala
            counterStop = counterStop + 1
            masina.stoptodo()
            CounterFolositPentruAMasuraStarea = 1
        else :
            print("dar nu sunt in starea de mers")
    if EsteParcare:
        print("avem parcare")
        if (masina.current_state == masina.initializare) :  # verific ca sunt in starea initial
                AMPARCAT = True
                masina.Parcheaza()
                CounterFolositPentruAMasuraStarea = 1
        else :
            print("dar nu sunt in starea de mers")



    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binarization = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

    inaltimeCadru, lungimeCadru, _ = frame.shape # H si L imagine
    MijlocCamera = int(lungimeCadru / 2.0)

    Sectiune = Banda() #initializare benzi.py

    Sectiune.setInaltimeSectiuneSus(int (inaltimeCadru * 1.0 / 2))
    Sectiune.setInaltimeSectiuneJos(int (inaltimeCadru * 0.65))

    centreSectiuni = Sectiune.calculCentreSectiuni(binarization, lungimeCadru)

################################################################################################
####### calc lat medie banda la fiecare 3 cadre cu detectare ################################################
################################################################################################

    if contorDistMedBenzi < 3: # CALCUL LATIME MEDIE BANDA DUPA 3 CADRE CU BANDA DETECTATA

        vectorLatimiBanda = calculLatimeBanda(centreSectiuni) # calcul latimi banda
        if vectorLatimiBanda[0] != -1 and vectorLatimiBanda[1] != -1:
            latimeSus = np.append( latimeSus, vectorLatimiBanda[0])
            latimeJos = np.append( latimeJos, vectorLatimiBanda[1])
            contorDistMedBenzi += 1
    else:
        contorDistMedBenzi = 0
        vectorLatimiMedii[0] = int(np.average(latimeSus))
        vectorLatimiMedii[1] = int(np.average(latimeJos))
        print("--> latimea medie a benzii este : " + str(vectorLatimiMedii))
        latimeSus = np.zeros(0)
        latimeJos = np.zeros(0)
    print("### vectorLatimiMedii ", vectorLatimiMedii)
#################################################################################################
#################################################################################################

    centreSectiuniCompletat = completareCentre(centreSectiuni, vectorLatimiMedii)
    vectorCentreMedii = Sectiune.calculCentreMedii(centreSectiuniCompletat)
    centruRelativ = Sectiune.calculCentruRelativ()
    distantaFataDeAx = Sectiune.calculDistantaFataDeAx( MijlocCamera)



    fps = cap.get(cv2.CAP_PROP_FPS)


    if not ESTE_PE_MASINA:
        cv2.putText(img, "FPS: " + str(fps), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 2)
    else:
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    if not ESTE_PE_MASINA:
        PutLines()

    try:
        del ObiectDrum
    except:
        pass

    try:
        del ObiectBanda
    except:
        pass

    nrBenziDetectate, _ = Sectiune.nrBenziDetectate()
    if nrBenziDetectate == 2:
        ObiectDrum = TwoLanes(Sectiune)
    elif nrBenziDetectate == 1:
        ObiectBanda = OneLane(Sectiune)
    else:
        print("Nicio banda detectata!")

    if DEBUG_ALL_DATA and ESTE_PE_MASINA:
        print("Benzi gasite:" + str(Sectiune.nrBenziDetectate()))
        print("\nCentre:\t" + str(Sectiune.centreSectiuni))
    else:
        cv2.putText(img, "Benzi identificate: "+ str(Sectiune.nrBenziDetectate()), (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    #if mijlocCalculat is  None:
    #    continue

    #if 'ObiectDrum' in locals() :
    #    MedDistanta = ObiectDrum.CalculMedDist()
    #    MijlocGeneric = ObiectDrum.mijlocCalculat
    #else:
    #    MijlocGeneric = ObiectBanda.CentruImaginar



    try:

        DiferentaFataDeMijloc = Sectiune.distantaFataDeAx
        if  DiferentaFataDeMijloc > EroareCentrare:
            pasAdaptare = pasAdaptare - 2
            if (pasAdaptare<(-22)):
                pasAdaptare=-20
            if ESTE_PE_MASINA:
                serialHandler.sendMove(0.20, pasAdaptare)
                print("<<<<")
                print("Unghi Adaptat pentru stanga: " + str(pasAdaptare))
            else:
                cv2.putText(img, "O luam la stanga", (10, 380),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        else:
            if -EroareCentrare < DiferentaFataDeMijloc < EroareCentrare:
                if ESTE_PE_MASINA:
                    serialHandler.sendMove(0.20, 0.0)
                    print("suntem pe centru")
                pasAdaptare = 0
            else:
                if ESTE_PE_MASINA:
                    serialHandler.sendMove(0.20, 2.0 + pasAdaptare)
                    print(">>>>>>")
                    print("Unghi Adaptat pentru dreapta:\t" + str(pasAdaptare))
                else:
                    cv2.putText(img, "O luam la dreapta", (10, 380),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                pasAdaptare = pasAdaptare + 5
                if (pasAdaptare > (22)):
                    pasAdaptare = 20

    except Exception as e:
        print(e)
        pass
#DA EROARE AICI:
   # nrBenziDetectate, _ = Sectiune.nrBenziDetectate()
   # if nrBenziDetectate == 2:
     #   ObiectDrum.draw()
   # elif nrBenziDetectate == 1:
   #     ObiectBanda.draw()

    if (not ESTE_PE_MASINA) :
        cv2.putText(img, "Stare: " + str(masina.current_state.value), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (250, 250, 250), 2)
    else :
        print(masina.current_state.value)

    if (not ESTE_PE_MASINA) :
        cv2.imshow("Image", img)
        cv2.imshow("binarizare", binarization)
        cv2.waitKey(0)  # 1=readare automata // 0=redare la buton
        time.sleep(0.0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #if stopOrPark(img, False) == 1:
    #    print("STOP")
    #    serialHandler.sendBrake(0)
if ESTE_PE_MASINA:
    serialHandler.sendPidActivation(False)
    serialHandler.close()

cap.release()
cv2.destroyAllWindows()