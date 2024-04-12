import csv
import requests
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
import os, sys, getopt

def presentacion()->None:
    print('=========================================================')
    print('Check-URLs 2024.04.12')
    print('Automatiza el checkeo de urls, utilizando un txt con ')
    print('las direcciones webs.')
    print('Genera un csv de reporte con las direcciones válidas')
    print('=========================================================')
    return

def modo_de_uso():
    print('Modo de uso:')
    print('py url_check.py -h              : Muestra esta ayuda')
    print('py url_check.py archivo.txt     : Procesa el archivo con')
    print('                                  las diferentes urls')
    return


def verifica_argumentos(argv):
    try:
        opts, args = getopt.getopt(argv, 'hc')
        for opt, args in opts:
            if opt == '-h':
                modo_de_uso()
        if (len(args) > 0):
            print(f'Leyendo {args[0]}')
            check_urls(args[0], 'active_urls.csv')
    except:
        print('py url_check.py -h para más información')
        sys.exit(2)

def check_urls(urls_file, output_file):
    active_urls = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    with open(urls_file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            try:
                response = requests.head(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    active_urls.append(url)
                    print(f"URL {url} está activo.")
                else:
                    print(f"URL {url} retornó el siguiente estado de código: {response.status_code}.")
            except requests.RequestException as e:
                print(f"Error al acceder a la URL {url}: {e}")

    # Write active URLs to CSV
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Active URLs'])
        for url in active_urls:
            writer.writerow([url])

if __name__ == "__main__":
    presentacion()
    verifica_argumentos(sys.argv[1:])
    print('Finalizado...')
