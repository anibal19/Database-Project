from tkinter import END, LEFT, Listbox, ttk, Tk, Canvas, Label, Frame, Entry, Button, W, E, Toplevel, StringVar, BOTTOM
import psycopg2
import os
import tkinter as tk
from tkinter import font as tkfont 
# root = Tk()
# root.title("Login Screen")


#TODO add label in between buttons to separate them 


login_options = {
  "Client":   "cli",
  "Admin":    "adm",
  "Employee": "emp"
}

def login(): #not the one in use
   login_screen = Toplevel(main_screen)
   login_screen.title("Login")
   login_screen.geometry("300x250")
   Label(login_screen, text="Entre los detalles para iniciar sesion").pack()
   
 
   global username_verify
   global password_verify
 
   username_verify = StringVar()
   password_verify = StringVar()
 
   
   Label(login_screen, text="Username * ").pack()
   username_login_entry = Entry(login_screen, textvariable=username_verify)
   username_login_entry.pack()
   Label(login_screen, text="").pack()
   Label(login_screen, text="Password * ").pack()
   password__login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
   password__login_entry.pack()
   Label(login_screen, text="").pack()
   if option == login_options[Client]:
      Button(login_screen, text="Login", width=10, height=1, command=login_verification).pack()
   elif option == login_options[Admin]:
       Button(login_screen, text="Login", width=10, height=1, command=login_verification).pack()
   else:
       Button(login_screen, text="Login", width=10, height=1, command=login_verification).pack()

def search(id, se_lf):
   conn = psycopg2.connect(dbname="postgres", user="postgres",password="Minecraft6485", host="localhost", port="5432")
   cursor = conn.cursor()
   query = '''SELECT * FROM students WHERE id=%s'''
   cursor.execute(query, (id))

   row = cursor.fetchone()
   # listbox = Listbox(frame, width=20, heigh=5)
   # listbox.grid(row = 10, columnspan = 4, sticky = W+E)

   # for x in row:
   #     listbox.insert(END, x)
   
   listbox = Listbox(se_lf, width = 30, height = 1)
   listbox.grid(row = 4, column=1)
   listbox.insert(END, row)

   conn.commit()
   conn.close()

def page_setup(se_lf, head_text): #used to display the head_text on a Frame
   label = tk.Label(se_lf, text=head_text, font=se_lf.controller.title_font)
   label.grid(row = 1, column=1, sticky="nsew")
   se_lf.grid_rowconfigure(1, weight=1)
   se_lf.grid_columnconfigure(1, weight=1)

#def login_handler:
   #se_lf.controller.show_frame("ClientPage")

def login_input(se_lf, option): #used to show login input on a Frame
   Label(se_lf, text="Entre los detalles para iniciar sesion").grid(row=2, column=1)
   Label(se_lf, text="").grid(row = 3, column=1)
 
   global username_verify
   global password_verify
 
   username_verify = StringVar()
   password_verify = StringVar()
   
   Label(se_lf, text="Username * ").grid(row=4, column=1)
   username_login_entry = Entry(se_lf, textvariable=username_verify)
   username_login_entry.grid(row=5, column=1)
   Label(se_lf, text="").grid(row=6, column=1)
   Label(se_lf, text="Password * ").grid(row=7, column=1)
   password__login_entry = Entry(se_lf, textvariable=password_verify, show= '*')
   password__login_entry.grid(row=8, column=1)
   Label(se_lf, text="").grid(row=9, column=1)
   if option == login_options["Client"]:
       Button(se_lf, text="Login", width=10, height=1, command=lambda: se_lf.controller.show_frame("ClientPage")).grid(row=10, column=1) 
   elif option == login_options["Admin"]:                                                #replace self with login_handler
       Button(se_lf, text="Login", width=10, height=1, command=lambda : se_lf.controller.show_frame("AdminPage")).grid(row=10, column=1)
   else:
       Button(se_lf, text="Login", width=10, height=1, command=lambda : se_lf.controller.show_frame("EmployeePage")).grid(row=10, column=1)

def test():
   print(1)

def save_new_student(name, age, Address):
   #print(name, age, Address)
   conn = psycopg2.connect(dbname="postgres", user="postgres",password="Minecraft6485", host="localhost", port="5432")
   cursor = conn.cursor()
   query = '''INSERT INTO students(name, age, address) VALUES (%s, %s, %s)'''
   cursor.execute(query, (name, age, Address))
   print("saved!")
   conn.commit()
   conn.close()

   display_students()

