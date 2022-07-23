#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 14:50:33 2022

@author: sk
"""

import random
import copy
import numpy as np
import matplotlib.pyplot as plt

inputs = ["a_an_example.in.txt", "c_coarse.in.txt", "e_elaborate.in.txt", "b_basic.in.txt", "d_difficult.in.txt"]
nivel = 4


def escribe(fichero,variable):
    f = open(str(fichero)+".txt", "a") # a<-w si quieres que pise
    f.write(str(variable))
    f.close()
    
    
# dadas 2 lineas de input
# devuelve persona: [[likes],[dislikes]]
def person(l):
    res = []
    for i in [0,1]:
        # like , dislike
        res.append(l[i].split("\n")[0].split(" ")[1:])
    return res

# dado el fichero input por lineas    
# devuelve limpio personas = [persona0,persona1,...]
def limpia(crudo):
    res = []
    i = 1
    while i+2<=len(crudo):
        res.append(person(crudo[i:i+2]))
        i+=2
    return res

# dados ingredientes y persona
# devuelve 1 si va a ir o 0 si no
def scoreP(ingredientes, persona):
    res = 1
    for like in persona[0]:
        if like not in ingredientes:
            return 0 
    for dislike in persona[1]:
        if dislike in ingredientes:
            return 0 
    return res

# daos ingredientes y personas
# devuelve cuantas personas iran
def score(ingredientes, personas):
    res = 0
    for persona in personas:
        res+=scoreP(ingredientes,persona)
    return res
        
        
personas = limpia(open('input_data/'+inputs[nivel], 'r').readlines())

# dadas personas
# devuelve lista de ingredientes existentes ordenadas
def getIngredientes(personas):
    res = []
    for persona in personas:
        for ingrediente in persona[0]+persona[1]:
            if ingrediente not in res:
                res.append(ingrediente)
    if nivel == 2 or nivel == 4: res.sort(key=lambda ingrediente: int(ingrediente.split("ingredient")[1]))
    else: res.sort()
    return res

ingredientesTotales = getIngredientes(personas)

print("HAY ", len(personas), " PERSONAS ")
print("HAY ", len(ingredientesTotales), " INGREDIENTES ")



def h(ingrediente, personas):
    res = 0
    for p in personas:
        # like
        if ingrediente in p[0]: 
            #print(ingrediente, " gusta a ",p)
            res+=1 
        # dislike
        if ingrediente in p[1]: 
            res-=1
            #print(ingrediente, " no gusta a ",p)
        # suda
        if ingrediente not in p[0]+p[1]: 
            res+=0
            #print(ingrediente, " suda a ",p)
    return res


#heuristica = {ing: h(ing,personas) for ing in ingredientesTotales}
#heuristicaLista = sorted(heuristica.items(), key=lambda x: -x[1])
#heuristica = dict(heuristicaLista)
#ingredientesOrdenados = list(heuristica)

#heuristica = dict(heuristicaLista)
#heuristicaLista = sorted(heuristica.items(), key=lambda x: -x[1])


#listaHeuristica = list(heuristica)
##############################################################3

"""
def hopi(personas):
    heuristicaIngredientes = {ing: 0 for ing in ingredientesTotales}
    heuristicaClientes = {i: 0 for i in range(len(personas))}
    for i in range(len(personas)):
        p = personas[i]
        for like in p[0]:
            heuristicaIngredientes[like]+=1/(len(p[0])+len(p[1]))
        for dislike in p[1]:
            heuristicaIngredientes[dislike]-=1/(len(p[0])+len(p[1]))
        heuristicaClientes[i]=len(p[0])+len(p[1])
    return heuristicaIngredientes, heuristicaClientes

