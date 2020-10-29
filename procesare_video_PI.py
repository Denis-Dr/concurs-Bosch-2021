import cv2
import time
import numpy as np
from benzi import Banda
import deseneaza

from Observer import DeplasareMasina
from StopAndPark import stopOrPark

import io
import picamera
from picamera.array import PiRGBArray


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

def get_frames(porneste):
    global serialHandler
    DEBUG_ALL_DATA = False
    ESTE_PE_MASINA = False
    VIDEO_RECORD = False
    AMPARCAT = False
    PRINT_DATE = True
    AFISARE_VIDEO = False

    ## VARIABILE
    latimeSus = np.zeros(0)
    latimeJos = np.zeros(0)
    vectorLatimiMedii = np.array([-1, -1])
    distantaFataDeAx = 0
    centruRelativ = 0
    exceptieDeInceput0 = 3  # exceptam primele 3 cadre de la regula de calcul a vectorLatimiMedii pt a obt o latime media reala pe care sa incercam sa o pastram
    exceptieDeInceput1 = 3

    EroareCentrare = 30

    pasAdaptare = 0
    pozitieMijlocAnterior = -1
    counter = 0
    masina = DeplasareMasina()
    ## END OF VARIABLE




    counterStop = 0
    contorDistMedBenzi0 = 0  # calculam distanda medie intre benzi
    contorDistMedBenzi1 = 0



    image = np.empty((480, 640, 3), dtype=np.uint8)
    time.sleep(0.1)

    for cadru in camera.capture_continuous(image, format="bgr", use_video_port=True):

        frame = np.array(cadru)
        
        points1 = np.float32([[100, 200], [540, 200], [0, 290], [640, 290]])
        points2 = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
        P = cv2.getPerspectiveTransform(points1, points2)
        output = cv2.warpPerspective(frame, P, (640, 480))
        img = output
        
        #img = frame

        #EsteStop, EsteParcare = stopOrPark(frame, AMPARCAT)

        counter = counter + 1
        if counter < 5:
            continue
        #if VIDEO_RECORD:
        #   out.write(frame)
        if not ESTE_PE_MASINA:
            cv2.putText(img, "Cadrul: " + str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (200, 255, 200), 2)

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
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        ret, binarization = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

        inaltimeCadru, lungimeCadru, _ = frame.shape  # H si L imagine
        MijlocCamera = int(lungimeCadru / 2.0)

        Sectiune = Banda()  # initializare benzi.py

        inaltimeSectiuneSus = Sectiune.setInaltimeSectiuneSus(int(inaltimeCadru * 0.5))
        inaltimeSectiuneJos = Sectiune.setInaltimeSectiuneJos(int(inaltimeCadru * 0.75))

        centreSectiuni = Sectiune.calculCentreSectiuni(binarization, lungimeCadru)

        #########################################################################################
        ####### calc lat medie banda la fiecare 3 cadre cu detectare ############################
        #########################################################################################
        vectorLatimiBanda = Sectiune.calculLatimeBanda(centreSectiuni)  # calcul latimi banda
        if contorDistMedBenzi0 <= 3:  # CALCUL LATIME MEDIE BANDA DUPA 3 CADRE CU BANDA DETECTATA
            if ((exceptieDeInceput0 > 0 or (vectorLatimiMedii[0] - 45 < vectorLatimiBanda[0] < vectorLatimiMedii[0] + 45)) and vectorLatimiBanda[0] != -1):
                latimeSus = np.append(latimeSus, vectorLatimiBanda[0])
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

        ########################################################################################
        ########################################################################################

        centreSectiuniCompletat = Sectiune.completareCentre(centreSectiuni, vectorLatimiMedii)
        vectorCentreMedii = Sectiune.calculCentreMedii(centreSectiuniCompletat)

        centruRelativ = Sectiune.calculCentruRelativ(vectorCentreMedii)
        distantaFataDeAx = Sectiune.calculDistantaFataDeAx(centruRelativ, MijlocCamera)

        nrBenziDetectate, partea = Sectiune.nrBenziDetectate()

        if PRINT_DATE:
            print("\n ----------- FRAME ", counter, " --------------")
            print(" ##centreSectiuni ", centreSectiuni, "\n ##vectorLatimiBanda ", vectorLatimiBanda, "\n ##vectorLatimiMedii ", vectorLatimiMedii, "\n ##centreSectiuniCompletat ",
                  centreSectiuniCompletat,
                  "\n ##vectorCentreMedii ", vectorCentreMedii, "\n ##distantaFataDeAx ", distantaFataDeAx, "  ##centruRelativ ", centruRelativ, "  ##MijlocCamera", MijlocCamera)

        intersectie = Sectiune.detectareIntersectie(binarization, lungimeCadru)
        if intersectie == 1:
            print("--> Urmeaza INTERSECTIE")

        #fps = cap.get(cv2.CAP_PROP_FPS)

        '''
        if not ESTE_PE_MASINA:
            cv2.putText(img, "FPS: " + str(fps), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 2)
        else:
            print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        '''

        if not ESTE_PE_MASINA:
            deseneaza.PutLines(img, binarization, inaltimeCadru, lungimeCadru, inaltimeSectiuneSus, inaltimeSectiuneJos)
            deseneaza.deseneazaDrum(PRINT_DATE, img, centreSectiuniCompletat, centreSectiuni, centruRelativ, distantaFataDeAx, nrBenziDetectate, partea, inaltimeSectiuneSus, inaltimeSectiuneJos,
                                    vectorCentreMedii, intersectie, inaltimeCadru, lungimeCadru, porneste)

        if DEBUG_ALL_DATA and ESTE_PE_MASINA:
            print("Benzi gasite:" + str(Sectiune.nrBenziDetectate()))
            print("\nCentre:\t" + str(Sectiune.centreSectiuni))
        else:
            cv2.putText(img, "Benzi identificate: " + str(Sectiune.nrBenziDetectate()), (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        try:

            DiferentaFataDeMijloc = distantaFataDeAx
            if DiferentaFataDeMijloc > EroareCentrare:
                pasAdaptare = pasAdaptare - 2
                if (pasAdaptare < (-22)):
                    pasAdaptare = -20
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

        '''
        if (not ESTE_PE_MASINA) :
            cv2.putText(img, "Stare: " + str(masina.current_state.value), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (250, 250, 250), 2)
        else :
            print(masina.current_state.value)
        '''

        if (not ESTE_PE_MASINA) and AFISARE_VIDEO:
            #cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('frame', 960, 720)
            cv2.imshow("frame", frame)

            #cv2.namedWindow('Img_procesata', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('Img_procesata', 960, 720)
            cv2.imshow("Img_procesata", img)

            #cv2.namedWindow('binarizare', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('binarizare', 960, 720)
            cv2.imshow("binarizare", binarization)


        cv2.waitKey(1)  # 1=readare automata // 0=redare la buton
        time.sleep(0.0)

        #image.truncate(0)

        yield img

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        '''
        if stopOrPark(img, False) == 1:
            print("STOP")
            serialHandler.sendBrake(0)
        '''


    if ESTE_PE_MASINA:
        serialHandler.sendPidActivation(False)
        serialHandler.close()

    cv2.destroyAllWindows()
    
    
if __name__ == "__main__":
    get_frames()