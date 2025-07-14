# Dify Local Project Memory Bank

## 1. Objetivo do Projeto

O objetivo principal é criar uma base de conhecimento no Dify para importar e analisar dados de Notas Fiscais Eletrônicas (NF-e).

## 2. Configuração Essencial

- **Diretório do Projeto:** `/Users/kaauanmatzenbacher/CascadeProjects/dify/`
- **Diretório Docker:** `docker/`
- **Diretório de Dados NF-e:** `/Users/kaauanmatzenbacher/CascadeProjects/nfe/data/json`

## 3. Comandos Importantes

- **Iniciar o Dify:**
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose up -d
  ```

- **Parar o Dify:**
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose down
  ```

- **Reset Completo do Ambiente:**
  *Para garantir uma instalação 100% limpa, é necessário apagar manualmente a pasta de volumes.*
  ```bash
  cd /Users/kaauanmatzenbacher/CascadeProjects/dify/docker
  docker compose down
  rm -rf volumes/*
  ```

- **URL de Acesso:** `http://localhost`