"""

def interseccionVacia(l1,l2):
    for li in l1:
        if li in l2:
            return 0
    return 1

def clientesIncompatibles(personas):
    #heuristicaClientesIncompatibles = {i: [] for i in range(len(personas))}
    heuristicaClientesIncompatibles = {i: 0 for i in range(len(personas))}
    for i in range(len(personas)):
        ci = personas[i]
        for j in range(len(personas)):
            if j>i:
                cj = personas[j]
                if interseccionVacia(ci[0],cj[1]) and interseccionVacia(ci[1],cj[0]):
                    #heuristicaClientesIncompatibles[i].append(j)
                    #heuristicaClientesIncompatibles[j].append(i)
                    heuristicaClientesIncompatibles[i]+=1
                    heuristicaClientesIncompatibles[j]+=1
    return heuristicaClientesIncompatibles
 
heuristicaClientesIncompatibles = clientesIncompatibles(personas) 
      
heuristicaClientesIncompatiblesLista = sorted(heuristicaClientesIncompatibles.items(), key=lambda x: -x[1])
heuristicaClientesIncompatibles = dict(heuristicaClientesIncompatiblesLista)
clientesIncompatiblesOrdenados = list(heuristicaClientesIncompatibles)


def clienteMete(ingredientes):
    global personas, clientesIncompatiblesOrdenados, heuristicaClientesIncompatibles
    scoreActual = score(ingredientes,personas)
    for ci in clientesIncompatiblesOrdenados:
        n = ingredientes[:]
        if scoreP(n,personas[ci])==0:
            for likes in personas[ci][0]:
                if likes not in n:
                    n.append(likes)
            for dislikes in personas[ci][1]:
                if dislikes in n:
                    n.remove(dislikes)
                    
            scoreNuevo = score(n,personas)
            if scoreNuevo>scoreActual:
                print(" aniado a C ", ci," con ",heuristicaClientesIncompatibles[ci]," score: ", scoreNuevo)
                return n
    print("sorry bro clienteU")
    return ingredientes

"""
scores = []
n = []
for i in range(len(clientesIncompatiblesOrdenados)):
    n = clienteMete(n)
    scores.append([i, score(n,personas)])
    
plt.plot([s[1] for s in scores])

scores = sorted(scores, key=lambda x: -x[1])
"""


def hopi(personas):
    heuristicaClientes = {i: 0 for i in range(len(personas))}
    sumaClientes = 0
    for i in range(len(personas)):
        p = personas[i]
        heuristicaClientes[i]=len(p[0])+len(p[1])
        sumaClientes+=len(p[0])+len(p[1])
    
    heuristicaIngredientes = {ing: 0 for ing in ingredientesTotales}
    for i in range(len(personas)):
        p = personas[i]
        for like in p[0]:
            heuristicaIngredientes[like]+=(1) #/(len(p[0])+len(p[1]))) #/(heuristicaClientes[i]/sumaClientes)
        for dislike in p[1]:
            heuristicaIngredientes[dislike]-=1 #/(len(p[0])+len(p[1])) #/(heuristicaClientes[i]/sumaClientes)
        
        
        
    return heuristicaIngredientes, heuristicaClientes

heuristicaIngredientes, heuristicaClientes = hopi(personas)

heuristicaIngredientesLista = sorted(heuristicaIngredientes.items(), key=lambda x: -x[1])
heuristicaIngredientes = dict(heuristicaIngredientesLista)
ingredientesOrdenados = list(heuristicaIngredientes)

heuristicaClientesLista = sorted(heuristicaClientes.items(), key=lambda x: x[1])
heuristicaClientes = dict(heuristicaClientesLista)
clientesOrdenados = list(heuristicaClientes)
            
def union(u1,u2):
    res = u1[:]
    [res.append(ui) for ui in u2 if ui not in u1]
    return res

def cuentaDislikes(ingrediente,personas):
    res = []
    for p in personas:
        if ingrediente in p[1]:
            res.append(p)
    return res
"""
scores = []
ingredientes = []
#for i in range(len(clientesOrdenados)):
for c in clientesOrdenados:
    ingredientes = union(ingredientes,personas[c][0])
    scores.append([clientesOrdenados, score(ingredientes,personas)])
    
