from tkinter import *
from tkinter import messagebox, ttk
import sqlite3, os, time


conn = sqlite3.connect('C:/MY_INV/DB/store.db')
cur = conn.cursor()

res = cur.execute('select Max(id) from inventory')
for r in res:
    id = r[0]
    
class UPDATE_MODULE:
    def __init__(self, root):
        self.root = root
        self.root.title('Modifier Produits'.upper())
        self.root.resizable(0,0)
        
        largeur = 920
        hauteur = 680

        largeur_ecran = root.winfo_screenwidth()
        hauteur_ecran = root.winfo_screenheight()

        x_coordinate = (largeur_ecran/2) - (largeur/2)
        y_coordinate = (hauteur_ecran/2) - (hauteur/2)

        root.geometry('%dx%d+%d+%d' % (largeur, hauteur, x_coordinate, y_coordinate))
#======================================= LABEL AND ENTRY===========================
#----------------------------------------------------------------------------------       
        self.lbl_titre = Label(root, text = 'Modifier produits', font = ('Times',30,'bold'),fg = 'green')
        self.lbl_titre.pack(fill=X)
         
        #=================== label and entry id ====================
        self.id = Label(root, text = 'Produit ID', font = ('Arial', 15, 'bold'))
        self.id.place(x=50,y=60)
        
        self.id_e = Entry(root, width = 15, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.id_e.place(x=250,y=60)
        self.id_e.focus()
        
        self.lbl_nom = Label(root, text = 'Nom Produit', font = ('Arial', 15, 'bold'))
        self.lbl_nom.place(x=50, y=90)
        
        self.nom_e = Entry(root, width = 25, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.nom_e.place(x=250,y=90)
        
        self.lbl_stock = Label(root, text = 'Stock Produit', font = ('Arial', 15, 'bold'))
        self.lbl_stock.place(x=50, y=120)
        
        self.stock_e = Entry(root, width = 25, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.stock_e.place(x=250,y=120)
        
        self.lbl_prix = Label(root, text = 'Prix Produit', font = ('Arial', 15, 'bold'))
        self.lbl_prix.place(x=50, y=150)
        
        self.prix_e = Entry(root, width = 25, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.prix_e.place(x=250,y=150)
        
        self.search = Entry(root, width = 20, font=('Times', 15), insertwidth = 8, insertbackground = 'green')
        self.search.place(x = 670, y = 270)
        self.search.bind("<Return>", self.product_search)
        
        #========================= box text ============
        self.tbox = Text(root,width = 40, height = 10)
        self.tbox.place(x=550,y=100)
        self.tbox.insert(END,'ID has reach up to : ' + str(id))
        
        #=================== Buttons ===================
        self.btn_sync = Button(root, text = 'sync'.upper(),font = ('Times',10,'bold'),width = 12, command = self.sync)
        self.btn_sync.place(x=450,y=220)
        
        self.btn_mod = Button(root, text = 'modifier'.upper(),font = ('Times',10,'bold'),width = 12, command = self.update_func)
        self.btn_mod.place(x=350,y=220)
        
        self.btn_clear = Button(root, text = 'supprimer'.upper(),font = ('Times',10,'bold'),width = 12, command = self.clear_func)
        self.btn_clear.place(x=250,y=220)
        
        self.btn_search = Button(root, text = 'recherche'.upper(), font = ('Times',10,'bold'),width = 12, command = self.search_func)
        self.btn_search.place(x=410,y=60)
        
        #=============TREEVIEW AND STYLE  ========
        style = ttk.Style()
        
        style.theme_use('clam')# Default, vista
        
        style.configure('Treeview',
                        #background = 'darkblue',
                        relief = 'flat',
                        borderwidth = 0,
                        foreground ="red",
                        rowheight = 25,
                        font = ('Arial', 13)
                        )
        
        style.map('Treeview',
                 background = [('selected', 'green')])
        
        #============= treeview display ===============
        self.tree = ttk.Treeview(self.root, column = (1,2,3,4), height = 5, show = "headings")
        self.tree.place(x = 0, y = 300, width = 900, height = 380)
        
        vsb = ttk.Scrollbar(self.root , orient="vertical",command=self.tree.yview)
        vsb.place(x=900, y=300, height=380, width =20)
        self.tree.configure(yscrollcommand=vsb.set)

#================================= treeview entete ============================
        self.tree.heading(1, text ="identifiant".upper())
        self.tree.heading(2, text ="nom produit".upper())
        self.tree.heading(3, text = "quantite stock".upper())
        self.tree.heading(4,text = "prix produit".upper())

        #==========================
        self.tree.column(1, width=50, anchor = 'center')
        self.tree.column(2, width=200, anchor = 'center')
        self.tree.column(3, width=150, anchor = 'center')
        self.tree.column(4, width=150, anchor = 'center')
        
        conn = sqlite3.connect("C:/MY_INV/DB/store.db")
        cur = conn.cursor()
        select = cur.execute("select * from inventory")
        conn.commit()
        for row in select:
            self.tree.insert('' , END , values = row)
        conn.close() 
        
    def sync(self, *args, **kwargs):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("C:/MY_INV/DB/store.db")
        cur = conn.cursor()
        select = cur.execute("select * from inventory")
        conn.commit()
        for row in select:
            self.tree.insert('' , END , values = row)
        conn.close()
        self.id_e.focus()
        
    def search_func(self, *args, **kwargs):
        num_id = self.id_e.get()
        if num_id =="":
            messagebox.showinfo('INFO','Vous devez taper le numero a modifier'.upper())
        else:
            sql1 = 'select * from inventory where id=?'
            res = cur.execute(sql1,(self.id_e.get())) 
            for r in res:
                self.n1 = r[1] #name
                self.n2 = r[2] #stock
                self.n3 = r[3] #price
            conn.commit()

            self.nom_e.delete(0, END)
            self.nom_e.insert(0, str(self.n1))
            
            self.stock_e.delete(0, END)
            self.stock_e.insert(0, str(self.n2))
            
            self.prix_e.delete(0, END)
            self.prix_e.insert(0, str(self.n3))

            
    def product_search(self,event,*args, **kwargs):
        for i in self.tree.get_children():
            self.tree.delete(i)
    
        nom = self.search.get()
        if nom == "":
            messagebox.showinfo("statut de recherche", "vous devez taper un nom")
        else:
            conn = sqlite3.connect("C:/MY_INV/DB/store.db")
            cur = conn.cursor()
            select = cur.execute("SELECT*FROM inventory where `nom_produit` = (?) " , (nom,))
            conn.commit()
            select = list(select)
            for row in select:
                self.tree.insert('' , END , values = row )
            self.search.delete(0, END)
            self.tree.selection_set(self.tree.get_children()[0])
            conn.close()
        
    def update_func(self,*args,**kwargs):
        self.u1 = self.nom_e.get()
        self.u2 = self.stock_e.get()
        self.u3 = self.prix_e.get()
        
        if self.u1 =="" or self.u2=="" or self.u3 =="":
            messagebox.showwarning('ATTENTION','verifier si les champs sont rempli'.upper())
        else:   
            query = 'update inventory set nom_produit=?,stock=?,prix=? where id=?'
            cur.execute(query, (self.u1,self.u2,self.u3,self.id_e.get()))
            conn.commit()
            
            self.sync()
            self.clear_func()
            messagebox.showinfo('INFO','VOTRE MODIFICATION EST VALIDER')
            self.id_e.focus()
    
    def clear_func(self,*args,**kwargs):
        #num = id + 1
        self.id_e.delete(0,END)
        self.nom_e.delete(0,END)
        self.stock_e.delete(0,END)
        self.prix_e.delete(0,END)
        self.id_e.focus()
        
root = Tk()
ob = UPDATE_MODULE(root)
root.mainloop()