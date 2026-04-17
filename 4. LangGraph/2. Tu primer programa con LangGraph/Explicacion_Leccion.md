# Tu primer programa con LangGraph

Comenzamos con nuestro primer programa con Landgraf.

Y antes de empezar es importante que entendamos los componentes fundamentales de este framework, que esencialmente son tres. El Estado, los nodos y las aristas. De hecho, en la clase anterior os he dejado un artículo donde se explican un poquito en detalle estos componentes, así que si no lo habéis leído, os recomiendo que paséis este vídeo y os vayáis a ese artículo antes de continuar con el desarrollo de este caso práctico.

En esencia, el Estado va a ser la información compartida a lo largo de todo el grafo y que de hecho, cada uno de los nodos va a ir actualizando. Luego tendremos los nodos que son la unidad básica de trabajo dentro del Landgraf y que se corresponden con funciones en Python o con Runnables. Es algo prácticamente idéntico a lo que teníamos por aquí en una cadena tradicional de LAMP Chain. Y por último, vamos a tener las aristas que son las conexiones dirigidas entre los diferentes nodos y que van a determinar el flujo de ejecución.

Así que con estos tres componentes lo que nosotros tenemos que hacer es constituir lo que se llama un grafo de Estado.

## Arquitectura de un Programa en LangGraph

Y cuál suele ser el esquema o la arquitectura de un programa desarrollado con Landgraf? Bueno, pues suele corresponderse con los siguientes pasos:

1. Primero, definir el estado, que suele ser un objeto de la clase Typeddict.
2. Después vamos a tener que crear un grafo de estado, un objeto perteneciente a esta clase que es statecraft.
3. Después vamos a definir la funcionalidad de los nodos, ya sean funciones en Python o importar diferentes runnables.
4. Añadimos los nodos al statecraft.
5. Conectaremos los nodos mediante esos ejes dirigidos y luego marcaremos el punto de entrada al grafo. Cuál es el nodo de inicio, el punto de salida, cuál es el nodo final y también cómo se interconectan los nodos entre ellos.
6. Y por último, lo que hacemos es compilar el grafo para ejecutarlo.

Entonces, estos pasos que acabo de mencionar suelen ser, por decirlo así, la arquitectura esencial de un programa desarrollado con Landgraf. 

Así que sin más, vamos a comenzar por un programa muy sencillito que ni siquiera va a utilizar inteligencia artificial, sino que va a implementar un workflow que va a procesar un texto en dos pasos. Primero va a convertir el texto a mayúsculas y después va a contar cuántos caracteres tiene ese texto.

Bien, pues vamos allá. Lo primero de todo, vamos a crearnos un nuevo directorio por aquí. Vamos a pulsar y vamos a crear un nuevo directorio que vamos a llamar Tema cuatro y que voy a sacar de ahí estaría de la carpeta Tema tres, Aquí lo tengo, vale. Tema cuatro y aquí vamos a guardar todos los ficheros. Así que el nuevo fichero y vamos a llamarlo primer programa barra baja Landgraf punto P.

## 1. Definición del Estado

Bueno, pues como os decía, uno de los componentes esenciales del Landgraf es el Estado y por lo tanto tenemos que definirlo y normalmente lo vamos a definir a través de un objeto de la clase Type dict, por si alguien se lo pregunta. Typeddict no es un componente, una estructura propia de Launching. Es una estructura propia de Python, pero se utiliza en combinación con Landgraf y en este caso lo que crea es un diccionario, pero cuyos valores y claves pueden tener un tipo específico. Entonces importamos type dict y luego vamos a importar. Y esto sí que es importante from landgraf.

Y fijaros, aquí nos encontramos con el primer problema y es que no tenemos landgraf instalado en nuestro entorno porque va a ser un paquete separado. Así que como ya estamos más que acostumbrados, nos abrimos una terminal. Importante aseguraros de estar en vuestro entorno virtual y vamos a poner pip install landgraf. Esto lo que va a hacer va a ser instalar esta librería. Ahí lo veis? Ya está recopilando todos los paquetes de la librería y muy rápidamente lo instala y podemos empezar a trabajar con él. Así que sin más, cerramos. Y ahora ya sí, si yo pongo por aquí From Landgraf. Ahí está. Estupendo. Vamos a ponerle Graff. Vamos a importar lo que son sus clases principales, que son la primera, el State Graph para crear ese grafo de estado. Y luego las directivas que nos van a permitir marcar cuál es el nodo de entrada con Start y cuál es el nodo de salida con END.

Bien, pues una vez hecho esto, vamos con el primer paso de la definición de la arquitectura de una aplicación con Landgraf, que es definir el esquema del Estado. El estado global que se va a compartir entre los nodos. Entonces, como ya sabemos, más que de sobra se define a partir de esa clase typeddict. Yo en mi caso lo voy a llamar Estado, que es como se suele llamar. Por convención heredamos de la clase Typeddict. Como estáis viendo, y aquí yo lo que hago es que establezco cuáles son las variables que va a tener el Estado, los datos que se van a ir compartiendo entre los nodos. 

