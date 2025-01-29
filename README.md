# RAG PDF Reader

## Descrição do Projeto
O **RAG PDF Reader** é uma aplicação que implementa um sistema de Recuperação Aumentada por Geração (RAG), permitindo que usuários enviem arquivos PDF e façam perguntas sobre seu conteúdo. A resposta é gerada com base nas informações extraídas do documento, utilizando **modelos da OpenAI** para processar as consultas.

A aplicação funciona da seguinte maneira:
1. O PDF enviado é processado e dividido em chunks de texto.
2. Os chunks são armazenados em um **banco de dados vetorial** usando **ChromaDB**.
3. Quando o usuário faz uma pergunta, a aplicação recupera os textos mais relevantes e os passa para um **modelo de linguagem da OpenAI**, que gera a resposta.
4. A resposta é retornada ao usuário via API REST criada com **Flask**.

## Requisitos
Para executar este projeto, você precisa instalar as seguintes dependências:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` inclui:
- **Flask**: Framework para criar a API REST.
- **python-dotenv**: Gerenciamento de variáveis de ambiente.
- **langchain**: Biblioteca para interação com LLMs.
- **langchain-openai**: Conector do LangChain para os modelos da OpenAI.
- **langchain-community**: Componentes adicionais do LangChain.
- **chromadb**: Banco de dados vetorial usado para buscas semânticas.
- **PyPDF2**: Biblioteca para leitura de PDFs.
- **sentence-transformers**: Modelo de embeddings para transformar textos em vetores.

## Como Usar
1. Inicie a aplicação executando:
   ```bash
   python main.py
   ```
2. Envie um arquivo PDF e uma pergunta para a rota `/read_pdf` via requisição **POST**.
3. A aplicação processará o documento e responderá com base nas informações contidas no arquivo.

Esse projeto pode ser expandido para suportar múltiplos documentos, diferentes formatos de arquivos e integrações com outros modelos de IA para respostas ainda mais precisas.

