from tkinter import *
from tkinter import messagebox, ttk
import sqlite3, os


conn = sqlite3.connect('C:/MY_INV/DB/store.db')
cur = conn.cursor()

res = cur.execute('select Max(id) from inventory')
for r in res:
    id = r[0]
    
class ADD_MODULE:
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.root.title('Ajouter Produits'.upper())
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
        self.lbl_titre = Label(root, text = 'Nouveau produits', font = ('Times',30,'bold'),fg = 'green')
        self.lbl_titre.pack(fill=X)
        
        self.lbl_nom = Label(root, text = 'Nom Produit', font = ('Arial', 15, 'bold'))
        self.lbl_nom.place(x=50, y=100)
        
        self.nom_e = Entry(root, width = 25, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.nom_e.place(x=250,y=100)
        self.nom_e.focus()
        
        self.lbl_stock = Label(root, text = 'Stock Produit', font = ('Arial', 15, 'bold'))
        self.lbl_stock.place(x=50, y=130)
        
        self.stock_e = Entry(root, width = 25, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.stock_e.place(x=250,y=130)
        
        self.lbl_prix = Label(root, text = 'Prix Produit', font = ('Arial', 15, 'bold'))
        self.lbl_prix.place(x=50, y=160)
        
        self.prix_e = Entry(root, width = 25, font = ('Times', 15, 'bold'), insertwidth = 8, insertbackground = 'green')
        self.prix_e.place(x=250,y=160)
        
        #========================= box text ============
        self.tbox = Text(root,width = 40, height = 10)
        self.tbox.place(x=550,y=100)
        self.tbox.insert(END,'L\'identifiant du dernier produit \n est : ' + str(id))
        
        #=================== Buttons ===================
        self.search = Entry(root, width = 19, font=('Times', 15), insertwidth = 8, insertbackground = 'green')
        self.search.place(x = 680, y = 270)
        self.search.bind("<Return>", self.product_search)
        
        self.btn_sync = Button(root, text = 'sync'.upper(),font = ('Times',10,'bold'), command = self.sync)
        self.btn_sync.place(x=475,y=270)
        
        self.btn_add = Button(root, text = 'ajouter'.upper(),font = ('Times',10,'bold'), command = self.add_func)
        self.btn_add.place(x=405,y=270)
        
        self.btn_sup = Button(root, text = 'supprimer'.upper(), font = ('Times',10,'bold'), command = self.supprimer)
        self.btn_sup.place(x=320,y=270)
        
        self.btn_clear = Button(root, text = 'effacer'.upper(),font = ('Times',10,'bold'), command = self.clear_func)
        self.btn_clear.place(x=252,y=270)
        
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
        
    def sync(self, *args, **kwargs):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("C:/MY_INV/DB/store.db")
        cur = conn.cursor()
        select = cur.execute("select * from inventory")
        conn.commit()
        for row in select:
            self.tree.insert('' , END , values = row)
        conn.close()
        
    def add_func(self, *args, **kwargs):
        self.name = self.nom_e.get()
        self.qt = self.stock_e.get()
        self.px = self.prix_e.get()
        
        if self.name == '' or self.qt == '' or self.px == '':
            messagebox.showwarning('ATTENTION','IL FAUT REMPLIR LES CHAMPS')
        else:
            sql = 'insert into inventory(nom_produit,stock,prix)values(?,?,?)'
            cur.execute(sql,(self.name,self.qt,self.px))
            conn.commit()
            #=================== textarea =============
            self.tbox.insert(END, '\n\nInsert'+str(self.name)+' into the DB')
            
            messagebox.showinfo('SUUCCES','PRODUIT AJOUTER A VOTRE DB')
            self.nom_e.focus()
            self.clear_func()
            self.sync()
            
    def supprimer(self, *args, **kwargs):
        try:
            noSelection = self.tree.item(self.tree.selection())['values'][0]
            conn = sqlite3.connect("C:/MY_INV/DB/store.db")
            cur = conn.cursor()
            delete = cur.execute("delete from inventory where id = {}".format(noSelection))
            conn.commit()
            conn.close()
            self.tree.delete(self.tree.selection())
        except IndexError:
            messagebox.showinfo('Info'.upper(), 'veillez selection un champ a supprimer'.upper())
        
    def clear_func(self,*args,**kwargs):
        #num = id + 1
        self.nom_e.delete(0,END)
        self.stock_e.delete(0,END)
        self.prix_e.delete(0,END)
        self.nom_e.focus()
        
root = Tk()
ob = ADD_MODULE(root)
root.mainloop()