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
     return [t, tf]
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
   return t
#