plt.plot([s[1] for s in scores])

scores = sorted(scores, key=lambda x: -x[1])
"""



        
#"""

#tipica
scores = []
for i in range(len(ingredientesOrdenados)):
    scores.append([ingredientesOrdenados[:i], score(ingredientesOrdenados[:i],personas)])
    
plt.plot([s[1] for s in scores])

scores = sorted(scores, key=lambda x: -x[1])



    
#############################################



def nuevosCandidatos(ingredientes):
    res = []
    global ingredientesOrdenados
    for ing in ingredientesOrdenados:
        if ing not in ingredientes:
            res.append(ing)
    return res

def swapeauno(ingredientes):
    res = ingredientes[:]
    scoreActual = score(ingredientes,personas)
    vecinos = nuevosCandidatos(ingredientes)
    for v in vecinos:
        for i in range(len(ingredientes)):
            candidato = ingredientes[i:]+ingredientes[i+1:]+[v]
            scoreNuevo = score(candidato,personas)
            if scoreNuevo>scoreActual:
                print("ENCONTRADO, voy por ", scoreNuevo)
                return candidato
    print("sorry bro")
    return ingredientes
    
def aniadeuno(ingredientes):
    global ingredientesOrdenados, heuristicaIngredientes
    scoreActual = score(ingredientes,personas)
    #vecinos = nuevosCandidatos(ingredientes)
    for v in ingredientesOrdenados:
    #for v in vecinos:
        if v not in ingredientes:
            scoreNuevo = score(ingredientes+[str(v)],personas)
            if scoreNuevo>scoreActual:
                print(" aniado al ",v, " con ", heuristicaIngredientes[v], "score: ",scoreNuevo)
                return ingredientes+[str(v)]
    print("sorry bro aniade")
    return ingredientes
       
def quitauno(ingredientes):
    global ingredientesOrdenados, heuristicaIngredientes
    scoreActual = score(ingredientes,personas)
    #ingredientes = ingredientes[::-1]
    serva = ingredientes[:]
    for ing in ingredientesOrdenados[::-1]:
        ingredientes = serva[:]
        if ing in ingredientes:
            ingredientes.remove(ing)
            scoreNuevo = score(ingredientes,personas)
            if scoreNuevo>scoreActual:
                print(" quito al ",ing, " con ", heuristicaIngredientes[ing], "score: ",scoreNuevo)
                return ingredientes
    print("sorry bro quita")
    return serva
        
    
def aniadek(k,ingredientes):
    res = []
    scoreActual = score(ingredientes,personas)
    vecinos = nuevosCandidatos(ingredientes)
    v = random.sample(ingredientes,k)
    if k ==1: scoreNuevo = score(ingredientes+[str(v)],personas)
    else: scoreNuevo = score(ingredientes+v,personas)
    if scoreNuevo>scoreActual:
        print("ENCONTRADO, voy por ", scoreNuevo)
        if k==1: return ingredientes+[str(v)]
        else: return ingredientes+v
    print("sorry bro")
    return ingredientes
    
def quitaC(k,ingredientes):
    res = []
    quitar = random.sample(ingredientes,k)
    for ing in ingredientes:
        if ing not in quitar:
            res.append(ing)
    return res

def quita(k,ingredientes):
    scoreActual = score(ingredientes,personas)
    for _ in range(1):
        nuevo = quitaC(k,ingredientes)
        scoreNuevo = score(nuevo,personas)
        if scoreNuevo>scoreActual:
            print("ole, ",scoreNuevo)
            return nuevo
        print("nah")
    print("sorry")
    return ingredientes
    
