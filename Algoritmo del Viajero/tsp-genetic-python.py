
import random
import copy
import os
import time
import math
import csv

try:
    from tkinter import *
    from tkinter.ttk import *
except Exception as e:
    print("[ERROR]: {0}".format(e))
    from Tkinter import *

list_of_cities =[]
# probabilidad de que una ruta individual mute
k_mut_prob = 0.2

# Number of generations to run for
k_n_generations = 100
# Tamaño de la población de 1 generación (RoutePop)
k_population_size = 100

# Tamaño de la selección del torneo.
tournament_size = 7

#Si el elitismo es verdadero, lo mejor de una generación pasará a la siguiente
elitism = True

# Logro leer los datos 
csv_cities = False

# Archivo
csv_name = 'cities.csv'


# City class
class City(object):

    def __init__(self, name, x, y, distance_to=None):
        # Nombre y coordenadas:
        self.name = name
        self.x = self.graph_x = x
        self.y = self.graph_y = y
        # Se adjunta a la lista global de ciudades:
        list_of_cities.append(self)
        # Crea un diccionario de las distancias a todas las demás ciudades (tiene que usar un valor para que se use a sí mismo - siempre 0)
        self.distance_to = {self.name:0.0}
        if distance_to:
            self.distance_to = distance_to

    def calculate_distances(self): 
        for city in list_of_cities:
            tmp_dist = self.point_dist(self.x, self.y, city.x, city.y)
            self.distance_to[city.name] = tmp_dist

        
    def point_dist(self, x1,y1,x2,y2):
        return ((x1-x2)**2 + (y1-y2)**2)**(0.5)


# Ruta
class Route(object):
    def __init__(self):
        #inicia un atributo de ruta igual a una lista_de_ciudades barajada aleatoriamente
        self.route = sorted(list_of_cities, key=lambda *args: random.random())
        ### Calcula su longitud:
        self.recalc_rt_len()

    def recalc_rt_len(self):

        # Pone 0 a la longitud
        self.length = 0.0
        # para cada ciudad en su atributo de ruta:
        for city in self.route:
            # configurar una variable de ciudad siguiente que apunte a la siguiente ciudad en la lista
            # y se envuelve al final:
            next_city = self.route[self.route.index(city)-len(self.route)+1]
            dist_to_next = city.distance_to[next_city.name]
            self.length += dist_to_next

    def pr_cits_in_rt(self, print_route=False):
        cities_str = ''
        for city in self.route:
            cities_str += city.name + ','
        cities_str = cities_str[:-1] # chops off last comma
        if print_route:
            print('    ' + cities_str)

    def pr_vrb_cits_in_rt(self):

        cities_str = '|'
        for city in self.route:
            cities_str += str(city.x) + ',' + str(city.y) + '|'
        print(cities_str)

    def is_valid_route(self):
        for city in list_of_cities:
            # helper function defined up to
            if self.count_mult(self.route,lambda c: c.name == city.name) > 1:
                return False
        return True

   
    def count_mult(self, seq, pred):
        return sum(1 for v in seq if pred(v))


# Contiene una población de objetos Route ()
class RoutePop(object):

    def __init__(self, size, initialise):
        self.rt_pop = []
        self.size = size
        if initialise:
            for x in range(0,size):
                new_rt = Route()
                self.rt_pop.append(new_rt)
            self.get_fittest()

    def get_fittest(self):

        sorted_list = sorted(self.rt_pop, key=lambda x: x.length, reverse=False)
        self.fittest = sorted_list[0]
        return self.fittest


