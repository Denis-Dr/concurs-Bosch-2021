import SerialHandler
import threading
import sys
import imutils
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
exceptieDeInceput = 3 # exceptam primele 3 cadre de la regula de calcul a vectorLatimiMedii pt a obt o latime media reala pe care sa incercam sa o pastram

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

def deseneazaDrum(centreSectiuniCompletat, centreSectiuni, centruRelativ, distantaFataDeAx, nrBenziDetectate, partea, inaltimeSectiuneSus, inaltimeSectiuneJos, vectorCentreMedii):
    cv2.putText(img, "Benzi gasite: " + str(nrBenziDetectate), (10, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (140, 140, 210), 2)

    if centruRelativ != 0:
        cv2.arrowedLine(img, (int(lungimeCadru / 2), 180), (int(centruRelativ), 180), (255, 255, 125), 2)
        cv2.putText(img, "Dist: " + str(distantaFataDeAx), (int(lungimeCadru / 2 + 50), 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 0, 60), 1)
        cv2.line(img, (int(centruRelativ), 0), (int(centruRelativ), inaltimeCadru), (255, 125, 125), 5)

    if vectorCentreMedii[0] != -1 and vectorCentreMedii[1] != -1:
        cv2.circle(img, (vectorCentreMedii[0], inaltimeSectiuneSus), 3, (200, 0, 230), 3)
        cv2.circle(img, (vectorCentreMedii[1], inaltimeSectiuneJos), 3, (200, 0, 230), 3)
        cv2.line(img, (vectorCentreMedii[0], inaltimeSectiuneSus), (vectorCentreMedii[1], inaltimeSectiuneJos), (170, 0, 0), 2)

    if nrBenziDetectate == 2:
        for j in range(2):
            if centreSectiuni[0][j] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[0][j]), (centreSectiuniCompletat[0][j] - 20, inaltimeSectiuneSus - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 210, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[0][j], inaltimeSectiuneSus), 3, (0, 0, 200), 3)
            else:
                cv2.putText(img, str(centreSectiuniCompletat[0][j]), (centreSectiuniCompletat[0][j] - 20, inaltimeSectiuneSus - 8), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 30, 200), 2)
                cv2.circle(img, (centreSectiuniCompletat[0][j], inaltimeSectiuneSus), 3, (200, 0, 0), 3)

        for j in range(2):
            if centreSectiuni[1][j] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[1][j]), (centreSectiuniCompletat[1][j] - 20, inaltimeSectiuneJos - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 210, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[1][j], inaltimeSectiuneJos), 3, (0, 0, 200), 3)
            else:
                cv2.putText(img, str(centreSectiuniCompletat[1][j]), (centreSectiuniCompletat[1][j] - 20, inaltimeSectiuneJos - 8), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 30, 200), 2)
                cv2.circle(img, (centreSectiuniCompletat[1][j], inaltimeSectiuneJos), 3, (200, 0, 0), 3)

    elif nrBenziDetectate == 1:
        if partea == "stanga":
            cv2.putText(img, "Detecteaza banda stanga", (380, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 180), 2)
            print("Detecteaza banda stanga. Pozitia aprox. a benzii dreapta este: ", centreSectiuniCompletat[0][1], "; ", centreSectiuniCompletat[1][1])
            if centreSectiuniCompletat[0][0] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[0][0]), (centreSectiuniCompletat[0][0] - 20, inaltimeSectiuneSus - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[0][0], inaltimeSectiuneSus), 3, (0, 200, 0), 3)

            if centreSectiuniCompletat[1][0] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[1][0]), (centreSectiuniCompletat[1][0] - 20, inaltimeSectiuneJos - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[1][0], inaltimeSectiuneJos), 3, (0, 200, 0), 3)

        elif partea == "dreapta":
            cv2.putText(img, "Detecteaza banda dreapta", (380, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 180), 2)
            print("Detecteaza banda dreapta. Pozitia aprox. a benzii stanga este: ", centreSectiuniCompletat[0][0], "; ", centreSectiuniCompletat[1][0])
            if centreSectiuniCompletat[0][1] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[0][1]), (centreSectiuniCompletat[0][1] - 20, inaltimeSectiuneSus - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[0][1], inaltimeSectiuneSus), 3, (0, 200, 0), 3)

            if centreSectiuniCompletat[1][1] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[1][1]), (centreSectiuniCompletat[1][1] - 20, inaltimeSectiuneJos - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[1][1], inaltimeSectiuneJos), 3, (0, 200, 0), 3)
    else:
        print("Nicio banda detectata!!!")
