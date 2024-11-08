# main.py
from funcoes.arquivos import criar_pastas, listar_arquivos_pendentes, ler_contas_do_arquivo, mover_para_processados, atualizar_status_conta, verificar_todas_processadas
from funcoes.login import executar_login

def main():
    print("=== Automação Login TikTok Ads ===")
    
    # Criar pastas se não existirem
    criar_pastas()
    
    # Listar e selecionar arquivo
    nome_arquivo = listar_arquivos_pendentes()
    if not nome_arquivo:
        return
        
    # Ler contas do arquivo
    contas = ler_contas_do_arquivo(nome_arquivo)
    
    if not contas:
        print("❌ Nenhuma conta encontrada no arquivo!")
        return
    
    print(f"\nEncontradas {len(contas)} contas para processar.")
    
    # Processar cada conta
    for i, conta in enumerate(contas, 1):
        if conta.get('status') == 'logada':
            print(f"\n⏭️ Conta {conta['email']} já está logada, pulando...")
            continue
            
        print(f"\n=== Processando conta {i}/{len(contas)} ===")
        print(f"Email: {conta['email']}")
        
        profile_id = input("\nDigite o ID do perfil AdsPower: ").strip()
        
        sucesso = executar_login(
            profile_id=profile_id,
            email=conta['email'],
            senha_email=conta['senha_email'],
            senha_tiktok=conta['senha_tiktok']
        )
        
        if sucesso == "pular":
            print("⏭️ Conta pulada pelo usuário")
            atualizar_status_conta(nome_arquivo, conta['email'], 'pulada')
        elif sucesso:
            print("✅ Login realizado com sucesso!")
            atualizar_status_conta(nome_arquivo, conta['email'], 'logada')
        else:
            print("❌ Falha no processo de login")
            atualizar_status_conta(nome_arquivo, conta['email'], 'falha')
        
        input("\nPressione ENTER para continuar...")
    
    # Verificar se todas as contas foram processadas
    if verificar_todas_processadas(nome_arquivo):
        print("\n✅ Todas as contas foram processadas!")
        mover_para_processados(nome_arquivo)
    else:
        print("\n⚠️ Ainda existem contas pendentes neste arquivo!")

if __name__ == "__main__":
    main()