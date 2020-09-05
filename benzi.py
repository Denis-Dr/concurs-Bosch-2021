import numpy as np
''' 
    Modulul detecteaza benzile prin intermediul a 6 sectini si calculeaza centrele pentru fiecare + centrul relativ al benzii (!de implementat).
    Functia calculCentreSectiuni() primeste imaginea binarizata (treshold) si lungimea cadrului (orizontala) si returneaza o 
matrice 3x2 cu abscisele centrelor. Inaltimile centrelor sunt prestabilite in fisierul principal.
    Matricea furnizeaza doua informatii: centrele si ne spune daca se detecteaaza banda (elemente != -1).
'''

class Banda:
    def __init__(self):
        self.centreSectiuni = np.array([[-1, -1], [-1, -1]])  # resetam centreSectiuni[][] dupa fiecare cadru
        self.vectorCentreMedii = np.array([-1, -1])
        self.inaltimeSectiuneSus = 0
        self.inaltimeSectiuneJos = 0
        self.centruRelativ = 0
        self.distantaFataDeAx = 0


    def setInaltimeSectiuneSus(self, valoare):
        self.inaltimeSectiuneSus = int(valoare)

    def setInaltimeSectiuneJos(self, valoare):
        self.inaltimeSectiuneJos = int(valoare)

    def calculCentreSectiuni(self, binarization, lungimeCadru):  # calculul centrelor celor 6 sectiuni

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune sus stanga
        for i in range(int(0.1*lungimeCadru), int(lungimeCadru *0.455)):
            if binarization[self.inaltimeSectiuneSus, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime += 1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneSus, i] == 0 or i == (int(lungimeCadru *0.455) -1) ):
                self.incepeSectiunea == 0
                self.sfarsit = i-1
                if self.contorLungime < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[0][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune sus dreaota
        for i in range(int(lungimeCadru *0.555), int(0.9 * lungimeCadru)):
            if binarization[self.inaltimeSectiuneSus, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime += 1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneSus, i] == 0 or i == (int(0.9 * lungimeCadru) -1)):
                self.incepeSectiunea == 0
                self.sfarsit = i-1
                if self.contorLungime < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[0][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune jos stanga
        for i in range(1, int(lungimeCadru / 2)):
            if binarization[self.inaltimeSectiuneJos, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime += 1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneSus, i] == 0 or i == (int(lungimeCadru / 2) -1)):
                self.incepeSectiunea == 0
                self.sfarsit = i-1
                if self.contorLungime < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[1][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune jos dreapta
        for i in range(int(lungimeCadru / 2), lungimeCadru):
            if binarization[self.inaltimeSectiuneJos, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime +=1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneSus, i] == 0 or i == (lungimeCadru -1)):
                self.incepeSectiunea == 0
                self.sfarsit = i-1
                if self.contorLungime < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[1][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break
        print("### centreSectiuni ", self.centreSectiuni)
        return self.centreSectiuni  # returnam matricea cu centrele sectiunilor



    def calculCentreMedii(self, centreSectiuniCompletat):
        if centreSectiuniCompletat[0][0] != -1 and centreSectiuniCompletat[0][1] != -1: # calcul centru mediu sus
            self.vectorCentreMedii[0] = int((centreSectiuniCompletat[0][0] + centreSectiuniCompletat[0][1]) / 2)
        if centreSectiuniCompletat[1][0] != -1 and centreSectiuniCompletat[1][1] != -1: # calcul centru mediu jos
            self.vectorCentreMedii[1] = int((centreSectiuniCompletat[1][0] + centreSectiuniCompletat[1][1]) / 2)
        return self.vectorCentreMedii

    def calculCentruRelativ(self, vectorCentreMedii):
        self.contor = 0
        self.suma = 0

        if self.vectorCentreMedii[0] != -1:
            self.suma = self.suma + vectorCentreMedii[0]
            self.contor = self.contor + 1

        if self.vectorCentreMedii[1] != -1:
            self.suma = self.suma + vectorCentreMedii[1]
            self.contor = self.contor + 1

        if self.contor != 0:
            self.centruRelativ = int(self.suma / self.contor)

        print("#### centruRelativ ", self.centruRelativ)
        return self.centruRelativ

    def calculDistantaFataDeAx(self,centruRelativ, MijlocCamera): # calc dist dintre centru camera si centru banda
        self.distantaFataDeAx = abs(centruRelativ - MijlocCamera)
        print("### distantaFataDeAx ", self.distantaFataDeAx, "  ### centruRelativ ", centruRelativ, "  ### MijlocCamera", MijlocCamera)
        return self.distantaFataDeAx

    def nrBenziDetectate(self): # calc nr benzi / partea pe care detect
        if ((self.centreSectiuni[0][0]==-1 and self.centreSectiuni[1][0]==-1) and
            (self.centreSectiuni[0][1]!=-1 or self.centreSectiuni[1][1]!=-1)):
            return 1, "dreapta"

        elif ((self.centreSectiuni[0][0]!=-1 or self.centreSectiuni[1][0]!=-1) and
            (self.centreSectiuni[0][1]==-1 and self.centreSectiuni[1][1]==-1)):
            return 1, "stanga"

        elif ((self.centreSectiuni[0][0]!=-1 or self.centreSectiuni[1][0]!=-1) and
            (self.centreSectiuni[0][1]!=-1 or self.centreSectiuni[1][1]!=-1)):
            return 2, ""

        else:
            return 0, ""
