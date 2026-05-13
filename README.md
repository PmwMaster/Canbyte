# FaceID Security

Sistema web FULLSTACK completo e funcional de reconhecimento facial.

## Tecnologias Utilizadas

**Backend:**
- Python 3
- Flask
- OpenCV (`opencv-python`)
- `face_recognition` (Dlib)
- SQLite
- SQLAlchemy (ORM)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5 (Dark Mode Customizado)
- Fetch API (Comunicação Assíncrona e Webcam em tempo real)

## Como Instalar

> **Pré-requisito (Windows):** A biblioteca `face_recognition` depende da compilação do `dlib`. É obrigatório ter o **Visual Studio Build Tools** (com suporte a C++) e o **CMake** instalados no Windows e adicionados à variável PATH do sistema.

1. Clone o repositório ou navegue até a pasta do projeto.
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\Activate.ps1
# No Linux/Mac:
source venv/bin/activate
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

Com o ambiente virtual ativado e as dependências instaladas, rode:
```bash
python app.py
```
Acesse o sistema no seu navegador: `http://localhost:5000`

## Estrutura do Projeto

```
/project
│
├── app.py                      # Arquivo principal do Flask e configurações
├── requirements.txt            # Dependências
├── README.md                   # Esta documentação
│
├── database/                   # Contém o arquivo SQLite
│   └── database.db
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── webcam.js
│   └── uploads/                # Imagens das faces salvas
│
├── templates/                  # Frontend (HTML)
│   ├── base.html
│   ├── index.html
│   ├── cadastro.html
│   ├── webcam.html
│   ├── upload_reconhecimento.html
│   ├── pessoas.html
│   └── dashboard.html
│
├── models/                     # Modelos de Banco de Dados
│   └── models.py
│
├── services/                   # Regras de Negócio e Processamento
│   ├── face_service.py
│   ├── recognition_service.py
│   └── webcam_service.py
│
└── routes/                     # Controladores e Endpoints
    ├── pessoas.py
    ├── reconhecimento.py
    └── dashboard.py
```

## Rotas (Endpoints Principais)
- `GET /`: Homepage
- `GET /dashboard`: Painel com métricas
- `GET /pessoas`: Listagem de cadastros
- `GET/POST /cadastro`: Cadastro de pessoa com upload de imagens
- `GET /webcam`: Interface de reconhecimento ao vivo
- `POST /api/reconhecer/frame`: Endpoint da API que processa os frames da webcam
- `GET/POST /upload-reconhecimento`: Busca de pessoas via upload manual de foto
- `POST /pessoas/excluir/<id>`: Excluir registro

## Prints Esperados
- **Homepage:** Interface limpa com atalhos para os módulos principais.
- **Cadastro:** Formulário escuro permitindo anexar múltiplos arquivos. As imagens serão gravadas localmente e o banco guardará o "encoding facial".
- **Dashboard:** Exibição de cards informativos e uma tabela atualizada com histórico dos últimos reconhecimentos (webcam ou upload).
- **Webcam:** Uso do Stream de Mídia (HTML5) gerando um canvas em overlay para eventuais caixas delimitadoras e uma sidebox (Último Reconhecimento) atualizada via AJAX.
