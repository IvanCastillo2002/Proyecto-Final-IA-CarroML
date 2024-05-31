"""Omar Adrian Acosta Santiago 
Ivan Eduardo Castillo Castro 
Edgar Alejandro Guangorena Arellano 
Cesar Osvaldo Marquez Rodriguez
Jose Andrés Ojeda González 
Nicole Guadalupe Marquez Garay"""

""" Este programa consiste en el aprendizaje de un automovil para poder superar una pista proporcionada a base de prueba y error
Al momento de ejecutar el programa nos abrira una terminal que nos mencionara la pista en la que queremos que el automovil 
comience su aprendizaje, al momento de elegir el mapa, se nos abrira una ventana la cual nos mostrara el mapa deseado y
veremos al automovil tratar de llegar a la meta a base de prueba y error.
Al momento de que el automovil "choque" o no de la vuelta de manera correcta se reiniciara la ejecucion pero el conocimiento no 
se eliminara, por ende el automovil sabra donde fue su error para que asi no vuelva a caer en el mismo error """

#imagen del carro https://www.flaticon.es/icono-gratis/carro-deportivo_3085411
#archivo config https://github.com/monokim/framework_tutorial/blob/master/neat/config-feedforward.txt

# Importamos las librerias necesarias para la ejecucion del programa
import sys # Proporciona acceso a algunas funciones que interactuan con Python
import neat # Libreria para la evolucion de redes neuronales usando algoritmos geneticos
import pygame # Libreria para desarrollar videojuegos en Python 
import math # Proporciona acceso a funciones matematicas

# Constantes
ANCHO = 1920
ALTO = 1080
TAMANO_COCHE_X = 60    
TAMANO_COCHE_Y = 60
COLOR_BORDE = (255, 255, 255, 255)  # Color para chocar
generacion_actual = 0  # Contador de generaciones

# Velocidades de simulación
VELOCIDAD_LENTA = 30
VELOCIDAD_NORMAL = 60
VELOCIDAD_ACCELERADA = 120

