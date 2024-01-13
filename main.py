import customtkinter as ck
import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import Image, ImageTk
import time
import io
from tkinter import ttk
import mysql.connector
global mainwindow

con = mysql.connector.connect(
    host='localhost',
    user='rameshkumar',
    password='',
    database='votingapplication'
)

root1 = tk.Tk() #ck.CTk()
root1.title('mainpage')
root1.geometry('2000x1000')
root1.config(background="#93FBF2")
root1.state("zoomed")

image = Image.open("setbut.png").resize((40, 40))
photo = ImageTk.PhotoImage(image)

image2 = Image.open("voteicon.png").resize((80, 80))
photo2 = ImageTk.PhotoImage(image2)

global nominee_1, nominee_2, nominee_3, nominee_4, nominee_5, ID, PASSWORD

totalnomines_counter = 0

nominee_1 = 0
nominee_2 = 0
nominee_3 = 0
nominee_4 = 0
nominee_5 = 0

global nominee_1_name, nominee_2_name, nominee_3_name, nominee_4_name, nominee_5_name
ID = None
PASSWORD = None
nominee_1_name = None
nominee_2_name = None
nominee_3_name = None
nominee_4_name = None
nominee_5_name = None

# nota
global photo_5_, photo_4_, photo_3_, photo_2_, photo_1_

photo_1_ = ''
photo_2_ = ''
photo_3_ = ''
photo_4_ = ''
photo_5_ = ''


def read_refresher_for_count():
    server = con.cursor()

    global nominee_1, nominee_2, nominee_3, nominee_4, nominee_5, ID, PASSWORD, nominee_1_name, nominee_2_name, nominee_3_name, nominee_4_name, nominee_5_name
    global logo_1, logo_2, logo_2, logo_3, logo_4, logo_5
    global logo_1_, logo_2_, logo_3_, logo_4_, logo_5_
    global photo_1_, photo_2_, photo_3_, photo_4_, photo_5_

    sql = "select * from image"
    server.execute(sql)
    nomdatas = server.fetchall()
    #print(nomdatas[0][1])
    logo_1 = nomdatas[0][1]

    logo_2 = nomdatas[1][1]
    logo_3 = nomdatas[2][1]
    logo_4 = nomdatas[3][1]
    logo_5 = nomdatas[4][1]


    sql = "select * from nominees"
    server.execute(sql)
    nomdatas = server.fetchall()

    nominee_1_name = nomdatas[0][1]
    nominee_2_name = nomdatas[1][1]
    nominee_3_name = nomdatas[2][1]
    nominee_4_name = nomdatas[3][1]
    nominee_5_name = nomdatas[4][1]

    nominee_1 = int(nomdatas[0][2])
    nominee_2 = int(nomdatas[1][2])
    nominee_3 = int(nomdatas[2][2])
    nominee_4 = int(nomdatas[3][2])
    nominee_5 = int(nomdatas[4][2])

    try:

        logo_1_ = Image.open(io.BytesIO(logo_1)).resize((80, 80))
        photo_1_ = ImageTk.PhotoImage(logo_1_)

        logo_2_ = Image.open(io.BytesIO(logo_2)).resize((80, 80))

        photo_2_ = ImageTk.PhotoImage(logo_2_)

        logo_3_ = Image.open(io.BytesIO(logo_3)).resize((80, 80))
        photo_3_ = ImageTk.PhotoImage(logo_3_)

        logo_4_ = Image.open(io.BytesIO(logo_4)).resize((80, 80))
        photo_4_ = ImageTk.PhotoImage(logo_4_)

        logo_5_ = Image.open(io.BytesIO(logo_5)).resize((80, 80))
        photo_5_ = ImageTk.PhotoImage(logo_5_)
    except Exception as e:
        print("error", type(e))

global setbuttons

