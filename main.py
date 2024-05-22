"""
    DEVELOPED BY : RAMESHKUMAR V
    DATE         : MAY 1-10 2024
    VERSION      : final  
"""


import clear_frame 
import customtkinter as ck
import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import Image, ImageTk
import time
import io
from tkinter import ttk
import sys
import os
import sqlite3 as sql



# GLOBALS
global setbuttons
global mainwindow
global id_remover


# RESOURCES PATH
def resources_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# DATABASE 

global con
con=sql.connect(resources_path("assets\\votingdb.db"))

# ALL NEEDED DATA FILE



global ID, PASSWORD
global NOMINEES_INFO

totalnomines_counter = 0


NOMINEES_INFO: list = []

IMAGES: list = []

ID = None
PASSWORD = None





def read_refresher_for_count():
    server = con.cursor()

   
   

    sql = "select * from nominees"
    server.execute(sql)
    nomdatas = server.fetchall()
    global NOMINEES_INFO
    NOMINEES_INFO=[]


    for j in nomdatas:
        NOMINEES_INFO.append({
            'NOMINEE_ID':j[0],
            'NOMINEE_NAME' : j[1],
            'NOMINEE_RESULT': j[2],
            'NOMINEE_LOGO': j[3]
        })

        

   

        
    

     













window = tk.Tk()
root1=window
 #ck.CTk()
window.title('mainpage')
window.geometry('2000x1000')
window.config(background="#93FBF2")
window.state("zoomed")

# VOTING PAGE






def voting_page():
    root1=window
     # Fills the available space

    votingframe =ck. CTkScrollableFrame(master=root1)
    votingframe.pack(fill="both", expand=True)
   
    def put_vote(b):
        VOTED=None
        for nom in NOMINEES_INFO:
            print('b is =',b)
            print('nom=',nom['NOMINEE_ID'])

            if int(nom['NOMINEE_ID'])==int(b):
                
                nom['NOMINEE_RESULT']=nom['NOMINEE_RESULT']+1
                
                messagebox.showinfo("Message", f" Voted Successfully : {nom['NOMINEE_RESULT']} ! ")

                try:
                    server = con.cursor()

                    sql = "UPDATE nominees SET nomresult=? WHERE id=?"
                    data = ( nom['NOMINEE_RESULT'],b)

                    server.execute(sql, data)
                    response=server.fetchall()
                    

                    con.commit()

                    read_refresher_for_count()

                except Exception as e:
                    print(e)
                    messagebox.showwarning('warning',f'{type(e).__name__}')
        else:
            print('error: voter id not found')

        

        

        votingframe.destroy()
        mainwindow()
        #voting_page()




    OFFSET=0
    ROW=0
    image2=Image.open(resources_path("assets//voteicon.png")).resize((50,50))
    photo2=ImageTk.PhotoImage(image2)
    for i in NOMINEES_INFO:
        
       
        

        NOM_LABEL= ck.CTkLabel(votingframe, text=f"NOMINEE {ROW} : " + i['NOMINEE_NAME'],height=5,width=50, font=("Times New Roman", 25, "bold"))
        nominee_logo_data = i['NOMINEE_LOGO']


        logo_image = Image.open(io.BytesIO(nominee_logo_data))
        logo_image_resized = logo_image.resize((80, 80))
        logo_tk = ImageTk.PhotoImage(logo_image_resized)



        NOM_LOGO=tk.Label(votingframe, image=logo_tk)
        NOM_LOGO.image = logo_tk 
        NOM_BTN=tk.Button(votingframe, text='vote',image=photo2,command=lambda: (votingframe.destroy(),put_vote(int(i['NOMINEE_ID']))))
        NOM_BTN.image=photo2

        NOM_LABEL.grid(row=ROW,column=1,padx=100,pady=20)
        NOM_LOGO.grid(row=ROW,column=0,padx=100,pady=20)
        NOM_BTN.grid(row=ROW,column=2,padx=100,pady=20)

        OFFSET=OFFSET+1
        ROW=ROW+1




# SETTING 

