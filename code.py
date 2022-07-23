import copy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
import heapq
import random
from copy import deepcopy
import functools



bins = 20

DATA_FOLDER = 'input_data/'
DATA_FILES = ["a_an_example.in.txt", "b_better_start_small.in.txt", "c_collaboration.in.txt", "d_dense_schedule.in.txt", "e_exceptional_skills.in.txt", "f_find_great_mentors.in.txt"]
SPLIT_CONSTANT = ' '

def escribe(fichero,variable):
    f = open(str(fichero)+".txt", "w") # a<-w si quieres que pise
    f.write(str(variable))
    f.close()
    
class Skill:
    def __init__(self, name_of_skill, level):
        self.name = name_of_skill
        self.level = level

    def __str__(self) -> str:
      return f'{{ name: {self.name}, level: {self.level} }}'

    def __repr__(self):
        return str(self)

class Person:
    def __init__(self, name_of_person, skills):
        self.name = name_of_person
        self.skills = {}
        for skill in skills:
            self.skills[skill.name] = skill
        self.heuristic_score = self.get_heuristic_score()
    
    def get_level(self, skill):
        if skill in self.skills:
            return self.skills[skill].level
        return 0

    def get_skills_names(self):
        return list(map(lambda skill: skill, self.skills))
    
    def get_heuristic_score(self):
        return sum(map(lambda skill: skill.level, self.skills.values()))
    
    def __str__(self) -> str:
      return f'{{ name: {self.name}, skills: {self.skills}, heuristic_score:{self.heuristic_score} }}'

    def __repr__(self):
        return str(self)

class Project:
    def __init__(self, name, required_time, score, due_date, skills):
        self.name = name
        self.required_time = required_time
        self.score = score
        self.due_date = due_date
        #self.roles_required = {}
        self.roles_required = []
        for skill in skills:
            #print("meto ",skill)
            #self.roles_required[skill.name] = skill
            self.roles_required.append(skill)
        self.assignments = []
        self.heuristic_score = self.get_heuristic_score()
        self.imputed_time = 0

    def get_level(self, skill):
        #if skill in self.roles_required:
        #    return self.roles_required[skill].level
        for skil in self.roles_required:
            if skill==skil.name:
                return skil.level
        return -1
    
    def get_roles_required_names(self):
        return list(map(lambda skill: skill, self.roles_required))

    def assign_worker(self, worker):
        self.assignments.append(worker)

    def get_heuristic_score(self):
        #return self.score  #self.score - self.required_time - len(self.roles_required)
        lvls = 0 
        for s in self.roles_required:
            lvls+=s.level
        #return self.score - self.required_time - len(self.roles_required) - lvls
        #return  - (self.due_date - self.required_time )
        return  self.score/len(self.roles_required)
    
    def __str__(self) -> str:
      return f'{{ name: {self.name}, required_time: {self.required_time}, score: {self.score}, due_date: {self.due_date}, roles_required: {self.roles_required}, heuristic_score:{self.heuristic_score} }}'

    def __repr__(self):
        return str(self)
    

class Input:
    def __init__(self, workers, projects):
        self.workers = workers
        self.projects = projects

    def get_workers_by_skill_ordered(self, skill):                
        return sorted(self.workers, key=lambda x: x.get_level(skill))

    def get_projects_by_heuristic_score(self):
        return sorted(self.projects, key=lambda x: x.heuristic_score, reverse=True)

    def get_workers_by_heuristic_score(self):
        return sorted(self.workers, key=lambda x: x.heuristic_score, reverse=True)

    def __str__(self) -> str:
      return f'{{ workers: {self.workers}, projects: {self.projects} }}'

    def __repr__(self):
        return str(self)

class Solution:
    def __init__(self, projects):
        self.projects = projects

    def get_score(self):
        score = 0
        day = 0
        workers_occupied = {}
        projects_started = []
        finished = False
        projects_to_complete = self.projects.copy()
        
        while not finished:
            
            for project in projects_to_complete:
                workers_availables = True
                for worker in project.assignments:
                    if worker.name in workers_occupied:
                        workers_availables = False
                if workers_availables:
                    for worker in project.assignments:
                        workers_occupied[worker.name] = worker
                    projects_to_complete.remove(project)
                    projects_started.append(project)

            for project in projects_started:
                project.imputed_time += 1
                if project.imputed_time >= project.required_time:
                    if project.imputed_time > project.required_time: 
                        print(f'ERROR, el proyecto {project.name} contiene más tiempo imputado que el requerido. REVISAR!!')
                    
                    for worker in project.assignments:
                        workers_occupied.pop(worker.name)
                    
                    projects_started.remove(project)
                    if day <= project.due_date:
                        score += project.score
                    else:
                        score += max(0, project.score - (day+1 - project.due_date))

            day += 1
            if len(projects_to_complete) == 0 and len(projects_started) == 0:
                finished = True

        return score

    def __str__(self):
        str = f'{len(self.projects)}\n'
            
        for project in self.projects:
            str += project.name + '\n'

            for person in project.assignments:
                str += person.name + ' '
            
            str = str[:-1] + '\n'
        
        return str[:-1]

    def __repr__(self):
        return str(self)

def clear_and_split(str):
    return str.replace('\n', '').split(SPLIT_CONSTANT)

def cargar_entrada(ruta):
    file = open(ruta, 'r')
    contributors_and_project_numbers = clear_and_split(file.readline())
    number_of_contributors = int(contributors_and_project_numbers[0])
    number_of_projects = int(contributors_and_project_numbers[1])
    workers = []
    projects = []

    for _ in range(number_of_contributors):
        worker_and_number_of_skills = clear_and_split(file.readline())
        worker_name = worker_and_number_of_skills[0]
        number_of_skills = int(worker_and_number_of_skills[1])
        skills = []
        
        for _ in range(number_of_skills):
            skill_and_level = clear_and_split(file.readline())
            skill_name = skill_and_level[0]
            skill_level = int(skill_and_level[1])

            skills.append(Skill(skill_name, skill_level))

        workers.append(Person(worker_name, skills))
    
    for _ in range(number_of_projects):
        project_and_integers = clear_and_split(file.readline())
        project_name = project_and_integers[0]
        required_time = int(project_and_integers[1])
        score = int(project_and_integers[2])
        due_date = int(project_and_integers[3])
        number_of_required_skills = int(project_and_integers[4])
        skills = []

        for _ in range(number_of_required_skills):
            skill_and_level = clear_and_split(file.readline())
            skill_name = skill_and_level[0]
            skill_level = int(skill_and_level[1])

            skills.append(Skill(skill_name, skill_level))
        
        projects.append(Project(project_name, required_time, score, due_date, skills))
    
    return Input(workers, projects)


def avanzaTiempo(proyectos, tiempo):
    for pi in proyectos:
        pi.due_date = pi.due_date-tiempo
    return proyectos

def cuantoAvanzo(proyectos):
    if len(proyectos)==0: return 0
    res = proyectos[0]
    for pi in proyectos:
        if pi.due_date<res.due_date:
            res = pi
    return res.due_date

def damePersona(name,personas):
    for pi in personas:
        if pi.name == name:
            return pi 
    return -1

level = 1
input = cargar_entrada(DATA_FOLDER + DATA_FILES[level])

print(input)
print(input.get_projects_by_heuristic_score())
print(input.get_workers_by_heuristic_score())
print(input.projects[0].get_level('C++'))
print(input.projects)
print(input.workers)

proyectosOrdenados = input.get_projects_by_heuristic_score()
personasOrdenadas = input.get_workers_by_heuristic_score()

personasOcupadas = {persona.name: 0 for persona in personasOrdenadas}
asignacionesProyecto = {proyecto.name: [] for proyecto in proyectosOrdenados}

proyectosRealizados = []
proyectosRealizandose = []
proyectosNoRealizados = proyectosOrdenados[:]

t = 0

