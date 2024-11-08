# funcoes/email_verificador.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
from config import URLS, TEMPO_ESPERA, PROFILE_ID_EMAIL
from .adspower import abrir_perfil_adspower, fechar_perfil

def verificar_email_adspower(email, senha_email):
    """Função para verificar email usando perfil AdsPower dedicado"""
    print("\n📧 Iniciando verificação de email no perfil dedicado...")
    
    selenium_port, webdriver_path = abrir_perfil_adspower(PROFILE_ID_EMAIL)
    
    if not selenium_port or not webdriver_path:
        print("❌ Não foi possível abrir perfil para verificação de email")
        return None

    try:
        # Configurar o driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{selenium_port}")
        driver = webdriver.Chrome(webdriver_path, options=chrome_options)
        
        # Acessar Outlook
        driver.get(URLS["outlook"])
        time.sleep(TEMPO_ESPERA["padrao"])
        
        # Fazer login no email
        try:
            # Campo de email
            email_field = WebDriverWait(driver, TEMPO_ESPERA["carregamento"]).until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            email_field.send_keys(email)
            email_field.send_keys(Keys.RETURN)
            time.sleep(TEMPO_ESPERA["padrao"])
            
            # Campo de senha
            password_field = WebDriverWait(driver, TEMPO_ESPERA["carregamento"]).until(
                EC.presence_of_element_located((By.NAME, "passwd"))
            )
            password_field.send_keys(senha_email)
            password_field.send_keys(Keys.RETURN)
            time.sleep(TEMPO_ESPERA["padrao"])
            
            # Botão "Não" para manter sessão não conectada
            try:
                no_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "idBtn_Back"))
                )
                no_button.click()
            except:
                print("Botão 'Não' não encontrado, continuando...")
            
            # Aguardar carregamento da caixa de entrada
            time.sleep(TEMPO_ESPERA["padrao"])
            
            # Procurar email do TikTok
            print("🔍 Procurando email de verificação...")
            emails = WebDriverWait(driver, TEMPO_ESPERA["email"]).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='listitem']"))
            )
            
            for email in emails:
                if "TikTok Ads" in email.text:
                    email.click()
                    time.sleep(TEMPO_ESPERA["padrao"])
                    
                    # Procurar código de verificação
                    conteudo = driver.page_source
                    codigo = re.search(r'verification code is (\d{6})', conteudo)
                    
                    if codigo:
                        codigo = codigo.group(1)
                        print(f"✅ Código encontrado: {codigo}")
                        return codigo
            
            print("❌ Email de verificação não encontrado")
            return None
            
        except Exception as e:
            print(f"❌ Erro durante verificação de email: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Erro geral na verificação: {e}")
        return None
        
    finally:
        try:
            driver.quit()
        except:
            pass
        fechar_perfil(PROFILE_ID_EMAIL)