def display_students():
   conn = psycopg2.connect(dbname="postgres", user="postgres",password="Minecraft6485", host="localhost", port="5432")
   cursor = conn.cursor()
   query = '''SELECT * FROM students'''
   cursor.execute(query)

   row = cursor.fetchall()

   listbox = Listbox(frame, width=20, heigh=5)
   listbox.grid(row = 10, columnspan = 4, sticky = W+E)

   for x in row:
       listbox.insert(END, x)
   
   conn.commit()
   conn.close()
   
def main_account_screen():
   global main_screen
   main_screen = Tk()
   #main_screen.geometry("300x250") Establishes window size
   main_screen.state('zoomed') #Goes Fullscreen
   main_screen.title("Account Login")
   Label(text="Sistema de Membresia", bg="gray74", width="300", height="2", font=("Calibri", 13)).pack()
   Label(text="").pack()
   Button(text="Employee", height="2", width="30", command = login).pack()
   Label(text="").pack()
   Button(text="Admin", height="2", width="30").pack()
   Label(text="").pack()
   Button(text="Client", height="2", width="30").pack()
 
   main_screen.mainloop()

def tabs_client(se_lf):
      
      TAB_CONTROL = ttk.Notebook(se_lf)
      #Tab1
      TAB1 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB1, text='             Informacion Cliente            ')
      
      TAB2 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB2, text='              Referido              ')

      TAB3 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB3, text='                Modificar Informacion            ')

      TAB_CONTROL.pack(expand=5, fill="both", pady=5)

      # label = Label(TAB1, text="Nombre: ")
      # label.grid(row = 0, column=0)
      # name = Entry(TAB1)
      # name.grid(row = 0, column=1)

      # label = Label(TAB1, text="Apellido: ")
      # label.grid(row = 2, column=0)
      # last_name = Entry(TAB1)
      # last_name.grid(row = 2, column=1)

      # label = Label(TAB1, text="Correo Fisico: ")
      # label.grid(row = 3, column=0)
      # mail_address = Entry(TAB1)
      # mail_address.grid(row = 3, column=1)

      label = Label(TAB2, text="Correo Electronico: ")
      label.grid(row = 4, column=0)
      mail_address = Entry(TAB2, width = 40)
      mail_address.grid(row = 4, column=1)
      
      label = Label(TAB1, text = "Nombre:")
      label.grid(row = 2, column = 1)
      
      listbox = Listbox(TAB1, width = 40, height = 1)
      listbox.grid(row = 2, column=2)
      listbox.insert(END, "Michael")

      label = Label(TAB1, text = "Apellido:")
      label.grid(row = 3, column = 1)

      listbox = Listbox(TAB1, width = 40, height = 1)
      listbox.grid(row = 3, column=2)
      listbox.insert(END, "Jackson")

      label = Label(TAB1, text = "Email:")
      label.grid(row = 4, column = 1)

      listbox = Listbox(TAB1, width = 40, height = 1)
      listbox.grid(row = 4, column=2)
      listbox.insert(END, "abc123@email.com")

      label = Label(TAB1, text = "Direccion Postal:")
      label.grid(row = 5, column = 1)

      listbox = Listbox(TAB1, width = 40, height = 1)
      listbox.grid(row = 5, column=2)
      listbox.insert(END, "1093 College Ave. New Paris, OH 45347")

      label = Label(TAB1, text = "Estado de Cuenta:")
      label.grid(row = 6, column = 1)

      listbox = Listbox(TAB1, width = 40, height = 1)
      listbox.grid(row = 6, column=2)
      listbox.insert(END, "Activo - 2")

      button = tk.Button(TAB3, text="Modificar", command=lambda: search(id_search.get(), TAB1))
      button.grid( column = 1)
      
      button = tk.Button(TAB2, text="Referir", command=lambda: search(id_search.get(), TAB1))
      button.grid( column = 1)



