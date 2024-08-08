# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 12:26:16 2024

@author: Estudiante
"""
#cargar la libreria
import wfdb
import numpy as np
import matplotlib.pyplot as plt

#cargar la informacion (señal)
#hay que tener ambos archivos: .dat .hea
#guardar codigo y datos en la misma carpeta
senal = wfdb.rdrecord('C04')

#verificacion de la cantidad de señales
print(senal.n_sig)

#visualizar valores de la señal
print(senal.p_signal)

#cuantos valores hay
print(senal.sig_len)

#almacenar los valores en una variable para poderlos manipular
valores = senal.p_signal.flatten()

#visualizar los valores
plt.plot(valores)

#calcular la media con el comando np.men()
media1 = np.mean(valores)
print("la media1 es:" , media1)

#calcular la desviacion estandar con el comando np.std
desviacion__estandar = np.std(valores)
print("la desviacion estandar es:",desviacion__estandar)

#calcular el coeficiente de variacion con el comando 
coeficinete_de_variacion = desviacion__estandar / media1
print("el coeficiente de variacion es:",coeficinete_de_variacion)


#calcular la media de los valores de la señal
# N determina el numero total de valores
#inicializamos la suma en cero
#se utiliza un for para sumar todos los valores
#establecemos un bucle que se ejecutara N veces de 0 hasta (N-1)
#en donde valore[i] accede a cada valor en la posicion i la lista en valores

suma = 0
N = len(valores)
for i in range(N):
    suma += valores[i]


media =  suma / N



# Calcular la desviación estándar de los valores de la señal usando la fórmula
# suma_cuadrados se almacenara la suma de los cuadrados de las diferencias entre cada valor y la media
#otra vez establecemos un for en donde se ejecutara N veces
# entonces (valores[i] - media) ** 2 establece la diferencia entre el valor en la posicion i y la media para luego elevarla al cuadrado
# en donde por ultimo se calcula la desviacion estandar dividiendo la suma_cuadrados  sobre N y tomando la raiz del resultado.
suma_cuadrados = 0

for i in range(N):
    suma_cuadrados += (valores[i] - media) ** 2

desviacion_estandar = (suma_cuadrados / N) ** 0.5

# Visualizar la media y la desviación estándar
print("La media de los valores de la señal es:", media)
print("La desviación estándar de los valores de la señal es:", desviacion_estandar)

#calcular el coeficiente de variacion
coeficiente_variacion = desviacion_estandar / media
print("El coeficiente de variacion de los valores de la señal es:", coeficiente_variacion)



#histograma crearlo
frecuencias , bordes = np.histogram(valores, bins=30)

#calculamos las densidades de probabilidad
densidades = frecuencias / (len(valores)*np.diff(bordes))

# Crear un histograma de los valores de la señal
plt.figure()
plt.hist(valores, bins = bordes,density=True,edgecolor = 'black' , alpha=0.5, label = 'histograma de probabilidad')
plt.plot(bordes[: -1], densidades, 'r-' , linewidth=2,label='funcion de probabilidad')
plt.title("Histograma de la Señal y funcion de probabilidad")
plt.xlabel("Valor")
plt.ylabel("densidad de la frecuencia ")
plt.legend()
plt.grid(True)
plt.show()





# calcular el ruido gaussiano
plt.figure()
N = len(valores)
RG = np.random.normal(0,1 , N)
plt.plot( RG, '.-')
plt.title("RG")
plt.xlabel("M")
plt.ylabel("A")
plt.show()
plt.close()


#unimos el ruido y la señal
senalG = valores + RG 
plt.figure()
plt.plot( senalG, '.-')
plt.title("RG+señal")
plt.xlabel("M")
plt.ylabel("A")
plt.show()
plt.close()




# calculamos la potencia de la señal
# inicializamos una variable suma_cuadrado que nos va acumular la suma de los valores
# de la señal. despues el bucle recorre cada i desde cero hasta n-1 calculando cada
#senal una por una, despues obtenemos el valor de la muestra y lo elevamos al cuadrado
# para ya crear nuestra potencia de la señal con suma_cuadrados1 sobre N 
suma_cuadradosS = 0 
for i in range (N):
    suma_cuadradosS += valores[i]**2
    
    p_senal= suma_cuadradosS / N
print("la potencia de la señal es", p_senal)
#calcular la potencia del ruido 
#hacemos lo mismo que en la potencia de la señal pero ahora con ruido utilizamos
#la misma N por que el ruido lo generamos con el mismo numero de muestras que la señal.
suma_cuadradosR = 0 
for i in range (N):
    suma_cuadradosR += RG[i]**2
    
    p_RG= suma_cuadradosR / N
print("la potencia del ruido es", p_RG)
    
#calculamos el SNR RG
#utilizamos la funcion de log en base 10 y dividimos las potencias y multiplicamos por 10.
SNR_RG = 10*np.log10(p_senal / p_RG)
SNR_RG1 = 10*np.log10(p_senal / p_RG+8)

print ("el SNR_RG es", SNR_RG)
print ("el SNR_RG1 es", SNR_RG1)


#generar el ruido impulso
#esto nos permite obtener el mismoconjunto de numeros aleatorios,
#cada vez que compilamos el codigo.
np.random.seed(0)

#establecemos el 5 % del total de las muestras   como el numero total de impulsos.
num_impulsos = int(N*0.05)

#creamos un array con el mismo tamaño de la señal.
ruido_impulso = np.zeros(N)

#ahora el num_impulsos nos ayuda para que vaya seleccionando las posiciones aleatorias 
#dentro del rango N que es el tamaño de la señal.
#replace nos ayuda para que no se seleccionen posiciones repetidas.
posiciones_impulsos = np.random.choice(N, num_impulsos, replace = False)


#genera valores aleatorios entre -10 y 10 que representa la amplitud 
amplitudes_impulsos = np.random.uniform (-4,4,num_impulsos)

#entonces el zip  nos ayuda a combinar las posiciones y amplitudes en el for
#se itera en cada par de poscion y amplitud y ya por ultimo 
#ruido impulso [pos] asigna el valor de la amplitud a la posicion especifica.
for pos ,amp in zip(posiciones_impulsos, amplitudes_impulsos):
    ruido_impulso[pos] = amp


# graficamos el ruido_impulso
plt.figure()
plt.plot( ruido_impulso, '.-')
plt.title("RI")
plt.xlabel("M")
plt.ylabel("A")
plt.show()
plt.close()

# graficamos el RI mas la señal.
senalRI = valores + ruido_impulso 
plt.figure()
plt.plot( senalRI, '.-')
plt.title("RI+seÑal")
plt.xlabel("M")
plt.ylabel("A")
plt.show()
plt.close()


# calculamos la potencia de la señal
# inicializamos una variable suma_cuadrado que nos va acumular la suma de los valores
# de la señal. despues el bucle recorre cada i desde cero hasta n-1 calculando cada
#senal una por una, despues obtenemos el valor de la muestra y lo elevamos al cuadrado
# para ya crear nuestra potencia de la señal con suma_cuadrados1 sobre N 
suma_cuadradosS = 0 
for i in range (N):
    suma_cuadradosS += valores[i]**2
    
    p_senal= suma_cuadradosS / N
print("la potencia de la señal es", p_senal)
    
#calcular la potencia del ruido 
#hacemos lo mismo que en la potencia de la señal pero ahora con ruido utilizamos
#la misma N por que el ruido lo generamos con el mismo numero de muestras que la señal.
suma_cuadradosR = 0 
for i in range (N):
    suma_cuadradosR += ruido_impulso[i]**2
    
    p_RI= suma_cuadradosR / N
    
print("la potencia del ruido es", p_RI)
    
#calculamos el SNR RG
#utilizamos la funcion de log en base 10 y dividimos las potencias y multiplicamos por 10.
SNR_RI = 10*np.log10(p_senal / p_RI)
SNR_RI1 = 10*np.log10(p_senal / p_RI+4)

print ("el SNR_RI es", SNR_RI)
print ("el SNR_RI1 es", SNR_RI1)


# generar el ruido artefacto
frecuencia_ruido = 50
#aca colocamos 50 por que es la frecuencia que representa el RA
ruido_artefacto = 0.5 *np.sin(2 * np.pi *frecuencia_ruido * np.arange(N)/ N)
#aca calculamos la funcion seno ya que se asemeja a una señal periodica que simula el RA
#despues multiplicamos 2 por np.pi y la frecuencia del ruido para dar la frecuencia angular
#creamos un array  de 0 hasta N-1 para despues dividirlo por N y normalizar el rango de los
#valores, y despues escalamos la amplitud a la mitad con el 0.5

#graficamos el ruido artefacto.
plt.figure()
plt.plot( ruido_artefacto, '.-')
plt.title("RA")
plt.xlabel("M")
plt.ylabel("A")
plt.show()
plt.close()

# graficamos el RA mas la señal.
senalRA = valores + ruido_artefacto
plt.figure()
plt.plot( senalRA, '.-')
plt.title("RA+señal")
plt.xlabel("M")
plt.ylabel("A")
plt.show()
plt.close()

# calculamos la potencia de la señal
# inicializamos una variable suma_cuadrado que nos va acumular la suma de los valores
# de la señal. despues el bucle recorre cada i desde cero hasta n-1 calculando cada
#senal una por una, despues obtenemos el valor de la muestra y lo elevamos al cuadrado
# para ya crear nuestra potencia de la señal con suma_cuadrados1 sobre N 
suma_cuadradosS = 0 
for i in range (N):
    suma_cuadradosS += valores[i]**2
    
    p_senal= suma_cuadradosS / N
print("la potencia de la señal es", p_senal)
    
#calcular la potencia del ruido 
#hacemos lo mismo que en la potencia de la señal pero ahora con ruido utilizamos
#la misma N por que el ruido lo generamos con el mismo numero de muestras que la señal.
suma_cuadradosR = 0 
for i in range (N):
    suma_cuadradosR += ruido_artefacto[i]**2
    
    p_RA= suma_cuadradosR / N
    
print("la potencia del ruido es", p_RA)
    
#calculamos el SNR RG
#utilizamos la funcion de log en base 10 y dividimos las potencias y multiplicamos por 10.
SNR_RA = 10*np.log10(p_senal / p_RA)
SNR_RA1 = 10*np.log10(p_senal / p_RA+7)

print ("el SNR_RI es", SNR_RI)
print ("el SNR_RI1 es", SNR_RI1)

    











