import re
import time
import requests 
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
            EC.element_to_be_clickable((By.XPATH, "<<<//*[@id="cookie-banner"]>>>"))
        )
        botao_cookies.click()
    except TimeoutException:
        pass

def fechar_popup_se_existir(driver, timeout=3):
    try:
        botao_fechar = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div/button"))
        )
        botao_fechar.click()
    except TimeoutException:
        pass

def resolver_desafio_matematico(driver, timeout=3):
    try:
        elemento_pergunta = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/div/form/label"))
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

            campo_resposta = driver.find_element(By.XPATH, "/html/body/main/div/form/input[2]")
            campo_resposta.clear()
            campo_resposta.send_keys(str(resultado))

            botao_confirmar = driver.find_element(By.XPATH, "/html/body/main/div/form/div/button")
            botao_confirmar.click()
            time.sleep(2)
    except TimeoutException:
        pass

# ==========================================
# INÍCIO DO FLUXO PRINCIPAL
# ==========================================
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
dados_autorizados = [] 

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

    botao_busca = wait.until(EC.element_to_be_clickable((By.ID, "/html/body/main/div[1]/form/div[3]/button")))
    try:
        botao_busca.click()
    except ElementClickInterceptedException:
        fechar_popup_se_existir(driver, 2)
        resolver_desafio_matematico(driver, 2)
        botao_busca.click()

    # ------------------------------------------
    # ETAPA 2: PAGINAÇÃO E EXTRAÇÃO
    # ------------------------------------------
    pagina_atual = 1

    while True:
        fechar_popup_se_existir(driver, 3)
        resolver_desafio_matematico(driver, 2)
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='resultados']/div[1]")))
        qtd_linhas = len(driver.find_elements(By.XPATH, "//*[@id='resultados']/div[1]"))
        
        for i in range(qtd_linhas):
            linhas_notas = driver.find_elements(By.XPATH, "//*[@id='resultados']/div[1]")
            linha = linhas_notas[i]
            
            try:
                status = linha.find_element(By.XPATH, ".//<<< PREENCHER_AQUI: XPATH_COLUNA_STATUS >>>").text.strip().lower()

                if "autorizada" in status:
                    # Correção de sintaxe: aspas simples dentro de aspas duplas e remoção dos colchetes
                    botao_abrir_nota = linha.find_element(By.XPATH, ".//*[@id='resultados']/div[1]/div[1]/a")
                    botao_abrir_nota.click()
                    
                    fechar_popup_se_existir(driver, 3)
                    resolver_desafio_matematico(driver, 2)

                    # Correção de sintaxe: remoção dos colchetes
                    chave_bruta = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[1]/table/tbody/tr[1]/td"))).text
                    # Limpa a chave para garantir apenas os 44 dígitos[cite: 1]
                    chave_limpa = re.sub(r'\D', '', chave_bruta) 
                    
                    valor = driver.find_element(By.XPATH, "/html/body/main/div[1]/table/tbody/tr[6]/td").text
                    
                    # Salva no formato exigido pela API[cite: 1]
                    dados_autorizados.append({'chave': chave_limpa, 'valor': valor}) 
                    
                    driver.back()
                    time.sleep(1)
                    
                    fechar_popup_se_existir(driver, 2)
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='resultados']/div[1]")))
                
            except NoSuchElementException:
                continue

        try:
            # Correção de sintaxe: aspas simples dentro de aspas duplas e remoção dos colchetes
            botao_proxima = driver.find_element(By.XPATH, "//*[@id='resultados']/div[2]/a")
            if botao_proxima.get_attribute("disabled") or "disabled" in botao_proxima.get_attribute("class"):
                break 
                
            botao_proxima.click()
            pagina_atual += 1
            time.sleep(2)
            
        except NoSuchElementException:
            break

finally:
    driver.quit()

# ==========================================
# ETAPA 3: ENVIO PARA A API (POST /api/submit)
# ==========================================
if dados_autorizados:
    url_api = "https://talkabit-z3eg.onrender.com/api/submit" # Endpoint de submissão do resultado[cite: 1]
    
    payload = {
        "teamToken": "BREAKINGBAD-VPJ7W", # Identifica sua equipe[cite: 1]
        "itens": dados_autorizados # Os pares extraídos[cite: 1]
    }
    
    headers = {
        "Content-Type": "application/json" 
    }

    try:
        resposta = requests.post(url_api, json=payload, headers=headers)
        
        print(f"Status da Resposta: {resposta.status_code}")
        print("Conteúdo da Resposta:", resposta.json())
        
        if resposta.status_code == 429:
            print("Limite de tentativas atingido ou cooldown ativo.") # Limite de 10 tentativas ou cooldown de 30s[cite: 1]
            
    except Exception as e:
        print(f"Erro ao enviar para a API: {e}")
