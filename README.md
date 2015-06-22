ABDCP REST Adapter
==================


FLUJO DE CONSULTA PREVIA
---

    RECIPIENT                             ABDCP                                 DONOR
        +                                   +                                     +  
        +--------------CP------------------->                                     |  
        <-------------[NI]------------------+                                     |  
        |                                   |                                     |  
        <--------------ANCP-----------------+                                     |  
        |                                   |                                     |  
        <-------------[CPRABD]-------------------------------ECPC----------------->  
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   <---------------[CPOCC]---------------+  
        <-------------[CPRABD]--------------+                                     |  
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   <-----------------CPAC----------------+  
        <--------------CPPR-----------------+                                     |  
        |                                   |                                     |  
        +                                   +                                     +  


GUIA PARA HACER DEBUG
===

Activar el virtualenv
    source venv/bin/activate

Ejecutar el archivo debug.py
    python debug.py

(c) 2014 - Red Científica Peruan
