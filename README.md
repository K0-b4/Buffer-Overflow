# Buffer-Overflow
Memoria del programa:

Cuando se ejecuta una aplicación binaria, ésta asigna memoria de una forma muy específica dentro de los binarios de memoria que utilizan los ordenadores modernos.

La siguiente imagen ilustra como se asigna los espacios de memoria en windows, 

![image](https://user-images.githubusercontent.com/122020487/210770532-5dd4aedd-df65-4026-9cc8-0ad1bffd637c.png)

The stack (la pila):

Cuando un hilo se está ejecutando, ejecuta código desde dentro de la imagen del programa o desde varios dlls cargados por la aplicación.

El hilo requiere un área de datos a corto plazo para funciones, variables locales e información de control del programa. 
Esta área de datos se conoce como pila, para facilitar la ejecución independiente de múltiples hilos, cada hilo de una aplicación en ejecución tiene su propia pila.

La CPU considera la memoria de pila como una estructura de último en entrar, primero en salir. Esto significa esencialmente que al acceder a la pila, los elementos introducidos en la parte superior de la pila se extraen primero. 

La arquitectura x86 implementa instrucciones en ensamblador push y pop dedicadas para añadir datos o eliminarlos de la pila 

Función de retorno mecánica (Function return mechanics):

Cuando el código dentro de un hilo llama a una función, debe saber a qué dirección volver una vez que la función finaliza. 

![image](https://user-images.githubusercontent.com/122020487/210770571-795adc6c-ce4d-456b-8325-a496f834f277.png)

Esta dirección de retorno, junto con los parámetros de la función y las variables locales, se almacena en la pila. Esta colección de datos está asociada a una llamada de función y se almacena en una sección de la memoria de la pila conocida como marco de pila.

Cuando una función finaliza, la dirección de retorno se toma de la pila y se utiliza para restaurar el flujo de ejecución de vuelta al programa principal o a la función de llamada. aunque esto describe el proceso a un alto nivel, debemos entender más sobre cómo se realiza esto realmente a nivel de la cpu

Registros de la CPU:

Para realizar una ejecución de código eficiente, la CPU mantiene y usa una 9 registros de 32 bits cada uno. Estos registros son pequeños pero extremadamente rápidos guardando información en las diferentes localizaciones  de memoria de la CPU, donde los datos pueden ser leidos o manupulados de una forma bastante eficaz. 
Los nombres de registro fueron establecidos por las arquitecturas de 16 bits las cuales fueron extendidas a las plataformas de 32 bits, de ahí la letra "E" en el acrónimo de los registros.

![image](https://user-images.githubusercontent.com/122020487/210770612-2c441fb2-1738-4053-a290-171663b53f6a.png)

Cada registro puede tener los valores; 32, 16 u 8 bits, en los respectivos subregistros como podremos ver en la siguiente imagen:

![image](https://user-images.githubusercontent.com/122020487/210770640-e8ea50f7-47cd-4cb7-99f3-b66262edd17e.png)

Propósitos generales de los registros:

Muchos registros son usados habitualmente como propósitos generales de registro para guardar datos temporales, los principales registros que debemos tener en cuenta son los siguientes:

EAX: Para instrucciones logicas y aritméticas
EBX: Puntero base de direcciones de memoria 
ECX: Bucle, desplazamiento y contador de rotaciones
EDX: Direccionamiento de puertos, multiplicación y división
ESI: Puntero de datos y fuente en las operaciones de copia de cadenas
EDI: Puntero de datos y destinos en las operaciones de copia de cadenas.

ESP, EBP y EIP:

Como hemos mencionado anteriormente la pila es la encargada de almacenor los datos, punteros y argumentos. Desde que la pila es dinámica y cambia constantemente durante la ejecución del programa, el ESP que es el puntero de pila, mantiene un registro de la última ubicación a la que se ha hecho referencia almacenando un puntero a la misma. 

Un puntero es una referencia a una dirección o ubicación en la memoria, por lo que cuando decimos que un registro guarda un puntero o punteros en una dirección, significa que el registro está almacenando esa dirección de destino.

Desde que la pila está en constante flujo desde la ejecución del hilo, puede resultar dificil para una función localizar su propio marco de pila, la cual almacena los argumentos requeridos, variables locales y la dirección de retorno.
EBP es la base del puntero, la cual resuelve este problema guardando el puntero en la parte superior de la pila cuando una función es llamada. Accediando a EBP, una función puede facilmente referenciar información desde su propio marcho de pila mediante desplazamientos mientras se ejecuta.  

El EIP es el puntero de instrucciones, es uno de los más importantes en buffer overflow, ya que simpre apunta hacia el siguiente código de instrucción de tiene que ser ejecutado. Por lo que esencialmente dirige el flujo de un programa y es el objetivo principal de un atacante que quiera realizar con éxito la explotación. 

Ejemplo de cófigo vulnerable a Buffer OverFlow:

Este es un código vulnerable a BO, en este caso está escrito en C:

![image](https://user-images.githubusercontent.com/122020487/210770683-7f7f9e4e-9a75-4b20-9a17-b9a0d8c59d27.png)

Este código es un programa en C que hace lo siguiente:

	1. Declara una variable "buffer" de tipo "char" (un arreglo de caracteres) con un tamaño de 64 elementos.
	2. Verifica si se han pasado menos de dos argumentos al programa al ejecutarlo. Si es así, imprime un mensaje de error y termina la ejecución del programa con un          valor de retorno de 1.
	3. Si se han pasado al menos dos argumentos al programa, copia el contenido del segundo argumento (es decir, argv[1]) en la variable "buffer".
	4. Finalmente, el programa devuelve 0 para indicar que ha finalizado correctamente.

Por ejemplo, si ejecutamos el programa de la siguiente manera:

./mi_programa "hola mundo"

Entonces el valor de argc sería 2 (un argumento es el nombre del programa y el otro es "hola mundo"), y el contenido de argv sería:

argv[0] = "./mi_programa"
argv[1] = "hola mundo"

En este caso, el contenido de "hola mundo" se copiaría en la variable "buffer".

Si el argumento que pasamos es menor o igual a 64 carácteres, el programa funcionará correctamente, pero si procedemos a poner más caracteres de los permitidos, como por ejemplo 80, parte de la pila adyacente al búfer de destino será sobrescrita por los 16 carácteres restantes:

![image](https://user-images.githubusercontent.com/122020487/210770760-1fb17e46-f3e4-440c-a752-596ce5741360.png)

Immunity debugger:

Podemos utilizar una herramienta llamada debugger para asistirnos con el proceso de explotación, el debugger actua como si fuera un proxy entre la aplicación y la CPU, lo que nos permite parar la ejecución del flujo en el momento que queramos para inspeccionar el contenido de los registros al igual que el proceso del espacio de memoria

Para ejecutar el software vulnerable, abrimos immunity debugger y en el apartado de archivo, procedemos a abrir el software que queramos auditar. En la prueba realizada antes de abrir el software, ponemos en argumentos 12 A ya que como hemos visto en el código anterior este software necesita unos valores de entre 2 a 64 para funcionar correctamente.

Immunity debugger está dividido en cuatro pantallas, en la que cada una nos representa una información totalmente diferente.

La primera pantalla nos enseña las instrucciones que realiza la aplicación, la instrucción resaltada en azul, es la siguiente instrucción que va a ser ejecutada y la localización en la memoria del proceso is presentada en la columna izquierda

La segunda pantalla contiene todos los registros incluyendo los dos registros más interesantes: ESP y EIP. Ya que por definición EIP apunta hacia el siguiente código de instrucción que va a ser ejecutado, se establece en la dirección de la instrucción resaltada en la ventana de ensamblaje.

La tercera pantalla nos muestra los contenidos de la memoria de cualquier dirección, podemos ver 3 columnas: dirección de memoria, volcado hexadecimal y texto en formato plano. Esta ventana puede ser útil cuando buscamos o analizamos valores específicos en el espacio de memoria del proceso y nos puede enseñar información en diferentes formatos si clicamos con el botón del ratón derecho en la ventana

La cuarta pantalla nos presenta la pila y su contenido, en este caso vemos cuatro columnas: la dirección de memoria, la información en hexadecimal que residen en esa dirección, la representación en texto plano de la información y comentarios dinámicos que proveen mayor información. La información presentada en decimal que encontramos en la segunda columna esta presentada en un formato de 32 bits qye se llama DWORD, presentada en cuatro bites hexadecimales. Resaltamos que en este ejemplo el primer valor que vemos está resaltado en azul en la pantalla, el cual es el mismo que el valor del ESP de la segunda pantalla

![image](https://user-images.githubusercontent.com/122020487/210770782-3f67c19e-335f-4646-b08b-ff3fe7ae0305.png)

Navegando a través del código: 

Podemos ejecutar las siguiente instrucciones en la pestaña de debug, con las opciones step into o step over:

Step into -> Sigue el flujo de ejecución en un allamada a una función determinada
Step over -> Ejecuta la función completa y volvera de ella

Si el principio de las ejecuciones que vemos que se está haciendo en el programa no coincide con nuestro objetivo, procederemos a buscar la función que deseamos, para ello haremos click derecho en la primera ventana, seleccionaremos search for -> all referenced text strings y buscaremos la función de string copy, en nuestro caso con el texto: error - you must supply at least one argument, en el cual haremos dos veces click.

También podemos ver la función strcopy cuando se inicializa en debbuger, en el cual vemos que hace un salto con MV hacia C70424, en el cual nos da una idea que es a esa llamada de función en la que nos debemos situar:

![image](https://user-images.githubusercontent.com/122020487/210770806-fad300e6-e327-4c7a-87cd-9a347dc073da.png)

Una vez que estamos en la función que queremos, tendremos que poner un breakpoint en la función en la que estemos interesados, en nuestro caso strcopy:

![image](https://user-images.githubusercontent.com/122020487/210770830-ce81d247-0b61-4a9b-ba6a-fd870f4f36b3.png)

Para hacerlo, seleccionamos la línea y presinamos F2, una vez hecho, se seleccionará la línea y se resaltará en azul. Acto seguido seguimos la ejecución presionando F9.
Inmediatamente después de presinar F9, la ejecución del programa se pausará en el Breackpoint que hemos seleccionado, podemos ver que el EIP está en la misma dirección de memoria, ya que apunta a la siguiente instrucción que debe ser ejecutada. En la tercera ventana, podemos ver las A's que hemos puesto en la ejecución del programa, indicandonos así que estamos en la memoria correcta y también nos indica el destino de memoria donde las A's van a ser enviadas.

![image](https://user-images.githubusercontent.com/122020487/210770859-13220d4a-cc36-45e8-b9bf-a0e2020e6d43.png)

Procedemos a seguir con la ejecución de la función presionando F7 dos veces, para situarnos dentro de la función de strcopy, una vez situados dentro, hacemos doble click en la dirección de destino la cual es 0065FE70,
esto lo hacemos ya que no nos importa donde o como se copie nuestros strings, nos importa la parte a donde se envia:

![image](https://user-images.githubusercontent.com/122020487/210770898-c1c99741-29e2-4df2-bfed-e7ffa7687370.png)

Una vez analizado como funciona, podemos proceder a la ejecución del programa presionando Ctrl + F9. Depués nos dirigimos a la primera ventana, y seleccionamos RETN F7,  que es la que nos va a llevar otra vez a la función principal, ya que una vez copiado el string, el software vuelve hacia la función principal.

La siguiente instrucción mov EAX,0 es equivalente a return 0, el cual le dice al sistema operativo que finalice la ejecución del programa ya que ha terminado. 

![image](https://user-images.githubusercontent.com/122020487/210770913-d82e38ed-5c86-4589-b3f4-388a66f40710.png)

Por lo que, como hemos podido observar se ha realizado la ejecución del programa correctamente sin ningún problema, esto es debido a que hemos insertado un tamaño permitido de Bytes como entrada, por lo que el software no ha tenido problema alguno en ejecutar sus funciones y terminar el proceso exitosamente.

Overflowing the buffer:

En el ejemplo de arriba hemos puesto un tamaño correcto en la ejecución del programa, pero en este caso procederemos a ejecutar el programa superando ese tamaño máximo. Procedemos a abrir inmunity debugger nuevamente y seleccionamos el archivo, tenemos que recordad que inmunity debugger recuerda los break points de sesiones anteriores, por lo que ya tenemos el break point en la zona de memoria en la que lo hemos dejado anteriormente. Presionamos F9 para correr el programa hasta que se encuentre con el breakpoint, una vez hayamos dado con el breakpoint, pulsamos F7 para dirigirnos hacia strcopy, nos posicionamos nuevamente en la ventana 3 en la dirección de destino y pulsamos ctrl + F9, con lo que podemos ver lo siguiente:

![image](https://user-images.githubusercontent.com/122020487/210770940-ebf40005-b18f-470d-a7f2-7c609c0ded5f.png)

Si continuamos con la ejecución del programa con F7, vamos a ver que se ejecutará la función RETN, la llevará la función a ejecutar del copiado de las A's hacia el EIP, el cual es el encargado de direccionar la siguientes direcciones de memoria a ejecutar, en este caso como hemos superado el límite de tamaño de la capacidad máxima de memoria, el EIP se encontrará que tiene que ejecutar un hilo de A's, las cuales tienen la dirección 41 41 41 41, ya que es la representación en hexadecimal de nuestro strings de A's, por lo que al intentar llevar a cabo la intrucción, verá que no es una instrucción válida y el programa colapsará.  

Es importante recordar que el EIP es utilizado por el CPU para directamente ejecutar comandos a nivel ensamblador. 
