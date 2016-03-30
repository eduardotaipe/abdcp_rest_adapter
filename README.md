ABDCP REST Adapter
==================


CONSULTA PREVIA
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

CONSULTA PREVIA, el Cedente no responde la consulta
---

    RECIPIENT                             ABDCP                                 DONOR
        +                                   +                                     +  
        |                                   |                                     |  
        |                                   +----------------ECPC----------------->  -----------
        |                                   |                                     |      ^
        |                                   |                                     |      |    
        |                                   |                                     |  validation
        |                                   |                                     |  by donor
        |                                   |                                     |      |
        |                                   |                                     |      v
        |                                   |                                     |  -----------
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   |                                     |  
        <------------CPRABD-----------------+-------------------NE---------------->  
        |                                   |                                     |  
        |                                   |                                     |  
        +                                   +                                     +  


SOLICITUD DE PORTABILIDAD
---

    RECIPIENT                             ABDCP                                 DONOR
        +                                   +                                     +  
        +--------------SP------------------->                                     |  
        <-------------[NI]------------------+                                     |  
        |                                   |                                     |  
        <--------------ANS------------------+                                     |  
        |                                   |                                     |  
        <-------------[RABDCP]--------------+----------------ESC------------------>  
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   <---------------[OCC]-----------------+  
        <-------------[RABDCP]--------------+                                     |  
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   |                                     |  
        |                                   <-----------------SAC-----------------+  
        |                                   |                                     |  
        <---------------SPR-----------------+-----------------SPR----------------->
        |                                   |                                     |  
        +                                   +                                     +  


GUIA PARA HACER DEBUG
===

Activar el virtualenv

    source venv/bin/activate

Ejecutar el archivo debug.py

    python debug.py

(c) 2014 - Red Científica Peruan
