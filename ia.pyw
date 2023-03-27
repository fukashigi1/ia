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

        self.kNeuronas = {1: 1, 2: 3, 3: 3, 4: 1} 
        self.neuronas = {}
        self.capaPeso = {} #capaPEso Primer valor: Indice de peso, Lista: [0 = peso, 1 = j, 2 = i]

        self.backPropagationResults = {} #K, capa neuronal, Valor.
        self.sY = {} #Conformado por S: Y.
        self.wE = {} #Conformado por W: Error.

        #Iniciar metodos
        
        self.procesoUmbral()
        self.contadorPesos()
        self.creadorDeBD() #eliminar al poner interfaz
        self.convertidorDataALista()
        self.backPropagation()
        #self.imprimirRed()
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
        for x in range(1, 51):
            for s in range(1, 51):
                x = random.randint(-100, 100)
                if x >= 0:
                    s = 1
                else:
                    s = 0
                self.data[x] = s
    #________________________________________________________________________________________________________________________________________________________________________________________       

    def convertidorDataALista(self):
        for clave in self.data:
            self.listaData.append(clave)

    def entradaValor(self, valor, lista):
        valorConvertido = (valor - min(lista))/(max(lista) - min(lista))
        return round(valorConvertido, 4)

    def salidaValor(self, valorFinal, lista):
        return (max(lista) - min(lista) * valorFinal + min(lista))
    
    def procesoUmbral(self): #Se le añade al diccionario kNeuronas la cantidad de umbrales acorde a N en K.
        for capa in self.kNeuronas:
            self.neuronas[capa] = []
            for n in range(1, self.kNeuronas[capa]+1):
                if capa == 1:
                    self.neuronas[capa].append([n]) #Se omite la capa 1 porque es de entrada (X)
                else:
                    self.neuronas[capa].append([n, random.random()])

    def contadorPesos(self): # 1: 1 | 2: 4 | 3: 4 | 4: 1
        #capaPEso Primer valor: Indice de peso, Lista: [0 = peso, 1 = j, 2 = i]
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

    def imprimirRed(self):
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

    def backPropagation(self): #Funcion que hara el calculo final de Y.
        for k in self.neuronas:
            valor = 0
            self.backPropagationResults[k] = [] #Se inicia la clave K con una lista vacía para que se almecenen individualmente los valores de esa capa K.
            if k != 1: #si capa es 1 entonces son valores de entrada.
                valor = []
                #iterar en capas neuronales
                #iterar en back propagation capas
                #iterar en los pesos
                #iterar en capas denuevo
                iteracion = 0
                for resultadoNeuronaAnterior in self.backPropagationResults[k-1]:
                    for capapeso in self.capaPeso[k-1]:
                        for capa in self.neuronas[k]:
                            if capapeso[1] == self.neuronas[k-1][0][0] and capapeso[2] == capa[0]:
                                iteracion = iteracion + 1  
                                print(iteracion)
                        
            else:
                valor = self.entradaValor(10, self.listaData) #Se llama a la funcion que transforma valores de entrada a minimos y maximos.
                self.backPropagationResults[k].append(valor)
                self.backPropagationResults[k].append(valor+1)
                self.backPropagationResults[k].append(valor+2) #Se agrega a la capa K de backPropagationResults (diccionario), el valor (pasaría con todas las neuronas de entrada).




        #for k in reversed(self.kNeuronas):
        #    valor = 0
        #    self.backPropagationResults[k] = [] #Se inicia la clave K con una lista vacía para que se almecenen individualmente los valores de esa capa K.
        #    if k == 1: #si capa es 1 entonces son valores de entrada.
        #        valor = self.entradaValor(10, self.listaData) #Se llama a la funcion que transforma valores de entrada a minimos y maximos.
        #        self.backPropagationResults[k].append(valor) #Se agrega a la capa K de backPropagationResults (diccionario), el valor (pasaría con todas las neuronas de entrada).
        #    else:
        #        #Aquí en caso de que la capa no sea la primera, debemos hacer el calculo de su peso anterior por la neurona conectada por su umbral y almacenarlo en la capa correspondiente.
        #        for capaAnterior in self.neuronas[k-1]:
        #            



            #for funcion in self.backPropagationResults[k-1]:
            #    for omega in self.capaPeso[k-1]:
            #        for capa in self.neuronas[k]:
            #            if omega[1] == len(self.backPropagationResults[k-1]) and omega[2] == capa[0]:
            #                self.backPropagationResults[k].append((funcion*omega[0])+capa[1])
                            
        print(f'BP -> {self.backPropagationResults}')
        print(f'NEURONAS -> {self.neuronas}')
        print(f'PESOS -> {self.capaPeso}')
        #transformar el valor de entrada, multiplicar todos los pesos con los umbrales y almacenar el valor final Y, junto con S (otro diccionario)
        #luego sacar el error con respecto a cada peso y almacenarlo en otro diccionario (W: Error)
if __name__ == "__main__":
    ia()
