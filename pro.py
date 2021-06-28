from tkinter import *
import tkinter
from tkinter import ttk
#frame raising function
def raise_frame(frame):
    frame.tkraise()
window = Tk()

f1 = Frame(window,bg='#05386B')
f2 = Frame(window,bg='#05386B')
f3 = Frame(window,bg='#05386B')

window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)


for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')
    
#selected fluid data dictionary which will be updated
fld = {"w":0.012,
"pC":45.99 * 10**5,
"tC" :190.6,
"R":8.31}#pressure is in pascal and temp is in K

#frame 1 code

calZV = Button(f1, text='CALCULATE Z AND V',font=("Courier", 16), command=lambda:raise_frame(f2))
calZP = Button(f1, text='CALCULATE Z AND P',font=("Courier", 16), command=lambda:raise_frame(f3))

calZV.place(x=125,y=230)
calZP.place(x=125,y=280)

head = Label(f1, text="CALCULATE Z, MOLAR VOLUME, \nPRESSURE USING PITZER \nSECOND VIRIAL COEFFICIENT ",font=("Courier", 15))
head.place(x=50,y=10)
head.config(height = 6,width=35)

bottom = Label(f1,text= "Project by:\n Himanshu Khadatkar ",font=("Courier", 12))
bottom.place(x=150,y=400)

#frame 2 code

Button(f2, text='HOME PAGE',font=("Courier", 12), command=lambda:raise_frame(f1)).pack(side=BOTTOM)
Button(f2, text='CALCULATE Z AND P',font=("Courier", 12), command=lambda:raise_frame(f3)).pack(side=BOTTOM)

#background and heading
heading = Label(f2, text="CALCULATE Z AND MOLAR VOLUME",font=("Courier", 15))
heading.place(x=80,y=10)

#select fluid
h1 = Label(f2, text="Select Fluid",font=("Courier", 14))
h1.place(x=200,y=50)

#selecting fluid combobox
lb = Label(f2, text="  Fluid  ")
lb.place(x=180,y=100)
fluid_d= StringVar()
fluid_data=('Methane','Ethane','Propane','n-Butane','n-Pentane','n-Hexane',
            'Isobutane','Methanol','Ethanol','Acetone','Carbon dioxide','Ammonia'
            )
fluid_d.set('Methane')
cb=ttk.Combobox(f2, values=fluid_data,state="readonly")
cb.place(x=250, y=100)
cb.current(0)



#sselect units
h1 = Label(f2, text="Select Units",font=("Courier", 14))
h1.place(x=200,y=150)

#pressure units
lbl1=Label(f2, text="Unit Of Pressure to be entered")
lbl1.place(x=60, y=200)
pressureUnits = StringVar()
data1=('Pascal','Barr','MM of Hg','Atm')
pressureUnits.set("Pascal")
cb1=ttk.Combobox(f2, values=data1,state="readonly")
cb1.place(x=300, y=200)
cb1.current(0)


#temperature units
lbl2=Label(f2, text="Unit Of Temperature to be entered")
lbl2.place(x=60, y=230)
TempUnits = StringVar()
data2=('Kelvin','Celsius')
TempUnits.set('kelvin')
cb2=ttk.Combobox(f2, values=data2,state="readonly")
cb2.place(x=300, y=230)
cb2.current(0)

#volume units
lbl3=Label(f2, text="Unit Of Volume to be obtained")
lbl3.place(x=60, y=260)
VolUnits = StringVar()
data3=('cubic meter per mole ','Litre per mole')
VolUnits.set('cubic meter per mole')
cb3=ttk.Combobox(f2, values=data3,state="readonly")
cb3.current(0)
cb3.place(x=300, y=260)


##data entry
h2 = Label(f2, text="Enter Data",font=("Courier", 14))
h2.place(x=200,y=310)

#pressure entry
lb4 = Label(f2, text="Pressure ")
lb4.place(x=60,y=360)
pressure =Entry(f2,textvariable=IntVar())
pressure.place(x=150,y=360)

#temperature entry
lb5 = Label(f2, text="Temperature ")
lb5.place(x=60,y=390)
temperature=Entry(f2,textvariable=IntVar())
temperature.place(x=150,y=390)

#result label
msg1 = Label(f2)



def getOutput():
#updating fld dictionary based on selected fluid
    import pandas as pd
    fdata = pd.read_csv('fluid_dataset.csv')
    temp={}
    for i in range(0,fdata.shape[0]):
        if(fdata.iloc[i]['fluid']==cb.get()):
            temp['w'] =float(fdata.iloc[i]['w'])
            temp['tC']=float(fdata.iloc[i]['tC'])
            temp['pC']=float(fdata.iloc[i]['pC'])
            temp['R'] =float(fdata.iloc[i]['R'])

    fld.update(temp)

    press=float(pressure.get())
