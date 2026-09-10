import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

def aceitar_cookies_se_existir(driver, timeout=4):
    """Tenta encontrar e clicar no botão de aceitar cookies."""
    try:
        # [PREENCHER_AQUI] XPath do botão "Aceitar", "Concordar" ou "OK" dos cookies
        botao_cookies = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_ACEITAR_COOKIES]"))
        )
        botao_cookies.click()
        print("Aviso de cookies aceito.")
    except TimeoutException:
        pass

def fechar_popup_se_existir(driver, timeout=3):
    """Tenta fechar pop-ups genéricos que sobrepõem a tela."""
    try:
        botao_fechar = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div/button"))
        )
        botao_fechar.click()
        print("Pop-up genérico interceptado e fechado.")
    except TimeoutException:
        pass

def resolver_desafio_matematico(driver, timeout=3):
    """Busca e resolve desafios matemáticos de segurança na tela."""
    try:
        # [PREENCHER_AQUI] XPath do texto onde a pergunta matemática aparece
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
            
            print(f"Desafio matemático resolvido: {num1} {operador} {num2} = {resultado}")

            # [PREENCHER_AQUI] XPath do campo onde você digita a resposta
            campo_resposta = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_CAMPO_DIGITAR_RESPOSTA]")
            campo_resposta.clear()
            campo_resposta.send_keys(str(resultado))

            # [PREENCHER_AQUI] XPath do botão para confirmar a resposta do desafio
            botao_confirmar = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_CONFIRMAR_DESAFIO]")
            botao_confirmar.click()
            time.sleep(2)
            
    except TimeoutException:
        pass

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # ==========================================
    # ETAPA 1: LOGIN
    # ==========================================
    driver.get("https://talkabit-z3eg.onrender.com/app/login")
    
    # NOVA CHAMADA: Tenta aceitar os cookies logo ao entrar no site
    aceitar_cookies_se_existir(driver, 4)
    
    campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "teamToken")))
    campo_usuario.send_keys("BREAKINGBAD-VPJ7W")

    campo_senha = driver.find_element(By.ID, "password")
    campo_senha.send_keys("talkabit")

    botao_entrar = driver.find_element(By.XPATH, "/html/body/main/div/form/div/button")
    botao_entrar.click()

    # ==========================================
    # ETAPA 2: NAVEGAÇÃO E DEFESAS ATIVAS
    # ==========================================
    fechar_popup_se_existir(driver, 4)
    resolver_desafio_matematico(driver, 3)

    # [PREENCHER_AQUI] O ID (ou mude para By.XPATH) do botão que inicia a busca pelas notas
    botao_busca = wait.until(EC.element_to_be_clickable((By.ID, "[PREENCHER_AQUI: ID_DO_BOTAO_DE_BUSCA]")))
    try:
        botao_busca.click()
    except ElementClickInterceptedException:
        print("Clique na busca interceptado. Verificando bloqueios...")
        fechar_popup_se_existir(driver, 2)
        resolver_desafio_matematico(driver, 2)
        botao_busca.click()

    # ==========================================
    # ETAPA 3: FILTRAGEM DAS NOTAS FISCAIS
    # ==========================================
    # [PREENCHER_AQUI] XPath genérico que representa CADA LINHA da tabela de notas
    wait.until(EC.presence_of_element_located((By.XPATH, "[PREENCHER_AQUI: XPATH_DA_LINHA_DA_NOTA]")))
    linhas_notas = driver.find_elements(By.XPATH, "[PREENCHER_AQUI: XPATH_DA_LINHA_DA_NOTA]")
    
    dados_autorizados = []

    for linha in linhas_notas:
        try:
            # [PREENCHER_AQUI] XPath da coluna status. Mantenha o ".//"
            status = linha.find_element(By.XPATH, ".//[PREENCHER_AQUI: XPATH_COLUNA_STATUS]").text.strip().lower()

            if "autorizada" in status:
                # [PREENCHER_AQUI] XPath da coluna número da nota. Mantenha o ".//"
                numero_nota = linha.find_element(By.XPATH, ".//[PREENCHER_AQUI: XPATH_COLUNA_NUMERO_NOTA]").text
                dados_autorizados.append(numero_nota)
                print(f"Coletado: {numero_nota}")
                
        except NoSuchElementException:
            continue

    print(f"Total de notas autorizadas prontas para exportação: {len(dados_autorizados)}")

    # ==========================================
    # ETAPA 4: INSERIR NO SEGUNDO SITE
    # ==========================================
    if dados_autorizados:
        # [PREENCHER_AQUI] O link exato do site de destino
        driver.get("[PREENCHER_AQUI: LINK_DO_SEGUNDO_SITE]")
        
        # Tenta aceitar cookies também no segundo site, caso tenha
        aceitar_cookies_se_existir(driver, 4)
        fechar_popup_se_existir(driver, 3)
        resolver_desafio_matematico(driver, 3)

        for nota in dados_autorizados:
            # [PREENCHER_AQUI] O ID ou XPath do campo destino
            campo_destino = wait.until(EC.presence_of_element_located((By.ID, "[PREENCHER_AQUI: ID_CAMPO_DESTINO]")))
            campo_destino.clear()
            campo_destino.send_keys(nota)
            
            # [PREENCHER_AQUI] O XPath do botão para salvar
            botao_salvar = driver.find_element(By.XPATH, "[PREENCHER_AQUI: XPATH_BOTAO_SALVAR_DESTINO]")
            botao_salvar.click()
            
            time.sleep(1)

finally:
    driver.quit()