# Clase para reunir todos los métodos relacionados con el algoritmo genético
class GA(object):
    def crossover_experimental(routeA,routeB):

        child_rt = Route()


        # evita recalcular
        routeB_len = len(routeB.route)

        # Elige una ciudad al azar
        random_city = random.choice(list_of_cities)


        incrementing_a = True
        incrementing_b = True

        idx_a = routeA.route.index(random_city)
        idx_b = routeB.route.index(random_city)

        idx_a -= 1
        idx_b += 1

        if idx_a < 0:
            incrementing_a = False

        if idx_b >= routeB_len:
            incrementing_b = False

        child_rt.route = [random_city]

        # print(random_city.name)

        while (incrementing_a and incrementing_b):
            # print('idx_a: {}'.format(idx_a))

            if idx_a >= 0:
                if not (routeA.route[idx_a] in child_rt.route):
                    child_rt.route.insert(0, routeA.route[idx_a])

            idx_a -= 1

            if idx_a < 0:
                incrementing_a = False
                break

            # child_rt.pr_cits_in_rt()


            if idx_b < routeB_len:
                if not (routeB.route[idx_b] in child_rt.route):
                    child_rt.route.append(routeB.route[idx_b])

            idx_b += 1

            if idx_b >= routeB_len:
                incrementing_b = False
                break

            # print('idx_b: {}'.format(idx_b))
            # child_rt.pr_cits_in_rt()

       # ahora incrementing_a o incrementing_b debe ser falso

        shuffled_cities = sorted(routeA.route, key=lambda *args: random.random())
        for city in shuffled_cities:
            if not city in child_rt.route:
                child_rt.route.append(city)

        return child_rt

    def crossover(self, parent1, parent2):


        child_rt = Route()

        for x in range(0,len(child_rt.route)):
            child_rt.route[x] = None

        # Dos índices enteros aleatorios del parent1:
        start_pos = random.randint(0,len(parent1.route))
        end_pos = random.randint(0,len(parent1.route))



        if start_pos < end_pos:

            for x in range(start_pos,end_pos):
                child_rt.route[x] = parent1.route[x] # set the values to eachother

        elif start_pos > end_pos:
            for i in range(end_pos,start_pos):
                child_rt.route[i] = parent1.route[i] # set the values to eachother



        for i in range(len(parent2.route)):
            #
            if not parent2.route[i] in child_rt.route:
               
                for x in range(len(child_rt.route)):
                    if child_rt.route[x] == None:
                        child_rt.route[x] = parent2.route[i]
                        break

        child_rt.recalc_rt_len()
        return child_rt

    def mutate(self, route_to_mut):

        # k_mut_prob %
        if random.random() < k_mut_prob:

            # 2 indices random
            mut_pos1 = random.randint(0,len(route_to_mut.route)-1)
            mut_pos2 = random.randint(0,len(route_to_mut.route)-1)

           
            if mut_pos1 == mut_pos2:
                return route_to_mut

         
            city1 = route_to_mut.route[mut_pos1]
            city2 = route_to_mut.route[mut_pos2]

            route_to_mut.route[mut_pos2] = city1
            route_to_mut.route[mut_pos1] = city2

        # Recalculate the length of the route (updates it's .length)
        route_to_mut.recalc_rt_len()

        return route_to_mut

    def mutate_2opt(route_to_mut):
 
        # k_mut_prob %
        if random.random() < k_mut_prob:

            for i in range(len(route_to_mut.route)):
                for ii in range(len(route_to_mut.route)): # i is a, i + 1 is b, ii is c, ii+1 is d
                    if (route_to_mut.route[i].distance_to[route_to_mut.route[i-len(route_to_mut.route)+1].name]
                     + route_to_mut.route[ii].distance_to[route_to_mut.route[ii-len(route_to_mut.route)+1].name]
                     > route_to_mut.route[i].distance_to[route_to_mut.route[ii].name]
                     + route_to_mut.route[i-len(route_to_mut.route)+1].distance_to[route_to_mut.route[ii-len(route_to_mut.route)+1].name]):

                        c_to_swap = route_to_mut.route[ii]
                        b_to_swap = route_to_mut.route[i-len(route_to_mut.route)+1]

                        route_to_mut.route[i-len(route_to_mut.route)+1] = c_to_swap
                        route_to_mut.route[ii] = b_to_swap 

            route_to_mut.recalc_rt_len()

        return route_to_mut

    def tournament_select(self, population):


        # Nueva población más pequeña (no inicializada)
        tournament_pop = RoutePop(size=tournament_size,initialise=False)

        # lo llena con individuos al azar (puede elegir lo mismo dos veces)
        for i in range(tournament_size-1):
            tournament_pop.rt_pop.append(random.choice(population.rt_pop))
        
        # devuelve el más apto:
        return tournament_pop.get_fittest()

    def evolve_population(self, init_pop):

        # crea una nueva población:
        descendant_pop = RoutePop(size=init_pop.size, initialise=True)

        # Compensación de elitismo (cantidad de Rutas () transferidas a la nueva población)
        elitismOffset = 0

        # si tenemos elitismo, establezca la primera de la nueva población como la más apta de la vieja
        if elitism:
            descendant_pop.rt_pop[0] = init_pop.fittest
            elitismOffset = 1

        # Pasa por la nueva población y la llena con el hijo de dos campeones de torneos de la población anterior.
        for x in range(elitismOffset,descendant_pop.size):
            # 2 padres
            tournament_parent1 = self.tournament_select(init_pop)
            tournament_parent2 = self.tournament_select(init_pop)

            # un niño:
            tournament_child = self.crossover(tournament_parent1, tournament_parent2)

            
            descendant_pop.rt_pop[x] = tournament_child

        # Muta todas las rutas (la mutación ocurre con un problema p = k_mut_prob)
        for route in descendant_pop.rt_pop:
            if random.random() < 0.3:
                self.mutate(route)

       # Actualiza la ruta más apta:
        descendant_pop.get_fittest()

        return descendant_pop