#('Pascal','Barr','MM of Hg','Atm')   
    if cb1.get()=="Barr":
        press = press*100000
    elif cb1.get()=="MM of Hg":
        press = press*133.322
    elif cb1.get()=="Atm":
        press = press*101325
    
    temp =float(temperature.get())
#'Kelvin','Celsius'
    if cb2.get()=="Celsius":
        temp=temp+273.3
        
        
        
        
    if(press!=0 and temp!=0):
        if(verifyP(press,temp)):
            inst = calculateZV(press,temp)
            z =  round(inst.calculateZ(),5)
            v =  inst.calculateV()

            #'cubic meter per mole ','Litre per mole'  
            if cb3.get()=="Litre per mole":
                v = v*1000

            v =  round(v,5)
            t =  f'Compression factor: {z}\n Molar Volume : {v} '
            msg1.config(text=t,font=("Arial", 11))
            msg1.place(x=155,y=490)


        else:
            t='Pitzer corelation for the second virial coefficient will not \n appropriate for the given pressure and temperature'
            msg1.config(text=t,font=("Arial", 11))
            msg1.place(x=80,y=490)
     
    else:
        t='Enter positive values for pressure and temperature '
        msg1.config(text=t,font=("Arial", 11))
        msg1.place(x=90,y=490)

        
        
        
        
def verifyP(press,temp):
    tr = temp/fld['tC']
    pr = press/fld['pC']
    if (tr>3):
        return True
    else:
        pmax = 1.983856 + (0.2237026 - 1.983856)/(1 + (tr/1.238929)**10.93594)
        if(pr<=pmax):
            return True
        else:
            return False
           
    

#results button
results = Button(f2,text="Calculate Z and V",font=("Courier", 14),command=getOutput)
results.place(x=155,y=440)
results['background']='#8EE4AF'
#hover the button
def onEnter(event):
    results.config(bg='#CAFAFE')
def onLeave(event):
    results.config(bg='#8EE4AF')
    
results.bind('<Enter>', onEnter)
results.bind('<Leave>',onLeave)




class calculateZV():
    def __init__(obj,pressure,temperature):
        obj.pressure  = pressure
        obj.temperature = temperature
   

    
    def calculateZ(instance):
        pR = instance.pressure/fld.get('pC')
        tR = instance.temperature/fld.get('tC')
        w = fld.get('w')
        b0 = 0.083-(0.422/tR**1.6)
        b1 = 0.139-(0.172/tR**4.2)
        Z0 = 1+b0*pR/tR
        Z1 = b1*pR/tR
        global Z
        Z = Z0 + w*Z1
        return Z
    def calculateV(instance):
        V = (fld.get('R') * Z * instance.temperature)/instance.pressure
        return V

#frame 3 code

Button(f3, text='HOME PAGE',font=("Courier", 12), command=lambda:raise_frame(f1)).pack(side=BOTTOM)
Button(f3, text='CALCULATE Z AND VOLUME',font=("Courier", 12), command=lambda:raise_frame(f2)).pack(side=BOTTOM)

#background and heading
heading = Label(f3, text=" CALCULATE Z AND PRESSURE ",font=("Courier", 15))
heading.place(x=80,y=10)

#select fluid
h1 = Label(f3, text="Select Fluid",font=("Courier", 14))
h1.place(x=200,y=50)

#selecting fluid combobox
lb = Label(f3, text="  Fluid  ")
lb.place(x=180,y=100)
fluid_d= StringVar()
fluid_data=('Methane','Ethane','Propane','n-Butane','n-Pentane','n-Hexane',
            'Isobutane','Methanol','Ethanol','Acetone','Carbon dioxide','Ammonia'
            )
fluid_d.set('Methane')
cb=ttk.Combobox(f3, values=fluid_data,state="readonly")
cb.place(x=250, y=100)
cb.current(0)



#sselect units
h1 = Label(f3, text="Select Units",font=("Courier", 14))
h1.place(x=200,y=150)

#volume units
lbl1=Label(f3, text="Unit Of Volume to be entered")
lbl1.place(x=60, y=200)
VolumeUnits = StringVar()
data1=('cubic meter per mole ','Litre per mole')
VolumeUnits.set('cubic meter per mole')
cb1=ttk.Combobox(f3, values=data1,state="readonly")
cb1.place(x=300, y=200)
cb1.current(0)

