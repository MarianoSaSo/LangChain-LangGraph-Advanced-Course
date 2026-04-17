# Resolución de Caso Práctico: Sistema de Procesamiento de Reuniones con LangGraph y OpenAI

Vamos allá con la resolución de la tarea que os planteaba en la clase anterior, donde os pedía que pusieseis en práctica todo lo que habíamos aprendido sobre el Landgraf hasta el momento en un proyecto ya medianamente realista en el que incorporábamos también algoritmos de inteligencia artificial.

En este caso lo que teníamos que hacer es desarrollar una aplicación sencillita que se encargase de coger un vídeo de una reunión o una transcripción, es decir, el texto de la reunión y convertirlo en un formato estructurado del que extraíamos participantes. También extraíamos los temas que se habían hablado en la reunión, extraíamos las acciones, un resumen, etcétera, etcétera.

Bueno, pues vamos a comenzar. Yo ya tengo por aquí el código desarrollado para ahorrar un poco de tiempo y vamos a empezar por las importaciones, que como podéis observar son muy sencillas. Esta, por cierto, no es la única manera de resolver este caso práctico. Es posible que alguno de vosotros lo haya resuelto de una manera un poco distinta. Sin embargo, lo que es la estructura principal debería de ser muy similar.

## 1. Importaciones y Configuración Inicial

Bien, yo lo que he hecho ha sido importar de Landgraf tanto el State Graph como el comienzo y final, para después poder establecer el orden de los nodos del hanchen. OpenAI ha importado chats OpenAI para hacer ciertas peticiones a los modelos de OpenAI y después tengo por aquí typeddict. En este caso, para poder establecer el estado de acuerdo que por aquí lo tendríamos y List para poder establecer ciertos atributos de mi estado, como una lista dentro de Python y no únicamente como un valor más estático, como una cadena de texto o un número entero.

Tengo por aquí un módulo para leer la ruta donde se encuentre el vídeo de la reunión y después yo pues he decidido crear una pequeña interfaz gráfica con Tkinter, que es un módulo que viene por defecto en Python para poder seleccionar el archivo que posteriormente vamos a procesar.

Y también ha importado la librería OpenAI para llamar a su modelo Whisper, que es su modelo de transcripción de un vídeo a texto. Tenemos también ciertas alternativas incluidas dentro del landgraf, como por ejemplo Assembly. Sin embargo, pues considero que ya que tenemos la clave API y hemos cargado presupuesto dentro de nuestra cuenta de OpenAI. Quizá lo más sencillo sea hacerlo directamente con el módulo externo de OpenAI.

> 💡 **Nota:** También veremos más adelante en el curso que existen ciertos modelos de código abierto que podríamos descargar dentro de nuestro equipo, como por ejemplo Whisper, que pertenece también a OpenAI, y podríamos usar algunas clases dentro de Lang Chain para procesar un vídeo y obtener su transcripción, Pero como eso requiere la instalación de más módulos y demás, pues por el momento vamos a continuar con OpenAI.

Bien, la configuración es muy sencilla. Fijaros que utilizo OpenAI Instancio este modelo GPT cuatro mini y le pongo una temperatura quizá un poco más alta de cero para que tenga un poco de flexibilidad para que no sea tan determinista a la hora de generar todo lo que le voy a pedir a continuación.

## 2. Definición del Estado del Grafo

Bien, lo siguiente es definir el Estado. Ya lo sabemos más que de sobra. Nuestro estado lo he denominado state hereda como siempre de type dict y aquí veis los atributos del estado que van a poder modificar los diferentes nodos después del grafo. Y tenemos por un lado lo que son las notas de la reunión, que será pues la transcripción de la reunión o en el caso de que le proporcione un vídeo, tendré primero que transcribirlo y después ya asignar dentro de las notas, pues esa transcripción tendré los participantes que fijaros. Qué interesante. En lugar de utilizar una cadena de texto, lo que le digo es que los participantes se corresponde con una lista. Vale, esto es una lista de Python sin más.

Tendría los temas que se han tratado en la reunión, que de nuevo es una lista las acciones que hay que realizar, que también es una lista, lo que es el acta de la reunión, que esto es lo que son los Minutes y tenemos un resumen muy cortito para terminar.

