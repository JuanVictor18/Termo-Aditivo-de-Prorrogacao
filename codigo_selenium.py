from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

navegador = webdriver.Chrome()

navegador.get("https://sip.pi.gov.br/sip/login.php?sigla_orgao_sistema=GOV-PI&sigla_sistema=SEI&infra_url=L3NlaS8=")

navegador.maximize_window()
time.sleep(2)

usuario_login = navegador.find_element("id","txtUsuario")
usuario_login.click()
usuario_login.send_keys("juan.leal@agespisa.com.br")
time.sleep(1)

senha_login = navegador.find_element("id","pwdSenha")
senha_login.click()
senha_login.send_keys("agespisa064@")
time.sleep(1)

select_orgao = navegador.find_element("id","selOrgao")
select_orgao.click()
time.sleep(1)

wait = WebDriverWait(navegador, 5)
select_orgao_el = wait.until(EC.element_to_be_clickable((By.ID, "selOrgao")))
select = Select(select_orgao_el)

select.select_by_visible_text("AGESPISA-PI")
time.sleep(2)

entrar = navegador.find_element("id","Acessar")
entrar.click()
time.sleep(3)

link_iniciar = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//ul[@id="infraMenu"]//a[.//span[normalize-space()="Iniciar Processo"]]')
    )
)
link_iniciar.click()
time.sleep(2)

tipo_processo = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//a[normalize-space()="Documento Oficial: Ofício, Memorando, Portaria, Edital, Instrução Normativa e outros"]')
    )
)
tipo_processo.click()
time.sleep(2)

label_restrito = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="optRestrito"]')))
label_restrito.click()
time.sleep(1)

hipotese_legal = navegador.find_element("id","selHipoteseLegal")
hipotese_legal.click()
time.sleep(1)

sel_hipotese = wait.until(EC.element_to_be_clickable((By.ID, "selHipoteseLegal")))
select_hipotese = Select(sel_hipotese)
time.sleep(1)

sel_hip = wait.until(EC.presence_of_element_located((By.ID, "selHipoteseLegal")))
navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", sel_hip)
time.sleep(1)

navegador.execute_script("""
const opt = document.querySelector("#selHipoteseLegal > option:nth-child(4)");
if (opt) {
  opt.selected = true;
  const sel = document.getElementById("selHipoteseLegal");
  sel.dispatchEvent(new Event("change", { bubbles: true }));
}
""")
time.sleep(2)

abas = navegador.window_handles
navegador.switch_to.window(abas[0])
time.sleep(1)

salvar_processo = navegador.find_element("id","btnSalvar")
salvar_processo.click()
time.sleep(3)

wait = WebDriverWait(navegador, 15)

#incluir documento
frame_proc = wait.until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[src*='acao=arvore_visualizar']")   
    )
)
time.sleep(2)

wait.until(EC.presence_of_element_located((By.ID, "divInfraAreaTelaD")))  

btn_incluir_doc = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='divArvoreAcoes']//a[.//img[@alt='Incluir Documento']]")
    )
)

navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_incluir_doc)
time.sleep(1)

btn_incluir_doc.click()  
time.sleep(3)  # deixa visível no final

wait = WebDriverWait(navegador, 15)

mem_link = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//table[contains(@id,'tblSeries') or contains(@class,'infraTable')]//a[normalize-space()='Memorando']")
    )
)

navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", mem_link)
time.sleep(1)

mem_link.click()
time.sleep(3)

wait.until(EC.presence_of_element_located((By.ID, "fldTextoInicial")))

lbl_doc_modelo = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='optProtocoloDocumentoTextoBase']"))
)
navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", lbl_doc_modelo)
time.sleep(1)

lbl_doc_modelo.click()

campo_protocolo_modelo = wait.until(
    EC.presence_of_element_located((By.ID, "txtProtocoloDocumentoTextoBase"))
)
time.sleep(3)

wait.until(EC.presence_of_element_located((By.ID, "btnEscolherDocumentoTextoBase")))
time.sleep(2)

selecionar_modelo = navegador.find_element("id","btnEscolherDocumentoTextoBase")
selecionar_modelo.click()
time.sleep(5)

wait = WebDriverWait(navegador, 15)

container_fav = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@style,'Lista de Favoritos') or contains(@class,'infraAreaTabela') or contains(@class,'infraTable') or contains(.,'Lista de Favoritos')]")
    )
)

linha_modelo = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//table[contains(@class,'infraTable') or contains(@id,'infraTable')]"
        "//tr[td[contains(normalize-space(.),'Memorando Para Aditivo de Prorrogação de Contrato')]]"
    ))
)

navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", linha_modelo)
time.sleep(1)

navegador.maximize_window()
time.sleep(2)

icone_selecionar = linha_modelo.find_element(
    By.XPATH, ".//a[.//img[contains(@alt,'Selecionar este Favorito') or contains(@title,'Selecionar este Favorito')]]"
)

navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", icone_selecionar)
time.sleep(1)
icone_selecionar.click()

time.sleep(2)
wait.until(EC.invisibility_of_element_located(
    (By.XPATH, "//div[contains(.,'Lista de Favoritos')][contains(@class,'infraArea') or contains(@class,'infraDialog') or contains(@style,'position')]")
))

wait.until(EC.element_to_be_clickable((By.ID, "btnSalvar")))

abas = navegador.window_handles
navegador.switch_to.window(abas[0])
time.sleep(1)


time.sleep(3)