""" La clase coche permite simular un coche que puede moverse, detectar colisiones, y utilizar
sensores(radares) para interactuar con su entorno"""
class Coche:
    def __init__(self):
        """ Cargar sprite del coche y rotar.
        Cargamos la imagen del coche('carro.png') y la convertimos para una manipulacion mas rapida"""
        self.sprite = pygame.image.load('carro.png').convert()  # Convertir acelera mucho
        # Escala la imagen del coche especificado por TAMANO_COCHE_X y TAMANO_COCHE_Y
        self.sprite = pygame.transform.scale(self.sprite, (TAMANO_COCHE_X, TAMANO_COCHE_Y))
        # Inicializamos otras propiedades del automovil
        self.sprite_rotado = self.sprite 
        self.posicion = [830, 920]  # Posición de inicio
        self.angulo = 0
        self.velocidad = 0
        self.velocidad_establecida = False  # Bandera para velocidad predeterminada más tarde
        self.centro = [self.posicion[0] + TAMANO_COCHE_X / 2, self.posicion[1] + TAMANO_COCHE_Y / 2]  # Calcular centro
        self.radares = []  # Lista para sensores / radares
        self.dibujar_radares = []  # Radares a dibujar
        self.vivo = True  # Booleano para verificar si el coche está chocado
        self.distancia = 0  # Distancia recorrida
        self.tiempo = 0  # Tiempo transcurrido
    """ Dibujamos el coche en la pantalla.
     Usamos 'blit' para dibujar el sprite del coche en la posicion actual.
      Llamamos a 'dibujar_radar' para dibujar los radares(sensores) """
    def dibujar(self, pantalla):
        pantalla.blit(self.sprite_rotado, self.posicion)  # Dibujar sprite
        self.dibujar_radar(pantalla)  # OPCIONAL PARA SENSORES
    # Dibujamos lineas y circulos verdes los cuales representa los sensores del coche
    def dibujar_radar(self, pantalla):
        # Opcionalmente dibujar todos los sensores / radares
        for radar in self.radares:
            posicion = radar[0]
            pygame.draw.line(pantalla, (0, 255, 0), self.centro, posicion, 1)
            pygame.draw.circle(pantalla, (0, 255, 0), posicion, 5)
    # Comprobamos si algun punto de las esquinas del coche toca el borde del mapa ('COLOR_BORDE) 
    def verificar_colision(self, mapa_juego):
        self.vivo = True
        for punto in self.esquinas:
            if mapa_juego.get_at((int(punto[0]), int(punto[1]))) == COLOR_BORDE:
                self.vivo = False
                break
    # Verificamos la distancia desde el coche hasta el borde del mapa en una direccion especifica
    def verificar_radar(self, grado, mapa_juego): # Calcula la distancia desde el coche hasta el borde en la direccion especificada por 'grado'
        longitud = 0
        x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grado))) * longitud)
        y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grado))) * longitud)

        while not mapa_juego.get_at((x, y)) == COLOR_BORDE and longitud < 300:
            longitud += 1
            x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grado))) * longitud)
            y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grado))) * longitud)

        dist = int(math.sqrt(math.pow(x - self.centro[0], 2) + math.pow(y - self.centro[1], 2)))
        self.radares.append([(x, y), dist])

    # Actualiza el estado del coche en cada frame
    def actualizar(self, mapa_juego):
        # Establecemos la velocidad inicial si no esta establecida
        if not self.velocidad_establecida: 
            self.velocidad = 20
            self.velocidad_establecida = True
        # Rotamos el sprite del coche y actualizamos su posicion y centro
        self.sprite_rotado = self.rotar_centro(self.sprite, self.angulo)
        self.posicion[0] += math.cos(math.radians(360 - self.angulo)) * self.velocidad
        self.posicion[0] = max(self.posicion[0], 20)
        self.posicion[0] = min(self.posicion[0], ANCHO - 120)
        self.distancia += self.velocidad
        self.tiempo += 1
        
        self.posicion[1] += math.sin(math.radians(360 - self.angulo)) * self.velocidad
        self.posicion[1] = max(self.posicion[1], 20)
        self.posicion[1] = min(self.posicion[1], ANCHO - 120)

        # Calculamos las nuevas posiciones de las esquinas del coche
        self.centro = [int(self.posicion[0]) + TAMANO_COCHE_X / 2, int(self.posicion[1]) + TAMANO_COCHE_Y / 2]

        longitud = 0.5 * TAMANO_COCHE_X
        izquierda_arriba = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 30))) * longitud, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 30))) * longitud]
        derecha_arriba = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 150))) * longitud, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 150))) * longitud]
        izquierda_abajo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 210))) * longitud, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 210))) * longitud]
        derecha_abajo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 330))) * longitud, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 330))) * longitud]
        self.esquinas = [izquierda_arriba, derecha_arriba, izquierda_abajo, derecha_abajo]

        # Verificamos colisiones y actualizamos los radares
        self.verificar_colision(mapa_juego)
        self.radares.clear()

        for d in range(-90, 120, 45):
            self.verificar_radar(d, mapa_juego)
    # Obtenemos los datos de los radares
    def obtener_datos(self):
        radares = self.radares
        valores_retorno = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radares):
            valores_retorno[i] = int(radar[1] / 30)
        return valores_retorno # Retornamos las distancias de los radares normalizadas
    # Verifica si el coche esta vivo
    def esta_vivo(self):
        return self.vivo # Retorna el estado de vivo
    
    # Calcula una recompensa basada en la distancia recorrida
    def obtener_recompensa(self):
        return self.distancia / (TAMANO_COCHE_X / 2) # Retorna la recompensa basada en la distancia recorrida

    # Rotamos la imagen del coche alrededor de su centro
    # Rota la imagen del coche y ajusta su posicion para mantener el centro
    def rotar_centro(self, imagen, angulo):
        rectangulo = imagen.get_rect()
        imagen_rotada = pygame.transform.rotate(imagen, angulo)
        rectangulo_rotado = rectangulo.copy()
        rectangulo_rotado.center = imagen_rotada.get_rect().center
        imagen_rotada = imagen_rotada.subsurface(rectangulo_rotado).copy()
        return imagen_rotada

