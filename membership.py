import sys
import psycopg2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import re
from datetime import datetime

pass_text = "Minecraft6485"
#TODO Arreglar lo de las pantallas cuando retornas al main window
#NOTE corchetes seems to fix the problem of cursor.execute(query, item)
#TypeError: not all arguments converted during string formatting

#TODO hacer el cursor que conecta al database una funcion
#Mostrar posible lista de las personas referidas
#Añadir fechas de membresias, posiblementes hacerlo una tabla distinta (Nivel, fecha de Inicio, fecha de Vencimiento)
#TODO Mover el projecto a un Env para posiblemente poder hacer el exe mas facil
#TODO Añadir verificacion de Existencia en el db

#Implement this for the passwords
def polynomialRollingHash(str):
     
    # P and M
    p = 31
    m = 1e9 + 9
    power_of_p = 1
    hash_val = 0
 
    # Loop to calculate the hash value
    # by iterating over the elements of string
    for i in range(len(str)):
        hash_val = ((hash_val + (ord(str[i]) -
                                 ord('a') + 1) *
                              power_of_p) % m)
 
        power_of_p = (power_of_p * p) % m
 
    return int(hash_val)

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("loginPage.ui", self)
        self.Enter.clicked.connect(self.gotoclient)
        self.adminButton.clicked.connect(self.gotoadmin)
        self.employeeButton.clicked.connect(self.gotoemployee)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def loginfunction(self):
        username = self.Username.text()
        password = self.Password.text()
        print(username, password)

    def gotoclient(self):
        clientpage=clientPage(self.Username.text(), self.Password.text())
        widget.addWidget(clientpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoadmin(self):
        adminpage = adminPage()
        widget.addWidget(adminpage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoemployee(self):
        employeepage = employeePage()
        widget.addWidget(employeepage)
        widget.setCurrentIndex(widget.currentIndex()+1)



class clientPage(QDialog):
    def __init__(self, key, key2):
        super(clientPage,self).__init__()
        self.loadClientInfo(key, key2)
        loadUi("ClientPage.ui", self)
        
        self.rButton.clicked.connect(self.clientRefer)
        # self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.modifyButton.clicked.connect(lambda: self.modifyClientInfo(key))
        self.returnMain.clicked.connect(self.gotomain)
        self.deleteButton.clicked.connect(self.deleteAccount)
        
    def test(self):
        print(1)

    def clientRefer(self):
        email = self.rEmail.text()
        print("Email sent to " + email)

    def loadClientInfo(self, key, key2):
        conn = psycopg2.connect(dbname="member_project", user="postgres", password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''SELECT * FROM mem WHERE member_id = %s AND person_id = %s'''
        cursor.execute(query, [str(polynomialRollingHash(key)), str(polynomialRollingHash(key2))])

        row = cursor.fetchall() #ListaDoble row[0][0]
        
        conn.commit()
        conn.close()

        
        if row:
            self.clientNameLine.setText(row[0][1])
            self.clientLastNameLine.setText(row[0][2])
            self.clientEmailLine.setText((row[0][4])) 
            self.clientAddressLine.setText(row[0][5])
            self.memTierLine.setText(str(row[0][6]))
            
            if datetime.today().strftime('%Y-%m-%d') > str(row[0][7]):
                accState  = " Vencida "
            else:
                accState = " Activa hasta: " + str(row[0][7])

            self.clientAccStateLine.setText(accState)
        
    
    def modifyClientInfo(self,key):#Key can be changed to suit the proper command of the sql
        print(not self.clientNameLine_3.text()) #This works to know if the string is empty
        print("modify", key)

    def deleteAccount(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres", password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''DELETE FROM mem WHERE person_id = %s'''
        cursor.execute(query, [str(polynomialRollingHash(self.clientEmailLine.text()))])

        conn.commit()
        conn.close()

        self.gotomain()
        return
    
    def gotomain(self):
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex()-1)


class adminPage(QDialog):
    def __init__(self): #Add key to verify admin
        super(adminPage,self).__init__()
        loadUi("AdminPage.ui", self)
        
        self.load()

        self.refreshButton.setIcon(QtGui.QIcon('refresh.png'))
        self.refreshButton.setIconSize(QtCore.QSize(25,25))
        self.refreshButton_2.setIcon(QtGui.QIcon('refresh.png'))
        self.refreshButton_2.setIconSize(QtCore.QSize(25,25))
        self.refreshButton.clicked.connect(self.ref)
        self.refreshButton_2.clicked.connect(self.ref)


        self.addItemButton.clicked.connect(self.addItem)


        self.addBuildingButton.clicked.connect(self.addBuildings)
        self.BuildingListDel.itemActivated.connect(self.deleteBuilding)
        self.ProductListDel.itemActivated.connect(self.deleteItem)
        self.buildingList.itemActivated.connect(self.modifyBuild)
        self.itemList.itemActivated.connect(self.modifyProd)
        self.returnMain.clicked.connect(self.gotomain)

        self.modifyBuilding.clicked.connect(self.modifyBuildingdb)
        self.ModItemButton.clicked.connect(self.modifyProductdb)

    def modifyBuildingdb(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''UPDATE edificio SET nombre = %s, nivel = %s WHERE nombre = %s;'''
        cursor.execute(query, [self.buildingModify.text(), self.buildingToAddMem_2.text(), self.buildSelecLabel.text()]) 

        conn.commit()
        conn.close()
        self.loadBuildings(self.buildingList)
    
    def modifyProductdb(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''UPDATE articulos SET idarticulo = %s, nombre = %s, precio = %s WHERE idarticulo = %s; '''
        cursor.execute(query, [self.itemModify.text(), self.itemModify_1.text(), self.itemModify_2.text(), self.prodSelecLabel.text()]) 

        conn.commit()
        conn.close()
        self.loadArticles(self.itemList)
        
    def load(self):
        self.loadArticles(self.itemList)
        self.loadBuildings(self.buildingList)
        self.loadArticles(self.ProductListDel)
        self.loadBuildings(self.BuildingListDel)

    def ref(self):
        self.itemList.clear()
        self.buildingList.clear()
    
        self.loadArticles(self.itemList)
        self.loadBuildings(self.buildingList)

    def addItem(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''INSERT INTO articulos (idArticulo, nombre, precio)
                   VALUES(%s, %s, %s);'''
        cursor.execute(query, [self.itemToAddId.text(), self.itemToAddName.text(), self.itemToAddPrice.text()]) 

        conn.commit()
        conn.close()
        self.itemList.clear()
        self.loadArticles(self.itemList)
    
    def addBuildings(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''INSERT INTO edificio (nombre, Nivel)
                   VALUES(%s, %s);'''
        cursor.execute(query, [self.buildingToAdd.text(), self.buildingToAddMem.text()]) 

        conn.commit()
        conn.close()
        self.buildingList.clear()
        self.loadBuildings(self.buildingList)
    
    def loadBuildings(self, listToShow):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''SELECT * FROM public.edificio'''
        cursor.execute(query) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            name = row[x][0]
            Level = row[x][1]

            temp = "\nNombre Edificio: " + str(name) + "\nNivel de Membresía: "+ str(Level) + "\n"
            listToShow.addItem(temp)

    def loadArticles(self, listToShow): #could load everything here
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''SELECT * FROM public.articulos'''
        cursor.execute(query) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            num = row[x][0]
            name = row[x][1]
            price = row[x][2]

            temp = "Numero ID: " + str(num) + "\nNombre Producto: " + str(name) + "\nPrecio: "+ str(price) + "\n"
            listToShow.addItem(temp)

    def deleteBuilding(self, item):

        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        name = filter.group(2)
        
        conn = psycopg2.connect(dbname="member_project", user="postgres", password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''DELETE FROM edificio WHERE nombre = %s'''
        cursor.execute(query, [name])

        conn.commit()
        conn.close()

        self.BuildingListDel.clear()
        self.loadBuildings(self.BuildingListDel)

    
    def deleteItem(self, item):
        
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        id_number = filter.group(2)

        conn = psycopg2.connect(dbname="member_project", user="postgres", password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''DELETE FROM articulos WHERE idarticulo = %s'''
        cursor.execute(query, [id_number])

        conn.commit()
        conn.close()
        
        self.ProductListDel.clear()
        self.loadArticles(self.ProductListDel)

    def modifyProd(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        id_number = filter.group(2)
        self.prodSelecLabel.setText(str(id_number))
        
    def modifyBuild(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        name = filter.group(2)
        self.buildSelecLabel.setText(str(name))
        
    
    def gotomain(self): #Works so Far
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex()-1)
        

class employeePage(QDialog):
    def __init__(self):
        super(employeePage, self).__init__()
        loadUi("EmployeePage.ui", self)
        self.rButton.clicked.connect(self.paymentNotice)
        self.addClientButton.clicked.connect(self.addNewClient)
        self.search.clicked.connect(self.searchClient)
        self.returnMain.clicked.connect(self.gotomain)
        self.addPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def searchClient(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''SELECT * FROM mem WHERE member_id = %s'''
        item = str(polynomialRollingHash(self.clientEmailLine.text()))
        cursor.execute(query, [item]) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()
               
        self.clientNameLine.setText(row[0][1])
        self.clientLastNameLine.setText(row[0][2])
        self.clientEmailLine.setText((row[0][4])) 
        self.clientAddressLine.setText(row[0][5])

        if datetime.today().strftime('%Y-%m-%d') > str(row[0][7]):
            accState  = " Vencida "
        else:
            accState = " Activa hasta: " + str(row[0][7])

        self.accStateLine.setText(accState)
        self.memTierLine.setText(str(row[0][6]))

    def addNewClient(self):
        conn = psycopg2.connect(dbname="member_project", user="postgres",password=pass_text, host="localhost", port="5432")
        cursor = conn.cursor()
        query = '''INSERT INTO mem (person_id, name, lastname, member_id, email, address, tier, mem_ven)
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s);'''
        cursor.execute(query, [str(polynomialRollingHash(self.addPassword.text())), self.addClientName.text(), self.addClientLastName.text(), str(polynomialRollingHash(self.addClientEmail.text())) ,
        self.addClientEmail.text(), self.addClientAddress.text(), self.addMemTier.text(), self.clientAccState.text()])
        
        conn.commit()
        conn.close()

    def paymentNotice(self):
        print(self.rEmail.text())
    
    def gotomain(self):
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex()-1)

class accountCreation(QDialog):
    def __init__(self):
        super(accountCreation, self).__init__()



app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
# widget.showFullScreen()
# widget.showMaximized()
widget.setWindowIcon(QtGui.QIcon('icon.png'))
widget.setWindowTitle("Club Membership System")
widget.show()
app.exec_()

#Implement this for the passwords
def polynomialRollingHash(str):
     
    # P and M
    p = 31
    m = 1e9 + 9
    power_of_p = 1
    hash_val = 0
 
    # Loop to calculate the hash value
    # by iterating over the elements of string
    for i in range(len(str)):
        hash_val = ((hash_val + (ord(str[i]) -
                                 ord('a') + 1) *
                              power_of_p) % m)
 
        power_of_p = (power_of_p * p) % m
 
    return int(hash_val)
 
# # Driver Code
# if __name__ == '__main__':
 
#     # Given string
#     str1 = "sdfa" 
 
#     print("Hash of '{}' = {}".format(
#           str1, polynomialRollingHash(str1)))


# TODO Hacer login de admin con hashing
# TODO Hacer login de Empleado con email @club con password/ID
# MemberID con el hashing es el email, personID es el password con Hashing
#Pensar bien como modificar la informacion de un cliente
