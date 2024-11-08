# funcoes/arquivos.py
import os
import shutil
from datetime import datetime
from config import CAMINHOS

def criar_pastas():
    """Cria as pastas necessárias se não existirem"""
    for pasta in CAMINHOS.values():
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"Pasta '{pasta}' criada!")
        else:
            print(f"DEBUG: Pasta '{pasta}' já existe")

def ler_contas_do_arquivo(caminho_arquivo):
    """Lê as contas de um arquivo específico"""
    contas = []
    print(f"DEBUG: Tentando ler arquivo em: {caminho_arquivo}")
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha and not linha.startswith('#'):  
                    dados = linha.split()
                    if len(dados) >= 3:
                        conta = {
                            'email': dados[0],
                            'senha_email': dados[1],
                            'senha_tiktok': dados[2],
                            'arquivo': caminho_arquivo,
                            'status': dados[3] if len(dados) > 3 else 'pendente'
                        }
                        contas.append(conta)
                        print(f"Conta encontrada: {conta['email']}")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        print(f"Tentando ler arquivo: {caminho_arquivo}")
    return contas

def atualizar_status_conta(nome_arquivo, email, novo_status):
    """Atualiza o status de uma conta específica no arquivo"""
    contas = []
    try:
        print(f"DEBUG: Atualizando status em: {nome_arquivo}")
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                    
                dados = linha.split()
                if dados[0] == email:  
                    if len(dados) > 3:
                        dados[3] = novo_status
                    else:
                        dados.append(novo_status)
                contas.append(' '.join(dados))
        
        with open(nome_arquivo, 'w') as arquivo:
            for linha in contas:
                arquivo.write(linha + '\n')
                
        return True
    except Exception as e:
        print(f"Erro ao atualizar status: {e}")
        return False

def verificar_todas_processadas(nome_arquivo):
    """Verifica se todas as contas no arquivo foram processadas"""
    try:
        print(f"DEBUG: Verificando processamento em: {nome_arquivo}")
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith('#'):
                    continue
                    
                dados = linha.split()
                if len(dados) <= 3 or dados[3] != 'logada':
                    return False
        return True
    except Exception as e:
        print(f"Erro ao verificar status: {e}")
        return False

def listar_arquivos_pendentes():
    """Lista os arquivos .txt na pasta pendentes"""
    try:
        print(f"\nDEBUG: Caminho configurado: {CAMINHOS['pendentes']}")
        print(f"DEBUG: Caminho existe? {os.path.exists(CAMINHOS['pendentes'])}")
        print(f"DEBUG: Caminho absoluto: {os.path.abspath(CAMINHOS['pendentes'])}")
        
        arquivos = os.listdir(CAMINHOS["pendentes"])
        print(f"DEBUG: Arquivos encontrados no diretório: {arquivos}")
        
        arquivos_txt = [f for f in arquivos if f.endswith('.txt')]
        print(f"DEBUG: Arquivos .txt encontrados: {arquivos_txt}")
        
        if not arquivos_txt:
            print("\n❌ Nenhum arquivo .txt encontrado na pasta 'pendentes'!")
            return None
        
        print("\nArquivos encontrados:")
        for i, arquivo in enumerate(arquivos_txt, 1):
            print(f"{i}. {arquivo}")
        
        while True:
            try:
                escolha = input("\nDigite o número do arquivo que deseja processar: ")
                indice = int(escolha) - 1
                if 0 <= indice < len(arquivos_txt):
                    caminho_completo = os.path.join(CAMINHOS["pendentes"], arquivos_txt[indice])
                    print(f"DEBUG: Caminho completo selecionado: {caminho_completo}")
                    return caminho_completo
                else:
                    print("⚠️ Número inválido! Tente novamente.")
            except ValueError:
                print("⚠️ Por favor, digite um número válido!")
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        print(f"DEBUG: Erro completo: {str(e)}")
        return None

def mover_para_processados(nome_arquivo):
    """Move o arquivo para a pasta de processados"""
    try:
        nome_base = os.path.basename(nome_arquivo)
        destino = os.path.join(CAMINHOS["processados"], nome_base)
        print(f"DEBUG: Movendo de {nome_arquivo} para {destino}")
        os.rename(nome_arquivo, destino)
        print(f"✅ Arquivo {nome_base} movido para processados")
    except Exception as e:
        print(f"❌ Erro ao mover arquivo: {e}")