import numpy as np
''' 
    Modulul detecteaza benzile prin intermediul a 6 sectini si calculeaza centrele pentru fiecare + centrul relativ al benzii (!de implementat).
    Functia calculCentreSectiuni() primeste imaginea binarizata (treshold) si lungimea cadrului (orizontala) si returneaza o 
matrice 3x2 cu abscisele centrelor. Inaltimile centrelor sunt prestabilite in fisierul principal.
    Matricea furnizeaza doua informatii: centrele si ne spune daca se detecteaaza banda (elemente != -1).
'''

class Banda:
    def __init__(self):
        self.centreSectiuni = [[-1, -1], [-1, -1], [-1, -1]]  # resetam centreSectiuni[][] dupa fiecare cadru
        self.vectorCentreMedii = [-1, -1, -1]
        self.inaltimeSectiuneSus = 0
        self.inaltimeSectiuneMijloc = 0
        self.inaltimeSectiuneJos = 0
        self.centruRelativ = 0
        self.distantaFataDeAx = 0


    def setInaltimeSectiuneSus(self, valoare):
        self.inaltimeSectiune = int(valoare)

    def setInaltimeSectiuneMijloc(self, valoare):
        self.inaltimeSectiune = int(valoare)

    def setInaltimeSectiuneJos(self, valoare):
        self.inaltimeSectiune = int(valoare)


    def calculCentreSectiuni(self, binarization, lungimeCadru):  # calculul centrelor celor 6 sectiuni

        self.incepeSectiunea = 0  # sectiune sus stanga
        for i in range(int(0.25*lungimeCadru), int(lungimeCadru / 2)):
            if binarization[self.inaltimeSectiuneSus, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
            if self.incepeSectiunea == 1 and binarization[self.inaltimeSectiuneSus, i] == 0:
                self.sfarsit = i - 1
                if (self.sfarsit - self.inceput) < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit - self.inceput) / 2)
                    self.centreSectiuni[0][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.incepeSectiunea = 0  # sectiune sus dreaota
        for i in range(int(lungimeCadru / 2), int(0.75 * lungimeCadru)):
            if binarization[self.inaltimeSectiuneSus, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
            if self.incepeSectiunea == 1 and binarization[self.inaltimeSectiuneSus, i] == 0:
                self.sfarsit = i - 1
                if (self.sfarsit - self.inceput) < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit - self.inceput) / 2)
                    self.centreSectiuni[0][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.incepeSectiunea = 0  # sectiune mijloc stanga
        for i in range(int(0.1 * lungimeCadru), int(lungimeCadru / 2)):
            if binarization[self.inaltimeSectiuneMijloc, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
            if self.incepeSectiunea == 1 and binarization[self.inaltimeSectiuneSus, i] == 0:
                self.sfarsit = i - 1
                if (self.sfarsit - self.inceput) < 150:  # eliminam eroarea = sectiune pream mare v
                    self.mijlocSectiune = int((self.sfarsit - self.inceput) / 2)
                    self.centreSectiuni[1][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.incepeSectiunea = 0  # sectiune mijloc dreapta
        for i in range(int(lungimeCadru / 2), int(0.9 * lungimeCadru)):
            if binarization[self.inaltimeSectiuneMijloc, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
            if self.incepeSectiunea == 1 and binarization[self.inaltimeSectiuneSus, i] == 0:
                self.sfarsit = i - 1
                if (self.sfarsit - self.inceput) < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit - self.inceput) / 2)
                    self.centreSectiuni[1][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.incepeSectiunea = 0  # sectiune jos stanga
        for i in range(1, int(lungimeCadru / 2)):
            if binarization[self.inaltimeSectiuneJos, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
            if self.incepeSectiunea == 1 and binarization[self.inaltimeSectiuneSus, i] == 0:
                self.sfarsit = i - 1
                if (self.sfarsit - self.inceput) < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit - self.inceput) / 2)
                    self.centreSectiuni[2][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.incepeSectiunea = 0  # sectiune jos dreapta
        for i in range(int(lungimeCadru / 2), lungimeCadru):
            if binarization[self.inaltimeSectiuneJos, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
            if self.incepeSectiunea == 1 and binarization[self.inaltimeSectiuneSus, i] == 0:
                self.sfarsit = i - 1
                if (self.sfarsit - self.inceput) < 150:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit - self.inceput) / 2)
                    self.centreSectiuni[2][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        return self.centreSectiuni  # returnam matricea cu centrele sectiunilor



    def calculCentreMedii(self, centreSectiuniCompletat):
        if centreSectiuniCompletat[0][0] != -1 and centreSectiuniCompletat[0][1] != 0: # calcul centru mediu sus
            self.vectorCentreMedii[0] = int((centreSectiuniCompletat[0][0] + centreSectiuniCompletat[0][1]) / 2)
        if centreSectiuniCompletat[1][0] != -1 and centreSectiuniCompletat[1][1] != 0: # calcul centru mediu mijloc
            self.vectorCentreMedii[1] = int((centreSectiuniCompletat[1][0] + centreSectiuniCompletat[1][1]) / 2)
        if centreSectiuniCompletat[2][0] != -1 and centreSectiuniCompletat[2][1] != 0: # calcul centru mediu jos
            self.vectorCentreMedii[2] = int((centreSectiuniCompletat[2][0] + centreSectiuniCompletat[2][1]) / 2)
        return self.vectorCentreMedii

    def calculCentruRelativ(self):
        self.contor = 1
        self.suma = 0
        for i in range(3):
            if self.vectorCentreMedii[i] != -1:
                self.suma = self.suma + self.vectorCentreMedii[i]
                self.contor = self.contor + 1
        self.centruRelativ = int(self.suma / self.contor)
        return self.centruRelativ

    def calculDistantaFataDeAx(self, MijlocCamera): # calc dist dintre centru camera si centru banda
        self.distantaFataDeAx = abs(self.centruRelativ - MijlocCamera)
        return self.distantaFataDeAx

    def nrBenziDetectate(self): # calc nr benzi / partea pe care detect
        if ((self.centreSectiuni[0][0]==-1 and self.centreSectiuni[1][0]==-1 and self.centreSectiuni[2][0]==-1) and
            (self.centreSectiuni[0][1]!=-1 or self.centreSectiuni[1][1]!=-1 or self.centreSectiuni[2][1]!=-1)):
            return 1, "dreapta"

        elif ((self.centreSectiuni[0][0]!=-1 or self.centreSectiuni[1][0]!=-1 or self.centreSectiuni[2][0]!=-1) and
            (self.centreSectiuni[0][1]==-1 and self.centreSectiuni[1][1]==-1 and self.centreSectiuni[2][1]==-1)):
            return 1, "stanga"

        elif ((self.centreSectiuni[0][0]!=-1 or self.centreSectiuni[1][0]!=-1 or self.centreSectiuni[2][0]!=-1) and
            (self.centreSectiuni[0][1]!=-1 or self.centreSectiuni[1][1]!=-1 or self.centreSectiuni[2][1]!=-1)):
            return 2, ""

        else:
            return 0, ""
