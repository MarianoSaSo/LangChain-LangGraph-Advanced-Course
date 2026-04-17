# Tema 2: Fundamentos y Componentes Core
## Lección 4: Procesamiento por Lotes (Batch)

En la clase anterior vimos cómo procesar de manera paralela múltiples pasos dentro de una misma cadena utilizando `RunnableParallel`. Pero, ¿cómo procesamos múltiples reseñas de manera eficiente?

La opción más instintiva podría ser iterar sobre nuestra lista de reseñas empleando un bucle `for` e invocar la cadena con `chain.invoke()` en cada iteración, es decir, de manera *secuencial*.

Si bien esta alternativa es funcional, **resulta ineficiente** si la cantidad de reseñas comienza a crecer considerablemente.

### El método `.batch()`

Para resolver esto, los `Runnables` (y por tanto, nuestras cadenas compiladas con LCEL) nos proveen un método muy poderoso llamado `.batch()`. Este método está diseñado para ejecutar la cadena sobre un conjunto de datos (una lista) de manera paralela.

#### Ventajas de utilizar `.batch()`

1. **Eficiencia Computacional:** `.batch()` procesa múltiples elementos simultáneamente, sacando provecho a los recursos computacionales de nuestra máquina. Podrás notar que LangChain tarda prácticamente lo mismo en procesar 3 reseñas de manera simultánea que en procesar solo 1.
2. **Optimización de la API:** Hace un mejor uso por debajo de las interfaces que nos provee LangChain.
3. **Tolerancia a Fallos:** Si el procesamiento de un único elemento falla (por un texto malformado, etc.), LangChain gestiona los errores por nosotros permitiendo que la cadena siga procesando los demás elementos sin detener abruptamente el programa.
4. **Simplicidad en el Código:** Nos evita tener que implementar lógicas complejas de bucles o manejo de hilos (Threads) por nuestra cuenta. El código se vuelve muchísimo más limpio.

### Ejemplo de Uso

En lugar de hacer esto:
```python
resultados = []
for review in reviews_batch:
    resultados.append(chain.invoke(review))
```

Simplemente hacemos esto:
```python
resultados_batch = chain.batch(reviews_batch)
```

¡Y listo! Al final obtenemos una lista de resultados donde cada elemento se corresponde con la reseña de entrada, procesada de principio a fin, incluyendo las ramas en paralelo (`RunnableParallel`).

### Conclusión sobre los Runnables
Con esta práctica terminamos de ahondar en el componente núcleo de las abstracciones de LangChain: **Los Runnables y el LangChain Expression Language (LCEL)**. A partir de ahora utilizaremos este conocimiento para sacar el máximo partido al resto de los componentes funcionales (Memory, Prompts, Agents, etc.).
