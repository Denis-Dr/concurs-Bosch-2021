import numpy as np
''' 
    Modulul detecteaza benzile prin intermediul a 6 sectini si calculeaza centrele pentru fiecare + centrul relativ al benzii (!de implementat).
    Functia calculCentreSectiuni() primeste imaginea binarizata (treshold) si lungimea cadrului (orizontala) si returneaza o 
matrice 2x2 cu abscisele centrelor. Inaltimile centrelor sunt prestabilite in fisierul principal.
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
        self.eroareGrosimeBanda = 80

    def setInaltimeSectiuneSus(self, valoare):
        self.inaltimeSectiuneSus = int(valoare)
        return self.inaltimeSectiuneSus

    def setInaltimeSectiuneJos(self, valoare):
        self.inaltimeSectiuneJos = int(valoare)
        return self.inaltimeSectiuneJos

    def calculCentreSectiuni(self, binarization, lungimeCadru):  # calculul centrelor celor 6 sectiuni

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune sus stanga
        for i in range(int(lungimeCadru *0.02), int(lungimeCadru *0.46)):
            if binarization[self.inaltimeSectiuneSus, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime += 1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneSus, i] == 0 or i == (int(lungimeCadru *0.46) -1) ):
                self.incepeSectiunea == 0
                self.sfarsit = i-1
                if self.contorLungime < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[0][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune sus dreapta
        for i in range(int(lungimeCadru *0.98), int(lungimeCadru *0.54), -1):
            if binarization[self.inaltimeSectiuneSus, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime += 1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneSus, i] == 0 or i == (int(lungimeCadru *0.54) +1)):
                self.incepeSectiunea == 0
                self.sfarsit = i+1
                if self.contorLungime < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[0][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune jos stanga
        for i in range(1, int(lungimeCadru * 0.5)):
            if binarization[self.inaltimeSectiuneJos, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime += 1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneJos, i] == 0 or i == (int(lungimeCadru * 0.5) -1)):
                self.incepeSectiunea == 0
                self.sfarsit = i-1
                if self.contorLungime < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[1][0] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        self.contorLungime = 0
        self.incepeSectiunea = 0  # sectiune jos dreapta
        for i in range(lungimeCadru-1, int(lungimeCadru * 0.5), -1):
            if binarization[self.inaltimeSectiuneJos, i] == 255:
                if self.incepeSectiunea == 0:
                    self.incepeSectiunea = 1
                    self.inceput = i
                self.contorLungime +=1

            if self.incepeSectiunea == 1 and (binarization[self.inaltimeSectiuneJos, i] == 0 or i == (int(lungimeCadru * 0.5) +1)):
                self.incepeSectiunea == 0
                self.sfarsit = i+1
                if self.contorLungime < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijlocSectiune = int((self.sfarsit + self.inceput) / 2)
                    self.centreSectiuni[1][1] = self.mijlocSectiune  # atribuim centrul calculat sectiunii corespunzatoare
                    break
                else:
                    break

        if abs(self.centreSectiuni[1][0] - self.centreSectiuni[0][0]) >150 and (self.centreSectiuni[1][0] != -1 and self.centreSectiuni[0][0] != -1):
            self.centreSectiuni[0][0] = -1 # eliminam cazul in care avem reflexia soarelui pe podea (mai ales in curba)
        elif abs(self.centreSectiuni[1][1] - self.centreSectiuni[0][1]) >150 and (self.centreSectiuni[1][1] != -1 and self.centreSectiuni[0][1] != -1):
            self.centreSectiuni[0][1] = -1

        if (self.centreSectiuni[1][0] != -1 and self.centreSectiuni[0][1] != -1 and self.centreSectiuni[0][0] == -1
                                        and self.centreSectiuni[1][1] == -1): # eliminam cazul cand, in curba, banda e detectata pe partea cealalta
            self.centreSectiuni[0][1] = -1
        elif (self.centreSectiuni[1][1] != -1 and self.centreSectiuni[0][0] != -1 and self.centreSectiuni[0][1] == -1
                                        and self.centreSectiuni[1][0] == -1):
            self.centreSectiuni[0][0] = -1

        if abs(self.centreSectiuni[1][1] - self.centreSectiuni[1][0]) < 50 and (self.centreSectiuni[1][1] != -1 and self.centreSectiuni[1][0] != -1) :
            # eliminam cazul cand una din benzi este detectata pe partea cealalta
            if self.centreSectiuni[0][0] == -1 and self.centreSectiuni[0][1] != -1:
                self.centreSectiuni[0][1] = -1
                self.centreSectiuni[1][1] = -1
            elif self.centreSectiuni[0][0] != -1 and self.centreSectiuni[0][1] == -1:
                self.centreSectiuni[0][0] = -1
                self.centreSectiuni[1][0] = -1

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
        self.distantaFataDeAx = MijlocCamera - centruRelativ
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

    def detectareIntersectie(self, binarization, lungimeCadru): # detecteaza linia orizontala de la inceputul intersectiei
        self.vectorIntersectie = [-1, -1, -1]
        self.contorLungime1 = 0
        self.contorLungime2 = 0
        self.contorLungime3 = 0
        self.incepeSectiunea1 = 0
        self.incepeSectiunea2 = 0
        self.incepeSectiunea3 = 0

        for i in range(self.inaltimeSectiuneSus, self.inaltimeSectiuneJos):
            if binarization[i, int(0.33 * lungimeCadru)] == 255: # sectiunea STANGA
                if self.incepeSectiunea1 == 0:
                    self.incepeSectiunea1 = 1
                    self.inceput1 = i
                self.contorLungime1 += 1
            if self.incepeSectiunea1 == 1 and (binarization[i, int(0.33 * lungimeCadru)] == 0 or i == (self.inaltimeSectiuneJos - 1)):
                self.incepeSectiunea1 == 0
                self.sfarsit1 = i - 1
                if self.contorLungime1 < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijloc1 = int((self.sfarsit1 + self.inceput1) / 2)
                    self.vectorIntersectie[0] = self.mijloc1

            if binarization[i, int(0.5 * lungimeCadru)] == 255: # sectiunea MIJLOC
                if self.incepeSectiunea2 == 0:
                    self.incepeSectiunea2 = 1
                    self.inceput2 = i
                self.contorLungime2 += 1
            if self.incepeSectiunea2 == 1 and (binarization[i, int(0.5 * lungimeCadru)] == 0 or i == (self.inaltimeSectiuneJos - 1)):
                self.incepeSectiunea2 == 0
                self.sfarsit2 = i - 1
                if self.contorLungime2 < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijloc2 = int((self.sfarsit2 + self.inceput2) / 2)
                    self.vectorIntersectie[1] = self.mijloc2

            if binarization[i, int(0.67 * lungimeCadru)] == 255: # sectiunea DREAPTA
                if self.incepeSectiunea3 == 0:
                    self.incepeSectiunea3 = 1
                    self.inceput3 = i
                self.contorLungime3 += 1
            if self.incepeSectiunea3 == 1 and (binarization[i, int(0.67 * lungimeCadru)] == 0 or i == (self.inaltimeSectiuneJos - 1)):
                self.incepeSectiunea3 == 0
                self.sfarsit3 = i - 1
                if self.contorLungime3 < self.eroareGrosimeBanda:  # eliminam eroarea = sectiune pream mare
                    self.mijloc3 = int((self.sfarsit3 + self.inceput3) / 2)
                    self.vectorIntersectie[2] = self.mijloc3

        print("### vectorIntersectie ", self.vectorIntersectie)

        if (self.vectorIntersectie[0] != -1 and self.vectorIntersectie[1] != -1 and self.vectorIntersectie[2] != -1):
            if (self.vectorIntersectie[0] <= self.vectorIntersectie[1] <= self.vectorIntersectie[2]) or (self.vectorIntersectie[0] >= self.vectorIntersectie[1] >= self.vectorIntersectie[2]):
                return 1
        else:
            return 0

