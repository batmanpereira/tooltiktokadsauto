import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import os
import shutil
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import re

PROFILE_ID_EMAIL = "kpgi01h"  # ID do perfil dedicado para verificação de emails

def abrir_perfil_adspower(user_id):
   # URL e parâmetros conforme documentação
   url = "http://local.adspower.net:50325/api/v1/browser/start"
   params = {
       'user_id': user_id,           # ID único do perfil
       'open_tabs': 0,               # Não abrir abas extras
       'ip_tab': 0,                  # Não abrir página de IP
       'headless': 0,                # Não usar modo headless
       'enable_password_saving': 1,   # Permitir salvar senhas
       'cdp_mask': 1                 # Mascarar detecção CDP
   }
   
   try:
       print(f"Tentando abrir perfil com ID: {user_id}")
       print(f"URL completa: {url}")
       print(f"Parâmetros: {json.dumps(params, indent=2)}")
       
       response = requests.get(url, params=params, timeout=30)
       print(f"Status Code: {response.status_code}")
       print(f"Resposta: {response.text}")
       
       if response.status_code == 200:
           data = response.json()
           if data.get('code') == 0:
               print("✅ Perfil aberto com sucesso!")
               return data['data']['ws']['selenium'], data['data']['webdriver']
           else:
               print(f"❌ Erro ao abrir perfil: {data.get('msg')}")
               return None, None
   except Exception as e:
       print(f"❌ Erro: {str(e)}")
       return None, None

def aceitar_cookies(driver):
   try:
       print("Procurando botão de aceitar cookies...")
       accept_button = WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
       )
       print("Botão de cookies encontrado, clicando...")
       accept_button.click()
       time.sleep(2)
       return True
   except Exception as e:
       print("Não foi encontrado botão de cookies ou já foi aceito")
       return False

def esperar_captcha(driver):
    print("\n⚠️ CAPTCHA detectado!")
    print("Por favor, resolva o captcha manualmente.")
    
    # Loop para tentar resolver o CAPTCHA
    tentativas = 3  # número máximo de tentativas
    for tentativa in range(tentativas):
        if tentativa > 0:
            print(f"\nTentativa {tentativa + 1} de {tentativas}")
        
        # Aguardar confirmação do usuário
        captcha_resolvido = confirmar_captcha()
        
        if captcha_resolvido:
            print("✅ Continuando com o processo...")
            time.sleep(2)  # Esperar possível redirecionamento
            return True
        
        if tentativa == tentativas - 1:
            print(f"❌ CAPTCHA não resolvido após {tentativas} tentativas")
            return False
    
    return False

def esperar_verificacao_email(driver):
   print("\n📧 Verificação de email detectada!")
   print("Por favor, verifique seu email e insira o código de verificação.")
   print("Você tem 120 segundos para inserir o código...")
   
   # Esperar até 120 segundos ou até a URL mudar
   for i in range(120):
       current_url = driver.current_url.lower()
       if "dashboard" in current_url or "home" in current_url or "overview" in current_url:
           print("✅ Código verificado com sucesso!")
           return True
       time.sleep(1)
       if i % 10 == 0:  # Mostrar mensagem a cada 10 segundos
           print(f"Aguardando... {120-i} segundos restantes")
           print("Dica: Abra seu email em outra janela e insira o código de verificação")
   
   print("❌ Tempo esgotado para verificação de email")
   return False