def setting(mainframe):

    global security,setbuttons


    def security(var):
        mainframe.destroy()
        securityframe=tk.Frame(root1,background="#D6F6F2")
        securityframe.pack(anchor="center",pady=200)
        def process():
                a = str(id_entry.get())
                b = str(pass_entry.get())
                if a == 'rkking' and b == '1234':
                    messagebox.showinfo("Message", "Access Granted ! ")
                    securityframe.destroy()
                    if var==1:
                        id_appending()
                        print("function appending executed ! ")
                    if var==2:
                        reset()
                        print("reset function executed !")
                    if var==3:
                        show_results()
                    if var==4:
                        nameset()
                    if var==5:
                        imagechange()
                    if var==6:
                        show_logs()




                else:
                    messagebox.showerror("Message", "Access Denied ! ")



        global id_label, pass_label, id_entry, pass_entry, exit_button, buttoning
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
        global reset
        def reset():

            server = con.cursor()
            sql = "update nominees set nomresult=0"
            server.execute(sql)
            con.commit()

            messagebox.showinfo("Message", "Reseted Suceesfully")


            pass
        security(2)
    def append():
        security(1)
        global id_appending
        def add():

            # exit_button.configure(command=destroyer5)
            m: str = str(adhaar_entry_.get()) if len((adhaar_entry_.get())) >= 10 else messagebox.showerror('message',
                                                                                                            'Id missing')
            n: str = str(dob_entry_.get()) if len(str(dob_entry_.get())) >= 9 else messagebox.showerror('message',
                                                                                                        'Passward missing')
            if len(m) >= 10 and len(n) >= 9:

                server = con.cursor()
                sql = "insert into voters(votername,voterpass) values (%s,%s)"
                user = (m, n)
                server.execute(sql, user)
                con.commit()

                adhaar_entry_.delete(0, tk.END)
                dob_entry_.delete(0, tk.END)
                messagebox.showinfo("Message", "VOTER ADDED SUCCESSFULLY ! ")
            else:
                messagebox.showwarning('message', 'id and pass is incorrect they extend long ! ')

        def id_appending():
            addingfram=tk.Frame(root1,bg="#D6F6F2")
            addingfram.pack(anchor="center")

            exit_button = ck.CTkButton(addingfram, text="EXIT",
                                       command=lambda: (addingfram.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)


            #exit_button.configure(command=destroyer5)
            global adhaar_fetcher, dob_fetcher, adde, adhaar_entry_, dob_entry_
            adhaar_fetcher = ck.CTkLabel(addingfram, text="ENTER ADHAAR NUMBER", font=('', 30, "bold"))

            adhaar_entry_ = ck.CTkEntry(addingfram, height=40, width=200)

            dob_fetcher = ck.CTkLabel(addingfram, text="ENTER DOB *(DD/MM/YYYY) ", font=('', 28, "bold"))
            dob_entry_ = ck.CTkEntry(addingfram, show="*", height=40, width=200)

            adde = ck.CTkButton(addingfram, text="ADD", command=add)

            adhaar_fetcher.grid(row=3,column=2,padx=40,pady=20)
            adhaar_entry_.grid(row=3,column=3,padx=40,pady=0)

            dob_fetcher.grid(row=4,column=2,padx=40,pady=20)
            dob_entry_.grid(row=4,column=3,padx=40,pady=0)

            adde.grid(row=6,column=3,padx=40,pady=20)


    def logs():
        global show_logs
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
                file = ["hello world"]
                table.insert('', j, values=(i))
                j = j + 1
            # back_button=ck.CTkButton(root1,text='BACK',command=destroytable)
            # back_button.pack()

            # pass
        security(6)
    def results():
        global show_results
        def show_results():
            resultpage=tk.Frame(root1,bg="#D6F6F2")
            resultpage.pack(anchor="center")

            exit_button = ck.CTkButton(resultpage, text="EXIT",
                                       command=lambda: (resultpage.destroy(), mainwindow()))
            exit_button.pack(anchor='nw')


            #exit_button.configure(command=exit6)

            read_refresher_for_count()
            print("nominee is ", nominee_1)
            global result_label_nom1, result_label_nom2, result_label_nom3, result_label_nom4, result_label_nom5, result_winner
            result_label_nom1 = ck.CTkLabel(resultpage, text=("NOMINEE 1 : " + str(nominee_1)),
                                            font=("Times New Roman", 50, "bold"))
            result_label_nom1.pack(pady=20)

            result_label_nom2 = ck.CTkLabel(resultpage, text=("NOMINEE 2 : " + str(nominee_2)),
                                            font=("Times New Roman", 50, "bold"))
            result_label_nom2.pack(pady=20)

            result_label_nom3 = ck.CTkLabel(resultpage, text=("NOMINEE 3 : " + str(nominee_3)),
                                            font=("Times New Roman", 50, "bold"))
            result_label_nom3.pack(pady=20)

            result_label_nom4 = ck.CTkLabel(resultpage, text=("NOMINEE 4 : " + str(nominee_4)),
                                            font=("Times New Roman", 50, "bold"))
            result_label_nom4.pack(pady=20)
            result_label_nom5 = ck.CTkLabel(resultpage, text=("NOMINEE 5: " + str(nominee_5)),
                                            font=("Times New Roman", 50, "bold"))
            result_label_nom5.pack(pady=20)
            winner: str = None


            if nominee_1 == nominee_2 == nominee_3 == nominee_4 == nominee_5:
                winner = "Tied the Election ! "
            if nominee_1 >=(nominee_2 >= nominee_3 >= nominee_4 >= nominee_5):
                winner = "NOMINEE 1"
            if nominee_2 >= (nominee_1 >= nominee_3 >= nominee_4 >= nominee_5):
                winner = "NOMINEE 2"
            if nominee_3 >= (nominee_1 >= nominee_2 >= nominee_4 >= nominee_5):
                winner = "NOMINEE 3"
            if nominee_4 >= (nominee_1 >= nominee_2 >= nominee_3 >= nominee_5):
                winner = "NOMINEE 4"
            if nominee_5 >= (nominee_1 >= nominee_2 >= nominee_3 >= nominee_4):
                winner = "NOMINEE 5"

            global result_winner
            result_winner = ck.CTkLabel(resultpage, text=f"WINNER : {winner}", font=("Times New Roman", 50, "bold"))
            result_winner.pack(anchor='center')
            winner = None
        security(3)
    def settings_for_self_image():
        global imagechange
        security(5)

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
                            print("path is ",paths)
                            ids=int(c.get())
                            print(c,"c value is ")
                            values=(paths,)
                            server = con.cursor()
                            sql = "update image set iim=(%s) where iid=(%s)"

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
            c=ttk.Combobox(imageframe,values=(['1','2','3','4','5']))
            c.grid(row=2,column=2,padx=40,pady=10)
            c.set('1')
            tk.Label(imageframe, text='SELECT IMAGE PATH',font=('',20)).grid(row=3,column=2,padx=40,pady=10)
            b=ck.CTkButton(imageframe,text='PATH',command=pathselector)
            b.grid(row=4,column=2,padx=40,pady=10)
            exit_button = ck.CTkButton(imageframe, text="EXIT",
                                       command=lambda: (imageframe.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)



    def settings_for_self():
        read_refresher_for_count()
        security(4)
        global nameset
        def nameset():
            def upd_name():
                n1=str(name1e.get())
                n2 = str(name2e.get())
                n3 = str(name3e.get())
                n4 = str(name4e.get())
                n5 = str(name5e.get())
                l=[n1,n2,n3,n4,n5]
                server=con.cursor()
                for i in range(1,6):
                    sql="update nominees set nomname=(%s) where ide=(%s)"
                    query=(str((l[i-1])),i)
                    server.execute(sql,query)
                    con.commit()

                messagebox.showinfo('',"Name changed !")


            nameframe=tk.Frame(root1,bg="#D6F6F2")
            nameframe.pack(pady=100)
            read_refresher_for_count()

            global nominee_1_name, nominee_2_name, nominee_3_name, nominee_4_name, nominee_5_name

            nominee_1_name = nominee_1_name
            nominee_2_name = nominee_2_name
            nominee_3_name = nominee_3_name
            nominee_4_name = nominee_4_name
            nominee_5_name = nominee_5_name

            ides = 'rkking'
            passwords = '1234'

            name1 = ck.CTkLabel(nameframe, text='NOMINEE 1 ',font=('',40))
            name1.grid(row=2,column=2,padx=40,pady=10)
            name1e = ck.CTkEntry(nameframe,font=('',30))
            name1e.insert(tk.END, str(nominee_1_name))
            name1e.grid(row=2,column=4,padx=40,pady=10)

            name2 = ck.CTkLabel(nameframe, text='NOMINEE 2 ',font=('',40))
            name2.grid(row=3,column=2,padx=40,pady=10)
            name2e = ck.CTkEntry(nameframe,font=('',30))
            name2e.insert(tk.END, str(nominee_2_name))
            name2e.grid(row=3,column=4,padx=40,pady=10)

            name3 = ck.CTkLabel(nameframe, text='NOMINEE 3 ',font=('',40))
            name3.grid(row=4,column=2,padx=40,pady=10)
            name3e = ck.CTkEntry(nameframe,font=('',30))
            name3e.insert(tk.END, str(nominee_3_name))
            name3e.grid(row=4,column=4,padx=40,pady=10)

            name4 = ck.CTkLabel(nameframe, text='NOMINEE 4 ',font=('',40))
            name4.grid(row=5,column=2,padx=40,pady=10)
            name4e = ck.CTkEntry(nameframe,font=('',30))
            name4e.insert(tk.END, str(nominee_4_name))
            name4e.grid(row=5,column=4,padx=40,pady=10)

            name5 = ck.CTkLabel(nameframe, text='NOMINEE 5 ',font=('',40))
            name5.grid(row=6,column=2,padx=40,pady=10)
            name5e = ck.CTkEntry(nameframe,font=('',30))
            name5e.insert(tk.END, str(nominee_5_name))
            name5e.grid(row=6,column=4,padx=40,pady=10)
            upd_button = ck.CTkButton(nameframe, text="update", command=upd_name)
            upd_button.grid(row=7,column=4,padx=40,pady=40)
            exit_button = ck.CTkButton(nameframe, text="EXIT",
                                       command=lambda: (nameframe.destroy(), mainwindow()))
            exit_button.grid(row=0, column=0)



    def show_menu():
        global set_buttons

        menubar = tk.Menu(root1, tearoff=0,bg='#D6F6F2',font=('',10,'bold'))
        menubar.add_command(label="APPEND", command=append)
        menubar.add_command(label="RESET ALL", command=resetall)
        menubar.add_command(label="LOGS", command=logs)
        menubar.add_command(label="RESULT", command=results)
        menubar.add_command(label="EXIT", command=lambda: root1.destroy())
        menubar.add_command(label="NAME CHANGE", command=settings_for_self)

        menubar.add_command(label="IMAGE CHANGE", command=settings_for_self_image)

        menubar.post(set_buttons.winfo_rootx(), set_buttons.winfo_rooty() + set_buttons.winfo_height())

    show_menu()


def voting_page():

    votingframe=tk.Frame(root1,bg='#D6F6F2')
    votingframe.pack()
    global nominee_1, nominee_2, nominee_3, nominee_4, nominee_5, nom1_label, nom2_label, nom3_label, nom4_label, nom5_label, nom3_button, nom3_label, nom1_button, nom2_button, nom3_button, nom4_button, nom5_button
    # destroy()
    global photo_5_
    global photo_5_, photo_4_, photo_3_, photo_2_, photo_1_

    def put_vote(b):

        global nominee_1, nominee_2, nominee_3, nominee_4, nominee_5

        if b == 0:
            messagebox.showinfo("Message", "Voted Nominee_1 ! ")

            nominee_1 = nominee_1 + 1





        elif b == 1:
            messagebox.showinfo("Message", "Vorted Nominee_2 ! ")

            nominee_2 = nominee_2 + 1

        elif b == 2:
            messagebox.showinfo("Message", "Vorted Nominee_3 ! ")

            nominee_3 = nominee_3 + 1

        elif b == 3:
            messagebox.showinfo("Message", "Voted Nominee_4 ! ")

            nominee_4 = nominee_4 + 1


        elif b == 4:
            messagebox.showinfo("Message", "Voted Nota ! ")

            nominee_5 = nominee_5 + 1


        else:
            messagebox.showinfo("Message", "Voted Nota ! ")


        try:

            server = con.cursor()
            list_data = [(nominee_1, 1), (nominee_2, 2), (nominee_3, 3), (nominee_4, 4), (nominee_5, 5)]
            sql = "update nominees set nomresult= %s where ide= %s"
            for i, j in list_data:
                print(i, j)
                data = (i, j)
                server.execute(sql, data)
                con.commit()
        except Exception as e:
            messagebox.showwarning('',f'{type(e).__name__}')

        read_refresher_for_count()
        mainwindow()
        #voting_page()




    print('nom1 name is ', nominee_1_name)
    nom1_label = ck.CTkLabel(votingframe, text="NOMINEE 1 : " + nominee_1_name,height=5,width=40, font=("Times New Roman", 25, "bold"))
    nom2_label = ck.CTkLabel(votingframe, text="NOMINEE 2 : " + nominee_2_name, height=5,width=40,font=("Times New Roman", 25, "bold"))
    nom3_label = ck.CTkLabel(votingframe, text="NOMINEE 3 : " + nominee_3_name, height=5,width=40,font=("Times New Roman", 25, "bold"))
    nom4_label = ck.CTkLabel(votingframe, text="NOMINEE 4 : " + nominee_4_name, height=5,width=40,font=("Times New Roman", 25, "bold"))
    nom5_label = ck.CTkLabel(votingframe, text="NOMINEE 5 : " + nominee_5_name, height=5,width=40,font=("Times New Roman", 25, "bold"))

    nom1_label.grid(row=2,column=4,padx=100,pady=20)
    nom2_label.grid(row=3,column=4,padx=100,pady=20)
    nom3_label.grid(row=4,column=4,padx=100,pady=20)
    nom4_label.grid(row=5,column=4,padx=100,pady=20)
    nom5_label.grid(row=6,column=4,padx=100,pady=20)

    global logo_label_1, logo_label_2, logo_label_3, logo_label_4, logo_label_5

    logo_label_1 = tk.Button(votingframe, image=photo_1_)
    logo_label_2 = tk.Label(votingframe, image=photo_2_)
    logo_label_3 = tk.Label(votingframe, image=photo_3_)
    logo_label_4 = tk.Label(votingframe, image=photo_4_)
    logo_label_5 = tk.Label(votingframe, image=photo_5_)

    logo_label_1.grid(row=2,column=2,padx=100,pady=20)
    logo_label_2.grid(row=3,column=2,padx=100,pady=20)
    logo_label_3.grid(row=4,column=2,padx=100,pady=20)
    logo_label_4.grid(row=5,column=2,padx=100,pady=20)
    logo_label_5.grid(row=6,column=2,padx=100,pady=20)

    nom1_button = tk.Button(votingframe, text='vote', image=photo2, command=lambda: (votingframe.destroy(),put_vote(0)))

    nom2_button = tk.Button(votingframe, text='vote', image=photo2, command=lambda: (votingframe.destroy(),put_vote(1)))
    nom3_button = tk.Button(votingframe, text='vote', image=photo2, command=lambda: (votingframe.destroy(),put_vote(2)))
    nom4_button = tk.Button(votingframe, text='vote', image=photo2, command=lambda: (votingframe.destroy(),put_vote(3)))
    nom5_button = tk.Button(votingframe, text='vote', image=photo2, command=lambda: (votingframe.destroy(),put_vote(4)))

    nom1_button.grid(row=2,column=8,padx=100,pady=20)
    nom2_button.grid(row=3,column=8,padx=100,pady=20)
    nom3_button.grid(row=4,column=8,padx=100,pady=20)
    nom4_button.grid(row=5,column=8,padx=100,pady=20)
    nom5_button.grid(row=6,column=8,padx=100,pady=20)


def condition_checkers(mainframe):



    def id_remover(a):
        try:
            import time
            server=con.cursor()
            time=time.ctime()
            sql="insert into logindetails(logername,logertime) values (%s,%s)"
            values=(str(adhar_data),str(time))
            server.execute(sql,values)
            con.commit()
        except Exception as e:
            print(type(e))
            messagebox.showerror('','logindetails issues founded !')

        a = 1


    adhar_data: str = str(adhar_entry.get())
    dob_data: str = str(dob_entry.get())
    adhar_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    print("selected at voters")
    mainframe.destroy()

    server = con.cursor()
    sql = "select * from voters"
    server.execute(sql)
    result = (server.fetchall())

    for i in range(0, len(result)):
        a = result[i][0]
        b = result[i][1]
        c = adhar_data
        d = dob_data

        if (result):
            print("its also true da")
            dummy = str(result[i][1])
            print(adhar_data, dob_data)
            print('a', a, 'b', b, 'c', c, 'd', d)
            if a == c and b == d:
                print("condition True")
                messagebox.showinfo("Message", "Welcome To Voting ! ")
                voting_page()
                id_remover(1)
                break

        if (result):
            if a == c and b != d:
                messagebox.showwarning("Message", "Incorrect passward ! ")
                print("showed succesfully ! ")
                mainwindow()

                break


    else:
        mainwindow()
        id_remover(1)
        messagebox.showwarning("Messagebox", "User Not Found")






global mainwindow
def mainwindow():





    read_refresher_for_count()

    global button, adhar_label, dob_label, adhar_entry, dob_entry
    mainframe=tk.Frame(root1,bg='#D6F6F2')
    mainframe.pack(anchor="center",pady=100)
    global set_buttons
    set_buttons = ck.CTkButton(mainframe, text='Setting', command=lambda : (setting(mainframe)))
    set_buttons.grid(row=0,column=0,padx=10,pady=10)
    title=ck.CTkLabel(mainframe,text="ELECTION MANAGEMENT SYSTEM", font=('', 40, 'bold'))
    #title.grid(row=1,columnspan=8,padx=50,pady=100)
    dummylabel = ck.CTkLabel(mainframe, text=None)
    #dummylabel.grid(padx=0,pady=150)


    # labels for mainwindow
    adhar_label = ck.CTkLabel(mainframe, text="ENTER ADHAAR NUMBER ", font=('', 30, 'bold'))
    # adhar_label.pack(anchor="center")
    adhar_label.grid(row=2,column=2,padx=40,pady=50)
    global adhar_entry

    adhar_entry = ck.CTkEntry(mainframe, height=40, width=300)
    # adhar_entry.pack(anchor="center")
    adhar_entry.grid(row=2,column=3,padx=80,pady=20)
    dob_label = ck.CTkLabel(mainframe, text='ENTER DOB                          ', font=('', 30, 'bold'))
    # dob_label.pack(anchor="center")
    dob_label.grid(row=4,column=2,padx=40,pady=20)
    dob_entry = ck.CTkEntry(mainframe, height=40, width=300)
    # dob_entry.pack(anchor="center")
    dob_entry.grid(row=4,column=3,padx=80,pady=10)
    dummylabel = ck.CTkLabel(mainframe, text=None)

    button = ck.CTkButton(mainframe, text='Enter', height=40, width=100, command=lambda: (condition_checkers(mainframe)))
    # button.pack(anchor="center")
    button.grid(row=6,column=3,padx=100,pady=20)
    # button.destroy()



read_refresher_for_count()
mainwindow()

#voting_page()

root1.mainloop()