def tabs_employee(se_lf):
   #Create Tab Control
      TAB_CONTROL = ttk.Notebook(se_lf)
      #Tab1
      TAB1 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB1, text='             Buscar Cliente            ')
      
      TAB2 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB2, text='                Añadir Cliente            ')

      TAB3 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB3, text='                Modificar Cliente            ')

      TAB4 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB3, text='                Aviso de Pago            ')

      TAB_CONTROL.pack(expand=5, fill="both", pady=5)


      label = Label(TAB2, text="Nombre: ")
      label.grid(row = 0, column=0)
      name = Entry(TAB2, width = 40)
      name.grid(row = 0, column=1)

      label = Label(TAB2, text="Apellido: ")
      label.grid(row = 2, column=0)
      last_name = Entry(TAB2, width = 40)
      last_name.grid(row = 2, column=1)

      label = Label(TAB2, text="Correo Fisico: ")
      label.grid(row = 3, column=0)
      mail_address = Entry(TAB2, width = 40)
      mail_address.grid(row = 3, column=1)

      label = Label(TAB2, text="Correo Electronico: ")
      label.grid(row = 4, column=0)
      mail_address = Entry(TAB2, width = 40)
      mail_address.grid(row = 4, column=1)

      label = Label(TAB2, text="Estado de la Cuenta: ")
      label.grid(row = 5, column=0)
      mail_address = Entry(TAB2, width = 40)
      mail_address.grid(row = 5, column=1)

   
      label = Label(TAB1, text="Busqueda Cliente/Edificio")
      label.grid(row = 2, column = 1)

      id_search = Entry(TAB1, width = 40)
      id_search.grid(row = 3, column = 1)

      button = tk.Button(TAB1, text="Buscar", command=lambda: search(id_search.get(), TAB1))
      button.grid(row = 3, column = 3)

      button = tk.Button(TAB2, text="Añadir", command=lambda: search(id_search.get(), TAB1))
      button.grid( column = 1)

      button = tk.Button(TAB3, text="Modificar", command=lambda: search(id_search.get(), TAB1))
      button.grid( column = 1)

def tabs_admin(se_lf):
   #Create Tab Control
      TAB_CONTROL = ttk.Notebook(se_lf)
      #Tab1
      TAB1 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB1, text='             Añadir  Empleado            ')
      
      #TAB2
      TAB2 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB2, text='             Añadir Edificio            ')
      
      #TAB5 
      TAB5 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB5, text='             Añadir Articulos           ')

      #TAB3
      TAB3 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB3, text='             Borrar             ')

      #TAB4
      TAB4 = ttk.Frame(TAB_CONTROL)
      TAB_CONTROL.add(TAB4, text='             Modificar             ')

      

      TAB_CONTROL.pack(expand=5, fill="both",pady=5)
      #Tab Name Labels
      # ttk.Label(TAB1, text="This is Tab 1").grid(column=0, row=0, padx=10, pady=10)
      # ttk.Label(TAB2, text="This is Tab 2", ).grid(column=0, row=0, padx=10, pady=10)
      #Tab buttons

      lista = ["Nombre: ", "Apellido: ", "Direccion Postal: ", "Correo Electronico: ", "Posicion del Empleado: "]

      for i in range(len(lista)):
         label = Label(TAB1, text=lista[i])
         label.grid(row = i, column=0)
         name = Entry(TAB1, width = 40)
         name.grid(row = i, column=1)
      
      label = Label(TAB3, text="ID: ")
      label.grid(row = 0, column=0)
      id_num = Entry(TAB3, width = 40)
      id_num.grid(row = 0, column=1)

      label = Label(TAB2, text="Nombre Edificio: ")
      label.grid(row = 0, column=0)
      name = Entry(TAB2, width = 40)
      name.grid(row = 0, column=1)

      label = Label(TAB2, text="Nivel Membresia: ")
      label.grid(row = 1, column=0)
      name = Entry(TAB2, width = 40)
      name.grid(row = 1, column=1)

      label = Label(TAB5, text="ID Articulo: ")
      label.grid(row = 0, column=0)
      name = Entry(TAB5, width = 40)
      name.grid(row = 0, column=1)

      label = Label(TAB5, text="Nombre: ")
      label.grid(row = 1, column=0)
      name = Entry(TAB5, width = 40)
      name.grid(row = 1, column=1)

      label = Label(TAB5, text="Precio: ")
      label.grid(row = 2, column=0)
      name = Entry(TAB5, width = 40)
      name.grid(row = 2, column=1)


      tab_B1 = tk.Button(TAB1, text="Añadir", command = lambda : test()) #Añadir condicion para saber si es empleado o no
      tab_B1.grid()
      
      tab_B1 = tk.Button(TAB2, text="Añadir", command = lambda : test()) #Añadir condicion para saber si es empleado o no
      tab_B1.grid()

      tab_B1 = tk.Button(TAB3, text="Eliminar", command = lambda : test()) #Añadir condicion para saber si es empleado o no
      tab_B1.grid(column = 1)
      
      tab_B1 = tk.Button(TAB4, text="Modificar", command = lambda : test()) #Añadir condicion para saber si es empleado o no
      tab_B1.grid(column = 1)
      
      tab_B1 = tk.Button(TAB5, text="Añadir", command = lambda : test()) #Añadir condicion para saber si es empleado o no
      tab_B1.grid(column = 1)



