from src.cargarDatos import CargarDatos

def main():
    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()
    print(grafo.categorias["Buprestoidea"][0])

if __name__ == "__main__":
    main()
