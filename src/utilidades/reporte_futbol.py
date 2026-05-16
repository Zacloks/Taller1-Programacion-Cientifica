from pathlib import Path

class ReporteFutbol:
    def __init__(self, carpetaResultados=None):
        if carpetaResultados is None:
            self.carpetaResultados = Path(__file__).resolve().parent.parent.parent / "results" / "reporte_futbol"
        else:
            self.carpetaResultados = Path(carpetaResultados)

    def imprimirPorConsola(self, grafo, ranking, grafo_futbol, ranking_futbol,
                           top_futbolistas, cats_grandes, cats_influyentes, comparacion):

        print("\n" + "="*15 + " ANÁLISIS DE FÚTBOL " + "="*15)

        articulos_futbol = []
        for id_nodo, score in ranking.items():
            nodo = grafo.articulos[id_nodo]
            if any(grafo_futbol.esCategoriaFutbol(cat) for cat in nodo.categorias):
                nombre_art = nodo.nombre if nodo.nombre else f"ID: {id_nodo}"
                articulos_futbol.append((nombre_art, score))

        print(f"Total de artículos de fútbol detectados: {len(articulos_futbol)}")
        print(f"Artículos en subgrafo: {grafo_futbol.cantidadArticulos()}")
        print(f"Enlaces en subgrafo: {grafo_futbol.cantidadEnlaces()}")

        articulos_futbol.sort(key=lambda x: x[1], reverse=True)
        print("\nTop 20 Artículos de Fútbol más influyentes (PageRank Global):")
        print("-" * 65)
        for i, (nombre, score) in enumerate(articulos_futbol[:20], start=1):
            print(f"  {i:2d}. {nombre:<40} -> PR Global: {score:.6f}")

        print("\nTop 10 Artículos por PageRank en subgrafo:")
        print("-" * 50)
        for i, (nombre, score, _) in enumerate(top_futbolistas, start=1):
            print(f"  {i}. {nombre} -> {score:.6f}")

        print("\nCategorías de Fútbol más grandes:")
        print("-" * 50)
        for nombre, cant in cats_grandes:
            print(f"  {nombre}: {cant} artículos")

        print("\nCategorías de Fútbol más influyentes:")
        print("-" * 50)
        for nombre, promedio, cant in cats_influyentes:
            print(f"  {nombre}: {promedio:.6f} ({cant} artículos)")

        print("\nComparación PageRank Global vs Fútbol:")
        print("-" * 50)
        for nombre, score_global, score_local in comparacion:
            print(f"  {nombre} -> Global: {score_global:.6f} | Fútbol: {score_local:.6f}")

    def exportar(self, grafo, ranking, grafo_futbol, ranking_futbol,
                 top_futbolistas, cats_grandes, cats_influyentes, comparacion):
        self.carpetaResultados.mkdir(parents=True, exist_ok=True)

        articulos_futbol_txt = []
        for id_nodo, score in ranking.items():
            nodo = grafo.articulos[id_nodo]
            if any(grafo_futbol.esCategoriaFutbol(cat) for cat in nodo.categorias):
                nombre_art = nodo.nombre if nodo.nombre else f"ID: {id_nodo}"
                articulos_futbol_txt.append((nombre_art, score))
        articulos_futbol_txt.sort(key=lambda x: x[1], reverse=True)

        lineas = ["Reporte de Fútbol - Red de Wikipedia", "=" * 50, "",
                  "=== Resumen Subgrafo de Fútbol ===",
                  f"Artículos de fútbol: {grafo_futbol.cantidadArticulos()}",
                  f"Enlaces de fútbol: {grafo_futbol.cantidadEnlaces()}",
                  f"Total artículos detectados: {len(articulos_futbol_txt)}", ""]

        lineas += ["=== Top 20 Artículos de Fútbol por PageRank Global ==="]
        for i, (nombre, score) in enumerate(articulos_futbol_txt[:20], start=1):
            lineas.append(f"  {i}. {nombre} -> {score:.6f}")

        lineas += ["", "=== Top 10 Artículos por PageRank en Subgrafo ==="]
        for i, (nombre, score, _) in enumerate(top_futbolistas, start=1):
            lineas.append(f"  {i}. {nombre} -> {score:.6f}")

        lineas += ["", "=== Top 10 Categorías de Fútbol más grandes ==="]
        for nombre, cant in cats_grandes:
            lineas.append(f"  {nombre}: {cant} artículos")

        lineas += ["", "=== Top 10 Categorías de Fútbol más influyentes ==="]
        for nombre, promedio, cant in cats_influyentes:
            lineas.append(f"  {nombre}: {promedio:.6f} ({cant} artículos)")

        lineas += ["", "=== Comparación PageRank Global vs Fútbol ==="]
        for nombre, score_global, score_local in comparacion:
            lineas.append(f"  {nombre} -> Global: {score_global:.6f} | Fútbol: {score_local:.6f}")

        ruta = self.carpetaResultados / "reporte_futbol.txt"
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        print("--- Reporte exportado a results/reporte_futbol/reporte_futbol.txt ---")