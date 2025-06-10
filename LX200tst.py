#-------------------------------------------------------------------------------
#  TEST PROGRAM za upravljanje teleskopom Meade LX200 Classic:
#-------------------------------------------------------------------------------
def move_up_down(smjer):  # Pomak gore/dolje s kontrolom granica visine
      ret = get_scope_info("#:GA#")
      alt = int(ret[1][1:2])
      t = ret[0]
      if t:
        if smjer == 'N':
           nar1 = '#:Mn#'
           nar2 = '#:Qn#'
           if alt > 75:
              t = False   
        else:
           nar1 = '#:Ms#'
           nar2 = '#:Qs#'
           if alt < 5:
              t = False   
        if t:    
           n = s.write(bytearray(nar1, 'ascii'))
           tt.sleep(0.5)
           n = s.write(bytearray(nar2, 'ascii'))
      return t; 
#-------------------------------------------------------------------------------
def set_scope_value(command): # Postavljanje varijabli u teleskopu (SET naredbe)
      n = s.write(bytearray(command, 'ascii'))
      u = 1
      t = True
      while u:
        c = (s.read(s.inWaiting())).decode()
        f = c.find("1")
        if f > -1:
          u = 0
          continue
        f = c.find("0")
        if f > -1:
           u = 0
           t = False
        return t;
#--------------------------------------------------------------------------------
def get_scope_info(command):  # Dohvaćanje informacija iz teleskopa (GET naredbe)
     n = s.write(bytearray(command, 'ascii'))
     u = 1
     poc = tt.time()
     c = ''
     while u:
       c = c + (s.read(s.inWaiting())).decode("utf-8","ignore")
#       print(c)
       f = c.find("#")
       if f > -1:
         u = 0
         t = True
       else:
         if tt.time() - poc > 3:
            print("Problem komunikacije s teleskopom!?")
            t = False
            u = 0
     return [t, c[:f]]
#------------------------------------------------------------------
def get_time_format():    # Funkcija za dohvaćanje formata vremena 
     ldc = "#:Gc#"        # dohvati format vremena (12 ili 24)
     n = s.write(bytearray(ldc, 'ascii'))
     u = 1
     t = True
     tf = '24'
     c = ''
     poc = tt.time()
     while u:
       c = c + (s.read(s.inWaiting())).decode("utf-8","ignore")
       f = c.find("12")
       if f > -1:
          u = 0
          tf = '12'
          print("12-satni format vremena.")
          continue
       f = c.find("#")
       if f > -1:
          print("24-satni format vremena.")
          u = 0
       else:
          if tt.time() - poc > 3:
             print("Problem komunikacije s teleskopom!?")
             t = False
             u = 0
     return [t, tf];
#------------------------------------------------------------------------------------   
def init_scope(dt):    #  Funkcija za postavljanje inicijalnih vrijednosti teleskopa
   t = True
#     Ispitivanje je li montaža AltAz (naredba <ACK>):   
   lsc = bytearray('\x06','ascii')
   n = s.write(lsc)
   u = 1
   f = -1
   poc = tt.time()
   while u:
      if f < 0:
         c = (s.read(s.inWaiting())).decode()
      f = c.find("A")
      if f > -1:
         break
      if (tt.time() - poc) > 3:
        print("Teleskop nije spojen!") 
        t = False
        u = 0
   if t:     
      if f < 0:    # Ako nije AlTAz postavi na AltAz: (?)
         lsc = bytearray('#:AA#','ascii')
         n = s.write(lsc)
         print("Postavljanje teleskopa na AltAz način aligment-a.")
   if t:           # Odaberite lokaciju (SITE) - :Wn#, n =1..4  - teleskopu se šalje 0..3 
      li = 0
      while li < 1 or li > 4:
         li = int(input("Upiši broj lokacije (1 - 4):>")) 
      n = s.write(bytearray("#:W" + str(li - 1)+ "#", 'ascii'))
   if t:                # Dohvaćanje naziva trenutne lokacije - :GM# ili :GN# ili :GO# ili :GP#
     if li == 1: 
        ldc = "#:GM#"
     elif li == 2:   
        ldc = "#:GN#"
     elif li == 3:   
        ldc = "#:GO#"
     else:   
        ldc = "#:GP#"
     ret = get_scope_info(ldc)
     t = ret[0]
   if t:           # Geografska širina lokacije promatranja:   
      print("Lokacija (SITE):", ret[1][:3])
      ss = 91
      mm = 61
      dl = ""
      while ss > 90 or mm > 60 or dl != '*':   
         lat = input("Upiši geografsku širinu od 0 do 90⁰ (SS*MM):>")
         ii = lat.find("*")
         if ii < 2:
            ss = int(lat[0:ii])
            sst = "0"*(3-ii) + lat[0:ii]
         else:   
            ss = int(lat[0:2])
            sst = lat[0:2]
         dl = lat[ii]
         mm = int(lat[ii+1:])
         mmt = lat[ii+1:]
      lat = "#:St+" + sst + dl + mmt + "#"
