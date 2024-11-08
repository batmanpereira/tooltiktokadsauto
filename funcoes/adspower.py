# funcoes/adspower.py
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import URLS

def abrir_perfil_adspower(user_id):
    """Abre um perfil no AdsPower e retorna as configurações necessárias"""
    params = {
        'user_id': user_id,
        'open_tabs': 0,
        'ip_tab': 0,
        'headless': 0,
        'enable_password_saving': 1,
        'cdp_mask': 1
    }
    
    try:
        print(f"Tentando abrir perfil com ID: {user_id}")
        response = requests.get(URLS["adspower"], params=params, timeout=30)
        
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

def fechar_perfil(profile_id):
    """Fecha um perfil específico do AdsPower"""
    try:
        requests.get(
            "http://local.adspower.net:50325/api/v1/browser/stop",
            params={'user_id': profile_id}
        )
        print(f"✅ Perfil {profile_id} fechado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao fechar perfil: {e}")

def criar_perfil_adspower(nome: str):
    """Cria um novo perfil no AdsPower com as configurações especificadas"""
    payload = {
        "name": nome,
        "group_name": "Default",
        "fingerprint_config": {
            "language": ["pt-BR", "en-US"],
            "webrtc": "disabled",
            "canvas": "1",
            "webgl": "3",
            "audio": "1"
        }
    }
    
    try:
        print(f"Tentando criar perfil com nome: {nome}")
        response = requests.post(
            "http://local.adspower.net:50325/api/v1/user/create",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                user_id = data['data']['id']
                print(f"✅ Perfil criado com sucesso! ID: {user_id}")
                return user_id
            else:
                print(f"❌ Erro ao criar perfil: {data.get('msg')}")
                return None
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None

def verificar_status_adspower(user_id: str):
    """Verifica se um perfil específico está ativo no AdsPower"""
    try:
        print(f"Verificando status do perfil: {user_id}")
        response = requests.get(
            "http://local.adspower.net:50325/api/v1/browser/active",
            params={'user_id': user_id},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('data', {}).get('status') == "Active"
            print(f"✅ Status do perfil {user_id}: {'Ativo' if status else 'Inativo'}")
            return status
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar status: {str(e)}")
        return False

def fechar_perfil_adspower(user_id: str):
    """Fecha um perfil específico do AdsPower"""
    try:
        print(f"Tentando fechar perfil: {user_id}")
        response = requests.get(
            "http://local.adspower.net:50325/api/v1/browser/stop",
            params={'user_id': user_id},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                print(f"✅ Perfil {user_id} fechado com sucesso")
                return True
            else:
                print(f"❌ Erro ao fechar perfil: {data.get('msg')}")
                return False
    except Exception as e:
        print(f"❌ Erro ao fechar perfil: {str(e)}")
        return False