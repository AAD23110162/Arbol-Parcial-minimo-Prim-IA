# Arbol-Parcial-minimo-Prim-IA
**Autor:** Alejandro Aguirre Díaz.  
**Descripción:** Este repositorio contiene un simulador Árbol Parcial mínimo de Prim programado en Python.  
**Última modificación:** Martes 11 de noviembre del 2025. 

## ¿Qué es?
El Árbol Parcial mínimo (APM) es un subconjunto de aristas de un grafo conectado que conecta todos los vértices con el menor peso total posible. El algoritmo de Prim construye un APM creciendo un árbol desde un vértice inicial y, en cada paso, añade la arista de menor peso que conecta el árbol actual con un vértice fuera de él. Implementaciones eficientes usan una cola de prioridad (heap).

Complejidad típica:
- Con heap (lista de adyacencia): $O(E \log V)$
- Implementación ingenua (matriz de adyacencia): $O(V^2)$

## ¿Para qué sirve?
- Diseño de redes (telecomunicaciones, distribución eléctrica, tuberías) minimizando coste de conexión.
- Subrutinas en clustering y algoritmos aproximados (por ejemplo, heurísticas para TSP).
- Reducción de coste en infraestructura física y virtual (cableado, rutas de mínimo coste).

## ¿Cómo se implementa en el mundo?
- Representación: lista de adyacencia o lista de aristas con pesos.
- Estructuras: cola de prioridad (heap), conjuntos de vértices visitados / no visitados.
- Librerías comunes: en Python, NetworkX para prototipos; en producción, implementaciones en C++/Go/Java para rendimiento.
- Formatos de entrada: lista de aristas (u, v, w) o matriz de adyacencia; salida: lista de aristas que forman el APM y coste total.
- Validación: pruebas sobre grafos aleatorios y casos límite (grafo conectado/desconectado, pesos negativos si aplican).

## ¿Cómo lo implementarías en tu vida?
- Planificación de rutas para conectar varios puntos (por ejemplo, puntos de interés en una propiedad) con el menor coste de instalación.
- Optimización de conexiones domésticas o de oficina para minimizar uso de material (cable, tubería).
- Aprendizaje y visualización: usar el simulador para entender greediness y demostrar por qué Prim garantiza mínimo local/global.

## ¿Cómo lo implementarías en tu trabajo o tu trabajo de ensueño?
- Integrarlo en herramientas de diseño de redes para generar topologías de coste mínimo y comparar con otras métricas (latencia, redundancia).
- Automatizar pruebas de escalabilidad usando grafos sintéticos y medir tiempo/uso de memoria; elegir estructuras de datos óptimas según tamaño/densidad del grafo.
- Extender el simulador para soportar restricciones prácticas (capacidad de aristas, costos fijos, requisitos de redundancia) y generar propuestas de ingeniería.

## Notas técnicas y contrato mínimo
- Entrada esperada: grafo conectado; si no está conectado, el algoritmo produce un bosque (APM por componente).
- API sugerida (ejemplo conceptual):
  - `prim(graph, start_vertex) -> (edges_in_mst, total_weight)`
  - `graph` en formato de lista de adyacencia o lista de aristas.
- Tests mínimos:
  - Grafo simple de 4 vértices con pesos conocidos.
  - Grafos densos y dispersos para comparar tiempos.
  - Caso no conectado: comprobar detección y manejo (error o forest result).
- Documentar complejidad y dependencias; incluir ejemplos de uso y visualizaciones para facilitar comprensión.
