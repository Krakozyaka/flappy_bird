from tkinter import *
from random import *
import time
import tkinter.messagebox as mb


class Flappy_bird():
    def __init__(self,bestpoint = 0):
        self.cur_ar = []
        self.ar_id = []
        self.win = Tk()
        self.win.title('Flappy bird')
        self.win.resizable(0,0)
        self.width = 800
        self.height = 800
        self.canvas = Canvas(self.win, width = self.width,height = self.height, bg = 'LightSkyBlue1')
        self.canvas.pack()
        self.v = 40
        self.g = 10
        self.y0 = 400
        self.y = 100
        self.x = 100
        self.t = 0
        self.t2 = 0
        self.point = 0
        self.bestpoint = bestpoint
        self.label = Label(text = 'Ваш результат: ' + str(self.point) + ' Макс результат: ' +str(self.bestpoint))
        self.label.place(x = 500,y = 5)
        
        self.label2 = Label(text = 'Чтобы взлететь нажмите лкм или пробел')
        self.label2.place(x = 200,y = 5)
      

  
    def coord_bird(self):#изменение координат птицы
        self.y = int(self.y0 - self.v*self.t + self.g*(self.t**2)/2)
        #self.canvas.coords(self.bird,self.x-25,self.y-25,self.x+25,self.y+25)
        self.canvas.coords(self.bird,self.x+25,self.y+25)
        #print(self.canvas.coords(self.bird))
        
        
        
    def space(self):#реакция птицы на нажатие на пробел или лкм
        self.t = 0
        self.y0 = self.y
        self.flag = True

    def check_crash(self):
        #if (self.y<self.cur_ar[-3][0][3]) and (self.x+25>self.cur_ar[-3][0][2]+300*(self.last-3)-cnt-100):
        #print(len(self.canvas.find_overlapping(self.x-25,self.y-25,self.x+25,self.y+25)))
        #print(self.x-25,self.y-25,self.x+25,self.y+25)
        if len(self.canvas.find_overlapping(self.x,self.y,self.x+50,self.y+50))>1 or self.canvas.coords(self.bird)[1]<0 or self.canvas.coords(self.bird)[1]>800:
            
            self.win.bind('<space>', lambda event: None)
            self.win.bind('<Button-1>', lambda event: None)
       
            self.v = 1
            self.t = 0
            while self.canvas.coords(self.bird)[1]<=800:
                self.y0 = self.y
                self.t+=0.005
                self.coord_bird()
                self.win.update()
                time.sleep(0.005)
                
            return False
        return True

    def points(self):
        if len(self.ar_id)>=3:
            if self.canvas.coords(self.ar_id[-3][0])[2]-25==100 :
                self.point +=1
                self.label['text'] = 'Ваш результат: ' + str(self.point) + ' Макс результат: ' +str(self.bestpoint)

        
    def obstacle(self): # Препятствия задаются рандомом с разбросом в 100 пкс от предыдущего
        
        a = randint(100,500)
        self.cur_ar.append([[800,0,900,a],[800,a+200,900,800]])
        self.ar_id.append([self.canvas.create_rectangle(self.cur_ar[-1][0],fill = 'green'),self.canvas.create_rectangle(self.cur_ar[-1][-1],fill = 'green')])
        
        k = True
        cnt = 0
        #self.bird = self.canvas.create_oval(self.x-25,self.y-25,self.x+25,self.y+25,fill = 'yellow')#создание птицы
        img = PhotoImage(file="bird.png")
        self.bird = self.canvas.create_image(self.x+25,self.y0+25, image=img)        
        self.win.bind('<space>', lambda event: self.space())
        self.win.bind('<Button-1>', lambda event: self.space())
        while k:
            
            cnt += 1 # начало цикла про препятствия
            
            for i in range(len(self.ar_id)):
                self.canvas.coords(self.ar_id[i][0],self.cur_ar[i][0][0]+300*i-cnt,self.cur_ar[i][0][1],self.cur_ar[i][0][2]+300*i-cnt,self.cur_ar[i][0][3])
                self.canvas.coords(self.ar_id[i][1],self.cur_ar[i][1][0]+300*i-cnt,self.cur_ar[i][1][1],self.cur_ar[i][1][2]+300*i-cnt,self.cur_ar[i][1][3])
                self.canvas.lower(self.ar_id[i][0])
                self.canvas.lower(self.ar_id[i][1])
                self.last = i
                
            if self.cur_ar[-1][0][0] + 300*self.last - cnt == self.width - 300:
                if a>=600:
                    a = randint(a-200,599)
                elif a<=200:
                    a = randint(1,a+200)
                elif a<600 and a>200:
                    a = randint(a-200,a)
                self.cur_ar.append([[800,0,900,a],[800,a+180,900,800]])
                self.ar_id.append([self.canvas.create_rectangle(self.cur_ar[-1][0],fill = 'green'),self.canvas.create_rectangle(self.cur_ar[-1][-1],fill = 'green')]) # конец цикла про препятствия
            
            self.coord_bird()
            k = self.check_crash()
            self.cnt = cnt
            #time.sleep(0.001)
            self.points()
            self.t += 0.05
            self.win.update()

        if self.point>self.bestpoint:
            self.bestpoint = self.point
        
        if mb.askyesno("Вы проиграли","Ваш результат: " + str(self.point)+"\nЛучший результат: " + str(self.bestpoint)+"\nНачать сначала?")== True:
            
            self.canvas.delete('all')
            self.cur_ar = []
            self.ar_id = []
            self.v = 40
            self.g = 10
            self.y0 = 400
            self.y = 100
            self.x = 100
            self.t = 0
            self.t2 = 0
            self.point = 0
            self.label = Label(text = 'Ваш результат: ' + str(self.point) + ' Макс результат: ' +str(self.bestpoint))
            self.label.place(x = 500,y = 5)
            
            fb.obstacle()
            
       

fb = Flappy_bird()
fb.obstacle()
fb.win.mainloop()
