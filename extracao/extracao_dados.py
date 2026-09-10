import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# ==========================================
# FUNÇÕES DE DEFESA CONTRA OBSTÁCULOS
# ==========================================
def aceitar_cookies_se_existir(driver, timeout=4):
    try:
        botao_cookies = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_ACEITAR_COOKIES]"))
        )
        botao_cookies.click()
        print("Aviso de cookies aceito.")
    except TimeoutException:
        pass

def fechar_popup_se_existir(driver, timeout=3):
    try:
        botao_fechar = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div/button"))
        )
        botao_fechar.click()
        print("Pop-up genérico interceptado e fechado.")
    except TimeoutException:
        pass

def resolver_desafio_matematico(driver, timeout=3):
    try:
        elemento_pergunta = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "[PREENCHER_AQUI: XPATH_TEXTO_DA_PERGUNTA]"))
        )
        texto_pergunta = elemento_pergunta.text
        
        padrao = r'(\d+)\s*([\+\-\*])\s*(\d+)'
        match = re.search(padrao, texto_pergunta)
        
        if match:
            num1 = int(match.group(1))
            operador = match.group(2)
            num2 = int(match.group(3))

            if operador == '+': resultado = num1 + num2
            elif operador == '-': resultado = num1 - num2
            elif operador == '*': resultado = num1 * num2
            
            print(f"Desafio resolvido: {num1} {operador} {num2} = {resultado}")

            campo_resposta = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_CAMPO_DIGITAR_RESPOSTA]")
            campo_resposta.clear()
            campo_resposta.send_keys(str(resultado))

            botao_confirmar = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_CONFIRMAR_DESAFIO]")
            botao_confirmar.click()
            time.sleep(2)
            
    except TimeoutException:
        pass


