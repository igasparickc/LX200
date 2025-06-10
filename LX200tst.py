#**************************************************************  
# GLAVNI KOD za testiranje upravljanja teleskopom Meade LX200:   
#**************************************************************  
import serial as ser
from datetime import datetime as dt
import time as tt
import keyboard as kb

from utils import *
#
print("***** Program za upravljanje teleskopom Meade LX200 *****")
print("                 (autor: Ivan Gašparić)")
print()
now = dt.now()
port = "COM5"
p = ""
while len(p) == 0:
   p = str.upper(input("Veza s teleskopom preko USB(U) ili COM(C):>"))
   if p[0] != "U":
      break
   else:
      port = "COM3"
try:      
       s = ser.Serial(port,9600,8,'N',1)       # COM5 - COM; COM3 - USB
except:
       print("Port", port, "ne postoji ili nije spojen!")
else:      
      # print(s.port)
      ret = init_scope(now)                   # Postavke teleskopa
      if ret:
        print("Pritisnite: N ili strelicu gore za Sjever (gore)") 
        print("            S ili strelicu dolje za Jug (dolje)") 
        print("            W ili strelicu desno za Zapad (desno)") 
        print("            E ili strelicu lijevo za Istok (lijevo)") 
        print("            Razmaknicu za Stop") 
        print("            0 za najmanju brzinu pomicanja (Guide)") 
        print("            1 za 2. najmanju brzinu pomicanja (Center)") 
        print("            4 za veću brzinu pomicanja (Find)") 
        print("            7 za najveću brzinu pomicanja (Slew)")
        print("            Q za završetak rada (komunikacije) s teleskopom")
        print(">")
        t = True
        while t:
          k = kb.read_key()
          print(">")
          if k == "right" or k == "w":        # Move West (right)
            n = s.write(bytearray(b'#:Mw#'))
            tt.sleep(0.5)
            n = s.write(bytearray(b'#:Qw#'))
          elif k == "left" or k == "e":       # Move East (left)
            n = s.write(bytearray(b'#:Me#'))
            tt.sleep(0.5)
            n = s.write(bytearray(b'#:Qe#'))
          elif k == "up" or k == "n":         # Move North (up)
            smjer = 'N'
            t = move_up_down(smjer)
      ##      n = s.write(bytearray(b'#:Mn#'))
      ##      tt.sleep(0.5)
      ##      n = s.write(bytearray(b'#:Qn#'))
          elif k == "down" or k == "s":       # Move South (down)
            smjer = "S"
            t = move_up_down(smjer)
      ##      n = s.write(bytearray(b'#:Ms#'))
      ##      tt.sleep(0.5)
      ##      n = s.write(bytearray(b'#:Qs#'))
          elif k == "space":                  # Stop move (space bar)
            n = s.write(bytearray(b'#:Q#'))
      ##      n = s.write(bytearray(b'#:Qw#'))
      ##      n = s.write(bytearray(b'#:Qe#'))
      ##      n = s.write(bytearray(b'#:Qn#'))
      ##      n = s.write(bytearray(b'#:Qs#'))
          elif k == "0":                      # Speed select GUIDE (0) - guiding rate
            n = s.write(bytearray(b'#:RG#'))
          elif k == "1":                      # Speed select CNTR (1) - centering rate
            n = s.write(bytearray(b'#:RC#'))
          elif k == "4":                      # Speed select FIND (4) - find rate
            n = s.write(bytearray(b'#:RM#'))
          elif k == "7":                      # Speed select SLEW (7) - slewing rate
            n = s.write(bytearray(b'#:RS#'))
          else:                               # Bilo koja druga tipka za završetak  
            break
      else:
        print("Neuspjela inicijalizacija teleskopa Meade LX200!")
      n = s.close()
finally:
        print("Završetak programa za upravljanje teleskopom Meade LX200.")
  

 
 
                       
                                
          
          
          
  