def fazer_login_tiktok(selenium_port, webdriver_path, email, senha_email, senha_tiktok):
   try:
       print("\nIniciando processo de login...")
       
       # Configurar o Chrome
       chrome_options = Options()
       chrome_options.add_experimental_option("debuggerAddress", selenium_port)
       
       # Iniciar o driver
       driver = webdriver.Chrome(options=chrome_options)
       
       # Abrir página do TikTok Ads
       print("Abrindo TikTok Ads...")
       driver.get("https://ads.tiktok.com/i18n/login")
       time.sleep(5)  # Esperar página carregar
       
       # Aceitar cookies se necessário
       aceitar_cookies(driver)
       
       # Esperar elementos de login com tempo maior
       print("Procurando campos de login...")
       try:
           email_field = WebDriverWait(driver, 20).until(
               EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @type='email']"))
           )
           print("Campo de email encontrado!")
       except:
           print("Tentando localizar campo de email de outra forma...")
           email_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='email' i]")
       
       # Preencher email com mais tempo entre ações
       print("Preenchendo email...")
       email_field.clear()
       time.sleep(1)
       for char in email:
           email_field.send_keys(char)
           time.sleep(0.1)
       time.sleep(2)
       
       # Preencher senha
       print("Procurando campo de senha...")
       try:
           password_field = WebDriverWait(driver, 20).until(
               EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
           )
           print("Campo de senha encontrado!")
       except:
           print("Tentando localizar campo de senha de outra forma...")
           password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
       
       print("Preenchendo senha...")
       password_field.clear()
       time.sleep(1)
       for char in senha_email:
           password_field.send_keys(char)
           time.sleep(0.1)
       time.sleep(2)
       
       # Clicar no botão de login com mais tentativas
       print("Procurando botão de login...")
       login_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Log') or contains(., 'Sign')]")
       if login_buttons:
           print("Botão encontrado, tentando clicar...")
           login_buttons[0].click()
       else:
           print("Tentando encontrar botão por CSS...")
           login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
           login_button.click()
       
       # Esperar login completar
       print("Aguardando login...")
       time.sleep(5)
       
       # Verificar se tem captcha
       if "login" in driver.current_url.lower():
           captcha_resolvido = esperar_captcha(driver)
           if not captcha_resolvido:
               print("❌ Não foi possível completar o login - Captcha não resolvido")
               return False
            
            # Se CAPTCHA foi resolvido, iniciar verificação de email
            print("\n📧 Iniciando verificação de email...")
            codigo = verificar_email_adspower(email, senha_email)
            
            if codigo:
                # Preencher código
                campos = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                for i, campo in enumerate(campos):
                    campo.send_keys(codigo[i])
                    time.sleep(0.5)
                print("✅ Código preenchido automaticamente!")
                return True
            else:
                print("❌ Não foi possível obter o código de verificação")
                return False
       
       # Verificar se tem verificação de email
       time.sleep(3)  # Esperar possível redirecionamento
       if "confirm" in driver.current_url.lower() or "verify" in driver.current_url.lower():
           email_verificado = esperar_verificacao_email(driver)
           if not email_verificado:
               print("❌ Não foi possível completar o login - Verificação de email não concluída")
               return False, driver
       
       # Verificar se login foi bem sucedido
       current_url = driver.current_url.lower()
       if "dashboard" in current_url or "home" in current_url or "overview" in current_url:
           print("✅ Login realizado com sucesso!")
           return True, driver
       else:
           print(f"❌ URL atual após tentativa de login: {current_url}")
           print("❌ Falha no login - verificar credenciais ou captcha")
           return False, driver
           
   except Exception as e:
       print(f"❌ Erro durante o login: {str(e)}")
       print("Stack trace completo:", str(e.__traceback__))
       return False, None

def executar_login(profile_id, email, senha_email, senha_tiktok):
    print("\n=== Iniciando processo de login ===")
    
    # Abrir perfil
    selenium_port, webdriver_path = abrir_perfil_adspower(profile_id)
    
    if selenium_port and webdriver_path:
        sucesso = fazer_login_tiktok(
            selenium_port=selenium_port,
            webdriver_path=webdriver_path,
            email=email,
            senha_email=senha_email,
            senha_tiktok=senha_tiktok
        )
        return sucesso
    return False

def criar_pastas():
    pastas = ['Pendentes', 'Processados']
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"Pasta '{pasta}' criada!")

def ler_contas_do_arquivo(nome_arquivo):
    contas = []
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    # Divide a linha em: email senha_email senha_tiktok
                    dados = linha.split()
                    if len(dados) >= 3:
                        conta = {
                            'email': dados[0],
                            'senha_email': dados[1],
                            'senha_tiktok': dados[2]
                        }
                        contas.append(conta)
                        print(f"Conta encontrada: {conta['email']}")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
    return contas

def confirmar_captcha():
    while True:
        print("\n🤖 Status do CAPTCHA:")
        print("1 - CAPTCHA resolvido com sucesso")
        print("2 - CAPTCHA falhou/Tentar novamente")
        
        resposta = input("Digite a opção (1 ou 2): ").strip()
        
        if resposta == "1":
            print("✅ Continuando com o processo...")
            return True
        elif resposta == "2":
            print("❌ CAPTCHA não resolvido")
            return False
        else:
            print("⚠️ Opção inválida! Digite 1 ou 2")

def listar_arquivos_pendentes():
    arquivos = os.listdir('Pendentes')
    arquivos_txt = [f for f in arquivos if f.endswith('.txt')]
    
    if not arquivos_txt:
        print("\n❌ Nenhum arquivo .txt encontrado na pasta 'Pendentes'!")
        exit()
    
    print("\nArquivos encontrados:")
    for i, arquivo in enumerate(arquivos_txt, 1):
        print(f"{i}. {arquivo}")
    
    while True:
        try:
            escolha = input("\nDigite o número do arquivo que deseja processar: ")
            indice = int(escolha) - 1
            if 0 <= indice < len(arquivos_txt):
                return os.path.join('Pendentes', arquivos_txt[indice])
            else:
                print("⚠️ Número inválido! Tente novamente.")
        except ValueError:
            print("⚠️ Por favor, digite um número válido!")

