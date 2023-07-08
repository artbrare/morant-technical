# Morant Consultores - Evaluación Inicial


---

> Resuelto por: *Arturo Bravo Reynaga*


```python
import math
import bisect
import time
```

# Problema 4


Encuentra el error y modifica el siguiente código para encontrar los números primos correctos que se encuentren entre dos números enteros.



```
find_primes <- function(start, end) {
  primes <- c()
  
  for (i in start:end) {
    if (i < 2) {
      next
    }
    if (i == 2) {
      primes <- c(primes, i)  
      next
    }
    is_prime <- FALSE
    for (j in 2:ceiling(sqrt(i))) {
      if (j == 2 || j %% 2 != 0) {
        if (i %% j == 0) {
          is_prime <- TRUE
          break
        }
      }
    }
    if (is_prime) {
      primes <- c(primes, i)
    }
  }
  
  return(primes)
}
```


## Respuesta

Lo que necesitamos hacer primero es entender el código, por lo que escribiremos la función, tal cual está, en Python



```python
def find_primes(start, end):

  primes = []

  # En python, el segundo argumento no es inclusivo
  for i in range(start, end + 1):

    # Se considera que el 1 no es primo.
    if i < 2:
      continue

    if i == 2: # (1)
      primes.append(i)
      continue

    is_prime = False # (2)

    # Para que i sea primo, i no tiene que tener divisores mayores que 1.
    # No es necesario revisar si todos los números [2, n-1] son divisores,
    # Basta revisar desde [2, ceil(sqrt(n))] ya que si n = a*b (no seria
    # primo), y consideremos que a < b, eso implica que a*a < a*b, que es
    # equivalente a que a*a < n o que a < sqrt(n).
    for j in range(2, math.ceil(math.sqrt(i)) + 1): # (3)
      # Notamos que el único lugar donde cambiaremos el flag "is_prime" es
      # dentro de este bloque. Notamos que para entrar al primer "if"
      # el número j (que será el divisor) tiene que ser 2 o impar, lo cual
      # indica el primer problema
      if j == 2 or j % 2 != 0: # (4)
        # En este momento j es el número 2 o es un número impar
        if i % j == 0:
          # si j divide a i entonces se marca la bandera "is_prime" como true,
          # vemos que j no es 1, y j divide a i, por definición no es primo.
          is_prime = True
          break

    if is_prime:
      primes.append(i)

  return primes

```


```python
# Probamos el código para encontrar los primos de los primeros 20 números y
# confirmamos que el código no funciona adecuadamente.
print(find_primes(1, 20))
```

    [2, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]



Pasos a seguir:

1.   Podemos eliminar el código marcado con "1" ya que podemos encontrar que 2 es primo con la solución propuesta.
2.   Podemos quitar la bandera "is_prime", ya que con la solución propuesta utilizaremos una función auxiliar "is_prime(), la cual envolverá el código para saber si el número i es primo."
3.   Esto no es necesario, sin embargo, hace que el código sea más claro. Podemeos cambiar el "for" por un "while" y la condición será while j * j <= i, que es equivalente pero nos evita trabajar con redondeos.
4.   Este bloque se tiene que modificar por completo, diremos que si j divide a i, i no es primo, por lo que saldremos del primer for sin agregar el número i a la lista de primos.




```python
# Para claridad del código
def is_prime(i):

  if i < 2: return False

  j = 2
  while j * j <= i:
    if i % j == 0: # j es divisor del número
      return False
    j += 1
  return True


def corrected_find_primes(start, end):

  primes = []

  for i in range(start, end + 1):
    if is_prime(i): primes.append(i)

  return primes

```


```python
# Probamos la función corregida con los primeros 20 números
print(corrected_find_primes(1, 20))
```

    [2, 3, 5, 7, 11, 13, 17, 19]


## Extra: Una solución para casos especificos

Existe otro método más rápido para encontrar los primeros n primos. Como nuestro problema considera un rango (start, end). Este método funcionará cuando start se considere pequeño o cuando la diferencia entre start y end se considere grande.


Utilizaremos la [criba de Erastótenes](https://es.wikipedia.org/wiki/Criba_de_Erat%C3%B3stenes), la cual es un algoritmo que nos permite encontrar todos los primos menores a n. En este caso encontraremos todos los primos menores o iguales a n.



```python
def find_primes_erathostenes(start, end):
  if end <= 1: return 0

  primes = [True] * (end + 1)
  primes[0], primes[1] = False, False

  j = 2
  while j * j <= end:
    if primes[j]:
      for k in range(j * j, end + 1, j):
        primes[k] = False
    j += 1

  # Solo nos quedamos con los números primos
  primes = [i for i, is_prime in enumerate(primes) if is_prime]

  # Usamos el método de bisección para ubicar nuestro nuevo start
  new_start = bisect.bisect_left(primes, start)
  return primes[new_start:]
```


```python
print(find_primes_erathostenes(1, 20))
```

    [2, 3, 5, 7, 11, 13, 17, 19]



```python
# Contamos el tiempo que se tarda find_primes vs find_primes_erathostenes
start = time.time()
original = corrected_find_primes(1, 10**6)
end = time.time()

find_primes_time = end - start

start_e = time.time()
erathostenes = find_primes_erathostenes(1, 10**6)
end_e = time.time()

find_primes_erathostenes_time = end_e - start_e

print(f'find_primes() time: {find_primes_time} s')
print(f'find_primes_erathostenes() time: {find_primes_erathostenes_time} s')
print(f'¿Las soluciones son iguales?: {original == erathostenes}')

print(len(original))
print(len(erathostenes))
```

    find_primes() time: 4.12822699546814 s
    find_primes_erathostenes() time: 0.06702494621276855 s
    ¿Las soluciones son iguales?: True
    78498
    78498

