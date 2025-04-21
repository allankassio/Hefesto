# 🛠️ Hefesto Game Lab

Sistema automatizado para geração de **Game Design Documents (GDDs)**, **código JavaScript educacional** e **artefatos desplugados**, usando **modelos de linguagem** executados localmente via Docker com [Ollama](https://ollama.com).

---

## 📁 1. Configure os modelos no `.env`

Antes de tudo, crie um arquivo `.env` na raiz do projeto e defina os modelos desejados:

```env
LLM_TEXT_MODEL=deepseek-r1
LLM_CODE_MODEL=deepseek-coder-v2
LLM_API_BASE_URL=http://llm:11434/v1
```

Você pode escolher **um modelo para linguagem geral** e **um modelo para código**.
Lembre-se que quanto maior e mais parâmetros tiver o modelo, mais recursos computacionais ele vai exigir, 
em compensação, mais eficiente e detalhado será o GDD gerado.

### 🔤 Modelos de linguagem geral disponíveis:

- `llama2`, `llama2:13b`, `llama2:70b`
- `llama3.1`, `llama3.2`, `llama3.3`
- `mistral`, `mistral-nemo`
- `gemma:2b`, `gemma:7b`, `gemma3:12b`, `gemma3:27b`
- `phi`, `phi4`, `phi4-mini`
- `deepseek-r1`, `deepseek-r1:671b`
- `qwen`, `qwen2`, `qwen2.5`
- `mixtral:8x7b`, `mixtral:8x22b`
- `starling-lm`, `neural-chat`, `olmo2`

### 💻 Modelos para geração de código:

- `codellama`
- `starcoder2`
- `qwen2.5-coder`
- `deepseek-coder-v2`

---

## 🧱 2. Construa a imagem base do servidor de modelos (Ollama)

Este projeto usa um `Dockerfile.base` customizado para configurar o servidor de modelos com suporte a CUDA ou CPU.
É importante executar esse Dockerfile antes pois ele gera uma imagem com todo recurso pesado. 
Evitando fazer download de várias dependências novamente.

Execute:

```bash
docker build -f Dockerfile.base -t mybase:cu12 .
```

> Isso cria a imagem `mybase:cu12`, usada pelo serviço `llm` no Docker Compose.

---

## 🚀 3. Execute os serviços

Você pode rodar **os serviços separadamente** ou **todos juntos** com o Docker Compose:

### ✅ Rodar tudo junto (recomendado):

```bash
docker compose up --build
```

### 🔧 Ou rodar separadamente:

- Primeiro, iniciar o servidor de modelos:

  ```bash
  docker compose up --build llm
  ```

- Em outro terminal, iniciar o app Streamlit:

  ```bash
  docker compose up --build app
  ```

---

## 🌐 Acessar a aplicação

Depois de iniciar os serviços, abra o navegador em:

```
http://localhost:8501
```

---

## 🧩 Funcionalidades

- Geração de GDDs com base em pilares do pensamento computacional
- Geração de código JavaScript educacional com modelos especializados
- Geração de artefatos desplugados para atividades offline
- Download dos arquivos gerados (`.md`, `.js`, `.txt`)
- Botões para gerar novamente, voltar e reiniciar
- Seleção de modelos por `.env` sem editar código

---

Claro! Aqui está um trecho institucional que você pode incluir no final do `README.md`:

---

## 🎓 Sobre a Pesquisa

Este sistema faz parte da pesquisa de doutorado de **Allan Kassio Beckman Soares da Cruz**, 
desenvolvida no **Programa de Pós-Graduação em Ciência da Computação da Universidade Federal do Maranhão (DCCMAPI/UFMA)**, 
sob orientação do **Professor Dr. Carlos de Salles Soares Neto**.

O objetivo da pesquisa é investigar o uso de **modelos de linguagem (LLMs)** e **experiências gamificadas** como apoio 
ao ensino de **pensamento computacional**, com foco em **prototipação automática de jogos educacionais** e **artefatos instrucionais**.