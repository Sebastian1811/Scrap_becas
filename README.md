# Scrap Becas

Primera etapa de TG, proyecto encargado de extracción de datos de becas a partir de diferentes fuentes
de información para conformar el dataset de becas.

# Ejecutar spider para comenzar extracción

Primero instale las dependencias del proyecto:

``` shell
pip install -r requirements.txt
```

Luego inicie el extractor:

``` shell
make scrap
```

Esto va generar un dataset cuyo nombre es un timestamp de la ejecución. El dataset contiene la información de las becas definidad para esta etapa del proyecto.

# Dev info

- Python version: 3.10.7
- Scrapy version: 2.6.2

# Autor

Jhoan Sebastian Andica - estudiante de ingeniería de sistemas UV.