""" Esta funcion ejecuta una simulacion utilizando la libreria Pygame y el algoritmo NEAT 
para entrenat redes neuronales.
Visualizamos la simulacion de coches controlados por redes neuronales evolutivas con NEAT.
Cada coche recibe entradas de sensores, y las redes neuronales determinan las acciones (girar, acelerar, frenar).
La simulacion controla la duracion, la visualizacion en pantalla, la velocidad de la simulacion y la actualizacion
del estado de los coches"""
def ejecutar_simulacion(genomas, config, nombre_mapa):
    redes = []
    coches = []

    pygame.init() # Inicializamos todos los modulos de Pygame
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) # Establece la pantalla en modo de pantalla completa con el tamaño 'ANCHO' y 'ALTO'
    reloj = pygame.time.Clock() # Creamos un objeto reloj para controlar el tiempo en la simulacion
    # Creamos una fuente para renderizar el texto
    fuente_generacion = pygame.font.SysFont("Arial", 30) 
    fuente_vivo = pygame.font.SysFont("Arial", 20)
    fuente_modo = pygame.font.SysFont("Arial", 20)
    # Carga y convierte el mapa del juego para una manipulacion rapida
    mapa_juego = pygame.image.load(nombre_mapa).convert()

    global generacion_actual # Incrementamos la generacion actual
    generacion_actual += 1 # Creamos un contador que controla la duracion de la simulacion

    contador = 0

    for i, g in genomas:
        # Creamos una red neuronal para cada genoma usando la configuracion 'config'
        red = neat.nn.FeedForwardNetwork.create(g, config)
        redes.append(red)
        g.fitness = 0 # Inizializamos fitness de cada genoma a 0
        coches.append(Coche()) # Creamos una instancia de 'Coche' para cada red neuronal

    # Capturamos la salida estándar
    sys.stdout = StdoutCapture() # Redirige la salida estandar a un objeto personalizado para capturar la salida

    # Velocidad de simulación
    velocidad_simulacion = VELOCIDAD_NORMAL

    # Bucle principal de simulacion
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Cierra la simulacion
                sys.exit(0)
            elif evento.type == pygame.KEYDOWN: # Captura pulsaciones de teclas para cambiar la velocidad de la simulacion 
                if evento.key == pygame.K_SPACE:  # Tecla espacio para acelerar
                    velocidad_simulacion = VELOCIDAD_ACCELERADA
                if evento.key == pygame.K_RETURN:  # Tecla Enter para volver a la velocidad normal
                    velocidad_simulacion = VELOCIDAD_NORMAL
                elif evento.key == pygame.K_LCTRL:
                    velocidad_simulacion = VELOCIDAD_LENTA # Tecla Left Ctrl para reducir la velocidad
        # Actualizacion de coches y redes neuronales
        for i, coche in enumerate(coches):
            salida = redes[i].activate(coche.obtener_datos()) # Activa la red neuronal con los datos del coche
            eleccion = salida.index(max(salida)) # Determina la accion basada en la salida de la red 
            # Ajustamos el angulo o velocidad del coche segun la accion elegida
            if eleccion == 0:
                coche.angulo += 10  # Izquierda
            elif eleccion == 1:
                coche.angulo -= 10  # Derecha
            elif eleccion == 2:
                if coche.velocidad - 2 >= 12:
                    coche.velocidad -= 2  # Reducir velocidad
            else:
                coche.velocidad += 2  # Acelerar
        # Verificacion de colisiones y estado de los coches 
        todavía_vivo = 0
        for i, coche in enumerate(coches):
            if coche.esta_vivo():
                todavía_vivo += 1
                coche.actualizar(mapa_juego) # Actualizamos la posicion de cada coche y verifica colisiones
                genomas[i][1].fitness += coche.obtener_recompensa() # Aumenta la aptitud del genoma si el coche sigue vivo

        if todavía_vivo == 0:
            break # Sale del bucle si todos los coches han colisionado

        contador += 1
        if contador == 30 * 40:  # Detener después de aproximadamente 20 segundos
            break

        # Renderizado y Actualizacion de la pantalla
        pantalla.blit(mapa_juego, (0, 0)) # Dibujamos el mapa del juego
        for coche in coches:
            if coche.esta_vivo(): # Dibujamos cada coche que siga vivo
                coche.dibujar(pantalla)
        
        # Renderizamos y dibujamos el texto de la generacion actual, el numero de coches vivos y el modo de velocidad
        texto_generacion = fuente_generacion.render("Generación: " + str(generacion_actual), True, (0,0,0))
        rect_texto_generacion = texto_generacion.get_rect()
        rect_texto_generacion.bottomright = (1920, 1000)
        pantalla.blit(texto_generacion, rect_texto_generacion)

        texto_vivo = fuente_vivo.render("Todavía vivo: " + str(todavía_vivo), True, (0, 0, 0))
        rect_texto_vivo = texto_vivo.get_rect()
        rect_texto_vivo.bottomright = (1920, 1080)
        pantalla.blit(texto_vivo, rect_texto_vivo)

        texto_modo = fuente_modo.render("Modo: " + ("Acelerado" if velocidad_simulacion == VELOCIDAD_ACCELERADA else "Velocidad lenta" if velocidad_simulacion < VELOCIDAD_NORMAL else "Normal"), True, (0, 0, 0))
        rect_texto_modo = texto_modo.get_rect()
        rect_texto_modo.bottomleft = (0, 1080)
        pantalla.blit(texto_modo, rect_texto_modo)

        pygame.display.flip() # Actualizamos la pantalla
        reloj.tick(velocidad_simulacion)  # Usamos la velocidad seleccionada

    # Restauramos la salida estándar
    sys.stdout = sys.__stdout__ # Sale del bucle principal si todos los coches han colisionado o ha pasado un tiempo predeterminado

