import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

class Graficos:
    def __init__(self, carpetaResultados=None):
        if carpetaResultados is None:
            self.carpetaResultados = Path(__file__).resolve().parent.parent.parent / "results"
        else:
            self.carpetaResultados = Path(carpetaResultados)
        self.carpetaResultados.mkdir(parents=True, exist_ok=True)

    # --- Gráfico 1: Top 10 artículos por grado de entrada ---
    def grafTopGradoEntrada(self, grafo, cantidad=10):
        nodos = grafo.topPorGradoEntrada(cantidad)
        nombres = [n.nombre if n.nombre else str(n.id) for n in nodos]
        valores = [n.gradoEntrada() for n in nodos]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(nombres[::-1], valores[::-1], color="steelblue")
        ax.set_xlabel("Grado de Entrada")
        ax.set_title(f"Top {cantidad} Artículos por Grado de Entrada")
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        ruta = self.carpetaResultados / "top_grado_entrada.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    # --- Gráfico 2: Distribución de grados (escala log) ---
    def grafDistribucionGrados(self, grafo, tipo="entrada"):
        distri = grafo.analizarDistribucionGrados(tipo)
        if isinstance(distri, str):
            print(distri)
            return None

        grados = list(distri.keys())
        cantidades = list(distri.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(grados, cantidades, s=10, color="steelblue", alpha=0.7)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Grado")
        ax.set_ylabel("Cantidad de Artículos")
        ax.set_title(f"Distribución de Grados de {'Entrada' if tipo == 'entrada' else 'Salida'} (escala log-log)")
        plt.tight_layout()

        ruta = self.carpetaResultados / f"distribucion_grados_{tipo}.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    # --- Gráfico 3: Top 10 artículos por PageRank ---
    def grafTopPageRank(self, grafo, puntajes, cantidad=10):
        ranking = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)[:cantidad]

        nombres = []
        valores = []
        for id_nodo, score in ranking:
            nodo = grafo.articulos.get(id_nodo)
            nombre = nodo.nombre if nodo and nodo.nombre else str(id_nodo)
            nombres.append(nombre)
            valores.append(score)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(nombres[::-1], valores[::-1], color="darkorange")
        ax.set_xlabel("PageRank")
        ax.set_title(f"Top {cantidad} Artículos por PageRank")
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        ruta = self.carpetaResultados / "top_pagerank.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    # --- Gráfico 4: Top 10 categorías por promedio PageRank ---
    def grafTopCategorias(self, ranking_categorias):
        # ranking_categorias es la lista de (nombre, promedio, cantidad) de grafo.ranking_categorias()
        nombres = [r[0] for r in ranking_categorias]
        promedios = [r[1] for r in ranking_categorias]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(nombres[::-1], promedios[::-1], color="seagreen")
        ax.set_xlabel("PageRank Promedio")
        ax.set_title("Top Categorías por PageRank Promedio")
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        ruta = self.carpetaResultados / "top_categorias_pagerank.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    def generarTodos(self, grafo, puntajes_pagerank, ranking_categorias):
        print("Generando gráficos...")
        self.grafTopGradoEntrada(grafo)
        self.grafDistribucionGrados(grafo, tipo="entrada")
        self.grafTopPageRank(grafo, puntajes_pagerank)
        self.grafTopCategorias(ranking_categorias)
        print("Gráficos generados en:", self.carpetaResultados)
    
    # --- Gráfico 5: Top 10 categorías por cantidad de artículos ---
    def grafTamanoCategorias(self, grafo, cantidad=10):
        ranking = sorted(grafo.categorias.items(), key=lambda x: len(x[1]), reverse=True)[:cantidad]
        
        nombres = [r[0] for r in ranking]
        cantidades = [len(r[1]) for r in ranking]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(nombres[::-1], cantidades[::-1], color="mediumpurple")
        ax.set_xlabel("Cantidad de Artículos")
        ax.set_title(f"Top {cantidad} Categorías por Cantidad de Artículos")
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        ruta = self.carpetaResultados / "top_categorias_tamanio.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta