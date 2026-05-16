import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

class GraficosFutbol:
    def __init__(self, carpetaResultados=None):
        if carpetaResultados is None:
            self.carpetaResultados = Path(__file__).resolve().parent.parent.parent / "results" / "reporte_futbol"
        else:
            self.carpetaResultados = Path(carpetaResultados)
        self.carpetaResultados.mkdir(parents=True, exist_ok=True)

    def grafTopFutbolistas(self, top_futbolistas):
        nombres = [r[0] if r[0] else "Sin nombre" for r in top_futbolistas]
        valores = [r[1] for r in top_futbolistas]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(nombres[::-1], valores[::-1], color="crimson")
        ax.set_xlabel("PageRank en Subgrafo de Fútbol")
        ax.set_title("Top Artículos de Fútbol por PageRank")
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        ruta = self.carpetaResultados / "futbol_top_pagerank.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    def grafCategoriasFutbolInfluyentes(self, cats_influyentes):
        nombres = [r[0] for r in cats_influyentes]
        promedios = [r[1] for r in cats_influyentes]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(nombres[::-1], promedios[::-1], color="darkorange")
        ax.set_xlabel("PageRank Promedio")
        ax.set_title("Top Categorías de Fútbol por PageRank Promedio")
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        ruta = self.carpetaResultados / "futbol_categorias_influyentes.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    def grafComparacionPageRank(self, comparacion):
        nombres = [r[0] if r[0] else "Sin nombre" for r in comparacion]
        scores_global = [r[1] for r in comparacion]
        scores_local = [r[2] for r in comparacion]

        x = range(len(nombres))
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar([i - 0.2 for i in x], scores_global, width=0.4, label="PageRank Global", color="steelblue")
        ax.bar([i + 0.2 for i in x], scores_local, width=0.4, label="PageRank Fútbol", color="crimson")
        ax.set_xticks(list(x))
        ax.set_xticklabels(nombres, rotation=45, ha="right", fontsize=7)
        ax.set_ylabel("PageRank")
        ax.set_title("Comparación PageRank Global vs PageRank en Subgrafo de Fútbol")
        ax.legend()
        plt.tight_layout()

        ruta = self.carpetaResultados / "futbol_comparacion_pagerank.png"
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"Gráfico guardado: {ruta}")
        return ruta

    def generarTodos(self, top_futbolistas, cats_influyentes, comparacion):
        print("Generando gráficos de fútbol...")
        self.grafTopFutbolistas(top_futbolistas)
        self.grafCategoriasFutbolInfluyentes(cats_influyentes)
        self.grafComparacionPageRank(comparacion)
        print("Gráficos de fútbol guardados en:", self.carpetaResultados)