solucion = {proyecto.name: [] for proyecto in proyectosOrdenados}

escribiendo = ""
lleva = 0
#for _ in range(10):
inicio = 1
while len(proyectosNoRealizados)>0 and (len(proyectosRealizandose)>0 or inicio == 1):
#while True:
#for _ in [1]:
    inicio = 0
    print("----------------------------------\n\n")
    for proyecto in proyectosNoRealizados:
        roles = 0
        viable = 0
        #if proyecto.due_date>0 and (proyecto.due_date-proyecto.required_time)>0:
        #if proyecto.score-(proyecto.required_time-proyecto.due_date)>0:
        #if proyecto.required_time>proyecto.due_date:
        if True:
            for rol in proyecto.roles_required:
                for persona in personasOrdenadas[::-1]:
                    if rol.name in persona.get_skills_names() and rol.level<=persona.get_level(rol.name):
                        if personasOcupadas[persona.name]==0 and roles<len(proyecto.roles_required):
                            roles+=1
                            asignacionesProyecto[proyecto.name].append(persona.name)
                            personasOcupadas[persona.name]=1
                            viable = 1
                            break
                if viable==0: 
                    # salgo del bucle rol. proyecto++
                    break
        if roles==len(proyecto.roles_required):
            lleva+=1
            print("proyecto viable: ",proyecto.name, " lleva: ",lleva)
            proyectosRealizandose.append(proyecto)
            escribiendo+="\n"+proyecto.name+"\n"
            for ai in asignacionesProyecto[proyecto.name]:
                escribiendo+=ai+" "
        else:
            for pi in asignacionesProyecto[proyecto.name]:
                personasOcupadas[pi]=0
            asignacionesProyecto[proyecto.name] = []
    
    for pi in proyectosRealizandose:
        if pi in proyectosNoRealizados: proyectosNoRealizados.remove(pi)
    
    avanza = cuantoAvanzo(proyectosRealizandose)
    t+=avanza
    proyectosRealizandose = avanzaTiempo(proyectosRealizandose,avanza)
    proyectosNoRealizados = avanzaTiempo(proyectosNoRealizados,avanza)
    
    proyectosBorra = []
    for pi in proyectosRealizandose:
        if pi.due_date == 0:
            
            #escribiendo+="\n"+pi.name+"\n"
            #for ai in asignacionesProyecto[pi.name]:
            #    escribiendo+=ai+" "
            
            print("se termino el proyecto ", pi.name)
            proyectosRealizados.append(pi)
            proyectosBorra.append(pi)
            solucion[pi.name] = asignacionesProyecto[pi.name]
            for i in range(len(asignacionesProyecto[pi.name])):
                ci = asignacionesProyecto[pi.name][i]
                personasOcupadas[ci]=0
                # sube leveles
                ci = damePersona(ci,personasOrdenadas)
                if ci.get_level(pi.roles_required[i].name) == pi.roles_required[i].level:
                    print("subo level a ",ci.name)
                    ci.skills[pi.roles_required[i].name].level+=1
                
    for pi in proyectosBorra:
        if pi in proyectosRealizandose: proyectosRealizandose.remove(pi)
    
    input = Input(personasOrdenadas,proyectosNoRealizados)
    proyectosNoRealizados = input.get_projects_by_heuristic_score()
    personasOrdenadas = input.get_workers_by_heuristic_score()


def dameSol(asignacionesProyecto):
    cuantos = 0
    sol = ""
    for ai in asignacionesProyecto:
        if len(asignacionesProyecto[ai])>0:
            cuantos+=1
            sol+=ai+"\n"
            for aii in asignacionesProyecto[ai]:
                sol+=aii+" "
            sol+="\n"
    sol = str(cuantos)+"\n"+sol
    return sol

#sol = dameSol(asignacionesProyecto)
#sol = dameSol(solucion)
#print(sol)
#escribe("sool"+str(level),sol)
escribiendo = str(lleva)+"\n"+escribiendo[1:]
escribe("sool"+str(level),escribiendo)