from time import time
from math import sin
from math import cos
from math import pi
from PIL.Image import *
from neopixel import *
from time import sleep
import RPi.GPIO as gp


im = open("/home/pi/Desktop/JugendForscht/TEST.png")
pix = im.load()

LED_COUNT   = 35# Anzahl der LED's auf dem LED-Streifen

LED_PIN1    = 18 # GPIO-Nummer des Pin's, mit dem man den LED-Streifen ansteuert.

LED_FREQ_HZ = 800000 # Blinkfrequenz
LED_DMA   = 5  # DMA-Kanal für generieren des Signals ?
LED_BRIGHTNESS = 100 # Helligkeit
LED_INVERT = False # Falls Transistor: True
MIN_RAD = 2.5

gp.setmode(gp.BCM)
gp.setwarnings(False)
gp.setup(17, gp.IN)

matrix = [[0 for x in range(0, 4* LED_COUNT)]for y in range(1,7)] # Erschaffen einer Liste, in der sechs Listen enthalten sind


t = 1 # Zeitabschnitt  
T = 2 # Umlaufzeit
i = 0 # Variable für die for-Schleife

x = MIN_RAD # Variable für die for-Schleife
for i in range(0, LED_COUNT):
    matrix[0][i] = i+1

def line(länge):
    s = ""
    for i in range(0, länge):
        s += "-"
    print(s)
    
def startPrint():
    #anzeigen der Starteinstellungen
    str1 = "Led Bikelight"
    str2 = "\nDie Momentanen Einstellungen sind:"
    line(50)
    print(str1)
    line(50)
    print(str2)
    print("")
    print("Anzahl der Led's = " + str(LED_COUNT))
    print("GPIO-Pins = " + str(LED_PIN1))
    print("f in Hz = " + str(LED_FREQ_HZ))
    print("DMA Kanal = " + str(LED_DMA))
    print("LED HElligkeit = " + str(LED_BRIGHTNESS))
    print("Invertiertes Signal = " + str(LED_INVERT))
    line(50)
    print("Drück Strg-C zum beenden.")
    line(50)


    
def bildAuslesen():
    global matrix
    global T
    global t
    global streifen
    
    w = 2 * pi / T
    k1 = w * t
    
    for i in range(0, 2*LED_COUNT):
        #ausrechnen des Winkels in rad
           #Berrechnung der Y Koordinate
        if i < LED_COUNT:
            pass
        elif i >= LED_COUNT:
            k1 += pi/2
        
        matrix[1][i] = int(cos(k1) * matrix[0][i]+37)    #Berechnung der X-Koordinate
        matrix[2][i] = int(sin(k1) * matrix[0][i]+37)

        r,g,b = pix[matrix[1][i], matrix[2][i]]                        #auslesen eines Pixels
        streifen.setPixelColor(i+1, Color(r, g, b))
        

    streifen.show()





def main():
    global T 
    global t
    global t1
    global matrix
    global streifen

    
    #   initialisierung des Led streifens

    streifen.begin()  #starten des LED-Streifens
    startPrint()                            #Drucken der Anfangseinstellungen
    while True:                             #Dauerschleife fuer die Zeit
        t1 = time()                         #startzeit t1
        
        if gp.input(17) == False:           #Damit die Zeit nur einmal pro umdrehung gemessen wird

            while gp.input(17) == False:
                t = time() - T              #Ausrechnen der größe des Zeitabschnitts
                bildAuslesen()
                    


            T = time() - t1                     #Ausrechnen von T nach T = t2 - t1

streifen = Adafruit_NeoPixel(4 * LED_COUNT, LED_PIN1, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)


main()
