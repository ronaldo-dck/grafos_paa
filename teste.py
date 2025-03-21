import os
import time
import subprocess
import csv
from tqdm import tqdm  # Biblioteca para a barra de progresso

def run_tests(input_folder, output_file):
    """
    Executa os testes para os arquivos de entrada na pasta especificada e salva os resultados.

    :param input_folder: Caminho para a pasta contendo os arquivos de entrada.
    :param output_file: Caminho para o arquivo onde os resultados serão salvos.
    """
    algorithms = ['kruskal', 'prim']
    results = []

    # Conta o número total de execuções (arquivos * algoritmos * repetições)
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    total_tests = len(input_files) * len(algorithms) * 30

    # Barra de progresso
    with tqdm(total=total_tests, desc="Executando testes", unit="execução") as pbar:
        # Percorre todos os arquivos na pasta de entrada
        for filename in input_files:
            input_path = os.path.join(input_folder, filename)
            
            for algorithm in algorithms:
                # Mede o tempo de execução
                for i in range(30):  # Repetições
                    start_time = time.time()
                    process = subprocess.run(
                        ['python3', 'main.py', algorithm, input_path],
                        capture_output=True,
                        text=True
                    )
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    # Captura a saída do programa
                    output = process.stdout.strip()
                    error = process.stderr.strip()

                    # Salva os resultados
                    results.append({
                        'input_file': filename,
                        'algorithm': algorithm,
                        'cost': output,
                        'execution_time': elapsed_time
                    })

                    # Atualiza a barra de progresso
                    pbar.update(1)

    # Escreve os resultados no arquivo CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['input_file', 'algorithm', 'cost', 'execution_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

# Configurações
input_folder = './inputs'  # Pasta contendo os arquivos de entrada
output_file = './logs/results.csv'  # Arquivo onde os resultados serão salvos

# Executa os testes
run_tests(input_folder, output_file)
print(f"Testes concluídos. Resultados salvos em {output_file}.")