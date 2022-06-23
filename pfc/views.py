from http import client
from matplotlib.pyplot import get
from matplotlib.style import context
from utils import get_db_handle, get_collection_handle
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import post, request
import pymongo
import pandas as pd
import pandas_profiling as pp
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import numpy as np
 
 
 
def profilage1(request):
        db_handle=get_db_handle()
        clients= get_collection_handle(db_handle,"clients")
        df = pd.DataFrame(list(clients.find()))
        prof = pp.ProfileReport(df)
        prof.to_file("templates/pfc/output1.html")
        return render(request,'pfc/output1.html')
       
def profilage2(request):
    db_handle=get_db_handle()
    clients= get_collection_handle(db_handle,"BaseDonnées")
    df = pd.DataFrame(list(clients.find()))
    prof = pp.ProfileReport(df)
    prof.to_file("templates/pfc/output2.html")
    return render(request,'pfc/output2.html')    
 
def profilage3(request):
    db_handle=get_db_handle()
    clients= get_collection_handle(db_handle,"produits")
    df = pd.DataFrame(list(clients.find()))
    prof = pp.ProfileReport(df)
    prof.to_file("templates/pfc/output3.html")
    return render(request,'pfc/output3.html')
 
def index(request):
    return render(request,'pfc/base.html')
    
def col1(request):
    if request.method == 'POST':
        db_handle=get_db_handle()
        produits= get_collection_handle(db_handle,"produits")
        df = pd.DataFrame(list(produits.find()))
 
        if request.POST.get('dedup2',None)=='on':
            duplicateRows = df[df.duplicated(subset=['productName'], keep =False)]
            df.drop_duplicates(subset=['productName'],keep='first', inplace=True)
 
        if request.POST.get('concat2',None)=='on':
            df = pd.DataFrame(df, columns= ['_id','productName','type','brand','url','priceNow','priceOld','percentage'])
            df['ProduitType']=df['type'].fillna('').map(str) + ' '+ df['brand'].fillna('')  
        return render(request,"pfc/dedup1.html",context={'list':df.values.tolist()})
 
def col3(request):
    if request.method == 'POST':
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
       
        if request.POST.get('concat3',None)=='on':
            df = pd.DataFrame(df, columns= ['n','n commande','date creation','date expedition','dernier statut','date dernier statut','date livraison/echec','prenom','nom','Gender','telephone','adresse','commune','wilaya','designation','prix','type','Brandt','frais livraison','freeshipping','paiement','id importation','type colis','premiere tentative','date premiere tentative','deuxieme tentative','date deuxieme tentative','troisieme tentative','date troisieme tentative'])
            df['fullname']=df['prenom'].fillna('').map(str) + ' '+ df['nom'].fillna('')
            df.fillna("-",inplace=True)
 
        if request.POST.get('invalid3',None)=='on':
            df = df.astype(str)
            df["telephone"]=df["telephone"].str.replace(' ', '')
            split_data = df["telephone"].str.split(".")
            data = split_data.to_list()
            names = ["telephone", "zeros"]
            new_df = pd.DataFrame(data, columns=names)
            df["telephone"]=new_df["telephone"]
            pd.set_option('display.max_rows',None)
            df['length'] = df.telephone.str.len()
            df = df[df.length == 9]
        if request.POST.get('omise3',None)=='on':
            df.fillna('inconnu', inplace = True)
 
        return render(request,"pfc/dedup2.html",context={'listt':df.values.tolist()})
 
def col8(request):
    if request.method=='POST':
        db_handle=get_db_handle()
        bd=get_collection_handle(db_handle,"BaseDonnées")
        df = pd.DataFrame(list(bd.find()))
 
    if request.POST.get('dedup1',None)=='on':
        duplicateRows = df[df.duplicated(subset=['designation'], keep =False)]
        df.drop_duplicates(subset=['designation'],keep='first', inplace=True)
   
    if request.POST.get('concat1',None)=='on':
        df = pd.DataFrame(df, columns= ['_id','nomtype','idproduit','designation','prix_unit','idmarque'])
        df['typeMarque']=df['idmarque'].fillna('').map(str) + ' '+ df['nomtype'].fillna('')
        df.fillna("-",inplace=True)
 
    if request.POST.get('miss1',None)=='on':
        df.fillna('inconnu', inplace = True)
 
    return render(request,"pfc/col8.html",context={'listbd':df.values.tolist()})
 
def col4(request):
    if request.method=='POST':
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
 
    return render(request,"pfc/df.html",context={'lists':df.values.tolist()})
 
def col5(request):
    if request.method=='POST':
        db_handle=get_db_handle()
        produits=get_collection_handle(db_handle,"produits")
        df=pd.DataFrame(list(produits.find()))
   
    return render(request,"pfc/col5.html",context={'listp':df.values.tolist()})
 
def col6(request):
    if request.method=='POST':
        db_handle=get_db_handle()
        based=get_collection_handle(db_handle,'BaseDonnées')
        df=pd.DataFrame(list(based.find()))
        df.fillna("-",inplace=True)
   
    return render(request,"pfc/col6.html",context={'listb':df.values.tolist()})
 
def col7(request):
    if request.method=="POST":
        if request.POST.get('qgender',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            qgender=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$Gender", "ca" : 
            {"$sum" :"$prix"}}} ] )
            df=list( db_handle.clients.aggregate(qgender))
        elif request.POST.get('qdate',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)        
            qdate=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$date creation", "ca" : 
            {"$sum" :"$prix"}}} ] )
            df=list(db_handle.clients.aggregate(qdate))
        elif request.POST.get('qtype',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            qtype=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$type", "ca" : 
            {"$sum" :"$prix"}}} ] )
            df=list(db_handle.clients.aggregate(qtype))
           
        else:
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            qgeo=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$wilaya", "ca" : 
            {"$sum" :"$prix"}}} ] )
            df=list(db_handle.clients.aggregate(qgeo))
        l=[]
        for element in df:
            l.append({'id':element['_id'],'ca':element['ca']})
 
        print(l)
        return render(request,"pfc/col7.html",
        context={'listqd':l})
       
 
def col9(request):
    if request.method=="POST":
        if request.POST.get('rgender',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            rgender=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$Gender", "Nbrventes" : 
            {"$sum" : 1}}} ] )
            df=list( db_handle.clients.aggregate(rgender))
        elif request.POST.get('rdate',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)        
            rdate=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$date creation", "Nbrventes" : 
            {"$sum" :1}}} ] )
            df=list(db_handle.clients.aggregate(rdate))
        elif request.POST.get('rtype',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            rtype=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$type", "Nbrventes" : 
            {"$sum" :1}}} ] )
            df=list(db_handle.clients.aggregate(rtype))
           
        else:
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            rgeo=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$wilaya", "Nbrventes" : 
            {"$sum" :1}}} ] )
            df=list(db_handle.clients.aggregate(rgeo))
        l=[]
        for element in df:
            l.append({'id':element['_id'],'Nbrventes':element['Nbrventes']})
 
        print(l)
        return render(request,"pfc/col9.html",
        context={'listrd':l})
 
def col10(request):
    if request.method=="POST":
        if request.POST.get('lgender',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            lgender=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$Gender", "livraison" : 
            {"$sum" : "$frais livraison"}}} ] )
            df=list( db_handle.clients.aggregate(lgender))
        elif request.POST.get('ldate',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)        
            ldate=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$date creation", "livraison" : 
            {"$sum" :"$frais livraison"}}} ] )
            df=list(db_handle.clients.aggregate(ldate))
        elif request.POST.get('ltype',None)=='on':
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            ltype=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$type", "livraison" : 
            {"$sum" :"$frais livraison"}}} ] )
            df=list(db_handle.clients.aggregate(ltype))
           
        else:
            db_handle=get_db_handle()
            clients=get_collection_handle(db_handle,"clients")
            df=pd.DataFrame(list(clients.find()))
            df.fillna("-",inplace=True)
            lgeo=([ {"$match": {"dernier statut": "Livre"}}, 
            {"$group" : {"_id" : "$wilaya", "Nbrventes" : 
            {"$sum" :"$frais livraison"}}} ] )
            df=list(db_handle.clients.aggregate(lgeo))
        l=[]
        for element in df:
            l.append({'id':element['_id'],'livraison':element['livraison']})
 
        print(l)
        return render(request,"pfc/col10.html",
        context={'listl':l})