def verificar_email_adspower(email, senha_email):
    """
    Função para verificar email usando perfil AdsPower dedicado
    """
    print("\n📧 Iniciando verificação de email no perfil dedicado...")
    
    # Abrir perfil dedicado para email
    selenium_port, webdriver_path = abrir_perfil_adspower(PROFILE_ID_EMAIL)
    
    if not selenium_port or not webdriver_path:
        print("❌ Não foi possível abrir perfil para verificação de email")
        return None
    
    try:
        # Configurar driver para o perfil de email
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", selenium_port)
        driver_email = webdriver.Chrome(options=chrome_options)
        
        # Acessar Outlook
        print("Acessando Outlook...")
        driver_email.get("https://outlook.live.com/owa/")
        time.sleep(3)
        
        # Verificar se já está logado
        if "login" in driver_email.current_url.lower():
            print("Fazendo login no Outlook...")
            try:
                # Email
                email_field = WebDriverWait(driver_email, 10).until(
                    EC.presence_of_element_located((By.NAME, "loginfmt"))
                )
                email_field.clear()
                email_field.send_keys(email)
                email_field.send_keys(Keys.RETURN)
                time.sleep(2)
                
                # Senha
                password_field = WebDriverWait(driver_email, 10).until(
                    EC.presence_of_element_located((By.NAME, "passwd"))
                )
                password_field.clear()
                password_field.send_keys(senha_email)
                password_field.send_keys(Keys.RETURN)
                time.sleep(2)
                
                # Se aparecer "Continuar conectado"
                try:
                    stay_signed_in = WebDriverWait(driver_email, 5).until(
                        EC.presence_of_element_located((By.ID, "idBtn_Back"))
                    )
                    stay_signed_in.click()
                except:
                    pass
            except Exception as e:
                print(f"❌ Erro no login do Outlook: {e}")
                return None
        
        # Aguardar e procurar email de verificação
        print("Procurando email de verificação...")
        codigo = None
        for tentativa in range(15):
            try:
                # Atualizar inbox
                driver_email.get("https://outlook.live.com/mail/0/inbox")
                time.sleep(2)
                
                # Procurar email mais recente do TikTok
                email_tiktok = WebDriverWait(driver_email, 5).until(
                    EC.presence_of_element_located((By.XPATH, 
                    "//div[contains(@class, 'ItemSubject') and contains(text(), 'TikTok')]"))
                )
                email_tiktok.click()
                time.sleep(1)
                
                # Extrair código
                corpo_email = driver_email.find_element(By.XPATH, "//*[contains(text(), 'verification code')]")
                texto_email = corpo_email.text
                codigo_match = re.search(r'\b\d{6}\b', texto_email)
                
                if codigo_match:
                    codigo = codigo_match.group(0)
                    print(f"✅ Código encontrado: {codigo}")
                    break
            except:
                print(f"Aguardando email chegar... ({tentativa + 1}/15)")
                time.sleep(2)
        
        # Limpar e fechar perfil
        print("\nFinalizando perfil de email...")
        requests.get("http://local.adspower.net:50325/api/v1/browser/clean", 
                    params={'user_id': PROFILE_ID_EMAIL})
        requests.get("http://local.adspower.net:50325/api/v1/browser/stop", 
                    params={'user_id': PROFILE_ID_EMAIL})
        
        return codigo
        
    except Exception as e:
        print(f"❌ Erro durante verificação de email: {e}")
        return None

if __name__ == "__main__":
    print("=== Automação Login TikTok Ads ===")
    
    # Criar pastas se não existirem
    criar_pastas()
    
    # Listar e selecionar arquivo
    nome_arquivo = listar_arquivos_pendentes()
    contas = ler_contas_do_arquivo(nome_arquivo)
    
    if not contas:
        print("❌ Nenhuma conta encontrada no arquivo!")
        exit()
    
    print(f"\nEncontradas {len(contas)} contas para processar.")
    
    for i, conta in enumerate(contas, 1):
        print(f"\n=== Processando conta {i}/{len(contas)} ===")
        print(f"Email: {conta['email']}")
        
        # Pedir ID do perfil para esta conta
        profile_id = input("\nDigite o ID do perfil AdsPower: ").strip()
        
        # Executar login
        sucesso = executar_login(
            profile_id=profile_id,
            email=conta['email'],
            senha_email=conta['senha_email'],
            senha_tiktok=conta['senha_tiktok']
        )
        
        if sucesso:
            print("✅ Login realizado com sucesso!")
        else:
            print("❌ Falha no processo de login")
        
        input("\nPressione ENTER para continuar...")