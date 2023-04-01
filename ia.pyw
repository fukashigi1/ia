import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

class ia():
    def __init__(self): #MAIN
        self.data = {} #clave X, valor S
        #Primer valor: k, Segundo valor: n, Tercer valor: u.
        #K, indice totales de columnas de neuronas.
        #N, cantidad de neuronas totales en K.
        #U, es el umbral correspondiente a cada neurona.
        self.listaData = []

        self.kNeuronas = {1: 1, 2: 3, 3: 1} #Se define la red neuronal.
        self.neuronas = {} #Aquí se almacenarán las neuronas PrimerValor: N, SegundoValor: Umbral
        self.capaPeso = {} #capaPEso Primer valor: Indice de peso, Lista: [0 = peso, 1 = j, 2 = i]

        self.forwardPropagationResults = {} #K, capa neuronal, Valor de la funcion de activacion.
        self.sY = {} #Conformado por S: Y.
        self.wE = {} #Conformado por W: Error.

        #Iniciar metodos
        
        self.procesoUmbral()
        self.contadorPesos()
        self.creadorDeBD() #eliminar al poner interfaz
        self.convertidorDataALista()
        self.forwardPropagation()
        self.imprimirRed()
        self.creadorListaSY()
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
       
    def creadorDeBD(self): #Este metodo es llamado desde el front end para generar la tabla.
        self.data.clear()
        for x in range(1, 101):
            x = random.randint(-1000, 1000)
            if x >= 0:
                s = 1
            else:
                s = 0
            self.data[x] = s
    #________________________________________________________________________________________________________________________________________________________________________________________       

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
        print("Forward Propagation ~")
        for resultado in self.forwardPropagationResults:
            print(f'{resultado} -> {self.forwardPropagationResults[resultado]}')
    def forwardPropagation(self): #Este metodo calcula toda la red neuronal aplicando la funcion de activacion sigmode 
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
                    self.forwardPropagationResults[k].append(self.entradaValor(neuronas+10, self.listaData))
        #luego sacar el error con respecto a cada peso y almacenarlo en otro diccionario (W: Error)

    def creadorListaSY(self):
        listaCantidadNeuronasFinales = self.forwardPropagationResults[len(self.kNeuronas)]
        for valor in listaCantidadNeuronasFinales:
            print(valor)
if __name__ == "__main__":
    ia()