def swapea(k,ingredientes):
    res = []
    vecinos = nuevosCandidatos(ingredientes)
    otros = random.sample(vecinos,k)
    mios = random.sample(ingredientes,k)
    if k == 1: 
        otros = [otros]
        mios = [mios]
    for ing in ingredientes:
        if ing not in mios:
            res.append(ing)
    for o in otros:
        res.append(o)
    scoreActual = score(ingredientes,personas)
    scoreNuevo = score(res,personas)
    if scoreNuevo>scoreActual:
        print("oleeee ",scoreNuevo)
        return res
    return ingredientes

##########################
def clienteUno(ingredientes):
    global personas, clientesOrdenados, heuristicaClientes, clientesIncompatiblesOrdenados
    scoreActual = score(ingredientes,personas)
    for ci in clientesIncompatiblesOrdenados:
    #for ci in clientesOrdenados:
        n = ingredientes[:]
        if scoreP(n,personas[ci])==0:
            for likes in personas[ci][0]:
                if likes not in n:
                    n.append(likes)
            for dislikes in personas[ci][1]:
                if dislikes in n:
                    n.remove(dislikes)
                    
            scoreNuevo = score(n,personas)
            if scoreNuevo>scoreActual:
                print(" aniado a C ", ci," con ",heuristicaClientes[ci]," score: ", scoreNuevo)
                return n
    print("sorry bro clienteU")
    return ingredientes

def clienteFuera(ingredientes):
    global personas, clientesOrdenados, heuristicaClientes
    scoreActual = score(ingredientes,personas)
    for ci in clientesIncompatiblesOrdenados[::-1]:
    #for ci in clientesOrdenados[::-1]:
        n = ingredientes[:]
        if scoreP(n,personas[ci])==1:
            for likes in personas[ci][0]:
                if likes in n:
                    n.remove(likes)
            for dislikes in personas[ci][1]:
                if dislikes not in n:
                    n.append(dislikes)
                    
            #n = clienteUno(n)
            scoreNuevo = score(n,personas)
            if scoreNuevo>scoreActual:
                print(" quitado a C ", ci," con ",heuristicaClientes[ci]," score: ", scoreNuevo)
                return n
    print("sorry bro clienteF")
    return ingredientes

def esteClienteFuera(clientes,ingredientes):
    cliente = [[],[]]
    for ci in clientes:
        cliente[0]+=ci[0]
        cliente[1]+=ci[1]
    global personas, clientesOrdenados, heuristicaClientes
    scoreActual = score(ingredientes,personas)
    n = ingredientes[:]
    for likes in cliente[0]:
        if likes in n:
            n.remove(likes)
    for dislikes in cliente[1]:
        if dislikes not in n:
            n.append(dislikes)
            
    scoreNuevo = score(n,personas)
    if scoreNuevo>scoreActual:
        print(" quitado cli score: ", scoreNuevo)
        return n
    print("sorry bro esteClienteFuera")
    return ingredientes

def esteClienteUno(clientes,ingredientes):
    cliente = [[],[]]
    for ci in clientes:
        cliente[0]+=ci[0]
        cliente[1]+=ci[1]
    global personas, clientesOrdenados, heuristicaClientes
    
    global personas, clientesOrdenados, heuristicaClientes
    scoreActual = score(ingredientes,personas)
    n = ingredientes[:]
    for likes in cliente[0]:
        if likes not in n:
            n.append(likes)
    for dislikes in cliente[1]:
        if dislikes in n:
            n.remove(dislikes)
                    
    scoreNuevo = score(n,personas)
    if scoreNuevo>scoreActual:
        print(" aniado a cli score: ", scoreNuevo)
        return n
    print("sorry bro esteClienteUno")
    return ingredientes

def clientesInsatisfechos(ingredientes):
    global clientesOrdenados, personas
    res = []
    for ci in clientesOrdenados:
        if scoreP(ingredientes,personas[ci])==0:
            res.append(personas[ci])
    return res

def ingredientesNoUsados(ingredientes):
    global ingredientesOrdenados
    res = []
    for ing in ingredientesOrdenados:
        if ing not in ingredientes:
            res.append(ing)
    return res