def stat(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$Gender", "nbrventes" : {"$sum" : 1}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_nbrventes = []
        l_id = []
        for obj in df :
             l_nbrventes.append(obj["nbrventes"])
             l_id.append(obj["_id"])
             
        labels = ['Inconnu', 'H', 'F']
        # Création du graphe
        x = np.arange(len(l_id))
        plt.figure(figsize = (10, 5))
        plt.bar(x, l_nbrventes, color ='green', width = 0.5)
        plt.xlabel("Genre")
        plt.ylabel("nbrventes")
        plt.title("Nombres des ventes par rapport aux Genre")
        plt.xticks( rotation=60)
        plt.xticks(x, labels)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat2(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$wilaya", "nbrventes" : {"$sum" : 1}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        # labels = ['Mila', 'Bordj Bou Arreridj',  'H', 'F']
        # Création du graphe
        # x = np.arange(len(l_id))
        plt.figure(figsize = (10, 5))
        plt.bar(l_id, l_nbrventes, color ='green', width = 0.5)
        plt.xlabel("Wilaya")
        plt.ylabel("nbrventes")
        plt.title("Nombres de ventes par rapport aux wilaya")
        plt.xticks( rotation=60)
        # plt.xticks(l_id, labels)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat3(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$date creation", "nbrventes" : {"$sum" : 1}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        # labels = ['Mila', 'Bordj Bou Arreridj',  'H', 'F']
        # Création du graphe
        x = np.arange(len(l_id))
        plt.figure(figsize = (10, 5))
        plt.bar(x, l_nbrventes, color ='green', width = 0.5)
        plt.xlabel("DATE")
        plt.ylabel("nbrventes")
        plt.title("Nombre de ventes par rapport à la Date")
        plt.xticks( rotation=60)
        # plt.xticks(l_id, labels)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat4(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$type", "nbrventes" : {"$sum" : 1}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        labels = [l_id]
        # Création du graphe
        # x = np.arange(len(l_id))
        plt.figure(figsize = (10, 5))
        plt.bar(l_id, l_nbrventes, color ='green', width = 0.5)
        plt.xlabel("Type")
        plt.ylabel("nbrventes")
        plt.title("Nombres de ventes par rapport aux types des produits")
        plt.xticks( rotation=60)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat5(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$Gender", "nbrventes" : {"$sum" : "$prix"}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        # x = np.arange(len(l_id))
        plt.figure(figsize = (7, 5))
        # x = np.random.normal(x,l_nbrventes)
        plt.pie(l_nbrventes, labels=l_id )
        # plt.xlabel("Type")
        # plt.ylabel("nbrventes")
        plt.title("")
        # plt.xticks(l_id, labels)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat6(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$wilaya", "nbrventes" : {"$sum" : "$prix"}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        # x = np.arange(len(l_id))
        plt.figure(figsize = (7, 5))
        # x = np.random.normal(x,l_nbrventes)
        plt.pie(l_nbrventes, labels=l_id, shadow = True)
        # plt.xlabel("Type")
        # plt.ylabel("nbrventes")
        plt.title("")
        # plt.xticks(l_id, labels)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
   
def stat7(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$type", "ChiffreA" : {"$sum" : "$prix"}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_ChiffreA = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_ChiffreA.append(obj["ChiffreA"])
        # x = np.arange(len(l_id))
        plt.figure(figsize = (7, 5))
        # x = np.random.normal(x,l_nbrventes)
        plt.pie(l_ChiffreA, labels=l_id, shadow = True)
        # plt.xlabel("Type")
        # plt.ylabel("nbrventes")
        plt.title("")
        # plt.xticks(l_id, labels)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat8(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$type", "nbrventes" : {"$sum" : 1}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        # x = np.arange(len(l_id))
        plt.figure(figsize = (7, 5))
        # x = np.random.normal(x,l_nbrventes)
        plt.plot(l_id,l_nbrventes, 'm--')
        # plt.xlabel("Type")
        # plt.ylabel("nbrventes")
        plt.title("")
        plt.xticks(rotation=60)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def stat9(request):
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
        df.fillna("-",inplace=True)
        p=([ {"$match": {"dernier statut": "Livre"}}, {"$group" : {"_id" : "$wilaya", "nbrventes" : {"$sum" : 1}}} ] )
        df=list( db_handle.clients.aggregate(p))
 
        l_id = []
        l_nbrventes = []
       
        for obj in df :
             l_id.append(obj["_id"])
             l_nbrventes.append(obj["nbrventes"])
        # x = np.arange(len(l_id))
        plt.figure(figsize = (7, 5))
        # x = np.random.normal(x,l_nbrventes)
        plt.scatter(l_id, l_nbrventes, c ="blue")
        # plt.xlabel("Type")
        # plt.ylabel("nbrventes")
        plt.title("")
        plt.xticks(rotation=60)
        plt.show()
        return render(request,"pfc/base.html",context= {'graphe':plt})
 
def statl1(request):
    pass

def statl2(request):
    pass

def statl3(request):
    pass

def statl4(request):
    pass

def export1(request):
   
        db_handle=get_db_handle()
        clients=get_collection_handle(db_handle,"clients")
        df=pd.DataFrame(list(clients.find()))
   
        df = pd.DataFrame(df, columns= ['n','n commande','date creation','date expedition','dernier statut','date dernier statut','date livraison/echec','prenom','nom','Gender','telephone','adresse','commune','wilaya','designation','prix','type','Brandt','frais livraison','freeshipping','paiement','id importation','type colis','premiere tentative','date premiere tentative','deuxieme tentative','date deuxieme tentative','troisieme tentative','date troisieme tentative'])
        df['fullname']=df['prenom'].fillna('').map(str) + ' '+ df['nom'].fillna('')
        df.fillna("-",inplace=True)
        df1=df.astype(str)
        df1["telephone"]=df1["telephone"].str.replace(' ', '')
        split_data = df1["telephone"].str.split(".")
        data = split_data.to_list()
        names = ["telephone", "zeros"]
        new_df = pd.DataFrame(data, columns=names)
        df1["telephone"]=new_df["telephone"]
        pd.set_option('display.max_rows',None)
        df1['length'] = df1.telephone.str.len()
        df1 = df1[df1.length == 9]
        df1.fillna('inconnu', inplace = True)
        # data = pd.read_csv(filename, encoding= 'unicode_escape')
        df1.to_excel("templates/pfc/excel.xlsx", index= False, encoding= 'unicode_escape')
        return render(request,'pfc/excel.xlsx')
 
def export2(request):
       db_handle=get_db_handle()
       produits= get_collection_handle(db_handle,"produits")
       df = pd.DataFrame(list(produits.find()))
       duplicateRows = df[df.duplicated(subset=['productName'], keep =False)]
       df.drop_duplicates(subset=['productName'],keep='first', inplace=True)
       df1 = pd.DataFrame(df, columns= ['_id','productName','type','brand','url','priceNow','priceOld','percentage'])
       df1['ProduitType']=df1['type'].fillna('').map(str) + ' '+ df['brand'].fillna('')  
       df1.to_excel("templates/pfc/excel1.xlsx", index= False, encoding= 'unicode_escape')
       return render(request,'pfc/excel1.xlsx')
 
def export3(request):
        db_handle=get_db_handle()
        bd=get_collection_handle(db_handle,"BaseDonnées")
        df = pd.DataFrame(list(bd.find()))
        duplicateRows = df[df.duplicated(subset=['designation'], keep =False)]
        df.drop_duplicates(subset=['designation'],keep='first', inplace=True)
        df1 = pd.DataFrame(df, columns= ['_id','nomtype','idproduit','designation','prix_unit','idmarque'])
        df1['typeMarque']=df1['idmarque'].fillna('').map(str) + ' '+ df1['nomtype'].fillna('')
        df1.fillna("-",inplace=True)
        df1.fillna('inconnu', inplace = True)
        df1.to_excel("templates/pfc/excel2.xlsx", index= False, encoding= 'unicode_escape')
        return render(request,'pfc/excel2.xlsx')