""" Configuramos y ejecutamos una simulacion de coches controlados por redes neuronales entrenadas con NEAT.
La clase 'StdoutCapture' se define para capturar cualquier salida estandar generada durante la simulacion, 
aunque no se usa explicitamente en el bloque principal"""
class StdoutCapture:
    def __init__(self):
        self.content = ""

    def write(self, string):
        self.content += string

    def flush(self): # Creamos un Metodo Vacio requerido para la compatibilidad con la interfaz de archivo de salida estandar
        pass

# Configuramos y ejecutamos la simulacion utilizando NEAT y Pygame
if __name__ == "__main__":
    ruta_config = "./config.txt" # Ruta al archivo de configuracion NEAT
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                ruta_config) # Creamos una configuracion para NEAT usando los parametros proporcionados y el archivo de configuracion

    print("Selecciona el mapa para la simulación:")
    print("1. Mapa 1")
    print("2. Mapa 2")
    print("3. Mapa 3")
    print("4. Mapa 4")
    print("5. Mapa 5")
    
    mapa_seleccionado = input("Ingresa el número del mapa deseado: ")

    if mapa_seleccionado == "1":
        nombre_mapa = "map1.png"
    elif mapa_seleccionado == "2":
        nombre_mapa = "map2.png"
    elif mapa_seleccionado == "3":
        nombre_mapa = "map3.png" 
    elif mapa_seleccionado == "4":
        nombre_mapa = "map4.png"
    elif mapa_seleccionado == "5":
        nombre_mapa = "map5.png"   
    else:
        print("Mapa no válido. Seleccionando mapa 1 por defecto.")
        nombre_mapa = "map1.png"

    poblacion = neat.Population(config) # Inicializamos una nueva poblacion con la configuracion 'config'
    poblacion.add_reporter(neat.StdOutReporter(True)) # Muestra el progreso en la salida estandar
    estadisticas = neat.StatisticsReporter() 
    poblacion.add_reporter(estadisticas)
    
    poblacion.run(lambda genomas, config: ejecutar_simulacion(genomas, config, nombre_mapa), 1000)


