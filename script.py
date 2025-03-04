from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, shutil, time

# Obter credenciais das variáveis de ambiente
USERNAME = os.environ.get("UFMG_USERNAME")
PASSWORD = os.environ.get("UFMG_PASSWORD")
ARQUIVOS_DIR = os.path.expanduser("~/Downloads/UFMG_20241")
PERIODO = "20241"
WAITING_PAGE = 5
WAITING_DOWNLOAD = 2

visitedLinks = set()
breadcrumbsDict = dict()
failedLinks = set()

if not USERNAME or not PASSWORD:
    print(
        "\033[91m "
        + "Erro: Credenciais não encontradas nas variáveis de ambiente."
        + "\033[0m"
    )
    exit(1)


def AbrirNavegador(pathToDownload=ARQUIVOS_DIR):
    # Configurar o WebDriver do Firefox
    options = Options()

    # This line sets a Firefox preference so that downloads are saved to a custom directory.
    options.set_preference("browser.download.folderList", 2)

    # Configurar o diretório de downloads
    options.set_preference("browser.download.dir", pathToDownload)

    # Configurar o download automático de PDFs e notebooks
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/pdf,application/x-ipynb+json",
    )

    options.enable_downloads = True

    # Desativar o visualizador de PDFs integrado
    options.set_preference("pdfjs.disabled", True)

    service = FirefoxService(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=service, options=options)
    browser.set_page_load_timeout(WAITING_PAGE)
    return browser


def AcessarPagina(browser, url):
    # Acessar a página
    browser.get(url)

    try:
        # Esperar até que os campos de login estejam visíveis
        username_field = WebDriverWait(browser, WAITING_PAGE).until(
            EC.presence_of_element_located((By.ID, "j_username"))
        )
        password_field = browser.find_element(By.ID, "j_password")
        submit_button = browser.find_element(By.ID, "submit")

        # Preencher e enviar o formulário de login
        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        submit_button.click()

    except Exception as e:
        print("\033[91m" + f"Erro durante o login ou busca de turmas: {e}" + "\033[0m")
        browser.quit()


def CriarPastas(caminhoBase, nomesPastas):
    caminhoAtual = caminhoBase
    for nome in nomesPastas:
        caminhoAtual = os.path.join(caminhoAtual, nome)
        os.makedirs(caminhoAtual, exist_ok=True)
    print(f"Estrutura de pastas criada em: {caminhoBase}")


def ExtrairBreadcrumbs(browser):
    try:
        breadcrumbItems = browser.find_elements(
            By.CSS_SELECTOR, "ol.breadcrumb li.breadcrumb-item"
        )
        return [item.text.strip() for item in breadcrumbItems if item.text.strip()]

    except Exception as e:
        print("\033[91m" + f"Erro ao extrair os breadcrumbs: {e}" + "\033[0m")
        return []


def GuardarArquivosCriados(urlPai, dirInicial=ARQUIVOS_DIR):
    arquivos = os.listdir(dirInicial)
    for fileName in arquivos:
        filePath = os.path.join(dirInicial, fileName)

        if not os.path.isfile(filePath):
            continue

        print("Arquivo encontrado: ", fileName)

        # Extrair breadcrumbs
        breadcrumbs = breadcrumbsDict[urlPai]
        print("Breadcrumbs: ", breadcrumbs)

        # Criar pastas
        CriarPastas(dirInicial, breadcrumbs)

        # Mover arquivo
        try:
            shutil.move(filePath, os.path.join(dirInicial, *breadcrumbs))
        except Exception as e:
            print("\033[91m " + f"Erro ao mover o arquivo {fileName}: {e}" + "\033[0m")
            try:
                os.remove(filePath)
                print("\033[91m" + f"Arquivo {fileName} removido." + "\033[0m")
            except Exception as e:
                print(
                    "\033[91m"
                    + f"Erro ao remover o arquivo {fileName}: {e}"
                    + "\033[0m"
                )
            continue

        print(
            "\033[92m" + f"Arquivo {fileName} baixado e movido com sucesso!" + "\033[0m"
        )
        print("\033[92m" + f"Arquivo proveniente de {urlPai} !" + "\033[0m")


def isValid(link, urlAtual):
    return (
        link
        and (
            # Um dos possiveis  tipos de links
            ("https://virtual.ufmg.br/" + PERIODO + "/course/view") in link
            or ("https://virtual.ufmg.br/" + PERIODO + "/mod/folder/view") in link
            or ("https://virtual.ufmg.br/" + PERIODO + "/mod/resource/view") in link
            or ("https://virtual.ufmg.br/" + PERIODO + "/pluginfile.php") in link
        )
        and link not in visitedLinks
        and (urlAtual + "#") not in link
    )


def PegarLinksPagina(browser, urlAtual):
    links = set()
    try:
        # Wait for links to load
        WebDriverWait(browser, WAITING_PAGE).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        for tag in browser.find_elements(By.TAG_NAME, "a"):
            link = tag.get_attribute("href")
            if isValid(link, urlAtual) and link not in links:
                print("\033[93m" + f"Adicionado link: {link}" + "\033[0m")
                links.add(link)

    except Exception as e:
        print("\033[91m" + f"Erro ao pegar os links da página {urlAtual}" + "\033[0m")

    return links


def ExistemArquivosNovos(qtArquivosAntes, urlAtual):
    tempoInicio = time.time()
    qtArquivosDepois = len(os.listdir(ARQUIVOS_DIR))

    while (qtArquivosDepois == qtArquivosAntes) and (
        time.time() - tempoInicio
    ) < WAITING_PAGE:
        qtArquivosDepois = len(os.listdir(ARQUIVOS_DIR))

    if qtArquivosAntes == qtArquivosDepois:
        return False

    return True


def PegarLinksRecursivamente(browser, urlAtual, urlPai, depth):
    if urlAtual in visitedLinks:
        return

    visitedLinks.add(urlAtual)
    qtArquivosAntes = len(os.listdir(ARQUIVOS_DIR))

    try:
        print(f"Acessando a página: {urlAtual} | Profundidade: {depth}")
        browser.get(urlAtual)

    except Exception as e:
        if ExistemArquivosNovos(qtArquivosAntes, urlAtual):
            GuardarArquivosCriados(urlPai)
            return
        else:
            print("\033[91m" + f"Erro ao carregar a página {urlAtual}: {e}" + "\033[0m")
            failedLinks.add(urlAtual)
            return

    links = PegarLinksPagina(browser, urlAtual)
    breadcrumbsDict[urlAtual] = ExtrairBreadcrumbs(browser)

    # Iterar recursivamente pelos links encontrados
    linksOrdenados = list(links)
    linksOrdenados.sort()
    for link in linksOrdenados:
        PegarLinksRecursivamente(browser, link, urlAtual, depth + 1)


def main():
    url = "https://virtual.ufmg.br/minhasturmas"

    # Criar o diretório de downloads
    os.makedirs(ARQUIVOS_DIR, exist_ok=True)

    # Abrir o navegador
    browser = AbrirNavegador()
    AcessarPagina(browser, url)

    # Pegar os links recursivamente
    PegarLinksRecursivamente(browser, url, url, 0)

    # Printar os links que falharam
    print("\033[91m" + "Links que falharam:" + "\033[0m")
    for link in failedLinks:
        print("\033[91m" + link + "\033[0m")

    browser.quit()


if __name__ == "__main__":
    main()
