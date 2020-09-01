import numpy as np
''' 
    Modulul detecteaza benzile prin intermediul a 6 sectini si calculeaza centrele pentru fiecare + centrul relativ al benzii (!de implementat).
    Functia calculCentreSectiuni() primeste imaginea binarizata (treshold) si lungimea cadrului (orizontala) si returneaza o 
matrice 3x2 cu abscisele centrelor. Inaltimile centrelor sunt prestabilite in fisierul principal.
    Matricae furnizeaza doua informatii: centrele si ne spune daca se detecteaaza banda (elemente != -1).
'''

class Banda:
    def __init__(self):
        self.centreSectiuni = [[-1, -1], [-1, -1], [-1, -1]]  # resetam centreSectiuni[][] dupa fiecare cadru

        self.inaltimeSectiuneSus = 0
        self.inaltimeSectiuneMijloc = 0
        self.inaltimeSectiuneJos = 0



    def setInaltimeSectiuneSus(self, valoare):
        self.inaltimeSectiune = int(valoare)

    def setInaltimeSectiuneMijloc(self, valoare):
        self.inaltimeSectiune = int(valoare)

    def setInaltimeSectiuneJos(self, valoare):
        self.inaltimeSectiune = int(valoare)

    def CalculDistantaFataDeBanda(self, lungimeCadru): # versiunea veche a functiei -> de modificat
        if self.centre.size == 2:
            self.DistantaBandaFrame = self.centre[1] - self.centre[0]
            print("La " + str(self.nume) + " - distanta dintre banda dreapta si cea stanga este: " + str(
                self.DistantaBandaFrame))
            self.MediereDistantaBanda()
            self.mijlocCalculat = int((self.centre[0] + self.centre[1]) / 2)
            self.DistantaFataDeAx = abs(self.mijlocCalculat - int(lungimeCadru / 2))


    def calculCentreSectiuni(self, binarization, lungimeCadru):  # calculul centrelor celor 6 sectiuni

        self.incepeSectiunea = 0  # sectiune sus stanga
        for i in range(lungimeCadru / 4, lungimeCadru / 2):
            if binarization[self.inaltimeSectiuneSus, i] == 1:
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
        for i in range(lungimeCadru / 2, int(0.75 * lungimeCadru)):
            if binarization[self.inaltimeSectiuneSus, i] == 1:
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

        incepeSectiunea = 0  # sectiune mijloc stanga
        for i in range(int(0.2 * lungimeCadru), lungimeCadru / 2):
            if binarization[self.inaltimeSectiuneMijloc, i] == 1:
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
        for i in range(lungimeCadru / 2, int(0.8 * lungimeCadru)):
            if binarization[self.inaltimeSectiuneMijloc, i] == 1:
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
        for i in range(1, lungimeCadru / 2):
            if binarization[self.inaltimeSectiuneJos, i] == 1:
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
        for i in range(lungimeCadru / 2, lungimeCadru):
            if binarization[self.inaltimeSectiuneJos, i] == 1:
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
