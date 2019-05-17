import pygame,time,serial,sys
'''
MiniFRC Driver Station
By GooseFairy/XelaLord

TODO:
add hats rendering
stay open during errors
fix/add scrolling
'''

version = 4.1

#gui deals with the console and anything visible to the user
class gui:
    def __init__(self):
        self.resolution = [1100,500]
        
        #setup pygame and window
        pygame.init()
        self.window = pygame.display.set_mode(self.resolution,pygame.RESIZABLE)
        pygame.display.set_caption("MiniFRC Driver Station V%s" % (str(version)))

        self.font = pygame.font.SysFont("courier",self.resolution[0]//80)
        
        #colors
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.green = (0,155,0)
        self.blue = (0,0,255)
        self.orange = (255,140,0)
        
        #console stuff
        self.needs_render = False
        self.stack = []
        self.width = self.resolution[0] // 2.35
        self.scroll = 0
        
    #Adds text to console stack
    def log(self, text, color = None):
        self.needs_render = True
        if color != None:
            self.stack.append((text,color))
        else:
            self.stack.append((text,self.black))

    #writes console to file and kills pygame
    def bail(self):
        with open("LOGFILE.txt","w") as f:
            for item in self.stack:
                f.write(item[0] + "\n")
        pygame.quit()

    #updates the size of everything
    def resize(self,event):
        self.resolution = [event.dict['size'][0],event.dict['size'][1]]
        self.window = pygame.display.set_mode(self.resolution,pygame.RESIZABLE)
        self.font = pygame.font.SysFont("courier",self.resolution[0]//80)
        self.width = self.resolution[0] // 2.35
        self.needs_render = True
        

    #puts text onto the screen
    def make_text(self,text,color,x,y,scale,center=False):
        font = pygame.font.SysFont("courier",scale)
        rect = font.render(text,1,color)
        if center:
            x-= int(rect.get_rect().width // 2)
        self.window.blit(rect,(x,y))

    #this renders everything in the stack & wraps lines if needed.
    def render_stack(self):
        pygame.draw.rect(self.window,self.white,(0,0,self.width,self.resolution[1]))
        self.needs_render = False
        scale= self.resolution[0]//80
        final = []
        for item in self.stack:
            text = item[0].split(" ")
            while True:
                temp = []
                while self.font.size(" ".join(text))[0] > self.width-2:
                    temp.append(text.pop())
                final.append((" ".join(text), item[1]))
                if len(temp) <= 0:
                    break
                else:
                    text = temp[::-1]
        depth = len(final)
        max_depth = self.resolution[1] // scale
        offset = min(max_depth - depth,0)*scale + self.scroll
        for i in range(len(final)):
            self.make_text(final[i][0],final[i][1],5,offset + (i*scale), scale)

    def render_button(self,button,center):
        radius = self.resolution[0] // 90
        #write the name:
        self.make_text(button.name,self.black,center,(self.resolution[1]//2) - int(radius*4),self.resolution[0]//70,True)
        #make the button:
        if button.value == 0:
            pygame.draw.circle(self.window,self.blue,(center,self.resolution[1]//2), radius, 2)
        else:
            pygame.draw.circle(self.window,self.blue,(center,self.resolution[1]//2), radius, 0)

    def render_axis(self,axis,center):
        height = self.resolution[1] // 5
        y = self.resolution[1]//2
        #text
        self.make_text(axis.name,self.black,center,-(height//2)-self.resolution[1]//10+y,self.resolution[0]//70,True)
        self.make_text('1', self.black, center,-(self.resolution[0]//45+height//2)+y,self.resolution[0]//60,True)
        self.make_text('-1', self.black, center,(height//2)+y,self.resolution[0]//60,True)
        #lines
        pygame.draw.line(self.window,self.black,(center,height//2 + y),(center,-height//2+y),2)
        pygame.draw.line(self.window,self.black,(center-15,height//2 +y),(center+15,height//2+y),2)
        pygame.draw.line(self.window,self.black,(center-15,-height//2 +y),(center+15,-height//2+y),2)
        #marker
        pygame.draw.rect(self.window,self.blue,(center-4,-axis.value*height//2 + y-5,10,10))
        
        
    def render_hat(self,hat,center):
        pass
            
    #renders everything on gui
    def render(self,inputs,pack):
        #render console if needed
        if self.needs_render: self.render_stack()

        #render inputs area
        pygame.draw.rect(self.window,self.white,(self.width,0,(self.resolution[0]-self.width),self.resolution[1]))
        pygame.draw.line(self.window,self.black,(self.width,0),(self.width,self.resolution[1]),2)
        start = int(self.width + 40)
        for item in inputs:
            start += item.render(self,start)

        #render package readout
        self.make_text(pack,self.black, self.width + 10, self.resolution[1] - self.resolution[0]//35, self.resolution[0]//40)
            
        pygame.display.update()        

#keeps track of key inputs
class Key:
    def __init__(self,name,*args):
        self.name = name
        self.forward = args[0] #Works with both buttons and axes
        self.backward = args[1] if len(args) > 1 else None
        self.value = 0
    def error(self):
        return ": Key %s %s named %s" % (self.forward, self.backward, self.name)
    def get(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == self.forward:
                    self.value = 1
                elif pygame.key.name(event.key) == self.backward:
                    self.value = -1
            else:
                if self.value == 1 and pygame.key.name(event.key) == self.forward:
                    self.value = 0
                elif self.value == -1 and pygame.key.name(event.key) == self.backward:
                    self.value = 0
        return self.value
    def render(self,gui,start):
        if self.backward == None:
            gui.render_button(self,start)
            return gui.resolution[0] // 15
        else:
            gui.render_axis(self,start)
            return gui.resolution[0] // 15

#keeps track of joystick inputs
class Joy:
    def __init__(self,mode,name,num,index):
        self.name = name
        self.joynum = int(num)
        self.mode = mode#0=joybutton,1=joyaxis,2=joyhat
        self.index = int(index)
        self.value = 0.0
    def error(self):
        if self.mode == 0:
            mode = "button"
        elif self.mode == 1:
            mode = "axis"
        else:
            mode = "hat"
        return ": Joystick #%s, %s %s" % (str(self.joynum), mode, str(self.index))
    def get(self,joysticks,prec):
        if self.mode == 0:
            self.value = joysticks[self.joynum].get_button(self.index)
            return self.value
        elif self.mode == 1:
            self.value = round(joysticks[self.joynum].get_axis(self.index),prec)
            return self.value
        else:
            self.value = joysticks[self.joynum].get_hat(self.index)
            return str(self.value[0]) + ";" +str(self.value[1])
    def render(self,gui,start):
        if self.mode == 0:
            gui.render_button(self,start)
            return gui.resolution[0] // 15
        elif self.mode == 1:
            gui.render_axis(self,start)
            return gui.resolution[0] // 15
        else:
            gui.render_hat(self,start)
            return gui.resolution[0] // 15

class Mode:
    def __init__(self,name,inputs):
        self.name = name
        self.inputs = inputs
        self.value = 0
    def get(self, events, joysticks, prec):
        for i in range(len(self.inputs)):
            if isinstance(self.inputs[i],Joy):
                if int(self.inputs[i].get(joysticks,prec)) == 1:
                    self.value = i
                    return str(i)
            else:
                if int(self.inputs[i].get(events)) == 1:
                    self.value = i
                    return str(i)
        return str(self.value)
    def render(self,gui,start):
        return gui.resolution[0] // 15

class driver:
    def __init__(self):
        #setup
        self.inputs = []
        self.g = gui()
        self.g.log("MiniFRC Driver Station v%s"%(str(version)))

        #config things
        self.legacy_packet = False
        self.enable_joysticks = False
        self.baudrate = 9600
        self.precision = 1
        self.autoport = False
        self.mode = 1 #0=test, 1=active
        self.com = "COM0"
        self.FPS = 20
        
        #load config file
        try:
            with open("config.txt","r") as f:
                self.g.log("[INFO] Found config.txt, reading...",self.g.black)
                raw =[line.replace(" ","") for line in f.read().split("\n") if (len(line) > 0 and line.find("//") == -1)]
        except Exception as e:
            self.g.log('[WARNING] Could not find/open "config.txt"', self.g.red)
            self.error(e)
            
        #parse config file
        line_num = -1
        try:
            for line in raw:
                line_num += 1
                if line.find("COM") != -1:
                    self.com = line.replace("=","")
                    if line.find("test") != -1:
                        self.mode = 0
                        self.g.log("[NOTICE] Test mode enabled",self.g.orange)
                    else:
                        self.g.log("[INFO] Configured to use com port %s"%(self.com))
                elif line.find("AUTOPORT") != -1:
                    if line.lower().find("true") != -1:
                        self.autoport = True
                        self.g.log("[INFO] AutoPort Enabled, Driver Station will attempt to connect to robot over multiple ports if needed")
                elif line.find("LEGACY") != -1:
                    if line.lower().find("true") != -1:
                        self.legacy_packet = True
                        self.g.log("[INFO] Legacy Packets are enabled.")
                elif line.find("BAUD") != -1:
                    self.baudrate = int(line.split("=")[1])
                    self.g.log("[INFO] Configured baudrate to %s"%(self.baudrate))
                elif line.find("FPS") != -1:
                    self.FPS = int(line.split("=")[1])
                    self.g.log("[INFO] Configured FPS to %s"%(self.FPS))
                elif line.find("PRECISION") != -1:
                    self.precision = int(line.split("=")[1])
                    self.g.log("[INFO] Configured precision to %s"%(self.precision))
                elif line.find("JOYSTICK") != -1:
                    if line.lower().find("true") != -1:
                        self.enable_joysticks = True
                elif line.find("button") != -1:
                    data = line.split(",")
                    if data[2].isdigit():
                        self.enable_joysticks = True
                        self.inputs.append(Joy(0,data[1],data[2],data[3]))
                        self.g.log("[INFO] Added a button controlled by joystick #%s button #%s" %(data[2],data[3]))
                    else:
                        self.inputs.append(Key(data[1],data[2].replace("#","")))
                        self.g.log("[INFO] Added a button controlled by key '%s'"%(data[2]))
                elif line.find("axis") != -1:
                    data = line.split(",")
                    if data[2].isdigit():
                        self.enable_joysticks = True
                        self.inputs.append(Joy(1,data[1],data[2],data[3]))
                        self.g.log("[INFO] Added an axis controlled by joystick #%s axis #%s" %(data[2],data[3]))
                    else:
                        self.inputs.append(Key(data[1],data[2].replace("#",""),data[3].replace("#","")))
                        self.g.log("[INFO] Added an axis controlled by keys '%s' and '%s'"%(data[2],data[3]))
                elif line.find("hat") != -1:
                    data = line.split(",")
                    self.enable_joysticks = True
                    self.inputs.append(Joy(2,data[1],data[2],data[3]))
                    self.g.log("[INFO] Added a hat switch controlled by joystick #%s hat #%s" %(data[2],data[3]))
                elif line.find("mode") != -1:
                    data = line.split(",")
                    temp = []
                    skip = False
                    for i in range(2,len(data)):
                        if skip:
                            skip = False
                            continue
                        if data[i].isdigit():
                            self.enable_joysticks = True
                            skip = True
                            temp.append(Joy(0,data[1],data[i],data[i+1]))
                        else:
                            temp.append(Key(data[1],data[i]))
                    self.inputs.append(Mode(data[1],temp))
                    self.g.log("[INFO] Added a Mode switch")
        except Exception as e:
            self.g.log("[WARNING] Improperly formatted config file",self.g.red)
            self.g.log("[WARNING] Could not parse: '%s'" % (str(raw[line_num])),self.g.red)
            self.error(e)
        
        #prep joysticks if enabled
        if self.enable_joysticks == False:
            self.joysticks = []
            self.g.log("[INFO] Joysticks not enabled")
        else:
            self.g.log("[INFO] Enabled joysticks")
            pygame.joystick.init()
            self.joysticks =[pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            if len(self.joysticks) < 1:
                self.g.log("[WARNING] Joysticks enabled but no joystick was found",self.g.red)
                self.error("No joysticks found")
            for item in self.joysticks: item.init()
            for i in range(3):
                pygame.event.get()
                time.sleep(0.1)
            #display all joystick data if test mode is enabled
            if self.mode == 0:
                self.g.log("[INFO] Detected %s joystick(s)" % (len(self.joysticks)))
                for joystick in self.joysticks:
                    self.g.log("[INFO] Joystick '%s'"%(joystick.get_name()))
                    axes = joystick.get_numaxes()
                    self.g.log("[INFO] Number of axes: %s"%(axes))
                    for i in range(axes): self.g.log("  [INFO] Axis %s value: %s" % (i,joystick.get_axis(i)))
                    buttons = joystick.get_numbuttons()
                    self.g.log("[INFO] Number of buttons: %s"%(buttons))
                    for i in range(buttons): self.g.log("  [INFO] Button %s value: %s" % (i,joystick.get_button(i)))
                    hats = joystick.get_numhats()
                    self.g.log("[INFO] Number of hats: %s"%(hats))
                    for i in range(hats): self.g.log("  [INFO] Hat %s value: %s" % (i,joystick.get_hat(i)))
        if self.mode == 1:
            self.serial = self.connect()
        self.run()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            #clamp to fps
            clock.tick(self.FPS)

            #get all events from pygame, make a list of key events & handle others accordingly
            events = pygame.event.get()
            keys = []
            for event in events:
                if event.type == pygame.QUIT:
                    self.g.log("[INFO] Program closed, shutting down...")
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.g.resize(event)
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.g.log("[INFO] Escape key pressed, closing...")
                        running = False
                    keys.append(event)

            #create the pack to send to the bot
            pack = "z" if self.legacy_packet else "a"
            for item in self.inputs:
                if isinstance(item,Joy):
                    temp = "0"
                    try:
                        temp = str(item.get(self.joysticks,self.precision))+';'
                    except Exception as e:
                        ez = str(e)
                        try:
                            ez += item.error()
                        except: pass
                        self.error(ez,True)
                    pack += temp
                elif isinstance(item,Key):
                    temp = "0"
                    try:
                        temp = str(item.get(keys)) + ';'
                    except Exception as e:
                        ez = str(e)
                        try:
                            ez += item.error()
                        except: pass
                        self.error(ez,True)
                    pack += temp
                else:
                    temp = "0"
                    try:
                        temp = item.get(keys, self.joysticks, self.precision) + ";"
                    except Exception as e:
                        self.error(e)
                    pack += temp
                        
            pack += 'z' if not self.legacy_packet else ""

            #send it
            if self.mode == 1:
                try:
                    self.serial.write(bytes(pack,'utf-8'))
                except serial.SerialTimeoutException:
                    self.g.log("[WARNING] Serial Timed out, attempting to reconnect...",self.g.red)
                    self.serial = self.connect(True)
                except Exception as e:
                    self.g.log("[WARNING] Could not send package to robot",self.g.red)
                    self.error(e,False)

            #render
            self.g.render(self.inputs,pack)
        self.g.bail()
        pygame.quit()
        sys.exit()

    #connects to robot on COM port
    def connect(self,reconnect = False):
        if reconnect:
            self.g.log("[NOTICE] Trying to auto-reconnect... takes 10-15 seconds",self.g.orange)
            self.g.render_stack()
            pygame.display.update()
            self.serial.close()
            while self.serial.is_open:
                time.sleep(0.1)
        try:
            s = serial.Serial(self.com,self.baudrate,write_timeout = 0.1)
            if s.is_open:
                if reconnect:
                    self.g.log("[INFO] Reconnected! GoGoGo!",self.g.green)
                return s
        except Exception as e:
            self.g.log("[WARNING] Could not connect to robot on specified COM port",self.g.red)
            self.error(e,False)

        if self.autoport == True and reconnect == False:
            for i in range(1,15):
                com = "COM" + str(i)
                try:
                    s = serial.Serial(com,self.baudrate,write_timeout = 0.1)
                    self.com = com
                    return s
                except:
                    time.sleep(0.2)
                    self.g.log("[WARNING] Could not connect to robot on %s"%(com),self.g.red)
        if not reconnect:
            self.g.log("[WARNING] Could not connect to robot on ANY port",self.g.red)
            self.error("Unable to connect to robot")
        if reconnect:
            return self.connect(True)

    #logs an error
    def error(self,e,kill=True):
        self.g.log("[WARNING] Error logged as: %s"%(e), self.g.red)
        if kill:
            self.g.log("[INFO] Driver Station has stopped, press any key to exit.", self.g.orange)
            self.g.render_stack()
            pygame.display.update()
            while True:
                kill = False
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT :
                        kill = True
                if any(pygame.key.get_pressed()) or kill == True:
                    self.g.bail()
                    sys.exit()

cool = driver()
