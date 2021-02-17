#==============----------------- GESTION STOCK ET VENTES SYSTEME ------------------============
#-------------- Auteur : KERVENS VASTY GUIVALDO DESIR
#-------------- Languages Programmation : Python-Tkinter (Font-end) / Sqlite3(Back-end)
#-------------- Paradigme OOP(Programmation Oriente Object)
#-------------- Nom du Logiciel : 

from tkinter import *
import datetime, time, math , os, random, sqlite3
from tkinter import messagebox, ttk

#=====--------------- MEMO APP -------------===============
#screen display (1600x900)
#windows architecture (x64)


conn = sqlite3.connect('C:/MY_INV/DB/store.db')
cur = conn.cursor()

date = datetime.datetime.now().date()

edate = time.strftime('%d/%m/%Y')
etime = time.strftime('%H:%M:%S')

#=============== temporary list ================
products_list=[]
product_price=[]
product_quantity=[]
product_id=[]
#==== label list for sales =====
sales_labels = []

class InvoicePay:
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.root.title('ventes'.upper())
        self.root.resizable(0,0)
        
        largeur = 1000
        hauteur = 680

        largeur_ecran = root.winfo_screenwidth()
        hauteur_ecran = root.winfo_screenheight()

        x_coordinate = (largeur_ecran/2) - (largeur/2)
        y_coordinate = (hauteur_ecran/2) - (hauteur/2)

        root.geometry('%dx%d+%d+%d' % (largeur, hauteur, x_coordinate, y_coordinate))
        
        #================== VARIABLES ============
        self.montant = StringVar()
        self.somme = IntVar()
        self.remise = IntVar()
        
        self.prodName = StringVar()
        self.prixProd = StringVar()
        self.qtProd = StringVar()

        #================== Frame parts==============
        self.left= Frame(root, width = 550, height = 680, bg='green')
        self.left.pack(side = LEFT)
        
        self.right= Frame(root, width = 550, height = 680, bg ='white')
        self.right.pack(side = RIGHT)
        
        self.head = Label(self.left, text = 'ventes'.upper(), font = ('Calligrapher', 40,'bold'), bg = 'green', fg = 'white')
        self.head.place(x=0, y=0)
        
        self.id = Label(self.left, text = 'PRD CODE', font = ('Times',15,'bold'), bg='green',fg='white')
        self.id.place(x=25,y=117)
        
        self.id_e = Entry(self.left, width = 25, font = ('Times',15,'bold'), insertwidth = 10, insertbackground = 'green')
        self.id_e.place(x=150,y=120)
        self.id_e.focus()
        #============ Binding action function ====================
        self.id_e.bind("<Return>", self.ajax)
        
        self.date = Label(self.right, text = 'Date : ',font = ('Times',20,'bold'), bg = 'white', fg = 'green')
        self.date.place(x = 150, y = 0)
        self.heure()

        #==================== produit et prix =========================
        self.prod_name = Label(self.left, text = '', font = ('Times', 25, 'bold'),bg='green',fg='white')
        self.prod_name.place(x=0,y=260)
        
        self.prod_price = Label(self.left, text = '', font = ('Times', 25, 'bold'),bg='green',fg='white')
        self.prod_price.place(x=0,y=310)
        
        #================= total show ================
        self.total_sale = Label(self.right, text = '', font = ('centirion', 30, 'bold'), bg= 'white', fg = 'green')
        self.total_sale.place(x=0,y=620)

        #============== DIRECTIVE ================
        self.d_cash = Label(self.left, text = 'Toucher [F5]', font = ('Times', 12, 'bold'), fg = 'black', bg='green')
        self.d_cash.place(x=60,y=580)
        
        #=============TREEVIEW AND STYLE  ========
        style = ttk.Style()
        
        style.theme_use('clam')# Default, vista
        
        style.configure('Treeview',
                        #background = 'darkblue',
                        relief = 'flat',
                        borderwidth = 0,
                        foreground ="red",
                        rowheight = 25,
                        #fieldbackground = 'darkblue',
                        font = ('Arial', 13)
                        )
        
        style.map('Treeview',
                 background = [('selected', 'green')])
        
        #============= treeview display ===============
        self.tree = ttk.Treeview(self.right, column = (1,2,3), height = 5, show = "headings")
        self.tree.place(x = 0, y = 50, width = 450, height = 550)
        
        vsb = ttk.Scrollbar(self.right , orient="vertical",command=self.tree.yview)
        vsb.place(x=630, y=50, height=550, width =20)
        self.tree.configure(yscrollcommand=vsb.set)

