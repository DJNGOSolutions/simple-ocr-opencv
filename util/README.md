# Reconocimiento Optico de Documentos de Identidad para El Salvador.

### Definición del sistema.
Este sistema pretende ser utilizado para el escaneo y obtención de datos obtenidos dentro de el DUI (Documento Único de Identidad en El Salvador). Esta información sera recolectada por el programa y enviada por medio de una API a un sistema web para posteriormente ser mostrado con amabilidad para el usuario.

### Requisitos del sistema.
* Python versión 2.7, 3.x
* IDE capaz de compilar y ejecutar codigo Python.
* Entorno Python de desarrollo con los siguientes paquetes instalados.
* opencv-python (Sirve para el reconocimiento de objetos).
* pytesseract (Reconocimiento óptico de caracteres).
* imutils (Manipulacion de imagenes).
* matplotlib.
* numpy (Libreria numerica de Python).
* pip.
* scikit-image (Manipulacion de imagenes).
* Tener instalado el programa de tesseract, para mas informacion sobre como instalarlo siga aqui: [windows], [linux] y [Mac].

### Procedimiento para utilizar el programa.
1. Preparar el entorno de Python.
2. Agregar las imágenes a escanear dentro del folder “resources”, ubicado en simple-ocr-opencv/util/.
3. Cambiar dentro de scan.py la ruta de la imagen que recibe como parametro cada función.
4. Correr el programa scan.py.

### Funciones dentro del sistema.
#### scan.py: 
Este es el archivo main de nuestro programa, dentro de este se encuentra la logica central de todo el codigo utilizado para scanear y manipular la imagen.
#### textDetector.py: 
Dentro de este archivo se encuentran las funciones que hacen uso de tesseract para leer los textos contenidos dentro de la imagen.
#### transform.py: 
Aqui se encuentran las funciones encargadas de obtener las esquinas del objeto a escanear, modificar su visualización a modo perspectiva y la función para rotar imagenes (de ser necesario).


### Informacion a tomar en cuenta.
- La información obtenida dentro del sistema tiene una precisión aproximada del 60%.
- La correcta detección del dui depende de la resolución de la imagen y de la claridad de sus bordes con respecto al fondo que la contenga.

[windows]: https://github.com/UB-Mannheim/tesseract/wiki
[linux]: https://tesseract-ocr.github.io/tessdoc/Home.html
[Mac]: https://tesseract-ocr.github.io/tessdoc/Home.html

#### Copyright and notices

This project is available under the [GNU AGPLv3 License](https://www.gnu.org/licenses/agpl-3.0.txt), a copy
should be available in LICENSE. If not, check out the link to learn more.
 
    Copyright (C) 2012-2017 by the simple-ocr-opencv authors
    All authors are the copyright owners of their respective additions
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU AGPLv3 License, as found in LICENSE.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.    
  
