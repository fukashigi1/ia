import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

class ia():
    def __init__(self): #MAI
        #LISTAS Y DICCIONARIOS
        self.data = {} #clave X, valor S
        #Primer valor: k, Segundo valor: n, Tercer valor: u.
        #K, indice totales de columnas de neuronas.
        #N, cantidad de neuronas totales en K.
        #U, es el umbral correspondiente a cada neurona.
        self.listaData = []

        self.kNeuronas = {1: 2, 2: 4, 3: 4, 4: 2} #Se define la red neuronal.
        self.neuronas = {} #Aquí se almacenarán las neuronas PrimerValor: N, SegundoValor: Umbral
        self.capaPeso = {} #capaPEso Primer valor: Indice de peso, Lista: [0 = peso, 1 = j, 2 = i]

        self.historialMSE = []

        self.nuevosPesos = {}

        self.forwardPropagationResults = {} #K, capa neuronal, Valor de la funcion de activacion.
        self.sY = [] #Conformado por S: Y.
        self.wE = {} #Conformado por W: Error.

        self.listaCantidadNeuronasFinales = [] #Total de Y en todos los ejemplos de aprendizaje.

        #VARIABLES
        self.ratioAprendizaje = 0.01 #Esta constante es para establecer la multiplicación a la hora de calcular el nuevo peso.

        #Iniciar metodos
        
        self.procesoUmbral()
        self.contadorPesos()
        self.creadorDeBD() #eliminar al poner interfaz
        self.convertidorDataALista()
        for iteracion in range(0, len(self.listaData)):
            self.forwardPropagation(self.listaData[iteracion])
        #self.imprimirRed()
        self.clasificador()
        self.calculadorError()
        self.nuevoPeso()
        #self.ventanaDisplay()

    def ventanaDisplay(self): #Método para mostrar ventana FRONT END.
        raiz = Tk() 
        raiz.title("Red neuronal")
        raiz.iconbitmap("icon.ico")
        miFrame = Frame(raiz, width=700, height=600, bg="#3a3c40")
        miFrame2 = Frame(miFrame, width=450, height=400, bg="#3a3c40", borderwidth=2, relief="ridge")
        miFrame.pack()
        miFrame2.place(x=350, y=350, anchor=CENTER)
        font = ["gg sans", 10]
        Label(miFrame, text = "Entrenador automático", bg="#494c52", fg="white", font=("gg sans", 10, "bold")).place(x=350, y=30, anchor=CENTER)
        descripcion = "Esta inteligencia artificial describirá con porcentajes de 0 y 100 si el valor entregado es positivo, 0 o negativo: 100%\nsi el numero es positivo o 0, y 0% si el numero es negativo."
        resultado = "asdasdasdasdasdasdsa"
        Label(miFrame, text = descripcion, bg="#494c52", fg="white", font=(font), justify=LEFT).place(x=350, y=110, anchor=CENTER)

        generarTabla = Button(miFrame2, text = "Generar tabla (X, S)", bg="#767a85", fg="white", font=(font), width=18, cursor="hand2", command=self.creadorDeBD).place(x=135, y=50, anchor=CENTER)
        mostrarTabla = Button(miFrame2, text = "Mostrar tabla", bg="#767a85", fg="white", font=(font), width=18, cursor="hand2", command=self.mostrarTabla).place(x=315, y=50, anchor=CENTER)
        entrenar = Button(miFrame2, text = "Entrenar", bg="#767a85", fg="white", font=(font), width=18, cursor="hand2").place(x=225, y=80, anchor=CENTER)
        Label(miFrame2, text = "Número:", bg="#494c52", fg="white", font=(font), justify=LEFT).place(x=135, y=120, anchor=CENTER)
        cuadroTexto = Entry(miFrame2, bg="#494c52", fg="white", font=(font), justify=CENTER, width=18).place(x=315, y=120, anchor=CENTER)
        botonNumero = Button(miFrame2, text = "Aceptar", bg="#767a85", fg="white", font=(font), width=18, cursor="hand2").place(x=225, y=160, anchor=CENTER)
        Label(miFrame2, text = resultado, bg="#494c52", fg="white", font=(font), justify=LEFT, borderwidth=2, relief="ridge").place(x=225, y=310, anchor=CENTER)

        
        raiz.mainloop()
        
    def mostrarTabla(self): #Método TKINTER para mostrar la tabla, FRONT END.
        # Crea la ventana
        table_window = tk.Toplevel()
        table_window.title("Tabla")

        # Crea la tabla
        table = ttk.Treeview(table_window, columns=("X", "S"), show="headings")
        table.heading("X", text="X")
        table.heading("S", text="S")
        table.pack(fill="both", expand=True)
        # Agrega datos de ejemplo a la tabla
        for x, s in self.data.items():
            table.insert("", "end", values=(x, s))
        #________________________________________________________________________________________________________________________________________________________________________________________       
    


    def creadorDeBD(self): 
        self.data.clear()
        for x in range(0, 50):
            while True:
                clave = random.randint(-1000, 1000)
                if clave not in self.data:
                    break
            valor = 1 if clave >= 0 else 0
            self.data[clave] = valor

    def convertidorDataALista(self): #Este metodo transforma el diccionario self.data en una lista que almacena los valores de X
        for clave in self.data:
            self.listaData.append(clave)

    def entradaValor(self, valor, lista):
        valorConvertido = (valor - min(lista))/(max(lista) - min(lista))
        return round(valorConvertido, 4)

    def salidaValor(self, valorFinal, lista):
        return (max(lista) - min(lista) * valorFinal + min(lista))
    
    def procesoUmbral(self): #Se le añade al diccionario neuronas la cantidad de umbrales acorde a N en K.
        for capa in self.kNeuronas:
            self.neuronas[capa] = []
            for n in range(1, self.kNeuronas[capa]+1):
                if capa == 1:
                    self.neuronas[capa].append([n]) #Se omite la capa 1 porque es de entrada (X)
                else:
                    self.neuronas[capa].append([n, random.random()])

    def contadorPesos(self): #Metodo para contar los pesos acorde a sus capas.
        for k in self.kNeuronas:
            if k != len(self.kNeuronas):
                self.capaPeso[k] = []
                siguienteCapaNeuronal = self.kNeuronas[k+1]
                pesosTotalesEnCapa = self.kNeuronas[k]*siguienteCapaNeuronal
                for capa in range(1, pesosTotalesEnCapa+1):
                    self.capaPeso[k].append([random.random()])
                contador = 0
                for j in range(1, self.kNeuronas[k]+1):
                    for i in range(1, siguienteCapaNeuronal + 1):
                        self.capaPeso[k][contador].append(j)
                        self.capaPeso[k][contador].append(i)
                        contador = contador +1

    def imprimirRed(self): #Metodo para testear en consola.
        linea = "_____________________________________"
        print(linea)
        for capa in self.kNeuronas:
            print(f'Capa de neuronas {capa}')
            incremental = 0
            while incremental != self.kNeuronas[capa]:
                if(capa == 1): #El valor de entrada no lleva umbral
                    print(f'> Neurona número: [{self.neuronas[capa][incremental][0]}]\n> Umbral: [No posee]')
                    incremental = incremental + 1
                else:
                    print(f'> Neurona número: [{incremental+1}]\n> Umbral: [{self.neuronas[capa][incremental][1]}]')
                    incremental = incremental + 1
            print(linea)
        #capaPEso Primer valor: Indice de peso, Lista: [0 = peso, 1 = j, 2 = i].
        for capaPeso in self.capaPeso:
            print(f'Capa de peso: {capaPeso}')
            for cadaPeso in self.capaPeso[capaPeso]:
                print(f'> Peso: [{cadaPeso[0]}]')
                print(f'> j: [{cadaPeso[1]}]')
                print(f'> i: [{cadaPeso[2]}]')
            print(linea)

    def forwardPropagation(self, valorEntrada): #Este metodo calcula toda la red neuronal aplicando la funcion de activacion sigmode 
        def activacion(valor):
            return 1 / (1 + pow(2.71828, -valor))

        for k in self.kNeuronas: #Recorremos las capas neuronales.
            self.forwardPropagationResults[k] = [] #Se crea una clave K, y se rellena con una lista vacia, para almacenar las funciones de activación.
            if k != 1: #Si K == 1 entonces se va por el else y agrega a la clave 1 los valores de entrada convertidos con la funcion entradaValor().
                for neurona in self.neuronas[k]: #Para cada neurona en las neuronas totales de la capa K
                    sumatoria = [] #Se crea una lista vacía que se reinicia con cada iteración para almacenar la sumatoria de los pesos * la funcion de activación de la neurona anterior.
                    #print(neurona)
                    for pesos in self.capaPeso[k-1]: #Ahora se entra a la capa de los pesos y la recorremos (k-1, porque las capas de los pesos son una menos que las neuronas).
                        #print(pesos)
                        contador = 1 #Hacemos un contador extra.
                        for neuronaAnterior in self.forwardPropagationResults[k-1]: #Para cada funcion de activacion en las neuronas anteriores.
                            #print(f'if {contador} == {pesos[1]} and {pesos[2]} == {neurona[0]}:')
                            if contador == pesos[1] and pesos[2] == neurona[0]: #Se comprueba que se está lidiando con el peso correspondiente a las dos neuronas.
                                sumatoria.append(pesos[0] * neuronaAnterior) #Se agrega a la lista momentanea para hacer la sumatoria.
                            contador = contador + 1
                    sumatoriaPesosNeurona = 0 #Se declara una variable.
                    for suma in sumatoria: #Para cada valor en la sumatoria se sumarán todos.
                        sumatoriaPesosNeurona += suma
                    self.forwardPropagationResults[k].append(activacion(neurona[1] + sumatoriaPesosNeurona)) #Se agrega al diccionario de funciones de activación mediante el metodo activacion().
                    #print(f'sumatoriaPesosNeurona ----- {sumatoriaPesosNeurona}')        
                    #print(f'suma ------------------- {sumatoria}')
            else: #El else mencionado anteriormente
                for neuronas in range(1, self.kNeuronas[k]+1): 
                    self.forwardPropagationResults[k].append(self.entradaValor(self.listaData[neuronas-1], self.listaData))
        self.listaCantidadNeuronasFinales.append(self.forwardPropagationResults[len(self.kNeuronas)])
        #FIN METODO

    def calculadorError(self):
        #(1/50) * [(0 - y^1)^2 + (0 - y^2)^2 + ... + (-0.8560 - y^i)^2 + ... + (0 - y^50)^2]
        mse = []
        for i in range(0, len(self.sY)):
            #print(f'({self.sY[i][0]} - {self.sY[i][1][0]}**2) = {(self.sY[i][0]-self.sY[i][1][0])**2}')
            mse.append((self.sY[i][1][0] - self.sY[i][0])**2)
        sumaMse = 0
        for z in mse:
            sumaMse = sumaMse + z
        sumaMse = sumaMse / len(self.sY)
        self.historialMSE.append(sumaMse)

    def clasificador(self): #Este metodo agrega a una lista el valor esperado y el obtenido. En caso de tener mas de un valor esperado, cambiar X para una lista [] en self.data
        iterador = 0
        for x, s in self.data.items():
            self.sY.append([s, self.listaCantidadNeuronasFinales[iterador]])
            iterador = iterador + 1
    
    def nuevoPeso(self):
        def dEdY():
            #∂E/∂W = ∂E/∂Y * ∂Y/∂W
            #∂E/∂Y = 2/n * sum(Yi-Si)
            #w' = w - α * ∂E/∂W   α= tasa de aprendizaje (esta es la formula del descenso de gradiente)
            resultadoSumatoriaLista = []

            for i in range(0, len(self.sY)):
                resultadoSumatoriaLista.append(self.sY[i][1][0] - self.sY[i][0])

            sumaSum = 0
            for z in resultadoSumatoriaLista:
                sumaSum = sumaSum + z

            dEdY = (2/len(self.listaData)) * sumaSum
            return dEdY
        
        dEdW_Sumatoria = {}
        dYdW = {}

        def multiplicador(lista):
            resultado = 1
            for elemento in lista:
                resultado = resultado * elemento
            return resultado
        
        def derivadaSigmoide(valor):
            return (valor * (1 - valor))

        for cantidad in range(1, self.kNeuronas[len(self.kNeuronas)]+1):
            for capa in reversed(self.capaPeso):
                print(f'Capa -> {capa}')
                dYdW[capa] = []
                for peso in reversed(self.capaPeso[capa]):
                    print(f'Peso: {peso}')
                    ecuacion = []
                    puntero = 0
                    for i in self.forwardPropagationResults[capa]:
                        if puntero+1 == peso[1]:
                            ecuacion.append(derivadaSigmoide(i))
                        puntero = puntero + 1
                    puntero = 0
                    for i in self.forwardPropagationResults[capa+1]:
                        if puntero +1 == peso[2]:
                            ecuacion.append(derivadaSigmoide(i))
                        puntero = puntero + 1
                    if capa == len(self.kNeuronas)-1:
                        dYdW[capa].append([multiplicador(ecuacion), peso[1], peso[2]])
                    else:
                        #ESCRIBIR EL RESTO DE LA LÓGICA.
                        sumatoria = []
                        for pesoAnterior in reversed(self.capaPeso[capa+1]):
                            #idea 1_:por cada peso tomar el valor de i y tomar su neurona asociada, agregarlo a una lista independiente y al final agregarlo a ecuación.
                            #idea 2_:si el pesoAnterior[2] == cantidad entonces agregar a ****ecuación****.
                            suma = 0
                            if peso[2] == pesoAnterior[1]:
                                puntero = 0
                                for neuronaAnterior in reversed(self.forwardPropagationResults[capa+2]):
                                    #TOMAR LAS RUTAS ENTRE PESOS Y NEURONAS Y SUMARLAS AL FINAL
                                    if pesoAnterior[2] == puntero +1: #colocar if para comprobar que no es la ultima capa
                                        ecuacion.append([derivadaSigmoide(pesoAnterior[0]), derivadaSigmoide(neuronaAnterior)])
                                    puntero = puntero + 1
                    print(f'{ecuacion} ==== [j{peso[1]}] - [i{peso[2]}]')
        print(dYdW)
        #Recorrer neuronas y pesos, peso por peso en orden desde inicio a fin, si el peso de la iteración es igual al peso actual entonces pass else, ecuacion.append(neurona y peso)         
if __name__ == "__main__":
    ia()
