```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

sns.set(style="darkgrid")
```

# Morant Consultores - Evaluación Inicial


---

> Resuelto por: *Arturo Bravo Reynaga*

# Problema 3


Utilice la base de datos data/municipios_rezago.csv. Contiene una lista de municipios también ficticia que tiene las siguientes variables: población, población de 15 años o más analfabeta, población de 6 a 14 años que no asiste a la escuela, población sin derechohabiencia a servicios de salud y viviendas con piso de tierra. Todas estas son variables que expresan un tipo de rezago. Imagine que su cliente es el Gobierno Federal y quiere hacer un programa social que atienda el rezago, en general. Le pide elaborar un ranking con el propósito de saber a qué municipios dar mayor prioridad. Agregue una variable a la base de datos que exprese el orden de prioridad en donde 1 es el municipio más rezagado y nrow(bd) es el municipio menos rezagado. Para ello debe utilizar un criterio de rezago, justifica qué criterio utilizarías. Puedes utilizar combinaciones lineales de las variables o técnicas de reducción de dimensionalidad como análisis de componentes principales.

Nos inspiraremos en el [artículo escrito por Gustavo Santos](https://towardsdatascience.com/creating-scores-and-rankings-with-pca-c2c3081fdb26), donde genera un ranking en R utilizando análisis de componentes principales.


```python
url = 'https://raw.githubusercontent.com/morant-consultores/evaluacion_inicial/main/data/municipios_rezago.csv'
df3 = pd.read_csv(url)
```


```python
df3.head()
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
      <th>Municipio</th>
      <th>pob_total</th>
      <th>15_analfabeta</th>
      <th>6_14_sinescuela</th>
      <th>poblacion_sinsalud</th>
      <th>viv_pisotierra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Berriozábal</td>
      <td>863893</td>
      <td>1.427718</td>
      <td>4.490033</td>
      <td>17.918423</td>
      <td>0.446572</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mapastepec</td>
      <td>41</td>
      <td>6.451613</td>
      <td>0.000000</td>
      <td>14.634146</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Altamirano</td>
      <td>1169</td>
      <td>7.076566</td>
      <td>7.960199</td>
      <td>14.884517</td>
      <td>1.067616</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tonalá</td>
      <td>41</td>
      <td>10.344828</td>
      <td>14.285714</td>
      <td>75.609756</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Jiquipilas</td>
      <td>1054</td>
      <td>6.420765</td>
      <td>9.844560</td>
      <td>14.041746</td>
      <td>1.181102</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Ordenar los datos de mayor a menor y eliminar el primer registro
df3_sorted_pob = df3.sort_values(by='pob_total', ascending=False).iloc[1:]

plt.figure(figsize=(12, 6))
sns.barplot(x='Municipio', y='pob_total', data=df3_sorted_pob)

# Rotar las etiquetas del eje x para mayor legibilidad
plt.xticks(rotation=90)

plt.xlabel('Municipio')
plt.ylabel('Población Total')
plt.title('Población Total por Municipio')

plt.show()
```


    
![png](pregunta_3_files/pregunta_3_6_0.png)
    



```python
count_less_1000 = (df3_sorted_pob['pob_total'] < 1000).sum()
print(f"Municios con una población menor a 1000 habitantes: {count_less_1000} de un total de {df3.shape[0]}")
```

    Municios con una población menor a 1000 habitantes: 35 de un total de 50



```python
# Obtenemos los 5 municipios con los mayores valores en cada variable
# de rezago
top_analfabeta = df3.nlargest(5, '15_analfabeta')
top_sinescuela = df3.nlargest(5, '6_14_sinescuela')
top_sinsalud = df3.nlargest(5, 'poblacion_sinsalud')
top_pisotierra = df3.nlargest(5, 'viv_pisotierra')

# Configurar subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Top 5 Municipios por Variable de Rezago', fontsize=16)

# Gráfico 1: 15_analfabeta
sns.barplot(ax=axes[0, 0], x='Municipio',
            y='15_analfabeta', data=top_analfabeta)
axes[0, 0].set_title('Población de 15 años o más analfabeta')
axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(),
                           rotation=45, fontsize=8)
axes[0, 0].set_ylabel('%')

# Gráfico 2: 6_14_sinescuela
sns.barplot(ax=axes[0, 1], x='Municipio',
            y='6_14_sinescuela', data=top_sinescuela)
axes[0, 1].set_title('Población de 6 a 14 años que no asiste a la escuela')
axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(),
                           rotation=45, fontsize=8)
axes[0, 1].set_ylabel('%')

# Gráfico 3: poblacion_sinsalud
sns.barplot(ax=axes[1, 0], x='Municipio',
            y='poblacion_sinsalud', data=top_sinsalud)
axes[1, 0].set_title('Población sin derechohabiencia a servicios de salud ')
axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(),
                           rotation=45, fontsize=8)
axes[1, 0].set_ylabel('%')

# Gráfico 4: viv_pisotierra
sns.barplot(ax=axes[1, 1], x='Municipio',
            y='viv_pisotierra', data=top_pisotierra)
axes[1, 1].set_title('Viviendas con piso de tierra')
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(),
                           rotation=45, fontsize=8)
axes[1, 1].set_ylabel('%')

# Ajustar espaciado entre subplots
plt.tight_layout()

plt.show()
```


    
![png](pregunta_3_files/pregunta_3_8_0.png)
    


### Test de Bartlett

[El test de Bartlett ](https://www.tutorialspoint.com/how-to-perform-bartlett-s-test-in-python)se utiliza en este caso para evaluar si las correlaciones entre las variables "15_analfabeta", "6_14_sinescuela", "poblacion_sinsalud" y "viv_pisotierra" son estadísticamente diferentes de cero. El objetivo es determinar si las variables tenían varianzas significativamente diferentes entre sí.



```python
test_statistic, p_value = stats.bartlett(
    df3["15_analfabeta"],
     df3["6_14_sinescuela"],
     df3["poblacion_sinsalud"],
     df3["viv_pisotierra"])

print("Estadístico de prueba:", test_statistic)
print("p-value:", p_value)

if p_value > 0.05:
   print("Las varianzas no son significativamente diferentes.")
else:
   print("Las varianzas son significativamente diferentes.")
```

    Estadístico de prueba: 113.98768650019072
    p-value: 1.5206123129455142e-24
    Las varianzas son significativamente diferentes.


En este caso, el valor p obtenido del test de Bartlett fue de 1.5206123129455142e-24, lo que indica que es extremadamente pequeño. Dado que el valor p es menor que 0.05, rechazamos la hipótesis nula (Ho) de que las correlaciones son estadísticamente iguales a cero. Por lo tanto, podemos concluir que las varianzas entre las variables son significativamente diferentes.

Este resultado sugiere que las variables seleccionadas tienen diferentes niveles de variabilidad y, por lo tanto, aportan información única al análisis. Esto respalda la decisión de utilizar estas variables en el análisis de componentes principales (PCA).

### Matriz de correlaciones

La realización de la matriz de correlaciones tiene como objetivo principal analizar las relaciones lineales entre las variables.


```python
variables = ['pob_total','15_analfabeta', '6_14_sinescuela','poblacion_sinsalud', 'viv_pisotierra']
data_selected = df3[variables]
correlation_matrix = data_selected.corr()

sns.set(font_scale=1.2)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True)
plt.title('Matriz de Correlaciones')
plt.show()
```


    
![png](pregunta_3_files/pregunta_3_12_0.png)
    


Se observa que no hay una correlación fuerte entre variables.

### PCA

Hacemos el análisis de componentes principales como una [técnica para generar un ranking](https://www.journalijar.com/uploads/864_IJAR-17816.pdf) y observamos que se acumula el 85% de la varianza en los primeros 4 componentes.


```python
# Normalizar los datos antes de aplicar PCA
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_selected)

# Aplicar PCA
pca = PCA()
components = pca.fit_transform(data_scaled)

# Eigenvalores de cada componente principal
eigenvalues = pca.explained_variance_

# Porcentaje de varianza explicada por cada componente principal
explained_variance_ratio = pca.explained_variance_ratio_

# Varianza acumulada
cumulative_variance = explained_variance_ratio.cumsum()

summary_data = {
    'Componente': [f'Componente {i+1}' for i in range(len(eigenvalues))],
    'Eigenvalor': eigenvalues,
    'Varianza Explicada': explained_variance_ratio,
    'Varianza Acumulada': cumulative_variance
}

summary_df = pd.DataFrame(summary_data)
print(summary_df)
```

         Componente  Eigenvalor  Varianza Explicada  Varianza Acumulada
    0  Componente 1    1.392172            0.272866            0.272866
    1  Componente 2    1.094629            0.214547            0.487413
    2  Componente 3    1.051924            0.206177            0.693590
    3  Componente 4    0.848819            0.166369            0.859959
    4  Componente 5    0.714497            0.140041            1.000000


En PCA, los [loadings](https://scentellegher.github.io/machine-learning/2020/01/27/pca-loadings-sklearn.html) representan el aporte de las variables originales a cada componente principal. Cada componente principal es una combinación lineal de las variables originales, y los loadings indican la magnitud y la dirección de la contribución de cada variable a ese componente.


```python
# Obtener los loadings de cada variable por cada componente principal
loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'Component_{i+1}'for i in range(pca.n_components_)],
    index=variables)

print('Loadings:')
print(loadings)
```

    Loadings:
                        Component_1  Component_2  Component_3  Component_4  \
    pob_total             -0.283628    -0.619814    -0.424134     0.576622   
    15_analfabeta          0.639370     0.134909     0.107502     0.366710   
    6_14_sinescuela       -0.217418    -0.105976     0.848829     0.444068   
    poblacion_sinsalud     0.645029    -0.191673    -0.101127     0.220657   
    viv_pisotierra        -0.217780     0.741391    -0.278955     0.535858   
    
                        Component_5  
    pob_total             -0.151667  
    15_analfabeta         -0.653431  
    6_14_sinescuela        0.154243  
    poblacion_sinsalud     0.698773  
    viv_pisotierra         0.194810  


Los loadings al cuadrado representan la varianza explicada por cada variable en cada componente principal. Además notemos que loadings(PC1) al cuadrado es muy parecido a loadings(PC5) al cuadrado lo que da más fuerza a nuestra decisión de seleccionar las primeras 4 componentes principales.


```python
loadings_squared = loadings ** 2
print(loadings_squared)
```

                        Component_1  Component_2  Component_3  Component_4  \
    pob_total              0.080445     0.384169     0.179889     0.332493   
    15_analfabeta          0.408795     0.018201     0.011557     0.134476   
    6_14_sinescuela        0.047270     0.011231     0.720511     0.197196   
    poblacion_sinsalud     0.416062     0.036739     0.010227     0.048689   
    viv_pisotierra         0.047428     0.549660     0.077816     0.287144   
    
                        Component_5  
    pob_total              0.023003  
    15_analfabeta          0.426972  
    6_14_sinescuela        0.023791  
    poblacion_sinsalud     0.488283  
    viv_pisotierra         0.037951  



```python
# Obtenemos los loadings al cuadrado de los primeros 4 componentes principales
loadings_squared_selected = loadings_squared.iloc[:, :4]

# Realizamos la transformación lineal de data_scaled
transformed_data = np.matmul(data_scaled, loadings_squared_selected.values)

df3["score"] = np.sum(transformed_data, axis=1)

# Generamos el ranking acorde al score calculado
df3["ranking"] = df3["score"].rank(ascending=False)
df3 = df3.sort_values(by="ranking")

df3.head(50)
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
      <th>Municipio</th>
      <th>pob_total</th>
      <th>15_analfabeta</th>
      <th>6_14_sinescuela</th>
      <th>poblacion_sinsalud</th>
      <th>viv_pisotierra</th>
      <th>score</th>
      <th>ranking</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Berriozábal</td>
      <td>863893</td>
      <td>1.427718</td>
      <td>4.490033</td>
      <td>17.918423</td>
      <td>0.446572</td>
      <td>5.651045</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Ocozocoautla de Espinosa</td>
      <td>11</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>9.090909</td>
      <td>33.333333</td>
      <td>3.889606</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>36</th>
      <td>Palenque</td>
      <td>14</td>
      <td>0.000000</td>
      <td>50.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>3.045693</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tonalá</td>
      <td>41</td>
      <td>10.344828</td>
      <td>14.285714</td>
      <td>75.609756</td>
      <td>0.000000</td>
      <td>3.020849</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Las Margaritas</td>
      <td>37</td>
      <td>13.636364</td>
      <td>0.000000</td>
      <td>24.324324</td>
      <td>11.111111</td>
      <td>2.315897</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>41</th>
      <td>La Independencia</td>
      <td>264</td>
      <td>6.565657</td>
      <td>18.918919</td>
      <td>45.075758</td>
      <td>1.449275</td>
      <td>2.236302</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Salto de Agua</td>
      <td>157</td>
      <td>5.172414</td>
      <td>20.689655</td>
      <td>13.375796</td>
      <td>4.878049</td>
      <td>1.832740</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Las Rosas</td>
      <td>411</td>
      <td>6.081081</td>
      <td>21.333333</td>
      <td>15.085158</td>
      <td>2.941176</td>
      <td>1.740545</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th>47</th>
      <td>Tumbalá</td>
      <td>3362</td>
      <td>5.538187</td>
      <td>13.273002</td>
      <td>26.710291</td>
      <td>6.159895</td>
      <td>1.737966</td>
      <td>9.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Comitán de Domínguez</td>
      <td>468</td>
      <td>2.601156</td>
      <td>14.864865</td>
      <td>21.581197</td>
      <td>4.918033</td>
      <td>1.030239</td>
      <td>10.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Ocotepec</td>
      <td>419</td>
      <td>10.000000</td>
      <td>5.128205</td>
      <td>30.787589</td>
      <td>2.970297</td>
      <td>1.001669</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Mazatán</td>
      <td>354</td>
      <td>10.775862</td>
      <td>7.246377</td>
      <td>28.813559</td>
      <td>1.219512</td>
      <td>0.971426</td>
      <td>12.0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Chilón</td>
      <td>27</td>
      <td>5.555556</td>
      <td>0.000000</td>
      <td>85.185185</td>
      <td>0.000000</td>
      <td>0.921278</td>
      <td>13.0</td>
    </tr>
    <tr>
      <th>48</th>
      <td>Villa Comaltitlán</td>
      <td>174</td>
      <td>4.273504</td>
      <td>2.857143</td>
      <td>26.436782</td>
      <td>9.090909</td>
      <td>0.853229</td>
      <td>14.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Amatenango de la Frontera</td>
      <td>997</td>
      <td>8.771930</td>
      <td>4.242424</td>
      <td>32.096289</td>
      <td>3.174603</td>
      <td>0.791336</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>La Concordia</td>
      <td>192</td>
      <td>6.521739</td>
      <td>12.121212</td>
      <td>15.625000</td>
      <td>2.127660</td>
      <td>0.603000</td>
      <td>16.0</td>
    </tr>
    <tr>
      <th>39</th>
      <td>Tila</td>
      <td>4476</td>
      <td>5.888126</td>
      <td>5.354919</td>
      <td>19.504021</td>
      <td>4.221106</td>
      <td>0.278538</td>
      <td>17.0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Catazajá</td>
      <td>144</td>
      <td>13.684211</td>
      <td>0.000000</td>
      <td>22.916667</td>
      <td>0.000000</td>
      <td>0.163458</td>
      <td>18.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Tuxtla Gutiérrez</td>
      <td>1172</td>
      <td>3.385732</td>
      <td>6.763285</td>
      <td>33.959044</td>
      <td>2.215190</td>
      <td>0.112251</td>
      <td>19.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Jiquipilas</td>
      <td>1054</td>
      <td>6.420765</td>
      <td>9.844560</td>
      <td>14.041746</td>
      <td>1.181102</td>
      <td>0.097878</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Altamirano</td>
      <td>1169</td>
      <td>7.076566</td>
      <td>7.960199</td>
      <td>14.884517</td>
      <td>1.067616</td>
      <td>-0.009998</td>
      <td>21.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Villaflores</td>
      <td>55</td>
      <td>5.714286</td>
      <td>0.000000</td>
      <td>16.363636</td>
      <td>6.666667</td>
      <td>-0.043313</td>
      <td>22.0</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Tecpatán</td>
      <td>291</td>
      <td>8.648649</td>
      <td>3.389831</td>
      <td>16.838488</td>
      <td>1.388889</td>
      <td>-0.173347</td>
      <td>23.0</td>
    </tr>
    <tr>
      <th>34</th>
      <td>La Grandeza</td>
      <td>281</td>
      <td>10.552764</td>
      <td>0.000000</td>
      <td>27.402135</td>
      <td>0.000000</td>
      <td>-0.183201</td>
      <td>24.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Chicomuselo</td>
      <td>575</td>
      <td>5.432099</td>
      <td>2.912621</td>
      <td>36.869565</td>
      <td>0.806452</td>
      <td>-0.188257</td>
      <td>25.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Pichucalco</td>
      <td>322</td>
      <td>7.692308</td>
      <td>6.250000</td>
      <td>17.080745</td>
      <td>0.000000</td>
      <td>-0.248956</td>
      <td>26.0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Tuxtla Chico</td>
      <td>14</td>
      <td>12.500000</td>
      <td>0.000000</td>
      <td>14.285714</td>
      <td>0.000000</td>
      <td>-0.308044</td>
      <td>27.0</td>
    </tr>
    <tr>
      <th>46</th>
      <td>Chamula</td>
      <td>1377</td>
      <td>3.336704</td>
      <td>7.623318</td>
      <td>24.836601</td>
      <td>0.264550</td>
      <td>-0.464748</td>
      <td>28.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Ocosingo</td>
      <td>1225</td>
      <td>3.841932</td>
      <td>6.467662</td>
      <td>20.979592</td>
      <td>0.586510</td>
      <td>-0.585447</td>
      <td>29.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Motozintla</td>
      <td>318</td>
      <td>5.607477</td>
      <td>1.515152</td>
      <td>22.012579</td>
      <td>1.351351</td>
      <td>-0.708574</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>La Libertad</td>
      <td>27</td>
      <td>4.347826</td>
      <td>0.000000</td>
      <td>40.740741</td>
      <td>0.000000</td>
      <td>-0.728281</td>
      <td>31.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Tapachula</td>
      <td>493</td>
      <td>3.951368</td>
      <td>5.000000</td>
      <td>19.066937</td>
      <td>0.877193</td>
      <td>-0.751720</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>40</th>
      <td>Unión Juárez</td>
      <td>262</td>
      <td>4.225352</td>
      <td>0.000000</td>
      <td>36.641221</td>
      <td>0.000000</td>
      <td>-0.880286</td>
      <td>33.0</td>
    </tr>
    <tr>
      <th>49</th>
      <td>Aguascalientes</td>
      <td>2616</td>
      <td>2.874859</td>
      <td>3.490760</td>
      <td>16.743119</td>
      <td>2.030457</td>
      <td>-0.936519</td>
      <td>34.0</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Cintalapa</td>
      <td>1897</td>
      <td>3.615385</td>
      <td>3.216374</td>
      <td>22.720084</td>
      <td>0.421053</td>
      <td>-0.967238</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Ostuacán</td>
      <td>2805</td>
      <td>3.746098</td>
      <td>4.301075</td>
      <td>15.222816</td>
      <td>0.152672</td>
      <td>-1.110582</td>
      <td>36.0</td>
    </tr>
    <tr>
      <th>45</th>
      <td>Sabanilla</td>
      <td>1638</td>
      <td>1.944210</td>
      <td>5.395683</td>
      <td>12.454212</td>
      <td>0.941176</td>
      <td>-1.218692</td>
      <td>37.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mapastepec</td>
      <td>41</td>
      <td>6.451613</td>
      <td>0.000000</td>
      <td>14.634146</td>
      <td>0.000000</td>
      <td>-1.252441</td>
      <td>38.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Villa Corzo</td>
      <td>256</td>
      <td>5.945946</td>
      <td>4.000000</td>
      <td>2.734375</td>
      <td>0.000000</td>
      <td>-1.257306</td>
      <td>39.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Oxchuc</td>
      <td>11</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>45.454545</td>
      <td>0.000000</td>
      <td>-1.260953</td>
      <td>40.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Ixtacomitán</td>
      <td>468</td>
      <td>2.424242</td>
      <td>1.250000</td>
      <td>23.290598</td>
      <td>0.862069</td>
      <td>-1.292451</td>
      <td>41.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Pijijiapan</td>
      <td>536</td>
      <td>3.485255</td>
      <td>0.900901</td>
      <td>15.111940</td>
      <td>1.470588</td>
      <td>-1.317283</td>
      <td>42.0</td>
    </tr>
    <tr>
      <th>42</th>
      <td>Pantelhó</td>
      <td>1753</td>
      <td>2.023346</td>
      <td>3.942652</td>
      <td>13.291500</td>
      <td>0.216920</td>
      <td>-1.484121</td>
      <td>43.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Chiapa de Corzo</td>
      <td>1081</td>
      <td>2.550336</td>
      <td>1.546392</td>
      <td>20.536540</td>
      <td>0.000000</td>
      <td>-1.487649</td>
      <td>44.0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Frontera Comalapa</td>
      <td>3822</td>
      <td>1.560232</td>
      <td>2.900763</td>
      <td>14.965986</td>
      <td>0.108814</td>
      <td>-1.627041</td>
      <td>45.0</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Venustiano Carranza</td>
      <td>25</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>28.000000</td>
      <td>0.000000</td>
      <td>-1.833694</td>
      <td>46.0</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Arriaga</td>
      <td>96</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>20.833333</td>
      <td>0.000000</td>
      <td>-2.068329</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>43</th>
      <td>Simojovel</td>
      <td>28</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>10.714286</td>
      <td>0.000000</td>
      <td>-2.400983</td>
      <td>48.0</td>
    </tr>
    <tr>
      <th>44</th>
      <td>La Trinitaria</td>
      <td>17</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>-2.752713</td>
      <td>49.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>San Fernando</td>
      <td>9</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>-2.752778</td>
      <td>50.0</td>
    </tr>
  </tbody>
</table>
</div>




## Observaciones
*   Dado el ranking observado podemos notar que el municipio Berriozábal, aun con no tener los porcentajes más altos de rezago, queda en primer lugar, esto tiene sentido considerando que su población es mucho mayor que cualquier otro municipio. Esto se debe a que en números absolutos, Berriozábal es el municipio con mayor rezago.
*   Notamos además que, de manera correcta, el modelo considera en los últimos lugares a los municipios que no tienen variables de rezago y los acomoda por población.


