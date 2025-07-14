# Dify Local Project Memory Bank

Este documento resume as configurações, problemas encontrados e soluções aplicadas durante a configuração do ambiente Dify local para o projeto de análise de NF-e.

## 1. Objetivo do Projeto

- Configurar um ambiente de desenvolvimento Dify localmente usando Docker.
- Resolver problemas de autenticação de banco de dados para garantir que todos os serviços funcionem corretamente.
- Limpar completamente o ambiente para garantir uma instalação nova e sem dados antigos.
- Criar uma base de conhecimento no Dify e importar dados de NF-e (Nota Fiscal Eletrônica) para análise.

## 2. Configuração do Ambiente

- **Diretório do Projeto Dify:** `/Users/kaauanmatzenbacher/CascadeProjects/dify/`
- **Diretório Docker:** `/Users/kaauanmatzenbacher/CascadeProjects/dify/docker/`
- **Arquivo de Variáveis de Ambiente:** `docker/.env`
- **Arquivo de Template do Docker Compose:** `docker/docker-compose-template.yaml`
- **Diretório de Dados NF-e:** `/Users/kaauanmatzenbacher/CascadeProjects/nfe/data/json`

## 3. Problemas e Soluções

### Problema 1: Falha de Autenticação do `plugin_daemon`

- **Sintoma:** O contêiner `plugin_daemon` reiniciava em loop com o erro `password authentication failed for user "postgres"`.
- **Causa Raiz:** O serviço estava configurado no `docker-compose-template.yaml` para se conectar a um banco de dados separado (`DB_PLUGIN_DATABASE=dify_plugin`) que não usava a senha principal definida em `DB_PASSWORD`.
- **Solução:** Editamos o `docker-compose-template.yaml` para que o `plugin_daemon` usasse a variável `DB_DATABASE` (`dify`), garantindo que ele se conectasse ao banco de dados principal com as credenciais corretas.

### Problema 2: Persistência de Dados e Falha ao Resetar o Dify

- **Sintoma:** Mesmo após executar `docker compose down --volumes`, a interface do Dify não mostrava a tela de configuração inicial (`/install`) e redirecionava para a tela de login (`/signin`), indicando que os dados antigos ainda existiam.
- **Causa Raiz:** O Dify utiliza "bind mounts" (pastas locais) para persistir dados, que não são removidos pelo comando `docker compose down --volumes`. Os dados não estavam apenas no volume do banco de dados (`db`), mas também no cache do **Redis** (`redis`), que guardava o estado de "instalação concluída".
- **Solução (A Limpeza Definitiva):**
    1. Parar todos os contêineres: `docker compose down`
    2. Remover manualmente **todo o conteúdo** da pasta de volumes que armazena os dados persistentes de todos os serviços: `rm -rf /Users/kaauanmatzenbacher/CascadeProjects/dify/docker/volumes/*`

## 4. Comandos e URLs Essenciais

- **Para Iniciar os Serviços:**
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose up -d

- **Para Parar os Serviços:**
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose down

- **Para Limpar os Volumes:**
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose down --volumes

- **Para Limpar os Volumes e Remover os Contêineres:**
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose down --volumes --remove-orphans


URL Principal (Após Instalação): http://localhost