En mi caso van a ser dos. Un texto original que fijaros le puedo indicar que es un tipo de cadena de texto, un string y vamos a decirle que un texto en mayúsculas que va a ser también un string. Y por último, también va a tener un valor adicional, que es la longitud que se va a corresponder con un número entero. 

Entonces, ya veis, es como definir un diccionario en Python, pero cuyas claves y valores tienen un tipo específico. Tan sencillo como esto. Yo he definido la estructura del estado general de mi grafo. Esto es lo que se va a ir compartiendo entre los nodos que podrán ir modificando el estado, es decir, los valores que tienen asignados. Pues estos atributos texto original, texto Mayús y longitud.

## 2. Creación del StateGraph

Bueno, pues el segundo paso dentro de la arquitectura es, por supuesto, crear el grafo de estado y cómo lo creamos? Vamos a definir por aquí una variable que va a ser Graph y a continuación, con State Graph simplemente creo el grafo de estado y le proporciono. Fijaros que interesante mi estado actual, que es simplemente una referencia a esta clase state que yo he definido previamente, Lo que estoy indicándole es el estado que se va a compartir entre los nodos de este grafo. Es este de aquí viene definido por esta estructura que yo te he indicado previamente.

## 3. Definición de las Funciones de los Nodos

Bueno, pues cuál sería el tercer paso? Pues muy sencillo lo que hemos dicho, definir las funciones de los nodos que pueden ser runabouts que yo esté importando por aquí arriba, que ya hemos visto muchos dentro del engine o pueden ser funciones personalizadas de Python. 

En este caso, para simplificar vamos a crear dos funciones personalizadas, por ejemplo poner en mayúsculas que va a recibir el estado. Fijaros qué chulada y lo que va a devolver es primero del estado. Vamos a coger el texto original, fijaros del estado en texto original, todo el acceso y demás. Es como si fuese un diccionario y este estado como yo he creado el State Graph, a partir de esta clase ya landgraf por detrás, se va a preocupar de proporcionar a cada uno de los nodos cuando convierta esto en un nodo. Esta variable estado, entonces veis que se lo ponemos como parámetro en este caso, luego se lo proporcionará como argumento y aquí yo puedo acceder a los valores. Entonces le digo Mira, el texto original se encontrará dentro de texto original del estado y lo que tú vas a hacer, vamos a retornarlo por aquí va a ser retornar un diccionario en el que el texto mayusc. Esta es la clave. Se va a corresponder con el texto original que has extraído previamente en mayúsculas.

Bueno, una de las cosas muy interesantes y que también os mencionaba en el artículo de la clase anterior, es que estos nodos no necesitan necesariamente actualizar todos los componentes del estado, sino que pueden actualizar un componente concreto, como por ejemplo en este caso este atributo texto Mayús, que lo estoy actualizando añadiendo este texto que he leído de texto original y poniéndolo en mayúsculas y yo lo devuelvo como un diccionario y ya se encarga landgraf por detrás de recoger este valor. Comprobarlo con nuestra variable estado, ver que efectivamente nuestra variable estado se encuentra texto Mayús. Como estamos viendo que es un tipo String. Hacer la conversión de los datos y guardarlo para que el siguiente nodo ya pueda acceder a este valor. Vale.

Entonces, qué más funciones vamos a definir? Vamos a definir otra, por ejemplo contar caracteres. Perfecto. Y va a recibir de nuevo el Estado. Y qué es lo que va a hacer? Pues bueno, del Estado vamos a leer. Fijaros del State, el texto en mayúsculas, en este caso por cambiar un poco y vamos a retornar la longitud y vamos a decirle que va a ser la longitud de este texto que yo he extraído, es decir, en la siguiente función, que luego ahora las tendremos que ordenar y añadir al grafo. Veis que lo que hago es de nuevo recibo el Estado y del Estado. Estoy obteniendo lo que haya guardado dentro del texto Mayús y lo que estoy haciendo es pues es retornar un diccionario donde actualizo este atributo longitud con este valor de aquí que es la longitud del texto que he leído previamente.

## 4. Añadir los Nodos al Grafo

Bueno, pues una vez que yo he definido las funciones que voy a utilizar como nodos o he importado los runnables necesarios. El paso cuatro consiste en añadir los nodos al grafo. Y esto de nuevo, es un paso muy sencillito. Es tan sencillo como coger nuestro grafo que fijaros que lo he añadido anteriormente y le digo que quiero añadir un nodo. Qué nodo? Pues por un lado voy a añadir con el nombre mayus. Yo le puedo poner aquí el nombre que quiera, es un nombre que va a identificar a ese nodo dentro del grafo y le paso la referencia a mi función que sería poner mayúsculas. Y por otro lado Graph Node. Vamos a añadir otro nodo que este por ejemplo lo puedo llamar pues contar o como yo quiera y le paso contar caracteres. Entonces veis como estoy añadiendo las dos funciones como nodos separados dentro de mi grafo? El grafo que he creado previamente.

