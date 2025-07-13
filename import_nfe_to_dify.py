import os
import json
import requests
import time

# --- Configuração --- 
DIFY_API_URL = "http://localhost/api/v1"
# IMPORTANTE: Substitua com sua chave de API do Dify (Settings > API Keys)
DIFY_API_KEY = "YOUR_DIFY_API_KEY_HERE"
# IMPORTANTE: Substitua com o ID da sua base de conhecimento (Knowledge > nfe_pesos > Settings)
DATASET_ID = "YOUR_DATASET_ID_HERE"
# Caminho para a pasta com os arquivos JSON das notas fiscais
JSON_DIRECTORY = "/Users/kaauanmatzenbacher/CascadeProjects/nfe/data/json"

# --- Validações Iniciais ---
if DIFY_API_KEY == "YOUR_DIFY_API_KEY_HERE" or DATASET_ID == "YOUR_DATASET_ID_HERE":
    print("Erro: Por favor, configure seu DIFY_API_KEY e DATASET_ID no script.")
    exit()

headers = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
    "Content-Type": "application/json"
}

def add_item_to_dify(item, emitente_nome_fantasia="N/A"):
    """Envia um único item para a base de conhecimento do Dify."""
    endpoint = f"{DIFY_API_URL}/datasets/{DATASET_ID}/documents"

    # Formata o conteúdo do item para ser indexado, incluindo os novos campos
    content = (
        f"Emitente: {emitente_nome_fantasia}\n"
        f"--- Item ---\n"
        f"Código: {item.get('codigo', 'N/A')}\n"
        f"Descrição: {item.get('descricao', 'N/A')}\n"
        f"Unidade: {item.get('unidade', 'N/A')}\n"
        f"CFOP: {item.get('cfop', 'N/A')}\n"
        f"Quantidade: {item.get('quantidade', 0)}\n"
        f"Valor Unitário: {item.get('valor_unitario', 0.0)}\n"
        f"Valor Total: {item.get('valor_total', 0.0)}\n"
        f"Informações Adicionais: {item.get('informacoes_adicionais', 'Nenhuma')}"
    )

    # Cria um nome único para o documento baseado no código do item
    document_name = f"item_{item.get('codigo', 'sem_codigo')}_{int(time.time())}"

    payload = {
        "name": document_name,
        "text": content,
        "indexing_technique": "high_quality",
        "process_rule": {
            "mode": "automatic",
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": True}
                ],
                "segmentation": {
                    "separator": "\n",
                    "max_segment_length": 500,
                    "max_overlap": 50
                }
            }
        }
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Lança um erro para respostas 4xx/5xx
        print(f"Sucesso: Item '{item.get('descricao', 'N/A')}' (Cód: {item.get('codigo', 'N/A')}) adicionado ao Dify.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar item '{item.get('descricao', 'N/A')}': {e}")
        print(f"Resposta do servidor: {e.response.text if e.response else 'N/A'}")
        return False

def main():
    """Função principal para ler os arquivos JSON e iniciar a importação."""
    print(f"Iniciando a importação de itens do diretório: {JSON_DIRECTORY}")
    
    if not os.path.isdir(JSON_DIRECTORY):
        print(f"Erro: O diretório '{JSON_DIRECTORY}' não foi encontrado.")
        return

    processed_count = 0
    file_count = 0
    for filename in os.listdir(JSON_DIRECTORY):
        if filename.endswith('.json'):
            file_count += 1
            filepath = os.path.join(JSON_DIRECTORY, filename)
            print(f"\n--- Processando arquivo: {filename} ---")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    # O JSON parece ser uma lista contendo um dicionário
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        nfe_data = data[0]
                    else:
                        nfe_data = data # Caso não seja uma lista

                    # Extrai o nome fantasia do emitente
                    emitente_nome_fantasia = nfe_data.get('emitente', {}).get('nome_fantasia', 'N/A')

                    if 'itens' in nfe_data and isinstance(nfe_data['itens'], list):
                        for item in nfe_data['itens']:
                            if add_item_to_dify(item, emitente_nome_fantasia):
                                processed_count += 1
                            # Adiciona uma pequena pausa para não sobrecarregar a API
                            time.sleep(0.5)
                    else:
                        print(f"Aviso: Chave 'itens' não encontrada ou não é uma lista no arquivo {filename}")

            except json.JSONDecodeError:
                print(f"Erro: Falha ao decodificar JSON do arquivo {filename}")
            except Exception as e:
                print(f"Erro inesperado ao processar o arquivo {filename}: {e}")

    print("\n--- Processamento Concluído ---")
    print(f"Total de arquivos JSON encontrados: {file_count}")
    print(f"Total de itens processados e enviados ao Dify: {processed_count}")

if __name__ == "__main__":
    main()