# ==========================================
# INÍCIO DO FLUXO PRINCIPAL
# ==========================================
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # ------------------------------------------
    # ETAPA 1: LOGIN E BUSCA INICIAL
    # ------------------------------------------
    driver.get("https://talkabit-z3eg.onrender.com/app/login")
    aceitar_cookies_se_existir(driver, 4)
    
    campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "teamToken")))
    campo_usuario.send_keys("BREAKINGBAD-VPJ7W")

    campo_senha = driver.find_element(By.ID, "password")
    campo_senha.send_keys("talkabit")

    botao_entrar = driver.find_element(By.XPATH, "/html/body/main/div/form/div/button")
    botao_entrar.click()

    fechar_popup_se_existir(driver, 4)
    resolver_desafio_matematico(driver, 3)

    botao_busca = wait.until(EC.element_to_be_clickable((By.ID, "[PREENCHER_AQUI: ID_DO_BOTAO_DE_BUSCA]")))
    try:
        botao_busca.click()
    except ElementClickInterceptedException:
        fechar_popup_se_existir(driver, 2)
        resolver_desafio_matematico(driver, 2)
        botao_busca.click()


    # ------------------------------------------
    # ETAPA 2: PAGINAÇÃO E EXTRAÇÃO (O CORAÇÃO DO CÓDIGO)
    # ------------------------------------------
    dados_autorizados = [] # Vai guardar dicionários com chave e valor
    pagina_atual = 1

    while True: # Loop infinito que só para quando não houver próxima página
        print(f"\n--- Analisando Página {pagina_atual} ---")
        
        # Defesas ao carregar nova página
        fechar_popup_se_existir(driver, 3)
        resolver_desafio_matematico(driver, 2)
        
        # Espera as notas aparecerem
        wait.until(EC.presence_of_element_located((By.XPATH, "[PREENCHER_AQUI: XPATH_DA_LINHA_DA_NOTA]")))
        
        # Conta quantas notas tem na tabela atual
        qtd_linhas = len(driver.find_elements(By.XPATH, "[PREENCHER_AQUI: XPATH_DA_LINHA_DA_NOTA]"))
        
        for i in range(qtd_linhas):
            # IMPORTANTE: Busca as linhas novamente a cada rodada para evitar o StaleElementReference
            linhas_notas = driver.find_elements(By.XPATH, "[PREENCHER_AQUI: XPATH_DA_LINHA_DA_NOTA]")
            linha = linhas_notas[i]
            
            try:
                # Verifica o status da nota (cancelada, denegada, autorizada)
                status = linha.find_element(By.XPATH, ".//[PREENCHER_AQUI: XPATH_COLUNA_STATUS]").text.strip().lower()

                if "autorizada" in status:
                    print(f"Nota na posição {i+1} é AUTORIZADA. Abrindo...")
                    
                    # Clica para abrir a nota
                    botao_abrir_nota = linha.find_element(By.XPATH, ".//[PREENCHER_AQUI: XPATH_BOTAO_OU_LINK_QUE_ABRE_A_NOTA]")
                    botao_abrir_nota.click()
                    
                    # Lida com possíveis bloqueios na página da nota
                    fechar_popup_se_existir(driver, 3)
                    resolver_desafio_matematico(driver, 2)

                    # Extrai os dados que precisamos
                    chave = wait.until(EC.presence_of_element_located((By.XPATH, "[PREENCHER_AQUI: XPATH_CHAVE_DE_ACESSO]"))).text
                    valor = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_VALOR_TOTAL]").text
                    
                    # Salva em nossa lista principal
                    dados_autorizados.append({'chave': chave, 'valor': valor})
                    print(f"-> SUCESSO: Chave: {chave} | Valor: {valor}")
                    
                    # Volta para a tela da tabela
                    driver.back()
                    time.sleep(1) # Pausa rápida para a tabela renderizar novamente
                    
                    # Como voltamos de página, recarrega as defesas
                    fechar_popup_se_existir(driver, 2)
                    wait.until(EC.presence_of_element_located((By.XPATH, "[PREENCHER_AQUI: XPATH_DA_LINHA_DA_NOTA]")))
                
                else:
                    print(f"Nota na posição {i+1} ignorada (Status: {status})")
                    
            except NoSuchElementException:
                print(f"Erro ao ler a nota na posição {i+1}. Pulando...")
                continue

        # Terminou de ler todas as linhas da página atual, tenta ir para a próxima
        try:
            botao_proxima = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_PROXIMA_PAGINA]")
            
            # Se o botão estiver desabilitado (não clicável), significa que chegamos na última página
            if botao_proxima.get_attribute("disabled") or "disabled" in botao_proxima.get_attribute("class"):
                print("Fim das páginas alcançado.")
                break # Quebra o while True
                
            botao_proxima.click()
            pagina_atual += 1
            time.sleep(2) # Dá tempo da nova página carregar
            
        except NoSuchElementException:
            print("Botão de próxima página não encontrado. Fim da extração.")
            break # Quebra o while True

    print(f"\nTotal de notas autorizadas processadas: {len(dados_autorizados)}")

    # ------------------------------------------
    # ETAPA 3: INSERIR DADOS NO SEGUNDO SITE
    # ------------------------------------------
    if dados_autorizados:
        driver.get("[PREENCHER_AQUI: LINK_DO_SEGUNDO_SITE]")
        aceitar_cookies_se_existir(driver, 4)
        fechar_popup_se_existir(driver, 3)

        for dado in dados_autorizados:
            # Preenche a chave de acesso
            campo_chave = wait.until(EC.presence_of_element_located((By.ID, "[PREENCHER_AQUI: ID_CAMPO_CHAVE_DESTINO]")))
            campo_chave.clear()
            campo_chave.send_keys(dado['chave'])
            
            # Preenche o valor total
            campo_valor = driver.find_element(By.ID, "[PREENCHER_AQUI: ID_CAMPO_VALOR_DESTINO]")
            campo_valor.clear()
            campo_valor.send_keys(dado['valor'])
            
            botao_salvar = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_SALVAR_DESTINO]")
            botao_salvar.click()
            
            time.sleep(1)
            print(f"Enviado para o site 2: {dado['chave']}")

finally:
    driver.quit()