#########
#########
class TwoLanes:
    def __init__(self):
        pass

    def draw(self, centreSectiuniCompletat, centruRelativ, distantaFataDeAx, nrBenziDetectate):

        for centru in centreSectiuniCompletat:
            cv2.putText(img, str(centru), (int(centru - 20), int(inaltimeCadru * 2.0 / 3)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        self.nrBenzi, self._ = nrBenziDetectate()
        if self.nrBenzi > 1:
            cv2.arrowedLine(img, (int(lungimeCadru / 2), 300), (int(centruRelativ), 300), (255, 255, 125), 2)
            cv2.putText(img, "Dist: " + str(distantaFataDeAx), (int(lungimeCadru / 2 + 50), 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 0, 60), 1)
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
#######
#######
def PutLines():
    inaltimeCadru, lungimeCadru, _ = frame.shape

    cv2.line(img, (int(0.08*lungimeCadru), int(inaltimeCadru * 0.5)), (int(0.47*lungimeCadru), int(inaltimeCadru * 0.5)), (255, 255, 0), 2)
    cv2.line(img, (int(0.53 * lungimeCadru), int(inaltimeCadru * 0.5)), (int(0.92 * lungimeCadru), int(inaltimeCadru * 0.5)), (255, 255, 0), 2)

    cv2.line(img, (0, int(inaltimeCadru * 0.65)), (lungimeCadru, int(inaltimeCadru * 0.65)), (255, 255, 0), 2)

    cv2.line(img, (int(lungimeCadru / 2), 0), (int(lungimeCadru / 2), inaltimeCadru), (255, 255, 255), 2) # linia verticala

    cv2.line(binarization, (int(0.08 * lungimeCadru), int(inaltimeCadru * 0.5)), (int(0.47 * lungimeCadru), int(inaltimeCadru * 0.5)), (255, 255, 0), 2)
    cv2.line(binarization, (int(0.53 * lungimeCadru), int(inaltimeCadru * 0.5)), (int(0.92 * lungimeCadru), int(inaltimeCadru * 0.5)), (255, 255, 0), 2)

    cv2.line(binarization, (0, int(inaltimeCadru * 0.65)), (lungimeCadru, int(inaltimeCadru * 0.65)), (255, 255, 0), 2)
    cv2.line(binarization, (int(lungimeCadru / 2), 0), (int(lungimeCadru / 2), inaltimeCadru), (255, 255, 255), 2)  # linia verticala

def calculLatimeBanda(centreSectiuni):
    vectorLatimiBanda = [-1, -1]
    if centreSectiuni[0][1] != -1 and centreSectiuni[0][0] != -1:
        vectorLatimiBanda[0] = centreSectiuni[0][1] - centreSectiuni[0][0] # latime sus

    if centreSectiuni[1][1] != -1 and centreSectiuni[1][0] != -1:
        vectorLatimiBanda[1] = centreSectiuni[1][1] - centreSectiuni[1][0]
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
contorDistMedBenzi = 0 # calculam distanda medie intre benzi in primele 3 cadre ale videoului

while (cap.isOpened()):
    t1 = time.time()
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
    ret, binarization = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    inaltimeCadru, lungimeCadru, _ = frame.shape # H si L imagine
    MijlocCamera = int(lungimeCadru / 2.0)

    Sectiune = Banda() #initializare benzi.py

    inaltimeSectiuneSus = Sectiune.setInaltimeSectiuneSus(int (inaltimeCadru * 0.5))
    inaltimeSectiuneJos = Sectiune.setInaltimeSectiuneJos(int (inaltimeCadru * 0.65))

    centreSectiuni = Sectiune.calculCentreSectiuni(binarization, lungimeCadru)

#########################################################################################
####### calc lat medie banda la fiecare 3 cadre cu detectare ############################
#########################################################################################

    if contorDistMedBenzi < 3: # CALCUL LATIME MEDIE BANDA DUPA 3 CADRE CU BANDA DETECTATA

        vectorLatimiBanda = calculLatimeBanda(centreSectiuni) # calcul latimi banda

        if ((exceptieDeInceput > 0 or ((vectorLatimiMedii[0]-20 < vectorLatimiBanda[0] < vectorLatimiMedii[0]+20) and
                    vectorLatimiMedii[1]-20 < vectorLatimiBanda[1] < vectorLatimiMedii[1]+20)) and (vectorLatimiBanda[0] != -1 and vectorLatimiBanda[1] != -1)):

            latimeSus = np.append( latimeSus, vectorLatimiBanda[0])
            latimeJos = np.append( latimeJos, vectorLatimiBanda[1])
            contorDistMedBenzi += 1
            if exceptieDeInceput > 0:
                exceptieDeInceput -= 1
    else:
        contorDistMedBenzi = 0
        vectorLatimiMedii[0] = int(np.average(latimeSus))
        vectorLatimiMedii[1] = int(np.average(latimeJos))
        print("--> latimea medie a benzii este : " + str(vectorLatimiMedii))
        latimeSus = np.zeros(0)
        latimeJos = np.zeros(0)
    print("### vectorLatimiMedii ", vectorLatimiMedii)
########################################################################################
########################################################################################

    centreSectiuniCompletat = completareCentre(centreSectiuni, vectorLatimiMedii)
    vectorCentreMedii = Sectiune.calculCentreMedii( centreSectiuniCompletat)
    print("### vectorCentreMedii ", vectorCentreMedii)
    centruRelativ = Sectiune.calculCentruRelativ( vectorCentreMedii)
    distantaFataDeAx = Sectiune.calculDistantaFataDeAx( centruRelativ, MijlocCamera)

    nrBenziDetectate, partea = Sectiune.nrBenziDetectate()

    fps = cap.get(cv2.CAP_PROP_FPS)


    if not ESTE_PE_MASINA:
        cv2.putText(img, "FPS: " + str(fps), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 2)
    else:
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    if not ESTE_PE_MASINA:
        PutLines()

    #try:
    #    del ObiectDrum
    #except:
    #    pass

    try:
        del ObiectBanda
    except:
        pass

   # nrBenziDetectate, _ = Sectiune.nrBenziDetectate()
  #  if nrBenziDetectate == 2:
 #       ObiectDrum = TwoLanes()
    #    ObiectDrum.draw(centreSectiuniCompletat, centruRelativ, distantaFataDeAx, nrBenziDetectate)
    #elif nrBenziDetectate == 1:
    #    ObiectBanda = OneLane(Sectiune)
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

    deseneazaDrum(centreSectiuniCompletat, centreSectiuni, centruRelativ, distantaFataDeAx, nrBenziDetectate, partea,
                  inaltimeSectiuneSus, inaltimeSectiuneJos, vectorCentreMedii)
#DA EROARE AICI:
    #nrBenziDetectate, _ = Sectiune.nrBenziDetectate()
    #if nrBenziDetectate == 2:
    #    ObiectDrum.draw()
   # elif nrBenziDetectate == 1:
   #     ObiectBanda.draw()

    if (not ESTE_PE_MASINA) :
        cv2.putText(img, "Stare: " + str(masina.current_state.value), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (250, 250, 250), 2)
    else :
        print(masina.current_state.value)

    t2 = time.time() - t1
    print("timp executie", t2, "s")

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