## 3. Definición de Nodos de Extracción

Bien, pues una vez definido el estado, lo siguiente ya es empezar a definir los nodos de nuestro workflow, de nuestro grafo. Y aquí he creado varios nodos:

### Extracción de Participantes
El primero de extracción de participantes. Ya sabéis que esto es simplemente una nomenclatura para indicarle que recibe este argumento. Vale este parámetro. Cuando yo defino la función que es state, que es del tipo state, es decir, de esta clase que he definido por aquí y devuelve también un tipo state no devuelve exactamente un tipo state porque devuelve un diccionario, pero después lo que va a hacer Landgraf va a ser coger esto. Y como ya sabéis, más que de sobra lo va a incorporar en el estado final. Vale lo que estamos devolviendo.

Bien, pues nada, muy sencillito. Definimos por aquí un prompt de las siguientes notas de reunión. Extrae solo los nombres de los participantes. Notas del estado global. Leo las notas. Responde únicamente con una lista de nombres separados por comas y después uso el LLM Invoke, que ya conocemos más que de sobra, proporcionando directamente el prompt. Aquí tendría los participantes en la respuesta.

Fijaros cómo los proceso es tan sencillo como coger la respuesta. Accedo al contenido divido entre comas de acuerdo y me quedo después con cada uno de los elementos. Recordad que aquí podríamos usar, por ejemplo, clases de Pydantic modelos de pydantic para asegurarnos de que la respuesta de este LLM coincida exactamente con el formato que nosotros esperamos. Sin embargo, por simplificar, pues yo no lo he hecho.

Bueno, por aquí tendríamos ya sacando por pantalla que hemos extraído todos los participantes y devuelvo como veis los participantes que acabo de extraer. Simplemente ese atributo dentro del estado general y Landgraf ya se encargará de unirlo al estado global.

### Extracción de Temas y Acciones
Bien, pues poco más tendríamos por aquí otro nodo. Identificar topics, en este caso Temas Identifica los temas principales discutidos. Un prompt nuevamente identifica los tres o cinco temas principales. Le paso la transcripción de la reunión. Responde solo con los temas separados. Perfecto, esto es lo mismo, el LM punto Invoke. De nuevo obtengo el resultado, lo proceso. Me quedo con los temas y lo devuelvo con este atributo topics.

Y lo mismo hecho para extraer las acciones que lo tenemos aquí también generado lo que es el acta de la reunión.

### Generación del Acta (Minuta)
Bueno, el acta quizá es un poquito más compleja, tampoco mucho más. Lo único que he hecho ha sido leer del Estado los participantes de acuerdo, he leído del Estado los temas que se han extraído y he leído del Estado, las acciones. Entonces lo voy guardando por aquí. Una vez procesado y después se lo proporciono de nuevo al LLM para que me devuelva ya un acta final.

Entonces fijaros, genera una minuta formal y profesional basándote en la siguiente información Participantes, temas discutidos y acciones acordadas. Notas originales las tienes por aquí. Al final las notas es básicamente el acta de la reunión y genera una minuta profesional de máximo 150 palabras. Entonces se lo mando al LLM, obtengo la minuta y lo guardo en el estado global.

### Verificación del Resumen
Y ya por último tendríamos el resumen, que de nuevo pues es muy similar. Vale por aquí el prompt. Lo que he hecho ha sido incluir, por ejemplo, los participantes, he incluido también los temas, he incluido las acciones y al final le pido un resumen conciso.

## 4. Construcción y Compilación del Grafo

Bien, pues una vez que nosotros hemos definido los nodos, lo siguiente que tenemos que hacer es construir el grafo. En este caso lo que he hecho ha sido crear una función que crea automáticamente todo el workflow y lo que he hecho ha sido instanciar por aquí nuestro grafo con State Graph. Muy sencillito, proporcionándole por supuesto la clase que hemos definido como estado general y he agregado todos los nodos con add node.

Aquí veis Agrego extract participants, agrego el identificar temas, agrego identificar las acciones, la generación del acta y la generación del resumen. Muy sencillo y configuro el flujo secuencial cual le digo que es el nodo de comienzo? Pues extraer participantes por aquí lo tenemos de extraer participantes Se va a conectar con identificar temas de identificar temas. Se conecta con extraer las acciones de extraer las acciones, se conecta con generar el acta y de generar el acta se conecta con generar el resumen que se corresponde con el último nodo.

