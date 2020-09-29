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
from PIL import ImageGrab
from flask_opencv_streamer.streamer import Streamer


port = 3030
require_login = False
streamer = Streamer(port, require_login)


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
exceptieDeInceput0 = 3 # exceptam primele 3 cadre de la regula de calcul a vectorLatimiMedii pt a obt o latime media reala pe care sa incercam sa o pastram
exceptieDeInceput1 = 3



EroareCentrare = 30


pasAdaptare = 0
pozitieMijlocAnterior = -1
counter = 0
masina = DeplasareMasina()
## END OF VARIABLE



if VIDEO_RECORD:
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('cameraE.avi', fourcc, 20,(640, 480))



class Indicator:
    STOP = 1
    PARCARE = 2
    Eroare = 3

def deseneazaDrum(centreSectiuniCompletat, centreSectiuni, centruRelativ, distantaFataDeAx, nrBenziDetectate, partea, inaltimeSectiuneSus, inaltimeSectiuneJos, vectorCentreMedii, intersectie):
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
            cv2.putText(img, "Detecteaza banda stanga", (380, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 190), 2)
            print("Detecteaza banda stanga. Pozitia aprox. a benzii dreapta este: ", centreSectiuniCompletat[0][1], "; ", centreSectiuniCompletat[1][1])
            if centreSectiuniCompletat[0][0] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[0][0]), (centreSectiuniCompletat[0][0] - 20, inaltimeSectiuneSus - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[0][0], inaltimeSectiuneSus), 3, (0, 200, 0), 3)

            if centreSectiuniCompletat[1][0] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[1][0]), (centreSectiuniCompletat[1][0] - 20, inaltimeSectiuneJos - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[1][0], inaltimeSectiuneJos), 3, (0, 200, 0), 3)

        elif partea == "dreapta":
            cv2.putText(img, "Detecteaza banda dreapta", (380, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 190), 2)
            print("Detecteaza banda dreapta. Pozitia aprox. a benzii stanga este: ", centreSectiuniCompletat[0][0], "; ", centreSectiuniCompletat[1][0])
            if centreSectiuniCompletat[0][1] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[0][1]), (centreSectiuniCompletat[0][1] - 20, inaltimeSectiuneSus - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[0][1], inaltimeSectiuneSus), 3, (0, 200, 0), 3)

            if centreSectiuniCompletat[1][1] != -1:
                cv2.putText(img, str(centreSectiuniCompletat[1][1]), (centreSectiuniCompletat[1][1] - 20, inaltimeSectiuneJos - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 30, 0), 2)
                cv2.circle(img, (centreSectiuniCompletat[1][1], inaltimeSectiuneJos), 3, (0, 200, 0), 3)
    else:
        print("Nicio banda detectata!!!")

    if intersectie == 1:
        cv2.putText(img, "URMEAZA INTERSECTIE", (360, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 90, 255), 2)



def PutLines():
    inaltimeCadru, lungimeCadru, _ = frame.shape

    cv2.line(img, (int(0.02 * lungimeCadru), int(inaltimeCadru * 0.5)), (int(0.46*lungimeCadru), int(inaltimeCadru * 0.5)), (255, 255, 0), 2)
    cv2.line(img, (int(0.54 * lungimeCadru), inaltimeSectiuneSus), (int(0.98 * lungimeCadru), inaltimeSectiuneSus), (255, 255, 0), 2)

    cv2.line(img, (0, inaltimeSectiuneJos), (lungimeCadru, inaltimeSectiuneJos), (255, 255, 0), 2)

    cv2.line(img, (int(lungimeCadru / 2), 0), (int(lungimeCadru / 2), inaltimeCadru), (255, 255, 255), 2) # linia verticala

    cv2.line(binarization, (int(0.02 * lungimeCadru), inaltimeSectiuneSus), (int(0.46 * lungimeCadru), inaltimeSectiuneSus), (255, 255, 0), 2)
    cv2.line(binarization, (int(0.54 * lungimeCadru), inaltimeSectiuneSus), (int(0.98 * lungimeCadru), inaltimeSectiuneSus), (255, 255, 0), 2)

    cv2.line(binarization, (0, inaltimeSectiuneJos), (lungimeCadru, inaltimeSectiuneJos), (255, 255, 0), 2)
    cv2.line(binarization, (int(lungimeCadru / 2), 0), (int(lungimeCadru / 2), inaltimeCadru), (255, 255, 255), 2)  # linia verticala

    cv2.line(img, (int(0.33*lungimeCadru), inaltimeSectiuneSus), (int(0.33*lungimeCadru), inaltimeSectiuneJos), (255, 0, 255), 2)
    cv2.line(img, (int(0.5 * lungimeCadru), inaltimeSectiuneSus), (int(0.5 * lungimeCadru), inaltimeSectiuneJos), (255, 0, 255), 2)
    cv2.line(img, (int(0.67 * lungimeCadru), inaltimeSectiuneSus), (int(0.67 * lungimeCadru), inaltimeSectiuneJos), (255, 0, 255), 2)





counterStop=0
contorDistMedBenzi0 = 0 # calculam distanda medie intre benzi in primele 3 cadre ale videoului
contorDistMedBenzi1 = 0