def setting(mainframe):
    

    global security,setbuttons,fun




    def security(fun):
        root1=window

        mainframe.destroy()
        securityframe=tk.Frame(root1,background="#D6F6F2")
        securityframe.pack(anchor="center",pady=200)

        def process():
                a = str(id_entry.get())
                b = str(pass_entry.get())

                if a == 'rkking' and b == '1234':

                    messagebox.showinfo("Message", "Access Granted ! ")
                    securityframe.destroy()

                    return fun()
                
                else:
                    messagebox.showerror("Message", "Access Denied ! ")



        
        id_label = ck.CTkLabel(securityframe, text="ENTER ID       ", font=('', 40, "bold"))
        pass_label = ck.CTkLabel(securityframe, text="ENTER PASS  ", font=('', 40, "bold"))

        id_entry = ck.CTkEntry(securityframe, height=40, width=200)
        pass_entry = ck.CTkEntry(securityframe, height=40, width=200)

        buttoning = ck.CTkButton(securityframe, text="Proceed ! ", command=process)

        exit_button = ck.CTkButton(securityframe, text="EXIT",command=lambda :(securityframe.destroy(),mainwindow()))
        exit_button.grid(row=0,column=0)

        id_label.grid(row=2,column=2,padx=50,pady=40)
        id_entry.grid(row=2,column=3,padx=50,pady=0)
        pass_label.grid(row=4,column=2,padx=50,pady=10)
        pass_entry.grid(row=4,column=3,padx=50,pady=0)
        buttoning.grid(row=6,column=3,padx=50,pady=20)






    def resetall():
       
        def reset():

            server = con.cursor()
            sql = "update nominees set nomresult=0"
            server.execute(sql)
            con.commit()
            messagebox.showinfo("Message", "Reseted Suceesfully")

        security(reset)


            
    def Add_voter():
       
        def add_to_DB():

 
            m: str = str(adhaar_entry_.get()) if str(adhaar_entry_.get()).strip()!='' else messagebox.showerror('message',
                                                                                                            'Id missing')
            n: str = str(dob_entry_.get()) if str(dob_entry_.get()).strip()!='' else messagebox.showerror('message',
                                                                                                        'Passward missing')
            if m and n:

                server = con.cursor()
                sql = "insert into voters(votername,voterpass,STATUS) values (?,?,'notvoted')"
                user = (m, n)
                server.execute(sql, user)
                con.commit()

                adhaar_entry_.delete(0, tk.END)
                dob_entry_.delete(0, tk.END)
                messagebox.showinfo("Message", "VOTER ADDED SUCCESSFULLY ! ")
            else:
                messagebox.showwarning('message', 'id and pass is incorrect they extend long ! ')

        def id_appending():
            root1=window
            global adhaar_fetcher, dob_fetcher, adde, adhaar_entry_, dob_entry_


            addingfram=tk.Frame(root1,bg="#D6F6F2")
            addingfram.pack(anchor="center")

            exit_button = ck.CTkButton(addingfram, text="EXIT",
                                       command=lambda: (addingfram.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)


            #exit_button.configure(command=destroyer5)
            adhaar_fetcher = ck.CTkLabel(addingfram, text="USERNAME", font=('', 30, "bold"))

            adhaar_entry_ = ck.CTkEntry(addingfram, height=40, width=200)

            dob_fetcher = ck.CTkLabel(addingfram, text="PASSWORD", font=('', 28, "bold"))
            dob_entry_ = ck.CTkEntry(addingfram,  height=40, width=200)

            adde = ck.CTkButton(addingfram, text="ADD", command=add_to_DB)

            adhaar_fetcher.grid(row=3,column=2,padx=40,pady=20)
            adhaar_entry_.grid(row=3,column=3,padx=40,pady=0)

            dob_fetcher.grid(row=4,column=2,padx=40,pady=20)
            dob_entry_.grid(row=4,column=3,padx=40,pady=0)

            adde.grid(row=6,column=3,padx=40,pady=20)
        security(id_appending)


    def logs():
        root1=window
        
        def show_logs():
            logsframe=tk.Frame(root1,bg="#D6F6F2")
            logsframe.pack(anchor="center",pady=100)

            exit_button = ck.CTkButton(logsframe, text="EXIT",
                                       command=lambda: (logsframe.destroy(), mainwindow()))
            exit_button.pack(anchor='nw')
            try:
                server = con.cursor()
                sql = "select * from logindetails"
                server.execute(sql)

                file = server.fetchall()
            except Exception as e:
                messagebox.showwarning('','logs error !')
            if file:
                print("file founded")

            else:
                print("logs details not founded")

            print(file)
            table = ttk.Treeview(logsframe)
            table['show'] = 'headings'
            table.pack()
            table['columns'] = ['LOG ID', 'LOG TIME']

            table_design = ttk.Style(logsframe)
            table_design.theme_use('clam')
            table_design.configure('.', foreground=('black'), font=('Times New Roman', 15, 'bold'))
            table_design.configure('Treeview.Heading', foreground=('red'), font=('Times New Roman', 20, 'bold'))

            table.heading('LOG ID', text='LOG ID')
            table.heading('LOG TIME', text='LOG TIME')

            table.column('LOG ID', width=400, minwidth=400, anchor='center')
            table.column('LOG TIME', width=400, minwidth=400, anchor='center')
            j = 1
            for i in (file):
                
                table.insert('', j, values=(i))
                j = j + 1
         
        security(show_logs)

    def results():
        
        def show_results():
            resultpage=tk.Frame(root1,bg="#D6F6F2")
            resultpage.pack(anchor="center",
                            expand=True,
                            fill='both')

            exit_button = ck.CTkButton(resultpage,
                                        text="EXIT",
                                       command=lambda: (resultpage.destroy(), mainwindow()))
            exit_button.pack(anchor='center',fill='both')
           

         

            read_refresher_for_count()
            table = ttk.Treeview(resultpage,padding=20,height=1000)
            table['show'] = 'headings'
            table.pack(fill='both')
            table['columns'] = ['SI NO', 'NAME','RANK','RESULT']

            table.heading('SI NO', text='SI NO')
            table.heading('NAME', text='NAME')
            table.heading('RANK', text='RANK')
            table.heading('RESULT', text='RESULT')
            table_design = ttk.Style(resultpage)
            table_design.theme_use('clam')
            #table_design.configure('Custom.Treeview',rowheight=100, foreground=('black'), font=('Times New Roman', 40, 'bold'))
            table_design.configure('.',rowheight=100, foreground=('black'), font=('Times New Roman', 20))
            table_design.configure('Treeview.Heading', foreground=('red'), font=('Times New Roman', 25, 'bold'))
            

            ROW=1
            file=NOMINEES_INFO

            table.column('SI NO',width=400, minwidth=400, anchor='center')
            table.column('NAME', width=400, minwidth=400, anchor='center')
            table.column('RANK', width=400, minwidth=400, anchor='center')
            table.column('RESULT', width=400, minwidth=400, anchor='center')
            
            
            for i in (file):
                
                table.insert('', ROW, values=(i['NOMINEE_NAME'],'a','b','c'))
                ROW = ROW + 1
            
           
                

            winner: str = None



            global result_winner
            result_winner = ck.CTkLabel(resultpage, text=f"WINNER : {winner}", font=("Times New Roman", 50, "bold"))
            result_winner.pack(anchor='center')
            winner = None
        #security(3)
        mainframe.destroy()
        show_results()


    def settings_for_self_image():
       
        

        def imagechange():

            def pathselector():
                def process(path):
                    def convert_binary(filepath):
                        try:
                            with open(filepath, 'rb') as f:
                                binarydata = f.read()
                                return binarydata
                        except Exception as e:
                            messagebox.showerror('warning on binary function !', f'{e}')


                    def update():

                        try:
                            #sql=("update image set iim=(%s) where iid=(%s)")
                            paths=convert_binary(path)
                            ids=int(c.get())
                            values=(paths,)
                            server = con.cursor()
                            sql = "update image set iim=(?) where iid=(?)"

                            server.execute(sql,(paths,ids))
                            con.commit()
                            messagebox.showinfo('','success !')
                        except Exception as e:
                            messagebox.showwarning('',f'{type(e).__name__}')
                    update()
                try:
                    filepath=filedialog.askopenfilename(filetypes=[("JPG File","*.jpg"),("PNG File","*.png"),("Image Files","*.webp")])
                    if filepath:
                        messagebox.showinfo('','Path selected!')
                        pbut=ck.CTkButton(imageframe,text='UPDATE',command=lambda: process(filepath))
                        pbut.grid(row=5,column=2,pady=50)
                    else:
                        messagebox.showwarning('','user cancelled the operation !')
                except Exception as e:
                    messagebox.showerror('',f'{type(e)}')
            imageframe=tk.Frame(root1,bg="#D6F6F2")
            imageframe.pack(pady=100)
            global c

            tk.Label(imageframe,text='SELECT NOMINEE ID ',font=('',20)).grid(row=1,column=2,padx=40,pady=10)
            c=ttk.Combobox(imageframe,values=([i['NOMINEE_ID'] for i in NOMINEES_INFO]))
            c.grid(row=2,column=2,padx=40,pady=10)
            c.set('1')
            tk.Label(imageframe, text='SELECT IMAGE PATH',font=('',20)).grid(row=3,column=2,padx=40,pady=10)
            b=ck.CTkButton(imageframe,text='PATH',command=pathselector)
            b.grid(row=4,column=2,padx=40,pady=10)
            exit_button = ck.CTkButton(imageframe, text="EXIT",
                                       command=lambda: (imageframe.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)
        #security(imagechange)
        mainframe.destroy()
        imagechange()


    def settings_for_self():
        read_refresher_for_count()
        #security(4)
        
        global nameset
        def nameset():
            def upd_name(namew,id):
                name=str(namew.get())
                print('Name is : ',name)
                if name.strip()=='':
                    messagebox.showerror('',"Name Not changed becuase empty string!")
                    return 0
                try:
                    server=con.cursor()
                    
                    sql="update nominees set nomname=(?) where id=(?)"
                    query=(name,id)
                    server.execute(sql,query)
                    con.commit()

                    messagebox.showinfo('',"Name changed !")
                except Exception as e:
                    messagebox.showerror('',"Name Not changed !")
                    print(e)
                    pass
                finally:
                    server.close()



            nameframe=tk.Frame(root1,bg="#D6F6F2",height=2000,width=2000)
            nameframe.pack(fill='both',anchor='center',padx=100,pady=100)
            read_refresher_for_count()

            ROW=1            
            def on_select(new_name,id):

                name_in.delete(0,tk.END)
                name_in.insert(0, f"{str(new_name)}")

                button= ck.CTkButton(nameframe, text="UPDATE", command=lambda entry=name_in, id=id: upd_name(entry, id))
                button.grid(row=ROW,column=3,padx=40,pady=10)
                
            spinbox = ttk.Menubutton(nameframe, text="Select")
            spinbox.menu = tk.Menu(spinbox, tearoff=False)
            spinbox["menu"] = spinbox.menu
            name_in=ck.CTkEntry(nameframe,width=200)
            name_in.grid(row=1,column=2,padx=40,pady=10)
            spinbox.grid(row=1,column=0,padx=40,pady=10)
           
            for i in (NOMINEES_INFO):
            
                spinbox.menu.add_radiobutton(label=f"{i['NOMINEE_ID']}", command=lambda : on_select(i['NOMINEE_NAME'],i['NOMINEE_ID']))

                
                
            exit_button = ck.CTkButton(nameframe, text="EXIT",
                                       command=lambda: (nameframe.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)
        nameset()
        mainframe.destroy()
    
    def SET_DEL_NOM():
        read_refresher_for_count()
        #security(4)
        
        global nameset
        def del_to_DB():
            def upd_name(id):
                
                
                if not id:
                    messagebox.showerror('',"Nominee Not  becuase empty !")
                    return 0
                try:
                    server = con.cursor()
                    sql = "DELETE FROM nominees WHERE id = ?"
                    id = int(id)
                    server.execute(sql, (id,))
                    con.commit()
                    if server.rowcount > 0:
                        messagebox.showinfo('', "Nominee Deleted Successfully !")
                        selected_id_V.configure(text='')
                        selected_Name_V.configure(text='')
                        # button.destroy()
                    else:
                        messagebox.showinfo('', "No nominee found with id = 6")


                except Exception as e:
                    messagebox.showerror('',"Nominee Not Deleted!")
                    print(e)
                    pass
                finally:
                    server.close()



            nameframe=tk.Frame(root1,bg="#D6F6F2",height=2000,width=2000)
            nameframe.pack(fill='both',anchor='center',padx=100,pady=100)
            read_refresher_for_count()

            ROW=5           
            def on_select(id):
                selected_id_V.configure(text=f'{id}')
                selected_Name_V.configure(text=f'{id}')

           

                button= ck.CTkButton(nameframe, text="DELETE", command=lambda  id=id: upd_name( id))
                button.grid(row=ROW,column=3,padx=40,pady=20)
                
            spinbox = ttk.Menubutton(nameframe, text="Select")
            spinbox.menu = tk.Menu(spinbox, tearoff=False)
            spinbox["menu"] = spinbox.menu
            
            spinbox.grid(row=1,column=0,padx=40,pady=10)

            selected_id_L=ck.CTkLabel(nameframe,text='SELECTED NOM ID : ')
            selected_Name_L=ck.CTkLabel(nameframe,text='SELECTED NOM NAME : ')
            selected_id_V=ck.CTkLabel(nameframe,text='')
            selected_Name_V=ck.CTkLabel(nameframe,text='')

            selected_id_L.grid(row=3,column=1,padx=40,pady=10)
            selected_Name_L.grid(row=4,column=1,padx=40,pady=10)
            selected_id_V.grid(row=3,column=2,padx=40,pady=10)
            selected_Name_V.grid(row=4,column=2,padx=40,pady=10)
            print('Nominee info is : ',NOMINEES_INFO)
           
            for i in (NOMINEES_INFO):
            
                spinbox.menu.add_radiobutton(label=f"{i['NOMINEE_ID']}", command=lambda : on_select(i['NOMINEE_ID']))

                
                
            exit_button = ck.CTkButton(nameframe, text="EXIT",
                                       command=lambda: (nameframe.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)
        del_to_DB()
        mainframe.destroy()
    
    def  setting_for_add_nom():
        global FILEPATH_LOGO

        FILEPATH_LOGO=None
        mainframe.destroy()
        def Add_Nom_data_to_db(name,fpath):
            def convert_binary(filepath):
                        try:
                            with open(filepath, 'rb') as f:
                                binarydata = f.read()
                                return binarydata
                        except Exception as e:
                            messagebox.showerror('warning on binary function !', f'{e}')
            try:
                cursor=con.cursor()

                sql="INSERT INTO nominees(nomname,nomresult,img) values (?,?,?)"
                logobin=convert_binary(fpath)
                data=(name,0,logobin)

                cursor.execute(sql,data)
                
                
                
                print('ok')
                messagebox.showinfo('Info','Added success')
                con.commit()
              
            except Exception as e:
                print('Error in nom add Section : ',e)
                con.rollback()
                cursor.close()

        def Nom_name_change_f():
            Nom_name=nom_name_i.get()
            


            if Nom_name.strip() and FILEPATH_LOGO:

                Add_Nom_data_to_db(Nom_name,FILEPATH_LOGO)

                pass
        def ask_Nom_logo_path():
            global FILEPATH_LOGO
            
            filepath=filedialog.askopenfilename(filetypes=[("JPG File","*.jpg"),("PNG File","*.png"),("Image Files","*.webp")])
            if filepath:
                        messagebox.showinfo('','Path selected!')
                        FILEPATH_LOGO=filepath
                       
            else:
                messagebox.showinfo('','Operation Cancelled by the User')

        add_nom_frame=tk.Frame(root1)
        add_nom_frame.pack()

        nom_name_l=ck.CTkLabel(add_nom_frame,text='Enter Nominee Name ')
        nom_name_i=ck.CTkEntry(add_nom_frame)
        

        nom_logo_l=ck.CTkLabel(add_nom_frame,text='Select Logo ')
        nom_logo_i=ck.CTkButton(add_nom_frame,text='Select path',command=ask_Nom_logo_path)

        nom_add_btn=ck.CTkButton(add_nom_frame,command=Nom_name_change_f)

        nom_name_l.grid(row=1,column=1,padx=20,pady=40)
        nom_name_i.grid(row=1,column=2,padx=20,pady=50)

        nom_logo_l.grid(row=2,column=1,padx=20,pady=40)
        nom_logo_i.grid(row=2,column=2,padx=20,pady=50)
        nom_add_btn.grid(row=3,column=3,padx=20,pady=10)

        pass



    def show_menu():
        root1=window
        global set_buttons
       

        menubar = tk.Menu(root1, tearoff=0,bg='#D6F6F2',font=('',10,'bold'))
        
        EDIT_VOTER=tk.Menu(root1,tearoff=0,bg='#D6F6F2',font=('',10,'bold'))
        EDIT_VOTER.add_command(label="ADD VOTER   ", command=Add_voter)

        DB_INFO=tk.Menu(root1,tearoff=0,bg='#D6F6F2',font=('',10,'bold'))
        DB_INFO.add_command(label="LOGS", command=logs)
        DB_INFO.add_command(label="RESULT Page", command=results)
        DB_INFO.add_command(label="RESET ALL RESULT", command=resetall)
        menubar.add_command(label="EXIT", command=lambda: root1.destroy())

        NOMINEE_EDIT=tk.Menu(root1,tearoff=0,bg='#D6F6F2',font=('',10,'bold'))

        NOMINEE_EDIT.add_command(label="ADD NOMINEE", command=lambda : setting_for_add_nom())
        NOMINEE_EDIT.add_command(label="DEL NOMINEE", command=SET_DEL_NOM)
        NOMINEE_EDIT.add_command(label="UPD NOM NAME", command=settings_for_self)
        NOMINEE_EDIT.add_command(label="UPD NOM IMAGE", command=settings_for_self_image)

        menubar.add_cascade(label='Nominee Edit',menu=NOMINEE_EDIT)
        menubar.add_cascade(label='Voters Edit',menu=EDIT_VOTER)
        menubar.add_cascade(label='Database Info',menu=DB_INFO)

        menubar.post(set_buttons.winfo_rootx(), set_buttons.winfo_rooty() + set_buttons.winfo_height())
        

    show_menu()


# MAIN FRAME


def mainwindow():
    root1=window
    clear_frame.clear_frame(window)

    read_refresher_for_count()

    global button, adhar_label, dob_label, adhar_entry, dob_entry

    mainframe=tk.Frame(root1,bg='#D6F6F2',height=600,width=1000)
    mainframe.pack(anchor="center",pady=100,padx=100,fill='both',ipadx=300)

    global set_buttons

    set_buttons = ck.CTkButton(mainframe, text='Setting', command=lambda : (setting(mainframe)))
    set_buttons.grid(row=0,column=0,padx=10,pady=10)
   
    adhar_label = ck.CTkLabel(mainframe, text="USERNAME", font=('', 30, 'bold'))
    adhar_label.grid(row=2,column=2,padx=100,pady=20,sticky='w')
    global adhar_entry

    adhar_entry = ck.CTkEntry(mainframe, height=40, width=300)
    adhar_entry.grid(row=3,column=2,padx=200)

    dob_label = ck.CTkLabel(mainframe, text='PASSWORD', font=('', 30, 'bold'))
    dob_label.grid(row=4,column=2,padx=100,pady=20,sticky='w')

    dob_entry = ck.CTkEntry(mainframe,show='*', height=40, width=300)
    dob_entry.grid(row=5,column=2,padx=200,pady=1,columnspan=40)


    button = ck.CTkButton(mainframe, text='Enter', height=40, width=100, command=lambda: (condition_checkers(mainframe)))
    button.grid(row=6,column=2,padx=40,pady=10,columnspan=40)


# APP TITLE
def title():
    mainframe2=tk.Frame(window,bg='#D6F6F2')
    mainframe2.pack(anchor="n",fill='both')

    title=ck.CTkLabel(mainframe2,text="ELECTION MANAGEMENT SYSTEM", width=1500,font=('', 40))
    title.grid(row=0,column=0,padx=40,pady=5,ipadx=50,sticky='nw')

# CONDITION CHECKING FUNCTIONS 


def condition_checkers(mainframe):

    def remove_voter(id):

        server=con.cursor()
        sql2="UPDATE voters SET STATUS='voted' where votername=(?)"
        value=(str(adhar_data),)
        server.execute(sql2,value)
        con.commit()
        server.close()
        print('updated successfully')
    
    def add_log(id):
        import time
        server=con.cursor()
        sql2="INSERT INTO logindetails(logername,logertime) VALUES (?,?)"
        value=(str(id),str(time.ctime()))
        server.execute(sql2,value)
        con.commit()
        server.close()
        print('voter added')


    adhar_data: str = str(adhar_entry.get())
    dob_data: str = str(dob_entry.get())
    adhar_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    
    

    server = con.cursor()

    sql="""SELECT CASE 
    WHEN COUNT(*) > 0 THEN True
    ELSE False
    END AS result
    FROM voters 
    WHERE votername = ? AND voterpass = ? AND STATUS='notvoted'"""
    values=(adhar_data,dob_data)


    server.execute(sql,values)
    result = server.fetchall()
    print(result)

    #try:

    if (result[0][0]):

        messagebox.showinfo("Message", "Welcome To Voting ! ")
        mainframe.destroy()
        
        voting_page()
        #remove_voter(adhar_data) # remove voter
        add_log(adhar_data) # add log details

        
    else:
        messagebox.showwarning("Messagebox", "User Not Found")
            
    # except Exception as e:
    #     print('error: loginsection',e)
    # finally:
    #     server.close()

if __name__=='__main__':
    title()
    read_refresher_for_count()
    mainwindow()
    #voting_page()
    #mainwindow(window)
    window.mainloop()