Bueno, un grafo muy sencillo que realmente también podríamos haber replicado con lenguaje LC, el de Lung Chain. Porque si os fijáis, la salida de un nodo es la entrada del siguiente y en este caso es un flujo secuencial. Sin embargo, en la siguiente clase pues ya comenzaremos a ver flujos que tienen ciertos cambios, ciertas rutas nuevas, ciertas estructuras de control de flujo que ya hacen que este workflow no sea lineal.

Bueno, por último, lo que devuelvo ya es el grafo compilado. Fijaros workflow, compile perfecto.

## 5. Funciones Auxiliares (Transcripción con Whisper)

Y aquí tengo algunas funciones auxiliares de procesamiento que ya sabéis que a veces se requieren y a veces tenemos que salirnos un poco del ecosistema de Launching y Landgraf. En este caso la función principal es la de transcribir lo que sería el vídeo de la reunión. Entonces lo que estoy haciendo es, como os indico por aquí, utilizar directamente la API de OpenAI es muy sencillo, saco por pantalla transcribiendo con OpenAI. Fijaros Instancio un objeto de la clase OpenAI. Muy sencillo. Ya sabéis que la clave API la tenemos en el entorno y aquí lo que hago es que abro como veis el fichero de audio o en nuestro caso, un fichero de vídeo. Entonces es tan sencillo como a partir de este cliente que instanciado le digo audio transcription create.

Es decir, quiero crear una transcripción utilizando este modelo que es Whisper uno, que ya os digo que también podemos ejecutarlo en local y lo haremos. Le proporciono el fichero de audio, le digo que está en español. Le paso también un prompt para mejorar un poco la transcripción. Le digo esta es una reunión de trabajo en español con múltiples participantes y le digo que me devuelva esa transcripción en formato texto. Tan sencillo como esto. Y ya al finalizar le digo transcripción completada y devuelvo la transcripción.

Bien, aquí lo que tengo también es una función auxiliar que procesa, pues lo que es el acta de la reunión. Fijaros, procesa una reunión individual, es decir, aquí ya estamos invocando nuestro grafo, nuestro workflow, proporcionándole la transcripción de una reunión. Fijaros que recibe como argumento lo que son, lo que es la transcripción, que yo lo he denominado Notes y que se corresponde con una cadena de texto y recibe lo que es la aplicación que en definitiva se va a corresponder, pues con nuestro workflow, con nuestro grafo compilado.

Entonces, como siempre, lo primero que tengo que hacer es definir mi estado inicial, donde le digo que el único atributo que va a tener un valor son las notas, es decir, la transcripción de la reunión. Ahí lo veis como lo asigno, que es al final el argumento que se le proporcionará participantes, topics y tal, pues listas vacías y cadenas de texto vacías. Y aquí lo único que le digo es procesando nota de reunión. Lo saco por pantalla e invoco como veis mi workflow y que le proporciona mi workflow? Pues el estado inicial. Tan sencillo como esto.

Y aquí ya la última función auxiliar simplemente se encarga de mostrarnos por pantalla. Los resultados son diferentes prints que nos van a mostrar el resultado de la reunión, los participantes, los temas tratados, las acciones acordadas, el acta de la reunión y el resumen ejecutivo. Muy sencillo, es para mostrarlo y que lo veamos en la terminal.

## 6. Demostración y Ejecución Interfaz

Y ya invocamos nuestro programa. Lo único que hacemos por aquí es. Primero creamos el workflow. Vale. Invocando la función create Workflow que hemos visto previamente. Aquí he creado una pequeña interfaz gráfica para seleccionar un archivo, ya sea la propia transcripción de la reunión o las notas, o ya sea el propio vídeo de la reunión. Entonces ya veis con Tkinter.

Lo único que le digo es con Filedialog. Pues ábreme un archivo o más bien un cuadro de diálogo a partir del cual yo pueda seleccionar un archivo. Este es el título. Selecciona un vídeo o transcripción. Y estos son los formatos de archivo. Vale, las extensiones que quiero soportar, que son vídeos y texto. Bueno, si no se ha seleccionado el archivo, pues simplemente que cierre la aplicación con un error.

