from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

navegador = webdriver.Chrome()

navegador.get("https://sip.pi.gov.br/sip/login.php?sigla_orgao_sistema=GOV-PI&sigla_sistema=SEI&infra_url=L3NlaS8=")

navegador.maximize_window()
time.sleep(2)

usuario_login = navegador.find_element("id","txtUsuario")
usuario_login.click()
time.sleep(1)

usuario_login.send_keys("juan.leal@agespisa.com.br")
senha_login = navegador.find_element("id","pwdSenha")
senha_login.click()
time.sleep(1)

senha_login.send_keys("agespisa064@")
select_orgao = navegador.find_element("id","selOrgao")
select_orgao.click()
time.sleep(1)

wait = WebDriverWait(navegador, 5)
select_orgao_el = wait.until(EC.element_to_be_clickable((By.ID, "selOrgao")))
select = Select(select_orgao_el)
time.sleep(2)

select.select_by_visible_text("AGESPISA-PI")

time.sleep(3)

entrar = navegador.find_element("id","Acessar")
entrar.click()

time.sleep(2)


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

time.sleep(3)


label_restrito = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="optRestrito"]')))
label_restrito.click()

time.sleep(3)


hipotese_legal = navegador.find_element("id","selHipoteseLegal")
hipotese_legal.click()

time.sleep(3)


sel_hipotese = wait.until(EC.element_to_be_clickable((By.ID, "selHipoteseLegal")))
select_hipotese = Select(sel_hipotese)
time.sleep(2)


#doc_preparatorio = navegador.find_elements(By.XPATH, "//select[@id='selHipoteseLegal']/option[@value='3']")
#for doc in doc_preparatorio:
#    doc.click()

sel_hip = wait.until(EC.presence_of_element_located((By.ID, "selHipoteseLegal")))
navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", sel_hip)  # melhora estabilidade [web:113]
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

salvar_processo = navegador.find_element("id","btnSalvar")
salvar_processo.click()
time.sleep(3)

wait = WebDriverWait(navegador, 15)


frame_proc = wait.until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[src*='acao=arvore_visualizar']")   
    )
)  
time.sleep(3)

wait.until(EC.presence_of_element_located((By.ID, "divInfraAreaTelaD")))  

btn_incluir_doc = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='divArvoreAcoes']//a[.//img[@alt='Incluir Documento']]")
    )
)



navegador.execute_script("arguments.scrollIntoView({block:'center'});", btn_incluir_doc)
time.sleep(3)

btn_incluir_doc.click()  


time.sleep(5)



#def switch_to_process_iframe(navegador, wait):
#    try:
#        wait.until(EC.frame_to_be_available_and_switch_to_it(
 #           (By.CSS_SELECTOR, "iframe[id*='ifrVisualizacao']")))
  #      return True
   # except TimeoutException:
    #    pass

 #   driver.switch_to.default_content()
 #   for idx in range(0, 5):
 #       try:
 #           navegador.switch_to.frame(idx)
 #           if len(navegador.find_elements(By.ID, "divInfraAreaTelaD")) > 0:
 #               return True
 #       except Exception:
 #           navegador.switch_to.default_content()
 #           continue

 #   navegador.switch_to.default_content()
 #   all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
 #   for fr in all_iframes:
 #       navegador.switch_to.default_content()
 #       navegador.switch_to.frame(fr)
 #       if len(navegador.find_elements(By.ID, "divInfraAreaTelaD")) > 0:
 #           return True

  #  navegador.switch_to.default_content()
   # return False

#Opcao 2
#def find_incluir_documento(driver, wait):
#    locators = [
#        (By.XPATH, "//div[@id='divArvoreAcoes']//a[contains(@href,'acao=documento_escolher_tipo')]"),
#        (By.XPATH, "//div[@id='divArvoreAcoes']//a[.//img[@alt='Incluir Documento']]"),
#        (By.XPATH, "//div[@id='divArvoreAcoes']//a[contains(@onmouseover,'Incluir Documento')]"),
#    ]
#    last_err = None
#    for how, what in locators:
#        try:
#            el = wait.until(EC.element_to_be_clickable((how, what)))
#            return el
#        except Exception as e:
#            last_err = e
#    raise last_err