"""
scoreActual = score(n,personas)
serva = n[:]
for _ in range(1000):
    if random.random()<0.5:
        n = aniadek(2,n)
    else:
        n = quitaC(2,n)
    scor=score(n,personas)
    if scor>scoreActual:
        scoreActual=scor
        serva=n[:]
"""
def topea():
    nodo0 = scores[0][0]
    n = nodo0[:]
    nodos = [nodo0]
    s = [0,0,0,0]
    scoreActual = score(n,personas)
    escores = []
    mejorGlobal = n
    for _ in range(100000):
        escores.append(scoreActual)
        dado = random.random()
        if dado<0.25 and s[0]==0:
            n = aniadeuno(n)
            s[0]=1
        elif dado<0.5 and s[1]==0:
            n = quitauno(n)
            s[1]=1
        elif dado<0.75 and s[2]==0:
            n = clienteUno(n)
            s[2]=1
        elif s[3]==0:
            n = clienteFuera(n)
            s[3]=1
        scor = score(n,personas)
        if scor>1796:
            escribe("potencia",str(n)+"\n")
        if scor>scoreActual:
            print("MEJORADO")
            nodos.append(n)
            escribe("nodos","["+str(n)+"\n"+str(scor)+"]\n")
            s = [0,0,0,0]
            scoreActual = scor
            if scor>score(mejorGlobal,personas): 
                mejorGlobal = n
                escribe("mejorGlobal",str(n)+"\n"+str(score(mejorGlobal,personas))+"\n")
        if s[0] and s[1] and s[2] and s[3]:
            return n
            #s = [0,0,0,0]
            #print("RETROCEDO")
            #nodos = nodos[:-1]
            #n = nodos[-1]
            #scoreActual, scor = score(n,personas), score(n,personas)

#############################################
def decode(codigo):
    global ingredientesTotales
    res = []
    for c in codigo:
        res.append(ingredientesTotales[c])
    return res

def poblacionInicial(numeroIndividuos):
    global ingredientesTotales
    poblacion = []
    #maximos = max(personas, key=lambda x: int(len(x[0])))
    for _ in range(numeroIndividuos):
        individuo = []
        # uniforme
        cuantosIngredientes = random.randint(1,len(ingredientesTotales))
        for _ in range(cuantosIngredientes):
            aleatorio = random.choice(ingredientesTotales)
            if aleatorio not in individuo:
                individuo.append(aleatorio)
        poblacion.append(individuo)
    return poblacion

apariciones =  {ing: 0 for ing in ingredientesTotales}
listaApariciones = list(apariciones)

# [ [persona, score], [perso,sc], ... ]
def evalua(poblacion):
    global personas, apariciones
    evaluados = []
    for individuo in poblacion:
        evaluados.append([individuo, score(individuo, personas)])
        
       # for ingrediente in individuo:
            #print("ingrediente: ",ingrediente)
       #     apariciones[ingrediente]+=1
    
    evaluados.sort(key=lambda e: -int(e[1]))
    return [ev[0] for ev in evaluados]

  
