# Documentação do Script de Web Scraping com Selenium

## Visão Geral

Este script utiliza Selenium para automatizar a extração de arquivos do ambiente virtual da UFMG. Ele realiza login, navega entre as páginas e faz o download dos arquivos, organizando-os em pastas correspondentes.

## Configuração Inicial

Antes de executar o script, troque as variáveis UFMG_USERNAME e UFMG_PASSWORD pelo seu login e senha ou certifique-se de que as credenciais da UFMG estão configuradas como variáveis de ambiente:

### Configuração das variáveis de ambiente

**Linux/macOS:** Adicione as seguintes linhas ao arquivo `~/.bashrc` ou `~/.zshrc` e recarregue o shell:

```sh
export UFMG_USERNAME="seu_usuario"
export UFMG_PASSWORD="sua_senha"
```

Execute `source ~/.bashrc` ou `source ~/.zshrc` para aplicar as mudanças.

**Windows (cmd):**

```sh
setx UFMG_USERNAME "seu_usuario"
setx UFMG_PASSWORD "sua_senha"
```

Após configurar, reinicie o terminal para que as variáveis sejam aplicadas corretamente.

Caso essas variáveis não estejam configuradas, o script será encerrado com um erro.

## Dependências

As seguintes bibliotecas são utilizadas no script:

- `selenium`
- `webdriver_manager`
- `os`, `shutil`, `time`

Para instalar as dependências, utilize:

```sh
pip install selenium webdriver-manager
```

## Principais Configurações

- `ARQUIVOS_DIR`: Diretório onde os arquivos baixados serão armazenados (padrão: `~/Downloads/UFMG_20241`)
- `PERIODO`: Período acadêmico (padrão: `20241`)
- `WAITING_PAGE`: Tempo de espera máximo para carregamento de página (padrão: 5s)
- `WAITING_DOWNLOAD`: Tempo de espera para garantir que o download foi concluído (padrão: 2s)

## Funções Principais

### `AbrirNavegador(pathToDownload)`

Configura e inicia o navegador Firefox com as preferências de download, garantindo que os arquivos sejam baixados automaticamente para o diretório especificado. Define preferências para download automático de PDFs e notebooks.

### `AcessarPagina(browser, url)`

Acessa a URL especificada e executa o login no ambiente virtual da UFMG utilizando as credenciais fornecidas nas variáveis de ambiente.

### `CriarPastas(caminhoBase, nomesPastas)`

Cria uma estrutura de pastas baseada nos breadcrumbs extraídos da página, organizando os arquivos de forma estruturada.

### `ExtrairBreadcrumbs(browser)`

Obtém a estrutura de navegação da página atual para organizar os arquivos baixados de forma hierárquica.

### `GuardarArquivosCriados(urlPai, dirInicial)`

Move os arquivos baixados para as pastas correspondentes baseando-se na estrutura de navegação extraída.

### `isValid(link, urlAtual)`

Verifica se um link encontrado na página é válido para ser processado pelo script.

### `PegarLinksPagina(browser, urlAtual)`

Coleta todos os links válidos de uma página para navegação e download de arquivos.

### `ExistemArquivosNovos(qtArquivosAntes, urlAtual)`

Verifica se novos arquivos foram baixados comparando a quantidade de arquivos antes e depois de acessar uma página.

### `PegarLinksRecursivamente(browser, urlAtual, urlPai, depth)`

Executa a navegação recursiva pelos links da página, baixando arquivos e explorando outras seções do ambiente virtual.

### `main()`

Função principal que inicia o navegador, acessa a página principal e inicia a extração recursiva dos arquivos. Exibe também a lista de links que falharam ao serem acessados.

## Execução
Modifique a variável global PERIODO para o periodo em que queira baixar os arquivos:

```py
PERIODO = "20241"
```

Para executar o script, certifique-se de ativar um ambiente virtual Python (caso esteja utilizando um) e rode o seguinte comando no terminal:

```sh
python script.py
```

Certifique-se de que o navegador Firefox está instalado e atualizado.

## Possíveis Erros e Soluções

### Erro ao abrir o navegador

Execute o seguinte comando para remover possíveis drivers corrompidos:

```sh
rm -rf ~/.wdm/drivers/geckodriver/mac64/v0.36.0/
```

### Credenciais não encontradas

Verifique se as variáveis de ambiente `UFMG_USERNAME` e `UFMG_PASSWORD` estão definidas corretamente.

### Tempo de espera excedido

Se o site estiver carregando lentamente, tente aumentar `WAITING_PAGE` para um valor maior.

