from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

navegador = webdriver.Chrome()

navegador.get("https://sip.pi.gov.br/sip/login.php?sigla_orgao_sistema=GOV-PI&sigla_sistema=SEI&infra_url=L3NlaS8=")

navegador.maximize_window()

usuario_login = navegador.find_element("id","txtUsuario")
usuario_login.click()
usuario_login.send_keys("juan.leal@agespisa.com.br")
senha_login = navegador.find_element("id","pwdSenha")
senha_login.click()
senha_login.send_keys("agespisa064@")
select_orgao = navegador.find_element("id","selOrgao")
select_orgao.click()

# aguarda o <select> ficar presente/ativável e seleciona
wait = WebDriverWait(navegador, 5)
select_orgao_el = wait.until(EC.element_to_be_clickable((By.ID, "selOrgao")))
select = Select(select_orgao_el)

select.select_by_visible_text("AGESPISA-PI")

entrar = navegador.find_element("id","Acessar")
entrar.click()

# XPath casa o <a> que contém um <span> com o texto exato
link_iniciar = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//ul[@id="infraMenu"]//a[.//span[normalize-space()="Iniciar Processo"]]')
    )
)
link_iniciar.click()

# Selecionar o tipo de processo (texto do link conforme a página)
tipo_processo = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//a[normalize-space()="Documento Oficial: Ofício, Memorando, Portaria, Edital, Instrução Normativa e outros"]')
    )
)
tipo_processo.click()

label_restrito = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="optRestrito"]')))
label_restrito.click()

hipotese_legal = navegador.find_element("id","selHipoteseLegal")
hipotese_legal.click()

# Hipótese Legal: selecionar no <select id="selHipoteseLegal">
sel_hipotese = wait.until(EC.element_to_be_clickable((By.ID, "selHipoteseLegal")))
select_hipotese = Select(sel_hipotese)

#doc_preparatorio = navegador.find_elements(By.XPATH, "//select[@id='selHipoteseLegal']/option[@value='3']")
#for doc in doc_preparatorio:
#    doc.click()

sel_hip = wait.until(EC.presence_of_element_located((By.ID, "selHipoteseLegal")))
navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", sel_hip)  # melhora estabilidade [web:113]

navegador.execute_script("""
const opt = document.querySelector("#selHipoteseLegal > option:nth-child(4)");
if (opt) {
  opt.selected = true;
  const sel = document.getElementById("selHipoteseLegal");
  sel.dispatchEvent(new Event("change", { bubbles: true }));
}
""")

abas = navegador.window_handles
navegador.switch_to.window(abas[0])

salvar_processo = navegador.find_element("id","btnSalvar")
salvar_processo.click()

wait = WebDriverWait(navegador, 15)


frame_proc = wait.until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[src*='acao=arvore_visualizar']")   
    )
)  

time.sleep(5)