def selecciona(evaluados):
    #print("LOS EVALUADOS SON",evaluados)
    global apariciones, ingredientesTotales
    seleccionados = []
    # 10% los mejores sin cambios
    for i in range(int(len(evaluados)/10)):
        seleccionados.append(evaluados[i])
    # 40% cruze mejores elite
    for i in range(int(len(evaluados)/5)):
        progenitor1 = random.choice(evaluados[:int(len(evaluados)/50)])
        progenitor2 = random.choice(evaluados[:int(len(evaluados)/50)])
        hijo1, hijo2 = cruza(progenitor1,progenitor2)
        seleccionados.append(hijo1)
        seleccionados.append(hijo2)
    # 10% cruze normales
    for i in range(int(len(evaluados)/20)):
        progenitor1 = random.choice(evaluados[:int(len(evaluados)/2)])
        progenitor2 = random.choice(evaluados[:int(len(evaluados)/2)])
        hijo1, hijo2 = cruza(progenitor1,progenitor2)
        seleccionados.append(hijo1)
        seleccionados.append(hijo2)
    # 10% cruze peores
    for i in range(int(len(evaluados)/20)):
        progenitor1 = random.choice(evaluados[int(len(evaluados)/2):])
        progenitor2 = random.choice(evaluados[int(len(evaluados)/2):])
        hijo1, hijo2 = cruza(progenitor1,progenitor2)
        seleccionados.append(hijo1)
        seleccionados.append(hijo2)
    
    """
    # 10% no alcanzados/peores
    apariciones = sorted(apariciones.items(), key=lambda x: x[1])
    listaApariciones = list(apariciones)
    for i in range(int(len(evaluados)/10)):
        individuo = []
        # cuantosIngredientes = random.randint(1,len(ingredientesTotales)/2)
        cuantosIngredientes = np.random.normal(len(ingredientesTotales), int(len(ingredientesTotales)/4), 1)
        for _ in range(int(cuantosIngredientes)+1):
            individuo.append(listaApariciones[-random.randint(1,int(len(listaApariciones)/10))])
        seleccionados.append(individuo)
    # 10% ft mas usados
    apariciones = dict(apariciones)
    apariciones = sorted(apariciones.items(), key=lambda x: x[1])
    listaApariciones = list(apariciones)
    for i in range(int(len(evaluados)/10)):
        individuo = []
        #cuantosIngredientes = random.randint(1,len(ingredientesTotales)/2)
        cuantosIngredientes = np.random.normal(len(ingredientesTotales), int(len(ingredientesTotales)/4), 1)
        for _ in range(int(cuantosIngredientes)+1):
            individuo.append(listaApariciones[random.randint(1,int(len(listaApariciones)/10))])
        seleccionados.append(individuo)
    """
    
    # 20% mutaos mejores
    for i in range(int(len(evaluados)/5)):
        seleccionados.append(muta(evaluados[i]))
    # 10% nuevos
    [seleccionados.append(pi) for pi in poblacionInicial(int(len(evaluados)/10))]
    
    return seleccionados
    
        
        
    
def cruza(individuo1, individuo2):
    descendiente1, descendiente2 = [], []
    intercambios = min(len(individuo1),len(individuo2))+1
    for _ in range(int(intercambios/2)):
        i1 = random.choice(individuo1)
        if i1 not in descendiente2: descendiente2.append(i1)
        i2 = random.choice(individuo2)
        if i2 not in descendiente1: descendiente1.append(i2)
    #"""
    for _ in range(int(intercambios/2)):
        i1 = random.choice(individuo1)
        if i1 not in descendiente1: descendiente1.append(i1)
        i2 = random.choice(individuo2)
        if i2 not in descendiente2: descendiente2.append(i2)
    
    #"""
    return descendiente1, descendiente2
        
        
    
def muta(individuo):
    global ingredientesTotales, apariciones, ingredientesOrdenados, weight
    #listaApariciones = list(apariciones)
    res = copy.deepcopy(individuo)
    if random.random()<0.5: # pisa
        for _ in range(random.randint(1,int(len(individuo)/10) +2)):
            res[random.randint(0,len(individuo)-1)] = random.choices(population=ingredientesOrdenados,weights=weight,k=1)
    else:
        for _ in range(random.randint(1,int(len(individuo)/10) +2)):
            res.append(random.choices(population=ingredientesOrdenados,weights=weight,k=1))
    return res


    
mejores = []


#p = poblacionInicial(100)
"""
p = poblacionH

for i in range(10):
    print("VUELTA ",i)
    e = evalua(p)
    txt = str(e[0])+"\n"+str(score(e[0],personas))+"\n"
    escribe("resultados", txt)
    p = selecciona(e)
    print("valor: ",score(e[0],personas), "longitud: ",len(e[0]))
    apariciones = dict(apariciones)

"""