Y aquí lo que estoy haciendo es dividir lo que es la ruta del archivo. De acuerdo, lo divido, por eso utilizo Os.path punto Split text y me quedo con el segundo elemento que debería de ser la extensión. Vale? Bien, pues nada, compruebo si la extensión se encuentra dentro de las extensiones para vídeos que serían estas MP4, MOV, m4a, MP3, etcétera En el caso de que sea así, entonces invoco la función que se encarga de transcribir ese audio o vídeo y le proporciono la ruta al fichero este.

Lo que hace. Perdonad que me he dejado por aquí una nota. Esto lo que hace es directamente invocar por aquí arriba nuestra función para utilizar Whisper de OpenAI, vale? Y realizar la transcripción y nos devolverá esa transcripción en formato texto. 

Y en el caso de que no se encuentre dentro de estas extensiones, quiere decir que ya es un archivo de texto. Así que lo único que hago es leerlo. Vale, fijaros con este encoding UTF ocho. Si hay algún error lo ignoro y una vez que he leído esa transcripción o la he calculado previamente con Whisper ya lo que hago es que proceso como veis con Process Meeting Notes esa transcripción que le paso por aquí junto con mi workflow que lo he obtenido aquí arriba que hará ya el punto. Invoke le proporcionará ese estado inicial que yo había definido por aquí. Vale invocar a nuestro workflow con el estado inicial donde tendrá por aquí la transcripción de la reunión. Y tan sencillo como esto, se ejecutará todo nuestro grafo nos devolverá el resultado.

Y ya con Display Results, que es la función que previamente os había mostrado para bueno pues representar resultados en terminal. Obtendré pues una representación gráfica más o menos en la terminal de esa reunión.

## Conclusión y Resultados

Bien, pues vamos a ver qué tal funciona. Vamos a ejecutar nuestro programa y si todo va correctamente, debería de abrirse ese cuadro de diálogo. Aquí lo tenemos. Selecciono la reunión simulación de la reunión y ahí lo tenemos, transcribiendo con OpenAI Whisper API directa.

Bien, vamos a esperar que puede tardar unos segunditos o incluso algunos minutos en transcribirse. Por aquí lo tenemos. Fijaros que ya ha terminado de transcribirse. Me dice que son un total de 9411 caracteres, que no está nada mal y ahora ya está empezando a procesar. Como podemos observar por aquí arriba, pues toda la nota, toda la transcripción de la reunión y ha ido pues ejecutando nodo por nodo.

Fijaros que chulada! Participantes extraídos cinco personas Temas identificados cinco Temas Acciones extraídas ocho Minuta generada 144 palabras y resumen creado resultados.

Esto es una pasada, la verdad. O sea, podéis visualizar la reunión la tendréis adjunta en los recursos de la clase, pero es una chulada como una reunión de más de diez minutos. Hemos hecho la transcripción y aquí tenemos los resultados participantes Sergio Contreras, Ezequiel Pineda, Nayeli, Vanda, Luz Crisanto y Flor Rosales.

Temas tratados. Cambios en la empresa. Estrategias de producción. Propuestas de marketing. Innovaciones en la cadena de suministros. Mejoras en las ventas.
Acciones acordadas. Ezequiel Pinedo convocará Bla bla, bla. Bueno. Todas las acciones. La minuta que podría ser el acta para enviar por correo electrónico y el resumen ejecutivo.

Bueno, muy interesante la verdad. Más adelante veremos también cómo poder conectar esto con herramientas externas como Gmail para poder crear un borrador o enviar esto por correo electrónico. Pero aquí tenemos cómo utilizando Landgraf. Ha sido bastante sencillo poder crear este workflow que lo que hace es procesar una reunión y devolvernos pues diferentes cosas, como por ejemplo su acta.

Bien, pues ahora que hemos visto ya un ejemplo muy sencillito de Landgraf, en la práctica lo que vamos a hacer a continuación es continuar profundizando y realmente ver dónde está el verdadero potencial de Landgraf, porque esto que hemos visto es una ejecución secuencial que probablemente podríamos haber imitado también con Lacchain. Así que sin más, vámonos con la siguiente clase.