#================================= treeview entete ============================
        self.tree.heading(1, text ="nom produit".upper())
        self.tree.heading(2, text ="prix unit.".upper())
        self.tree.heading(3, text = "quantite".upper())

        #==========================
        self.tree.column(1, width=180, anchor = 'center')
        self.tree.column(2, width=80, anchor = 'center')
        self.tree.column(3, width=80, anchor = 'center')

        self.tree.bind("<Double-1>",self.ajaxMod)
    #=================== date and time  and binding discount entry =======================  
    def heure(self, *args, **kwargs):
        self.date_heure = time.strftime("%d/%m/%Y     %H:%M:%S")
        self.date.config(text = self.date_heure)
        self.date.after(200, self.heure)    
    #=========================================================\
    def ajaxMod(self,event, *args,**kwargs):
        for self.p in products_list:
            self.get_name = self.r[1]
            self.get_price = self.r[3]
            
        self.prod_name.configure(text = 'Nom Produit : '+str(self.get_name))
        self.prod_price.configure(text = 'Prix : '+str(self.get_price)+' HTD', fg = 'gold')
            
            
            
    #================= show and hide function =====================    
    def ajax(self,event, *args,**kwargs):
        self.get_id = self.id_e.get()
        if self.get_id =='':
            messagebox.showwarning('ATTENTION', 'VOUS DEVEZ ENTRER LE CODE D\'UN PRODUIT')
        else:
            req = 'select * from inventory where id=?'
            result = cur.execute(req, (self.get_id))
            for self.r in result:
                self.get_id = self.r[0]
                self.get_name = self.r[1]
                self.get_price = self.r[3]
                self.get_stock = self.r[2]
            self.prod_name.configure(text = 'Nom Produit : '+str(self.get_name))
            self.prod_price.configure(text = 'Prix : '+str(self.get_price)+' HTD', fg = 'gold')
            
            #================ quantity and discount label-entry ====================
            self.quantite1 = Label(self.left, text = 'Quantite', font = ('Times',20,'bold'), bg='green',fg='white')
            self.quantite1.place(x=20,y=370)
            
            self.quantite1_e = Entry(self.left, width = 20, font = ('Times',15,'bold'), insertwidth = 10, insertbackground = 'green')
            self.quantite1_e.place(x=150,y=380)
            self.quantite1_e.focus()
            
            self.quantite1_e.bind("<Return>", self.add)
            self.id_e.bind("<F5>", self.Paid)
#+========================================== add to table sale =======================
#-------------------------------------------------------------------------------------
    def add(self,*args,**kwargs):
        #======= get quantity from the DB ==================
        self.quantite_value = int(self.quantite1_e.get())
        if self.quantite_value > int(self.get_stock):
            messagebox.showwarning('Warning','Quantity is out of stock')
        else:
            self.final_price = float(self.quantite_value) * float(self.get_price)

            products_list.append(self.get_name)
            product_price.append(self.final_price)
            product_quantity.append(self.quantite_value)
            product_id.append(self.get_id)

            self.counter = 0

            self.tree.delete(*self.tree.get_children())
            for self.p in products_list:
                self.tree.insert('', END, values = [products_list[self.counter], 
                                                    product_price[self.counter], 
                                                    product_quantity[self.counter]])
                
            # ==============TOTAL CONFIGURATION =============
                self.total_sale.configure(text = 'TOTAL : ' + str(sum(product_price))+' HTD')
                #=========== delete ===========
                self.prod_name.configure(text='')
                self.prod_price.configure(text='')
                self.quantite1.place_forget()
                self.quantite1_e.place_forget()

                #============ focus after =============
                self.id_e.focus()
                self.id_e.delete(0,END)
                self.quantite1_e.focus()

                self.counter += 1