while True: #(cap.isOpened()):
    t1 = time.time()
    ret, frame = cap.read()
    if ret is False:
        break
    '''
    frame = np.array(ImageGrab.grab(bbox=(0, 40, 640, 480)))

    img = frame
    '''
    points1 = np.float32([[100, 200], [540, 200], [0, 290], [640, 290]])
    points2 = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
    P = cv2.getPerspectiveTransform(points1, points2)
    output = cv2.warpPerspective(frame, P, (640, 480))
    img = output

    EsteStop, EsteParcare = stopOrPark(frame, AMPARCAT)

    counter = counter + 1
    if counter < 5 :
        continue
    if VIDEO_RECORD:
        out.write(frame)
    if not ESTE_PE_MASINA:
        cv2.putText(img, "Cadrul: " + str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                   (200, 255, 200), 2)

    print("\n ----------- FRAME ", counter, " --------------")
    '''
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
    '''


    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    ret, binarization = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    inaltimeCadru, lungimeCadru, _ = frame.shape # H si L imagine
    MijlocCamera = int(lungimeCadru / 2.0)

    Sectiune = Banda() #initializare benzi.py

    inaltimeSectiuneSus = Sectiune.setInaltimeSectiuneSus(int (inaltimeCadru * 0.5))
    inaltimeSectiuneJos = Sectiune.setInaltimeSectiuneJos(int (inaltimeCadru * 0.75))

    centreSectiuni = Sectiune.calculCentreSectiuni(binarization, lungimeCadru)

#########################################################################################
####### calc lat medie banda la fiecare 3 cadre cu detectare ############################
#########################################################################################
    vectorLatimiBanda = Sectiune.calculLatimeBanda(centreSectiuni)  # calcul latimi banda
    if contorDistMedBenzi0 <= 3: # CALCUL LATIME MEDIE BANDA DUPA 3 CADRE CU BANDA DETECTATA
        if ((exceptieDeInceput0 > 0 or (vectorLatimiMedii[0]-45 < vectorLatimiBanda[0] < vectorLatimiMedii[0]+45)) and vectorLatimiBanda[0] != -1 ):
            latimeSus = np.append( latimeSus, vectorLatimiBanda[0])
            contorDistMedBenzi0 += 1
            if exceptieDeInceput0 > 0:
                exceptieDeInceput0 -= 1
    if contorDistMedBenzi0 == 3:
        contorDistMedBenzi0 = 0
        vectorLatimiMedii[0] = int(np.average(latimeSus))
        latimeSus = np.zeros(0)

    if contorDistMedBenzi1 <= 3:  # CALCUL LATIME MEDIE BANDA DUPA 3 CADRE CU BANDA DETECTATA
        if ((exceptieDeInceput1 > 0 or (vectorLatimiMedii[1] - 45 < vectorLatimiBanda[1] < vectorLatimiMedii[1] + 45)) and vectorLatimiBanda[1] != -1):
            latimeJos = np.append(latimeJos, vectorLatimiBanda[1])
            contorDistMedBenzi1 += 1
            if exceptieDeInceput1 > 0:
                exceptieDeInceput1 -= 1
    if contorDistMedBenzi1 == 3:
        contorDistMedBenzi1 = 0
        vectorLatimiMedii[1] = int(np.average(latimeJos))
        latimeJos = np.zeros(0)


    print("### vectorLatimiMedii ", vectorLatimiMedii)
########################################################################################
########################################################################################

    centreSectiuniCompletat = Sectiune.completareCentre(centreSectiuni, vectorLatimiMedii)
    vectorCentreMedii = Sectiune.calculCentreMedii( centreSectiuniCompletat)
    print("### vectorCentreMedii ", vectorCentreMedii)
    centruRelativ = Sectiune.calculCentruRelativ( vectorCentreMedii)
    distantaFataDeAx = Sectiune.calculDistantaFataDeAx( centruRelativ, MijlocCamera)

    nrBenziDetectate, partea = Sectiune.nrBenziDetectate()

    intersectie = Sectiune.detectareIntersectie(binarization, lungimeCadru)
    if intersectie == 1:
        print("--> Urmeaza INTERSECTIE")

   # fps = cap.get(cv2.CAP_PROP_FPS)


   # if not ESTE_PE_MASINA:
   #     cv2.putText(img, "FPS: " + str(fps), (10, 20),
    #                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 2)
   # else:
     #   print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    if not ESTE_PE_MASINA:
        PutLines()



    if DEBUG_ALL_DATA and ESTE_PE_MASINA:
        print("Benzi gasite:" + str(Sectiune.nrBenziDetectate()))
        print("\nCentre:\t" + str(Sectiune.centreSectiuni))
    else:
        cv2.putText(img, "Benzi identificate: "+ str(Sectiune.nrBenziDetectate()), (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)


    try:

        DiferentaFataDeMijloc = distantaFataDeAx
        if DiferentaFataDeMijloc > EroareCentrare:
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

    if (not ESTE_PE_MASINA):
        deseneazaDrum(centreSectiuniCompletat, centreSectiuni, centruRelativ, distantaFataDeAx, nrBenziDetectate, partea,
                  inaltimeSectiuneSus, inaltimeSectiuneJos, vectorCentreMedii, intersectie)


    #if (not ESTE_PE_MASINA) :
   #     cv2.putText(img, "Stare: " + str(masina.current_state.value), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
   #                 (250, 250, 250), 2)
   # else :
   #     print(masina.current_state.value)

    t2 = time.time() - t1
    print("timp executie", t2, "s")

    if (not ESTE_PE_MASINA) :
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 960, 720)
        cv2.imshow("frame", frame)

        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image', 960, 720)
        cv2.imshow("Image", img)

        cv2.namedWindow('binarizare', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('binarizare', 960, 720)
        cv2.imshow("binarizare", binarization)


        streamer.update_frame(img)

        if not streamer.is_streaming:
            streamer.start_streaming()

        cv2.waitKey(30)  # 1=readare automata // 0=redare la buton
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