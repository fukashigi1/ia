import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import pandas as pd

class ia():
    def __init__(self): #MAIN
        self.data = {} #clave X, valor S
        #Primer valor: k, Segundo valor: n
        #K, indice totales de columnas de neuronas.
        #N, cantidad de neuronas totales en K.
        self.kNeuronas = {1: [1], 2: [2], 3: [1]} 

        self.umbral = {} #Primer valor: k, Segundo valor: umbrales.
        self.capaPeso = {} #Primer valor: k, Segundo valor: cantidad de pesos, Tercer valor: j, Cuarto valor: i, Quinto valor: peso
        #Iniciar metodos
        self.procesoUmbral()
        self.contadorPesos()
        self.ventanaDisplay()
        self.selectorDePesos()

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
        print(self.data)
    #________________________________________________________________________________________________________________________________________________________________________________________       

    def entradaValor(valor, lista):
        valorConvertido = (valor - min(lista))/(max(lista) - min(lista))
        return round(valorConvertido, 4)

    def salidaValor(valorFinal, lista):
        return (max(lista) - min(lista) * valorFinal + min(lista))
    
    

    def contadorPesos(self):
        for k in self.kNeuronas:
            try:
                siguienteCapa = self.kNeuronas[k+1]
            except:
                break
            #capaPeso tomara valores de Primer valor: indice de peso, Segundo valor: Cantidad de pesos, Tercer valor: j, cuarto valor: i.
            self.capaPeso[k] = [siguienteCapa * k, k, siguienteCapa]
        print(self.capaPeso)

    def selectorDePesos(self): #Este metodo añade pesos al diccionario ya creado en "contadorPesos()".
        for capa in self.capaPeso: 
            for n in range(1, self.capaPeso[capa][0]+1): #TEST GITHUB
                self.capaPeso[capa].append(random.random())
        print(self.capaPeso)

    #def imprimirRed(self):
    #    for k, n in self.kNeuronas:
    #        
#
if __name__ == "__main__":
    ia()
