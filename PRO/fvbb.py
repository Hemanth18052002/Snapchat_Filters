from tkinter import *
import dbm

import Face_mesh_filter_image
import Face_mesh_filter_set_of_images
import tug_life_filter_image

import Face_mesh_live
import Eyes_smoke_filter_cam
import Face_mesh_eyes_smoke
import tug_life_filter_cam

class main:
    
    def __init__(self):
        self.Authen_root = Tk()
        
        self.x = self.Authen_root.winfo_screenwidth()
        self.y = self.Authen_root.winfo_screenheight()
        
        ww = 500
        wh = 500
        
        self.Authen_root.geometry(f"{ww}x{wh}+{(self.x-ww)//2}+{(self.y-wh)//2}")
        
        self.Authen_root.title("Login")
        self.Authen_root.configure(bg='yellow')
        self.Authen_root.resizable(width=False, height=False)
        
        self.blank()
        
        fr = Frame(self.Authen_root,bg='yellow')
        
        graphical_image = PhotoImage(file="Touch.png")
        canvas = Canvas(self.Authen_root, width=300, height=200,bg='yellow',highlightbackground='yellow',highlightthickness=5)
        canvas.create_image(0, 0, anchor=NW, image=graphical_image)
        canvas.pack()
        
        self.blank()
        
        Label(fr, text="Username : ",font=('Times',18),bg='yellow').grid(row=0, column=0)
        Label(fr, text="Password : ",font=('Times',18),bg='yellow').grid(row=1, column=0)
        
        self.entry_username = Entry(fr)
        self.entry_username.grid(row=0, column=1)
        self.entry_password = Entry(fr, show="*")
        self.entry_password.grid(row=1, column=1)

        Button(fr, text="Login", command=self.Home).grid(row=2,column=1,sticky='ns')
        Label(fr, text="",bg='yellow').grid(row=3, column=0)
        Label(fr,text='Don\'t have an account?',font=('Helvetica', 12),bg='yellow').grid(row = 4,column = 0)
        Button(fr,text='Sign up',command=self.appen).grid(row = 4,column=1,sticky=W)

        fr.pack()
        self.Authen_root.mainloop()


    def appen(self):
        
        self.data = Tk()
        
        self.data.title('Sign up')
        self.data.configure(bg='yellow')
        
        ww = 500
        wh = 500
        
        self.data.geometry(f"{ww}x{wh}+{(self.x-ww)//2}+{(self.y-wh)//2}")
        
        
        fr1 = Frame(self.data,bg='yellow')
        for i in range(3):
            Label(fr1,text="",bg='yellow').grid(row=i,column=0)

        Label(fr1, text="Username : ",font=('Times',18),bg='yellow').grid(row=3, column=0)
        self.entry_user = Entry(fr1)
        self.entry_user.grid(row=3, column=1)
        
        Label(fr1, text="Password : ",font=('Times',18),bg='yellow').grid(row=4, column=0)
        self.entry_pass = Entry(fr1, show="*")
        self.entry_pass.grid(row=4, column=1)
        
        Button(fr1,text='Sign up',command=self.add).grid(row = 6,column=1,sticky=W)
        
        fr1.pack()
        self.data.mainloop()


    def Filter_on_Image(self):
        
        self.filter_image = Tk()
        self.filter_image.title('Filters on image')
        self.filter_image.configure(bg='yellow')
        self.filter_image.resizable(width=False, height=False)
        
        ww = 387
        wh = 400
        self.filter_image.geometry(f"{ww}x{wh}+0+0")
        
        self.splt(self.filter_image,2,'yellow')  
        ba = Button(self.filter_image,text="Face mesh filter on image",fg='black',command=self.f1)
        ba.pack()
        
        self.splt(self.filter_image,2,'yellow')
        ba1 = Button(self.filter_image,text="Face mesh filter on set of image",fg='black',command=self.f2)
        ba1.pack()
        
        self.splt(self.filter_image,2,'yellow')    
        ba2 = Button(self.filter_image,text="TUG LIFE on image",fg='black',command=self.f3)
        ba2.pack()
        
        self.filter_image.mainloop()
        
        
        
    def Filter_on_Cam(self):
        
        self.filter_image = Tk()
        self.filter_image.configure(bg='yellow')
        self.filter_image.title('Filters by cam')
        
        ww = 387
        wh = 400
        
        x = self.filter_image.winfo_screenwidth()-ww
        
        self.filter_image.geometry(f"{ww}x{wh}+{x}+0")
        self.filter_image.resizable(width=False, height=False)
        
        self.splt(self.filter_image,2,'yellow')
        ba = Button(self.filter_image,text="Face Mesh",fg='black',command=self.f4)
        ba.pack()
        
        self.splt(self.filter_image,2,'yellow')
        ba1 = Button(self.filter_image,text="Animated eyes with fire smoke",fg='black',command=self.f5)
        ba1.pack()
        
        self.splt(self.filter_image,2,'yellow')    
        ba2 = Button(self.filter_image,text="Face mesh Animated eyes with fire smoke",fg='black',command=self.f6)
        ba2.pack()
        
        self.splt(self.filter_image,2,'yellow')    
        ba3 = Button(self.filter_image,text="TUG LIFE on cam",fg='black',command=self.f7)
        ba3.pack()
        
        self.filter_image.mainloop()


    def add(self):
        
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        dbo = dbm.open('data','w')
        dbo[f'{username}'] = f'{password}'
        
        dbo.close()
        self.data.destroy()


    def Home(self):
        
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        dbo = dbm.open('data','r')
        
        if username in dbo:
            
            k = dbo[f'{username}'].decode()
            
            if k==password:
                
                la = Label(self.Authen_root,text='Correct Password',fg='green',bg='yellow')
                la.pack()
            
                self.Authen_root.destroy()
                self.Home_root = Tk()
                self.Home_root.resizable(width=False, height=False)
                
                x = self.Home_root.winfo_screenwidth()
                y = self.Home_root.winfo_screenheight()
                
                ww = 500
                wh = 500
                
                self.Home_root.geometry(f"{ww}x{wh}+{(x-ww)//2}+{(y-wh)//2}")
                
                self.Home_root.title("Snapchat Filter")
                self.Home_root.configure(bg='yellow')
                c = 'yellow'
                
                self.splt(self.Home_root,2,c)
                
                l1 = Label(self.Home_root,text="SNAPCHAT FILTERS",font=('Times',20),fg = 'black',bg='yellow')
                l1.pack()
                
                graphical_image = PhotoImage(file="logo.png")
                canvas = Canvas(self.Home_root, width=200, height=113,bg='yellow',highlightbackground='yellow',highlightthickness=5)
                canvas.create_image(0, 0, anchor=NW, image=graphical_image)
                canvas.pack()
                
                
                self.splt(self.Home_root,2,c)
                b1 = Button(self.Home_root,text="Apply on Image",fg='black',width=15,command=self.Filter_on_Image)
                b1.pack()

                self.splt(self.Home_root,2,c)
                b3 = Button(self.Home_root,text='Apply by cam',fg='black',width=15,command=self.Filter_on_Cam)
                b3.pack()
                
                self.Home_root.mainloop()
            
            else:
                
                new = Tk()
                new.title('Message')
                
                for _ in range(2):
                    label_blank = Label(new,text="")
                    label_blank.pack()
                    
                new.geometry(f"{300}x{150}+{(self.x-300)//2}+{(self.y-150)//2}")
                la = Label(new,text='*Incorrect Password',font=('Times',20),fg='red')
                la.pack()
                
                dbo.close()
                new.mainloop()
                
        else:
            
            new = Tk()
            new.title('Message')
            
            for _ in range(2):
                label_blank = Label(new,text="")
                label_blank.pack()
                
            new.geometry(f"{300}x{150}+{(self.x-300)//2}+{(self.y-150)//2}")
            
            la = Label(new,text='Invaild Credentials',font=('Times',20),fg='red')
            la.pack()
            
            la1 = Label(new,text='Try to sign up\n If you already sign up check username')
            la1.pack()
            
            new.mainloop()
            dbo.close()
            return


    def blank(self):
        
        blank = Frame(self.Authen_root)
        
        for _ in range(3):
            label_blank = Label(blank,text="",bg='yellow')
            label_blank.pack()
            
        blank.pack()
    
    
    def splt(self,root,n,c):
        
        for _ in range(n):
            t = Label(root,text="",bg=c)
            t.pack()
            
    def f1(self):
        k = Face_mesh_filter_image.mesh_image()
        k.apply()
        
    def f2(self):
        k = Face_mesh_filter_set_of_images.mesh_set_image()
        k.apply()
        
    def f3(self):
        k = tug_life_filter_image.tuglife_image()
        k.apply()
        
    def f4(self):
        k = Face_mesh_live.mesh_cam()
        k.apply()
        
    def f5(self):
        k = Eyes_smoke_filter_cam.smoke_cam()
        k.apply()
        
    def f6(self):
        k = Face_mesh_eyes_smoke.mesh_smoke_cam()
        k.apply()
        
    def f7(self):
        k = tug_life_filter_cam.tuglife_cam()
        k.apply()

if __name__ == '__main__':
    obj = main()