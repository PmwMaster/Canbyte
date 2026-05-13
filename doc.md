# SISTEMA WEB DE RECONHECIMENTO FACIAL — PROMPT COMPLETO PARA ANTIGRAVITY

Crie um sistema web FULLSTACK completo e funcional de reconhecimento facial chamado **FaceID Security**.

O sistema deve possuir frontend moderno, backend estruturado, banco de dados, reconhecimento facial em tempo real via webcam e reconhecimento por upload de imagens.

Utilize arquitetura profissional e código limpo, organizado e escalável.

---

# STACK OBRIGATÓRIA

## Backend
- Python
- Flask
- OpenCV
- face_recognition
- SQLite
- SQLAlchemy

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5

---

# OBJETIVO DO SISTEMA

O sistema deve permitir:

1. Cadastro de pessoas
2. Upload de múltiplas imagens faciais
3. Processamento facial
4. Reconhecimento facial via webcam
5. Reconhecimento facial por upload de imagem
6. Exibição:
   - Nome da pessoa
   - ID da pessoa
   - Percentual de confiança

---

# ESTRUTURA DO PROJETO

Crie a estrutura abaixo:

/project
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database.db
│
├── static/
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── faces/
│
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   ├── webcam.html
│   ├── upload_reconhecimento.html
│   ├── pessoas.html
│   └── dashboard.html
│
├── models/
│   └── models.py
│
├── services/
│   ├── face_service.py
│   ├── recognition_service.py
│   └── webcam_service.py
│
└── routes/
    ├── pessoas.py
    ├── reconhecimento.py
    └── dashboard.py

---

# FUNCIONALIDADES OBRIGATÓRIAS

## 1. TELA INICIAL

Criar homepage moderna contendo:

- Menu de navegação
- Cards de funcionalidades
- Botões:
  - Cadastro de Pessoas
  - Reconhecimento Webcam
  - Reconhecimento por Imagem
  - Lista de Pessoas
  - Dashboard

Design moderno responsivo.

---

# 2. CADASTRO DE PESSOAS

Criar tela de cadastro contendo:

Campos:
- ID automático
- Nome
- CPF
- Upload de múltiplas fotos faciais

Regras:
- Validar se existe rosto na imagem
- Não permitir imagens sem rosto
- Salvar imagens em:
  /static/uploads
- Armazenar dados no banco SQLite

O sistema deve:
- Extrair encoding facial automaticamente
- Salvar encoding para reconhecimento posterior

---

# 3. BANCO DE DADOS

Criar tabelas:

## tabela pessoas
- id
- nome
- cpf
- data_cadastro

## tabela imagens
- id
- pessoa_id
- caminho_imagem

## tabela historico_reconhecimento
- id
- pessoa_id
- confianca
- data_hora
- origem (webcam/upload)

Usar SQLAlchemy ORM.

---

# 4. RECONHECIMENTO POR WEBCAM

Criar página que:

- Solicita acesso à webcam
- Captura vídeo em tempo real
- Detecta rostos ao vivo
- Compara com banco de faces
- Exibe:
  - Nome
  - ID
  - Confiança

Funcionalidades:
- Quadrado ao redor do rosto
- Nome acima do rosto
- Percentual de similaridade
- Atualização em tempo real

Utilizar:
- OpenCV
- face_recognition
- JavaScript getUserMedia()

---

# 5. RECONHECIMENTO POR UPLOAD

Criar página para envio de imagem.

O sistema deve:
- Detectar rostos na imagem enviada
- Comparar com banco facial
- Mostrar:
  - Nome encontrado
  - ID
  - Confiança
- Marcar rostos encontrados na imagem

---

# 6. DASHBOARD

Criar dashboard moderno com:

- Quantidade de pessoas cadastradas
- Total de imagens
- Reconhecimentos realizados
- Últimos reconhecimentos
- Gráficos estatísticos

Interface moderna usando Bootstrap.

---

# 7. LISTA DE PESSOAS

Criar tabela responsiva contendo:
- ID
- Nome
- CPF
- Quantidade de fotos
- Data de cadastro
- Botão visualizar
- Botão excluir

---

# 8. HISTÓRICO

Criar histórico de reconhecimentos contendo:
- Pessoa reconhecida
- Data/Hora
- Confiança
- Origem da identificação

---

# REQUISITOS TÉCNICOS

O sistema deve:

- Funcionar localmente
- Possuir frontend e backend separados
- Ter tratamento de erros
- Possuir código organizado
- Utilizar orientação a objetos
- Ser responsivo
- Ter comentários importantes
- Possuir arquitetura limpa

---

# INTERFACE

Crie interface moderna no estilo:
- Painel administrativo
- Dark mode elegante
- Cards com sombras
- Layout profissional
- Sidebar moderna
- Design semelhante SaaS profissional

Utilizar:
- Bootstrap 5
- Ícones Bootstrap Icons
- Animações suaves

---

# IMPLEMENTE TAMBÉM

## Extras
- Login administrativo
- Controle de sessão
- API REST
- Exportação PDF
- Reconhecimento múltiplo
- Detecção de múltiplos rostos
- Sistema de logs

---

# README

Gerar README.md completo contendo:

- Explicação do projeto
- Tecnologias utilizadas
- Como instalar
- Como executar
- Estrutura do projeto
- Rotas
- Prints esperados
- Dependências

---

# REQUIREMENTS.TXT

Gerar automaticamente:

flask
opencv-python
face_recognition
numpy
sqlalchemy
flask_sqlalchemy
pillow

---

# IMPORTANTE

O projeto deve:
- Estar totalmente funcional
- Sem código fictício
- Sem placeholders
- Com backend real
- Com reconhecimento facial real
- Com webcam funcional
- Com rotas Flask funcionando
- Com frontend completo
- Com CSS profissional
- Com JavaScript funcional

---

# OBJETIVO FINAL

Entregar um sistema completo pronto para:
- rodar localmente,
- cadastrar pessoas,
- reconhecer rostos via webcam,
- reconhecer rostos via upload,
- salvar histórico,
- utilizar banco de dados,
- apresentar interface moderna e profissional.