#temperature units
lbl2=Label(f3, text="Unit Of Temperature to be entered")
lbl2.place(x=60, y=230)
TempUnits = StringVar()
data2=('Kelvin','Celsius')
TempUnits.set('kelvin')
cb2=ttk.Combobox(f3, values=data2,state="readonly")
cb2.place(x=300, y=230)
cb2.current(0)

#pressure units
lbl3=Label(f3, text="Unit Of Pressure to be obtained")
lbl3.place(x=60, y=260)
VolUnits = StringVar()
data3=('Pascal','Barr','MM of Hg','Atm')
VolUnits.set('Pascal')
cb3=ttk.Combobox(f3, values=data3,state="readonly")
cb3.current(0)
cb3.place(x=300, y=260)


##data entry
h2 = Label(f3, text="Enter Data",font=("Courier", 14))
h2.place(x=200,y=310)

#pressure entry
lb4 = Label(f3, text="Volume ")
lb4.place(x=60,y=360)
volume =Entry(f3,textvariable=IntVar())
volume.place(x=150,y=360)

#temperature entry
lb5 = Label(f3, text="Temperature ")
lb5.place(x=60,y=390)
temperature=Entry(f3,textvariable=IntVar())
temperature.place(x=150,y=390)

#result label
msg2 = Label(f3)



def getOutput():
#updating fld dictionary based on selected fluid
    import pandas as pd
    fdata = pd.read_csv('fluid_dataset.csv')
    temp={}
    for i in range(0,fdata.shape[0]):
        if(fdata.iloc[i]['fluid']==cb.get()):
            temp['w'] =float(fdata.iloc[i]['w'])
            temp['tC']=float(fdata.iloc[i]['tC'])
            temp['pC']=float(fdata.iloc[i]['pC'])
            temp['R'] =float(fdata.iloc[i]['R'])

    fld.update(temp)

    
    vol=float(volume.get())
 #'cubic meter per mole ','Litre per mole'  
    if cb1.get()=="Litre per mole":
        vol = vol*0.001
        
    temp =float(temperature.get())
#'Kelvin','Celsius'
    if cb2.get()=="Celsius":
        temp=temp+273.3
    
    
        
        
    
    if(vol!=0 and temp!=0):
        if(verifyP(vol,temp)):
            inst = calculateZP(vol,temp)
            z =  round(inst.calculateZ(),5)
            p =  inst.calculateP()

            #('Pascal','Barr','MM of Hg','Atm')   
            if cb3.get()=="Barr":
                p = p*0.00001
            elif cb3.get()=="MM of Hg":
                p = p*0.00750062
            elif cb1.get()=="Atm":
                p = p*0.000009869
            p =  round(p,5)
            t =  f'Compression factor: {z}\n Pressure : {p} '
            msg2.config(text=t,font=("Arial", 11))
            msg2.place(x=155,y=490)


        else:
            t='Pitzer corelation for the second virial coefficient will not \n appropriate for the given pressure and temperature'
            msg2.config(text=t,font=("Arial", 11))
            msg2.place(x=80,y=490)
     
    else:
        t='Enter positive values for Volume and temperature '
        msg2.config(text=t,font=("Arial", 11))
        msg2.place(x=90,y=490)

        
        
        
        
def verifyP(vol,temp):
    press = (8.314*temp)/(vol)
    tr = temp/fld['tC']
    pr = press/fld['pC']
    if (tr>3):
        return True
    else:
        pmax = 1.983856 + (0.2237026 - 1.983856)/(1 + (tr/1.238929)**10.93594)
        if(pr<=pmax):
            return True
        else:
            return False
           
    

#results button
results = Button(f3,text="Calculate Z and P",font=("Courier", 14),command=getOutput)
results.place(x=155,y=440)
results['background']='#8EE4AF'
#hover the button
def onEnter(event):
    results.config(bg='#CAFAFE')
def onLeave(event):
    results.config(bg='#8EE4AF')
    
results.bind('<Enter>', onEnter)
results.bind('<Leave>',onLeave)




class calculateZP():
    def __init__(obj,volume,temperature):
        obj.volume  = volume
        obj.temperature = temperature
   

    
    def calculateP(instance):
        v = instance.volume
        t = instance.temperature
        tC = fld.get('tC')
        tR = t/tC
        pC = fld.get('pC')
        w = fld.get('w')
        b0 = 0.083-(0.422/tR**1.6)
        b1 = 0.139-(0.172/tR**4.2)
        B = b0 + w*b1
        b = B*8.314*tC/pC
        
        p = 8.314*t/(v-b)
        return p
    def calculateZ(instance):
        p = instance.calculateP()
        Z = (p * instance.volume)/(instance.temperature*8.314)
        return Z

raise_frame(f1)
window.title('Second Virial Corelation for Z V P T')
window.geometry("500x600+100+100")
window.mainloop()