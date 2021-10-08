# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 23:13:58 2021

@author: Miguel Angel Santamaria Vilchis
"""


import csv
import matplotlib.pyplot as plt


class Quaerit:
    
    
    """ Funciones de utilidad """
    
    # Lee los datos del un archivo csv y los regresa en forma de tabla
    def abrirCsv(self, csv_name):
        
        data = []
        
        with open(csv_name, "r") as archivo_csv:
            lector = csv.reader(archivo_csv)
            
            for linea in lector:    
                data.append(linea)
                
            data.pop(0)     # Elimina la fila de encabezados 
            
        return data
    
    # Obtiene los valores unicos de una columna y los regresa en un set
    def crearSet(self, data, columna):
        
        unique = set()
        
        for linea in data:
            unique.add(linea[columna])
            
        return unique
    
    
    def imprimirDict(self, diccionario):
        
        i = 1
        for key in diccionario:
            print(i, end=". ")
            print(key, end=": ")
            print(diccionario[key])
            i+=1
            
        print()
    
    def imprimirList(self, lista):
        
        i = 1
        for var in lista:
            print(i, end=". ")
            print(var)
            i+=1
            
        print()
        
    """ Todos los reportes """
    # Funcion que llama a las funciones que hacen los reportes
    def reporteGeneral(self, csv_name):
        """ Estructura de data
        [0] = register_id
        [1] = direction
        [2] = origin
        [3] = destination
        [4] = year
        [5] = date
        [6] = product
        [7] = transport_mode
        [8] = company_name
        [9] = total_value
        """
        
        data = self.abrirCsv(csv_name)
        
        
        self.reporteRutas(data)
        
        self.reporteTransportes(data)
        
        self.reporteTotales(data)
        
        print("Finished")
    
    
    
    """ Reportes """
    def reporteRutas(self, data):
        
        """ Reportes
        Estructura de exportaciones
        [key] = nombre de la ruta Pais1-Pais2
        [value] = valor acumulado
        
        Estructura de importaciones
        [key] = nombre de la ruta Pais1-Pais2
        [value] = valor acumulado
        """

        # Crea un set con los nombres de las rutas
        rutas = set()
        
        for row in data:
            
            p1 = row[2]
            p2 = row[3]
            
            if (p1 > p2):
                rutas.add(row[2]+"-"+row[3])
                
            else:
                rutas.add(row[3]+"-"+row[2])
        
        # Inicializa el diccionario de rutas
        rutas = dict.fromkeys(rutas, 0)
        
        # Obtiene la informacion de la tabla data
        for row in data:
            
            p1    = row[2]
            p2    = row[3]
            value = int(row[9])
            
            # Genera la ruta de la linea en formato Pais1-Pais2
            if (p1 > p2):
                ruta = (row[2]+"-"+row[3])
            else:
                ruta = (row[3]+"-"+row[2])
            
            rutas[ruta] = rutas[ruta] + value
            
        # Ordenar rutas de mayor a menor
        rutas = dict(sorted(rutas.items(), key=lambda item: item[1], reverse=True))
        
        
        print ("Reporte Rutas (valor total en USD)")  
        self.imprimirDict(rutas)
        
        """ Plot """
        fig, ax = plt.subplots(figsize=(16, 20))
        ax.barh(*zip(*rutas.items()))
        ax.invert_yaxis()
        ax.set_xlabel('Valor acumulado en 10 mil millones de USD')
        ax.set_ylabel('Nombre de ruta')
        ax.set_title('Valor acumulado por ruta')
        plt.tight_layout()
    
    
    def reporteTransportes(self, data):
        
        """ Estructura de reporte
        [key] = tipo de transporte
        [value] = valor acumulado
        """
        
        # Crea un set con los tipos de transporte
        transportes = self.crearSet(data, 7)
        
        # Inicializa el diccionario de reporte
        reporte = dict.fromkeys(transportes, 0)
        
        # Obtiene la informacion de la tabla data
        for row in data:
            
            transporte = row[7]
            
            reporte[transporte] = reporte[transporte] + int(row[9])
            
        
        # Ordenar reporte de mayor a menor
        reporte = dict(sorted(reporte.items(), key=lambda item: item[1], reverse=True))
        
        print("Reporte Transportes (valor total en USD)")
        self.imprimirDict(reporte)
        
        """ Plot """
        fig, ax = plt.subplots(figsize =(16, 9))
        ax.barh(*zip(*reporte.items()))
        ax.invert_yaxis()
        ax.set_ylabel('Valor acumulado en 10 mil millones de USD')
        ax.set_xlabel('Tipo de transporte')
        ax.set_title('Valor acumulado por transportes')
                     
        plt.tight_layout()
        
        
        """ Reporte
        Sea     100530622000    10688
        Rail    43628043000     3381
        Air     38262147000     2389
        Road    33270486000     2598
        """
        
    def reporteTotales(self, data):
        
        """ Reportes
        Estructura de exportaciones
        [key] = nombre del pais
        [value] = valor acumulado
        
        Estructura de importaciones
        [key] = nombre del pais
        [value] = valor acumulado
        """

        # Crea un set con los nombres de los paises
        paises_expor = self.crearSet(data, 2)
        paises_impor = self.crearSet(data, 3)
        
        # Inicializa los diccionarios de exportaciones e importaciones
        exportaciones = dict.fromkeys(paises_expor, 0)
        importaciones = dict.fromkeys(paises_impor, 0)
        
        # Obtiene la informacion de la tabla data
        for row in data:
            
            origen    = row[2]
            destino   = row[3]
            value     = int(row[9])
            
            exportaciones[origen] = exportaciones[origen] + value
            importaciones[destino] = importaciones[destino] + value
            
        
        # Ordenar reportes de mayor a menor
        exportaciones = dict(sorted(exportaciones.items(), key=lambda item: item[1], reverse=True))
        importaciones = dict(sorted(importaciones.items(), key=lambda item: item[1], reverse=True))
        
        
        # Obtiene las sumas de exportacioes e importaciones al 80%
        sum_exportaciones = sum(exportaciones.values()) * 0.8
        sum_importaciones = sum(importaciones.values()) * 0.8
        
        # Obtiene los paises que menejan el 80% del valor total
        top_exportaciones = []
        top_importaciones = []
        
        for pais in exportaciones:
            if (sum_exportaciones > 0):
                top_exportaciones.append(pais)
                sum_exportaciones -= exportaciones[pais]
            else:
                break
            
        print ("Top 80% Exportaciones (valor total en USD)")    
        self.imprimirList(top_exportaciones)
        
        for pais in importaciones:
            if (sum_importaciones > 0):
                top_importaciones.append(pais)
                sum_importaciones -= importaciones[pais]
            else:
                break
        
        print ("Top 80% Importaciones (valor total en USD)")  
        self.imprimirList(top_importaciones)
        
        
        """ Plot Exportaciones """
        fig1, ax1 = plt.subplots(figsize =(16, 9))
        ax1.barh(*zip(*exportaciones.items()))
        ax1.invert_yaxis() 
        ax1.set_ylabel('Pais')
        ax1.set_xlabel('Valor acumulado en 10 mil millones de USD')
        ax1.set_title('Valor acumulado de exportaciones por pais')
        
        """ Plot Importaciones """
        fig2, ax2 = plt.subplots(figsize =(16, 9))
        ax2.barh(*zip(*importaciones.items()))
        ax2.invert_yaxis() 
        ax2.set_ylabel('Pais')
        ax2.set_xlabel('Valor acumulado en 10 mil millones de USD')
        ax2.set_title('Valor acumulado de importaciones por pais')
            
        plt.tight_layout()
    

if __name__ == "__main__":
    
    qu = Quaerit()
    
    csv_name = "synergy_logistics_database.csv"
    qu.reporteGeneral(csv_name)
    
