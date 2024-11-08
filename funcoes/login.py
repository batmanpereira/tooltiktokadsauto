# funcoes/login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from config import URLS, TEMPO_ESPERA, SELETORES
from .adspower import abrir_perfil_adspower, fechar_perfil
from .email_verificador import verificar_email_adspower

def aceitar_cookies(driver):
    """Aceita os cookies do site"""
    try:
        botao_cookies = WebDriverWait(driver, TEMPO_ESPERA["padrao"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SELETORES["botao_cookies"]))
        )
        botao_cookies.click()
        print("✅ Cookies aceitos")
        return True
    except:
        print("⚠️ Botão de cookies não encontrado")
        return False

def confirmar_captcha_manual():
    """Solicita confirmação manual do captcha"""
    while True:
        print("\n🤖 Status do CAPTCHA:")
        print("1 - CAPTCHA resolvido com sucesso")
        print("2 - CAPTCHA falhou/Tentar novamente")
        print("3 - Pular esta conta")
        
        resposta = input("Digite a opção (1, 2 ou 3): ").strip()
        
        if resposta == "1":
            return True
        elif resposta == "2":
            return False
        elif resposta == "3":
            return None
        else:
            print("⚠️ Opção inválida! Digite 1, 2 ou 3")

def esperar_captcha(driver):
    """Aguarda resolução manual do captcha"""
    print("\n⚠️ CAPTCHA detectado!")
    print("Por favor, resolva o captcha manualmente.")
    
    tentativas = 3
    for tentativa in range(tentativas):
        if tentativa > 0:
            print(f"\nTentativa {tentativa + 1} de {tentativas}")
        
        resultado = confirmar_captcha_manual()
        
        if resultado is True:
            print("✅ CAPTCHA resolvido! Continuando...")
            time.sleep(2)
            return True
        elif resultado is None:
            print("⏭️ Pulando esta conta...")
            return None
        
        if tentativa == tentativas - 1:
            print(f"❌ CAPTCHA não resolvido após {tentativas} tentativas")
            return False
    
    return False

def esperar_verificacao_email(driver):
    """Verifica se é necessária verificação de email"""
    try:
        WebDriverWait(driver, TEMPO_ESPERA["padrao"]).until(
            EC.presence_of_element_located((By.XPATH, SELETORES["verificacao_email"]))
        )
        return True
    except:
        return False

def fazer_login_tiktok(selenium_port, webdriver_path, email, senha_email, senha_tiktok):
    """Realiza o processo de login no TikTok Ads"""
    try:
        # Configurar o driver
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", selenium_port)
        
        # Forma correta de inicializar o driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Acessar TikTok Ads
        driver.get(URLS["tiktok"])
        time.sleep(TEMPO_ESPERA["padrao"])
        
        # Aceitar cookies
        aceitar_cookies(driver)
        
        # Preencher email e senha com espera explícita
        print("Aguardando campos de login...")
        campo_email = WebDriverWait(driver, TEMPO_ESPERA["carregamento"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[type='email']"))
        )
        campo_email.clear()
        campo_email.send_keys(email)
        time.sleep(1)
        
        campo_senha = WebDriverWait(driver, TEMPO_ESPERA["carregamento"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        campo_senha.clear()
        campo_senha.send_keys(senha_tiktok)
        time.sleep(1)
        
        # Tentar diferentes métodos para encontrar o botão de login
        print("Procurando botão de login...")
        try:
            # Primeira tentativa: por texto
            botao_login = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log') or contains(text(), 'Sign')]"))
            )
        except:
            try:
                # Segunda tentativa: por tipo submit
                botao_login = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
            except:
                # Terceira tentativa: por classe comum de botão
                botao_login = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button, .submit-button"))
                )
        
        print("Botão de login encontrado, clicando...")
        botao_login.click()
        time.sleep(TEMPO_ESPERA["padrao"])
        
        # Esperar captcha
        captcha_resultado = esperar_captcha(driver)
        if captcha_resultado is None:
            return "pular"  # Novo status para indicar que deve pular a conta
        elif not captcha_resultado:
            return False
            
        # Verificar se precisa de verificação de email
        if esperar_verificacao_email(driver):
            print("\n📧 Verificação de email necessária")
            codigo = verificar_email_adspower(email, senha_email)
            
            if codigo:
                # Preencher código de verificação
                campo_codigo = WebDriverWait(driver, TEMPO_ESPERA["padrao"]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )
                campo_codigo.send_keys(codigo)
                
                # Clicar em enviar
                botao_enviar = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                botao_enviar.click()
                
                # Esperar login completar
                time.sleep(TEMPO_ESPERA["padrao"])
            else:
                print("❌ Não foi possível obter o código de verificação")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o login: {str(e)}")
        print(f"Stack trace completo: {e.__traceback__}")
        return False

def executar_login(profile_id, email, senha_email, senha_tiktok):
    """Executa todo o processo de login"""
    print("\n=== Iniciando processo de login ===")
    
    selenium_port, webdriver_path = abrir_perfil_adspower(profile_id)
    
    if selenium_port and webdriver_path:
        sucesso = fazer_login_tiktok(
            selenium_port=selenium_port,
            webdriver_path=webdriver_path,
            email=email,
            senha_email=senha_email,
            senha_tiktok=senha_tiktok
        )
        
        fechar_perfil(profile_id)
        return sucesso
        
    return False