#=============================== TOP LEVEL PAYMENT =============================================        
    #-------------------- LABEL AND ENTRY TOP LEVEL ---------------------    
    def Paid(self, *args, **kwargs):
        top = Toplevel()
        self.top = top    
        self.top.title('Paiement'.upper())
        self.top.transient(root)
        
        largeur = 500
        hauteur = 350

        largeur_ecran = root.winfo_screenwidth()
        hauteur_ecran = root.winfo_screenheight()

        x_coordinate = (largeur_ecran/2) - (largeur/2)
        y_coordinate = (hauteur_ecran/2) - (hauteur/2)

        top.geometry('%dx%d+%d+%d' % (largeur, hauteur, x_coordinate, y_coordinate))
        
        self.our_total=float(sum(product_price))
        self.montant.set(self.our_total)
        
        
        titleFacture = Label(self.top, text = 'Paiement Facture',font = ('Times', 20, 'bold'))
        titleFacture.place(x=120,y=20)
        
        lblMontant = Label(self.top, text = 'Total'.upper(), font = ('Arial', 15))
        lblMontant.place(x=10,y=110)
        entryMontant = Entry(self.top,textvariable = self.montant, width = 20, font = ('Arial', 13), state = 'readonly', justify = RIGHT)
        entryMontant.place(x=120, y=110)
        
        lblRecu = Label(self.top, text = 'Recu '.upper(), font = ('Arial', 15))
        lblRecu.place(x=10,y=160)
        self.entryRecu = Entry(self.top,textvariable = self.somme, width = 20, font = ('Arial', 13), justify = RIGHT)
        self.entryRecu.focus()
        self.entryRecu.place(x=120, y=160)
        self.entryRecu.bind("<Return>", self.valider)
        
        lblRemise = Label(self.top, text = 'Remise'.upper(), font = ('Arial', 15))
        lblRemise.place(x=10,y=210)
        entryRemise = Entry(self.top,textvariable = self.remise, width = 20, font = ('Arial', 13), state = 'readonly', justify = RIGHT)
        entryRemise.place(x=120, y=210)

        self.btn_total = Button(self.top, text = 'OK', width = 15, font = ('Arial', 12), state = 'disabled')#, command = self.generate_bill
        self.btn_total.place(x=300,y=300)
        self.btn_total.bind("<Return>", self.generate_bill)
        self.somme.set('')
        self.remise.set('')
    #-------------------------*** REMISE AND PAYMENT ***--------------------------
    def Paid_result(self):
        self.amount = float(self.somme.get())
        self.our_total = float(self.final_price)
        
        self.to_give = float(self.amount-self.our_total)
        
    #================= TOP LEVEL BINDING==================
    def valider(self, event, *args, **kwargs):
        if self.somme.get() < self.final_price:
            messagebox.showwarning('Statut', 'Votre somme est trop petit'.upper())
            self.somme.set('')
            self.entryRecu.focus()
        elif self.somme == "":
            messagebox.showwarning('','Valider un montant'.upper())
        elif self.somme != "" and (self.btn_total['state'] == 'disabled'):
            self.btn_total['state'] = 'normal'
            self.amount = float(self.montant.get())
            self.our_total = float(self.final_price)
            self.to_give = float(self.somme.get()) - float(self.amount)
            self.remise.set(self.to_give)
            self.btn_total.focus()
        else:
            self.btn_total['state'] = 'normal'
#================================== FINAL PAYMENT UP =================================

    #================================ Bill generator and header ==================================
    def generate_bill(self, *args,**kwargs):
        self.top.withdraw()
        # ============= invoice header =============
        #---------- create directory for sales -------------
        directory = 'C:/MY_INV/Invoices/' + str(date) + '/' + str()
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        #============= TEMPLATES BILL HEADER ===========
        company = '\tCompany Name\n'
        adress = '\tCompany Adresse \n'
        phone = '\tCompany phone number \n'
        type_s = '\tInvoices \n'
        #dt = '\t\t ' + str(date)
        dt = '\t'+str(edate) +" "+ str(etime)
        
        header_inv = '\n\t==============================\nProduits\tQte\tPrix\n\t=============================='
        final = company + adress + phone + type_s + dt + '\n' + header_inv
        
        
        file_name = str(directory) +  str(random.randrange(10000, 999999)) + '.txt'
        f = open(file_name, 'w')
        f.write(final)

        #========= bill dynamic ========
        r = 1
        i = 0
        for t in products_list:
            f.write('\n' +str(products_list[i])+'\t' +str(product_quantity[i]) +'\t' +str(product_price[i]))
            i += 1
            r += 1
        #======================== bill footer generator =====================
        f.write('\n\t==============================\n')
        f.write('\n\t\tTotal '+"  "+ str(sum(product_price)) + ' HTD')
        f.write('\n\t\tRemise '+"  "+ str(self.to_give) + ' HTD')
        f.write('\n\n\n ****   Merci a Bientot   ****')
        #os.startfile(file_name, 'print')
        f.close()
        #=========== diminution de stock ==========
        self.x = 0
        
        start = 'SELECT * FROM inventory WHERE id=?'
        result = cur.execute(start, (product_id[self.x], ))
        
        for i in products_list:
            for r in result:
                self.old_stock = r[2]
            self.new_stock = int(self.old_stock) - int(product_quantity[self.x])
            
            #====== update stock produit
            sql = 'UPDATE inventory SET stock=? WHERE id=?'
            cur.execute(sql, (self.new_stock, product_id[self.x]))
            conn.commit()
            
            ##========= insert sales into transaction table =============changes
            sql2 = 'INSERT INTO transactions (nom_produit, quantite_produit, prix_produit, date) VALUES (?,?,?,?)'
            cur.execute(sql2, (products_list[self.x],product_quantity[self.x],product_price[self.x], date ))
            conn.commit()
            
            # =========== increase ==========
            self.x += 1
            
        for self.p in products_list:
            self.tree.delete(*self.tree.get_children())


        self.top.destroy()
        self.id_e.focus()
        
        messagebox.showinfo('','FAIT')
    
root = Tk()
obj = InvoicePay(root)    
root.mainloop()