#      print(lat) 
      t = set_scope_value(lat)
   if t:                # Dohvaćanje geografske širine u teleskopu
     ret = get_scope_info("#:Gg#")
     t = ret[0]
   if t:        # Geografska dužina lokacije promatranja ( za istočne dužine LE upisati 360 - LE)
      print("Geografska širina u teleskopu:", ret[1])
      ss = 361
      mm = 61
      dl = ""
      while ss > 360 or mm > 60 or dl != '*':   
         lng = input("Upiši geografsku dužinu - prema zapadu od 0 do 360⁰(SSS*MM):>")
         ii = lng.find("*")
         if ii < 3:
            ss = int(lng[0:ii])
            sst = "0"*(3-ii) + lng[0:ii]
         else:   
            ss = int(lng[0:3])
            sst = lng[0:3]
         dl = lng[ii]
         mm = int(lng[ii+1:])
         mmt = lng[ii+1:]
      lng = "#:Sg" + sst + dl + mmt + "#"   
      n = s.write(bytearray(lng, 'ascii'))
      u = 1
      while u:
        c = (s.read(s.inWaiting())).decode()
        f = c.find("1")
        if f > -1:
          u = 0
          continue
        f = c.find("0")
        if f > -1:
           u = 0
           t = False
   if t:                # Dohvaćanje geografske dužine u teleskopu
     ret = get_scope_info("#:Gt#")
     t = ret[0]
   if t:        # Postavi trenutni datum teleskopa      
      print("Geografska dužina u teleskopu:", ret[1])
      ldc = "#:SC" + dt.strftime("%m/%d/%Y") + "#"
      lsc = bytearray(ldc,'ascii')
      n = s.write(lsc)
      u = 1
      while u:
         c = (s.read(s.inWaiting())).decode()
         f = c.find("1")
         if f > -1:
            u = 0
            continue
         f = c.find("0")
         if f > -1:
            u = 0
            t = False
   if t:                # Dohvaćanje datuma u teleskopu :GC#
     ret = get_scope_info("#:GC#")
     t = ret[0]
   if t:                        # Dohvati format vremena :Gc#
      print("Datum u teleskopu:", ret[1])
      ret = get_time_format()
      t = ret[0]
      tf = ret[1]
   if t:
     if tf == '12':             #  Promijeni u 24-satni prikaz vremena :H# (ako nije)
       ldc = "#:H#"
       n = s.write(bytearray(ldc, 'ascii'))
       ret = get_time_format()  # Dohvati format vremena da se vidi promjena
       t = ret[0]
   if t:                        # Slanje lokalnog vremena u teleskop 
     ltc = "#:SL" + dt.strftime("%H:%M:%S") + "#"
     n = s.write(bytearray(ltc, 'ascii'))
     u = 1
     while u:
       c = (s.read(s.inWaiting())).decode()
       f = c.find("1")
       if f > -1:
          u = 0
          continue
       f = c.find("0")
       if f > -1:
          u = 0
          t = False
   if t:                # Dohvaćanje vremena u teleskopu :GL#
     ldc = "#:GL#"
     ret = get_scope_info("#:GL#")
     t = ret[0]
   if t:                  #  Vremenska zona (UTC offset) - negativno na istok (:SGsHH.H#)
      print("Vrijeme u teleskopu:", ret[1])
      uo = "#:SG" + input("Upiši UTC offset (istok -, zapad +) u obliku sHH.H:>") + "#"
      n = s.write(bytearray(uo, 'ascii'))
      u = 1
      while u:
        c = (s.read(s.inWaiting())).decode()
        f = c.find("1")
        if f > -1:
          u = 0
          continue
        f = c.find("0")
        if f > -1:
           u = 0
           t = False
   if t:                # Dohvaćanje vremenske zone (UTC offset) - :GG#
     ret = get_scope_info("#:GG#")
     t = ret[0]
   if t:                # Najniža elevacija (:SoDD#) - 5 stupnjeva:
      print("UTC offset:", ret[1])
      n = s.write(bytearray("#:So05#", 'ascii'))
      while u:
        c = (s.read(s.inWaiting())).decode()
        f = c.find("1")
        if f > -1:
          u = 0
          continue
        f = c.find("0")
        if f > -1:
           u = 0
           t = False
   if t:                # Najviša elevacija (:ShDD#) - 75 stupnjeva
      n = s.write(bytearray("#:Sh75#", 'ascii'))
      while u:
        c = (s.read(s.inWaiting())).decode()
        f = c.find("1")
        if f > -1:
          u = 0
          continue
        f = c.find("0")
        if f > -1:
           u = 0
           t = False
   return t;
#
#**************************************************************  
# GLAVNI KOD za testiranje upravljanja teleskopom Meade LX200:   
#**************************************************************  
import serial as ser
from datetime import datetime as dt
import time as tt
import keyboard as kb
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
  

 
 
                       
                                
          
          
          
  