## 5. Conectar los Nodos

Bueno, pues cuál sería el paso cinco? Pues conectar los nodos en secuencia y para ello tengo que hacer uso de estas directivas. Tengo que indicarle cuál es el orden de conexión entre los nodos, cuál es el nodo de inicio, cuál es el nodo de final, etcétera. Cómo hacemos esto? Bueno, pues muy sencillo, por aquí ponemos graph. Punto. Y qué es lo que añado? Qué es lo que determina el orden? Qué es lo que determina el flujo de información? Lo determinan los ejes, las aristas.

Entonces, lo que tengo que añadir aquí es un eje, como estáis viendo. Y qué le digo? Pues mira, esto va a ser el nodo de comienzo. Veis que digo que empieza por el start? La directiva de comienzo es el nodo de inicio y el primer nodo va a ser Mayus. Es decir, lo primero que vas a hacer es pasar este estado a la primera función que has definido, que es poner en mayúsculas. 

Después en mi grafo vamos a añadir otro eje dirigido. Vamos a decirle que de Mayús lo que tiene que hacer es pasar al siguiente nodo que voy a decirle que es contar. Entonces aquí lo que estoy especificando es Mira, después de que ejecutes este nodo Mayús, ejecutas el nodo contar. Aquí ya la salida de un nodo no es la entrada del siguiente, sino que estos nodos acceden al estado global, con lo cual este nodo, por ejemplo, podría no modificar el estado global y el siguiente nodo podría estar utilizando información que modificó este. De aquí, que es uno de los anteriores, no es el inmediatamente anterior.

Y ya por último le digo que el nodo de final. Fijaros, añado otro eje indicándole que contar es precisamente el nodo de final de mi grafo. Y aquí tengo establecido, como veis conectados todos los nodos e indicada la dirección, en este caso el flujo de información de mi workflow.

## 6. Compilar el Grafo

El paso seis, por supuesto, es siempre compilar el grafo una vez que lo tenemos definido. Y esto es tan sencillo como decir que el grafo compilado Compile Graph va a ser igual a Graph. Punto compile. Vale, ya está. Grafo compilado. Esto quiere decir que ya se ha guardado toda esta configuración que nosotros hemos puesto por aquí arriba.

## 7. Invocar el Grafo

Y qué es lo que nos quedaría? Pues invocar el grafo, por supuesto, invocar el grafo con un estado Inicial. Esto es importante, A veces tendrá estado inicial, otras veces no, en este caso obviamente tiene un estado inicial que al menos una de estas. Uno de estos atributos tenemos que añadir lo que es el texto original. Ese es el estado inicial con el que parte nuestro grafo. 

Entonces el estado inicial vamos a definirlo por aquí barra baja inicial en una variable y va a ser pues un diccionario al uso, por ejemplo texto original y vamos a poner por aquí Hola mundo! Vale, este es nuestro primer Hola mundo en Landgraf. 

Entonces, cuál es el resultado de nuestro grafo? Pues muy sencillo, resultado va a ser igual a Compiled Graph. Vale, con toda la configuración utilizamos la interfaz que ya conocemos más que de sobra, que es Invoke para ejecutar nuestro grafo. Y qué le pasó? Pues el estado inicial. Fijaros que todo lo gestiono mediante diccionarios, es decir, nuestro Runnable. Sí, también nuestros nodos devuelven diccionarios. Todo se gestiona este estado mediante diccionarios y no necesariamente devolviendo todos los atributos, sino simplemente aquellos que queremos modificar. Entonces devuelvo el estado inicial.

Y por último, vamos a ver cuál es el resultado de la ejecución que se guardará en esta variable. Resultado. Bien, pues guardamos y vamos a ejecutar nuestro primer programa Hola mundo en Landgraf y fijaros qué chulada! Este es el resultado que es el estado realmente. Fijaros que lo que nos devuelve el grafo compilado es el estado diciéndonos texto original. Hola Mundo, Texto en mayúsculas, Hola Mundo en mayúsculas y longitud diez.

Después de que haya pasado por todos estos nodos que veíamos por aquí atrás, haya ejecutado las funciones o runnables que hayamos especificado y por supuesto nos haya devuelto pues el estado final. Con lo cual aquí podemos observar en un ejemplo muy sencillito los componentes fundamentales, que son pues el propio grafo, que son el Estado, que son los nodos y que son las aristas dirigidas que nos permiten interconectar estos nodos.

Bien, pues ahora que entendemos cómo implementar programas con Landgraf, vamos allá a ver cosas más avanzadas.