#main_account_screen()

class SampleApp(tk.Tk): #Change CLass Name !!!!!!!!!!!

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        
      #   width= self.winfo_screenwidth()               

      #   height= self.winfo_screenheight()               

      #   self.geometry("%dx%d" % (width, height))

        #self.geometry("800x500")
        #self.resizable(False, False)
        container = tk.Frame(self)
        
        #container.pack(side="top", fill="both", expand=True)
        container.grid(row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, AdminPage, ClientPage, EmployeePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sistema de Membresia", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Cliente",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Empleado", command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Administrador",    command=lambda: controller.show_frame("PageThree"))
        button1.pack(ipadx=34, ipady=12)
        label = Label(self, text="")
        label.pack()
        button2.pack(ipadx=27, ipady=12)
        label = Label(self, text="")
        label.pack()
        button3.pack(ipadx=16, ipady=12)


class PageOne(tk.Frame): #Client Login Page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        page_setup(self, "Login Cliente")
        login_input(self, "cli")
        
        label = tk.Label(self, text=" ", font=self.controller.title_font)
        label.grid(row = 11, column=1, sticky="nsew")

        button = tk.Button(self, text="Crear Cuenta", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=12, column=1)
        
        label = tk.Label(self, text=" ", font=self.controller.title_font)
        label.grid(row = 13, column=1, sticky="nsew")

        button = tk.Button(self, text="Volver a la Pagina Principal", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=14, column=1)


class PageTwo(tk.Frame): #Employee Login Page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        page_setup(self, "Login Empleado")
        login_input(self, "emp")
        
        button = tk.Button(self, text="Volver a la Pagina Principal", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=13, column=1)



class PageThree(tk.Frame): #Admin Login Page
   
   def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller

      page_setup(self, "Login Administador")
      login_input(self, "adm")


      button = tk.Button(self, text="Volver a la Pagina Principal", command=lambda: controller.show_frame("StartPage"))
      button.grid(row=12, column=1)
   

class AdminPage(tk.Frame): #Frame used to display all admin options, delete, add, etc

   def __init__(self, parent, controller):
        
      tk.Frame.__init__(self, parent)
      self.controller = controller

      #page_setup(self, "Admin Page")
      label = tk.Label(self, text="Admin Page", font=("Arial", 12))
      label.pack()

      tabs_admin(self)

      # page_setup(self, "Admin Login")
      # login_input(self, "adm")

      button = tk.Button(self, text="Volver a la Pagina Principal", command=lambda: controller.show_frame("StartPage"))
      button.pack()

class EmployeePage(tk.Frame): #Frame used to search Clients, etc. for the Employee
   def __init__(self, parent, controller):
        
      tk.Frame.__init__(self, parent)
      self.controller = controller

      #page_setup(self, "Employee Page")
      #login_input(self, "adm")

      label = tk.Label(self, text="Employee Page", font=("Arial", 12))
      label.pack()

      tabs_employee(self)

      button = tk.Button(self, text="Volver a la Pagina Principal", command=lambda: controller.show_frame("StartPage"))
      button.pack()
     

class ClientPage(tk.Frame): #Frame used to display the information of the client
   def __init__(self, parent, controller):
        
      tk.Frame.__init__(self, parent)
      self.controller = controller

      label = tk.Label(self, text="Client Page", font=("Arial", 12))
      label.pack()

      tabs_client(self)

      # page_setup(self, "Client Page")
      #login_input(self, "adm")

      


      button = tk.Button(self, text="Volver a la Pagina Principal", command=lambda: controller.show_frame("StartPage"))
      #button.pack(pady=25) 
      button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



# # Canvas
# canvas = Canvas(root, height=380, width=400)
# canvas.pack()

# frame = Frame()
# frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# # Name Input
# label = Label(frame, text='Add Student')
# label.grid(row=0, column=1)

# label = Label(frame, text="Name")
# label.grid(row=1, column=0)

# entry_name = Entry(frame)
# entry_name.grid(row=1, column=1)

# # Age Input
# label = Label(frame, text="Age")
# label.grid(row=2, column=0)

# entry_age = Entry(frame)
# entry_age.grid(row=2, column=1)

# # Address Input
# label = Label(frame, text="Address")
# label.grid(row=3, column=0)

# entry_address = Entry(frame)
# entry_address.grid(row=3, column=1)

# button = Button(frame, text = "Add", command=lambda:save_new_student(entry_name.get(), entry_age.get(), entry_address.get()))
# button.grid(row=4, column=1, sticky=W+E)

# display_students()
# root.mainloop()