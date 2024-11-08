# config.py
import os

URLS = {
    "tiktok": "https://ads.tiktok.com/i18n/login",
    "adspower": "http://local.adspower.net:50325/api/v1/browser/start",
    "outlook": "https://outlook.live.com/owa/"
}

# Caminho absoluto para o projeto
CAMINHOS = {
    "pendentes": "/Users/master/TikBoost/Automation/dados/Pendentes",
    "processados": "/Users/master/TikBoost/Automation/dados/Processados"
}

TEMPO_ESPERA = {
    "padrao": 5,
    "carregamento": 10,
    "captcha": 120,
    "email": 120
}

# ID do perfil para verificação de emails
PROFILE_ID_EMAIL = "kpgi01h"

# Seletores CSS e XPath
SELETORES = {
    "botao_cookies": "button[id='onetrust-accept-btn-handler']",
    "campo_email": "input[name='email']",
    "campo_senha": "input[name='password']",
    "botao_login": "button[type='submit']",
    "verificacao_email": "//div[contains(text(), 'Verificação de e-mail necessária')]"
}