class App(object):

    def __init__(self,n_generations,pop_size, graph=False):

        if csv_cities:
            self.read_csv()

        self.n_generations = n_generations
        self.pop_size = pop_size

    
        if graph:
            self.set_city_gcoords()
            
            self.window = Tk()
            self.window.wm_title("Generation 0")

            self.canvas_current = Canvas(self.window, height=300, width=300)
            self.canvas_best = Canvas(self.window, height=300, width=300)


            self.canvas_current_title = Label(self.window, text="Mejor ruta de generación actual:")
            self.canvas_best_title = Label(self.window, text="En general, el mejor hasta ahora:")

            # Inicia una barra de estado con una cadena
            self.stat_tk_txt = StringVar()
            self.status_label = Label(self.window, textvariable=self.stat_tk_txt, relief=SUNKEN, anchor=W)

            # crea puntos para las ciudades en ambos lienzos
            for city in list_of_cities:
                self.canvas_current.create_oval(city.graph_x-2, city.graph_y-2, city.graph_x + 2, city.graph_y + 2, fill='blue')
                self.canvas_best.create_oval(city.graph_x-2, city.graph_y-2, city.graph_x + 2, city.graph_y + 2, fill='blue')

            # Empaqueta todos los widgets (los crea físicamente y los coloca en orden)
            self.canvas_current_title.pack()
            self.canvas_current.pack()
            self.canvas_best_title.pack()
            self.canvas_best.pack()
            self.status_label.pack(side=BOTTOM, fill=X)

            # Runs the main window loop
            self.window_loop(graph)
        else:
            print("Calculating GA_loop")
            self.GA_loop(n_generations,pop_size, graph=graph)

    def set_city_gcoords(self):

        # define algunas variables (las configuraremos a continuación)
        min_x = 100000
        max_x = -100000
        min_y = 100000
        max_y = -100000

        # encuentra el máximo / mínimo adecuado
        for city in list_of_cities:

            if city.x < min_x:
                min_x = city.x
            if city.x > max_x:
                max_x = city.x

            if city.y < min_y:
                min_y = city.y
            if city.y > max_y:
                max_y = city.y

        # desplaza el gráfico_x para que la ciudad más a la izquierda comience en x = 0, lo mismo para y.
        for city in list_of_cities:
            city.graph_x = (city.graph_x + (-1*min_x))
            city.graph_y = (city.graph_y + (-1*min_y))

        # restablece las variables ahora que hemos realizado cambios
        min_x = 100000
        max_x = -100000
        min_y = 100000
        max_y = -100000

        #encuentra el máximo / mínimo adecuado
        for city in list_of_cities:

            if city.graph_x < min_x:
                min_x = city.graph_x
            if city.graph_x > max_x:
                max_x = city.graph_x

            if city.graph_y < min_y:
                min_y = city.graph_y
            if city.graph_y > max_y:
                max_y = city.graph_y

        # si x es la dimensión más larga, establezca el factor de estiramiento en 300 (px) / 
        # max_x. De lo contrario, hazlo por ti. Esto conserva la relación de aspecto.
        if max_x > max_y:
            stretch = 300 / max_x
        else:
            stretch = 300 / max_y

        # Estirar todas las ciudades para que la ciudad con las coordenadas más altas tenga tanto x como y <300
        for city in list_of_cities:
            city.graph_x *= stretch
            city.graph_y = 300 - (city.graph_y * stretch)


    def update_canvas(self,the_canvas,the_route,color):
    
        # elimina todos los elementos actuales con la etiqueta 'ruta'
        the_canvas.delete('path')

        # recorre la ruta
        for i in range(len(the_route.route)):

            # similar a i + 1 pero se repetirá al final
            next_i = i-len(the_route.route)+1

            # creates the line from city to city
            the_canvas.create_line(the_route.route[i].graph_x,
                                the_route.route[i].graph_y,
                                the_route.route[next_i].graph_x,
                                the_route.route[next_i].graph_y,
                                tags=("path"),
                                fill=color)


            the_canvas.pack()
            the_canvas.update_idletasks()

    def read_csv(self):
        with open(csv_name, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                new_city = City(row[0],float(row[1]),float(row[2]))

    def GA_loop(self,n_generations,pop_size, graph=False):
        # se toma el tiempo para medir el tiempo transcurrido
        start_time = time.time()

        # Crea la población:
        print("Crea la población:")
        the_population = RoutePop(pop_size, True)
        print ("Creación finalizada de la población")

        # the_population.rt_pop[0].route = [1,8,38,31,44,18,7,28,6,37,19,27,17,43,30,36,46,33,20,47,21,32,39,48,5,42,24,10,45,35,4,26,2,29,34,41,16,22,3,23,14,25,13,11,12,15,40,9]
        # the_population.rt_pop[0].recalc_rt_len()
        # the_population.get_fittest()

        # comprueba para asegurarse de que no haya ciudades duplicadas:
        if the_population.fittest.is_valid_route() == False:
            raise NameError('Varias ciudades con el mismo nombre. Consultar ciudades.')
            return # 

        
        initial_length = the_population.fittest.length

        # Crea una ruta aleatoria llamada best_route. Almacenará nuestra mejor ruta en general.
        best_route = Route()

        if graph:
            # Crea una ruta aleatoria llamada best_route. Almacenará nuestra mejor ruta en general.
            self.update_canvas(self.canvas_current,the_population.fittest,'red')
            self.update_canvas(self.canvas_best,best_route,'green')


        # Bucle de proceso principal (por número de generaciones)
        for x in range(1,n_generations):
            # Actualiza el lienzo actual cada n generaciones (para evitar que se quede atrás, aumente n)
            if x % 8 == 0 and graph:
                self.update_canvas(self.canvas_current,the_population.fittest,'red')

            # Evoluciona la población:
            the_population = GA().evolve_population(the_population)

            # Si hemos encontrado una nueva ruta más corta, guárdala en best_route
            if the_population.fittest.length < best_route.length:
                # establezca la ruta (copy.deepcopy porque the_population.fittest es persistente en este bucle, por lo que causará errores de referencia)
                best_route = copy.deepcopy(the_population.fittest)
                if graph:
                    self.update_canvas(self.canvas_best,best_route,'green')
                    self.stat_tk_txt.set('Longitud inicial {0:.2f} Mejor longitud = {1:.2f}'.format(initial_length,best_route.length))
                    self.status_label.pack()
                    self.status_label.update_idletasks()

            # Prints info to the terminal:
            self.clear_term()
            print('Generacion {0} of {1}'.format(x,n_generations))
            print(' ')
            print('El más apto en general tiene longitud {0:.2f}'.format(best_route.length))
            print('y pasa por:')
            best_route.pr_cits_in_rt(True)
            print(' ')
            print('El más apto actual tiene longitud {0:.2f}'.format(the_population.fittest.length))
            print('Y pasa por:')
            the_population.fittest.pr_cits_in_rt(True)
            print(' ')
            print('' 'La pantalla con los mapas puede dejar de responder si el tamaño de la población es demasiado grande. Se actualizará al final '' ')

            if graph:
       
                self.window.wm_title("Generacion {0}".format(x))
        if graph:
           
            self.window.wm_title("Generacion {0}".format(n_generations))

 
            self.update_canvas(self.canvas_best,best_route,'green')
            
        # toma la hora de finalización de la ejecución:
        end_time = time.time()

        # Imprime la salida final en el terminal:
        self.clear_term()
        print('Termino de evolicionar {0} generaciones.'.format(n_generations))
        print("El tiempo transcurrido fue {0:.1f} segundos.".format(end_time - start_time))
        print(' ')
        print('Mejor distancia inicial: {0:.2f}'.format(initial_length))
        print('Distancia final:   {0:.2f}'.format(best_route.length))
        print('La mejor ruta fue :')
        best_route.pr_cits_in_rt(print_route=True)

    def window_loop(self, graph):
        self.window.after(0,self.GA_loop(self.n_generations, self.pop_size, graph))
        self.window.mainloop()


    def clear_term(self):
        os.system('cls' if os.name=='nt' else 'clear')




def random_cities():
    i = City('i', 60, 200)
    j = City('j', 180, 190)
    k = City('k', 100, 180)
    l = City('l', 140, 180)
    m = City('m', 20, 160)
    n = City('n', 100, 160)
    o = City('o', 140, 140)
    p = City('p', 40, 120)
    q = City('q', 100, 120)
    r = City('r', 180, 100)
    s = City('s', 60, 80)
    t = City('t', 120, 80)
    u = City('u', 180, 60)
    v = City('v', 20, 40)
    w = City('w', 100, 40)
    x = City('x', 200, 40)
    a = City('a', 20, 20)
    b = City('b', 60, 20)
    c = City('c', 160, 20)
    d = City('d', 68, 130)
    e = City('e', 10, 10)
    f = City('f', 75, 180)
    g = City('g', 190, 190)
    h = City('h', 200, 10)

    for city in list_of_cities:
        city.calculate_distances()
    app = App(n_generations=k_n_generations,pop_size=k_population_size, graph=True)

if __name__ == '__main__':
    "" "Seleccione solo una función: aleatoria, específica o específica2" ""

    random_cities()

