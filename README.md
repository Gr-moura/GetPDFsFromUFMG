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
- `WAITING_DOWNLOAD`: Tempo de espera para garantir que o download foi concluído (padrão: 5s)

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

Caso queira evitar que o monitor desligue automaticamente enquanto um programa está rodando, existem algumas opções dependendo do sistema operacional.

### macOS

No **macOS**, você pode usar o comando `caffeinate` (já disponível no sistema) para evitar que o computador entre em repouso enquanto o script roda.  

```sh
caffeinate python script.py
```

Esse comando manterá o computador **acordado** até que o script termine.

---

### Linux

No **Linux**, há algumas alternativas para impedir o desligamento da tela e a suspensão do sistema.

#### 1. Usando o comando `caffeinate` (se disponível)  

Algumas distribuições (ou instalações via `snap`/`apt`) oferecem o comando `caffeinate`. Se estiver instalado, você pode usá-lo da mesma forma que no macOS:  

```sh
caffeinate python script.py
```

#### 2. Usando o comando `xset`  

Se `caffeinate` **não estiver disponível**, você pode **desativar temporariamente o protetor de tela e o gerenciamento de energia (DPMS)** com o `xset`:  

```sh
# Desativa o screensaver e o DPMS
xset s off -dpms
python script.py
# Restaura as configurações (opcional)
xset s on +dpms
```

#### 3. Utilizando o aplicativo **Caffeine**  

Existe também o aplicativo **Caffeine** para Linux, que impede que o sistema entre em repouso enquanto estiver ativado. Consulte a documentação da sua distribuição para instalar e usar esse utilitário.

---

### Windows  

No **Windows**, as opções não são nativas via linha de comando, mas há algumas alternativas viáveis.

#### 1. Utilitário **Caffeine**  

O aplicativo **Caffeine** simula uma tecla pressionada a cada 59 segundos, evitando que o computador durma.  
Você pode baixá-lo e executá-lo enquanto roda o script.  

[Baixar Caffeine](https://www.zhornsoftware.co.uk/caffeine/)

#### 2. Alteração temporária das configurações de energia  

Você também pode, via **Prompt de Comando**, desativar o desligamento automático do monitor com o comando `powercfg`.  

#### Para impedir que o monitor desligue:

```cmd
powercfg /change monitor-timeout-ac 0
python script.py
```

**Importante**: Essa alteração afeta as configurações do sistema.  
Para restaurar as configurações originais (por exemplo, definir um tempo de 10 minutos), use:  

```cmd
powercfg /change monitor-timeout-ac 10
```

---

## Possíveis Erros e Soluções

### Erro ao abrir o navegador

Execute o seguinte comando para remover possíveis drivers corrompidos:

```sh
rm -rf ~/.wdm/drivers/geckodriver/mac64/v0.36.0/
```

### Credenciais não encontradas

Verifique se as variáveis de ambiente `UFMG_USERNAME` e `UFMG_PASSWORD` estão definidas corretamente.

### Tempo de espera excedido

Se o site estiver carregando lentamente, tente aumentar `WAITING_PAGE` e `WAITING_DOWNLOAD` para um valor maior.

