```python
import pyreadr
import pandas as pd
import numpy as np
from scipy import stats
```

# Morant Consultores - Evaluación Inicial


---

> Resuelto por: *Arturo Bravo Reynaga*

# Problema 2

Descargue la base de datos data/encuesta_f.rda que contiene información de una encuesta ficticia. Esta encuesta tiene un diseño muestral polietápico que incluye etapas de estratos y etapas de conglomerados. La base de datos tiene un identificador de la persona, el partido por el que votaría y el peso correspondiente a cada entrevistado para la estimación.

Presente una estimación puntual de la proporción de personas a favor de cada partido.

¿De qué tamaño es la población sujeta a análisis?

Ahora suponga que la muestra fue extraída bajo un esquema de muestreo aleatorio simple, presente los intervalos de confianza para la estimación de la proporción de personas a favor de cada partido.

¿Qué podría concluir de estos intervalos?


```python
result = pyreadr.read_r('encuesta_f.rda')
df = result[None]

df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 400 entries, 0 to 399
    Data columns (total 3 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   id           400 non-null    int32  
     1   preferencia  400 non-null    object 
     2   peso         400 non-null    float64
    dtypes: float64(1), int32(1), object(1)
    memory usage: 7.9+ KB



```python
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>preferencia</th>
      <th>peso</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6731</td>
      <td>Partido 2</td>
      <td>6.793545</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2161</td>
      <td>Partido 2</td>
      <td>4.912335</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8019</td>
      <td>Partido 2</td>
      <td>39.257424</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9037</td>
      <td>Partido 2</td>
      <td>24.277547</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1099</td>
      <td>Partido 2</td>
      <td>10.351223</td>
    </tr>
    <tr>
      <th>5</th>
      <td>4244</td>
      <td>Partido 2</td>
      <td>33.473788</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1137</td>
      <td>Partido 1</td>
      <td>49.636285</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1758</td>
      <td>ns/nc</td>
      <td>11.090651</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2667</td>
      <td>Partido 2</td>
      <td>15.342555</td>
    </tr>
    <tr>
      <th>9</th>
      <td>6802</td>
      <td>Partido 2</td>
      <td>45.594544</td>
    </tr>
  </tbody>
</table>
</div>



Al explorar los datos, notamos un valor extraño "ns/nc", por lo que vemos cuales son los valores que la columna "preferencia" puede tomar.


```python
valores_preferencia = df['preferencia'].unique()
print(valores_preferencia)
```

    ['Partido 2' 'Partido 1' 'ns/nc' 'Partido 3']


Notamos que el único valor extraño es "ns/nc", suponemos que su significado es: personas que no están seguras o que no votarán por algún partido de los presentados en la encuesta, por lo que haremos el análisis considerando sólamente las personas que votarán por alguno de los tres partidos.


```python
# Filtrar las observaciones con partido válido (excluir "ns/nc")
df = df[df['preferencia'] != 'ns/nc']
print(df.shape[0])
```

    371


Observamos que 371 personas de 400 votarán por algún partido. El siguiente paso es obtener la estimación utilizando la ponderación de los pesos de cada persona, dada por el tipo de muestra en este ejemplo.


```python
total_ponderado = df['peso'].sum()

df.loc[:,'proporcion_ponderada'] = df['peso'] / total_ponderado

estimacion_puntual = df.groupby('preferencia')['proporcion_ponderada'].sum()
print(estimacion_puntual)
```

    preferencia
    Partido 1    0.433518
    Partido 2    0.474768
    Partido 3    0.091714
    Name: proporcion_ponderada, dtype: float64


    /var/folders/zp/c20v8419619gb_1d1q5vxk700000gn/T/ipykernel_62530/1026127889.py:3: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df.loc[:,'proporcion_ponderada'] = df['peso'] / total_ponderado


Observamos que el partido 2 tiene una ligera ventaja sobre el partido 1 utilizando este método.


Ahora, considerando un muestreo aleatorio simple, consideramos la muestra homogenea, por lo que los pesos no son necesarios. El siguiente paso es obtener [los estimadores de proporción y los intervalos de confianza](https://virtual.uptc.edu.co/ova/estadistica/docs/libros/estadistica1/cap01d.html) correspondientes.


```python

partidos_unicos = df['preferencia'].unique()
partidos_unicos.sort()
resultados = []

total_votos = df.shape[0]  # Número total de votos

for partido in partidos_unicos:
    votos_partido = df[df['preferencia'] == partido]['id']
    n = votos_partido.shape[0]
    proporcion = n / total_votos
    std_error = np.sqrt(proporcion * (1 - proporcion) / total_votos)
    intervalo_confianza = stats.norm.interval(0.95, loc=proporcion, scale=std_error)

    resultado = {
        'Partido': partido,
        'Estimador puntual': proporcion,
        'Intervalo de confianza (95%)': intervalo_confianza
    }
    resultados.append(resultado)

# Creamos un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados)

print(df_resultados)
```

         Partido  Estimador puntual                Intervalo de confianza (95%)
    0  Partido 1           0.444744   (0.39417744529417786, 0.4953104253257682)
    1  Partido 2           0.471698   (0.42090155504989785, 0.5224946713651966)
    2  Partido 3           0.083558  (0.05539958013465698, 0.11171632283030258)



```python
with pd.ExcelWriter('data.xlsx') as writer:
    df.to_excel(writer, sheet_name='data', index=False)
    estimacion_puntual.to_excel(writer, sheet_name='con_ponderacion', index=True)
    df_resultados.to_excel(writer, sheet_name='intervalos_confianza', index=False)
```

Podemos concluir lo siguiente:

1.   Partido 1: El estimador puntual de proporción de votos para el Partido 1 es del 44.47%. El intervalo de confianza del 95% indica que, con un 95% de confianza, la proporción de votos para el Partido 1 se encuentra entre el 39.42% y el 49.53%.
2.   Partido 2: El estimador puntual de proporción de votos para el Partido 2 es del 47.17%. El intervalo de confianza del 95% indica que, con un 95% de confianza, la proporción de votos para el Partido 2 se encuentra entre el 42.09% y el 52.25%.
3.   Partido 3: El estimador puntual de proporción de votos para el Partido 3 es del 8.36%. El intervalo de confianza del 95% indica que, con un 95% de confianza, la proporción de votos para el Partido 3 se encuentra entre el 5.54% y el 11.17%.






