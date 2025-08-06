# sistemamovemarias

# Prompt para Desenvolvimento de Sistema com GitHub Copilot

## Objetivo Geral

Desenvolver um sistema web moderno, funcional e com uma interface de usuário bonita, capaz de gerenciar e automatizar o preenchimento e a geração de documentos baseados nos formulários fornecidos. O sistema deve ser intuitivo, responsivo e garantir a integração de dados entre os diferentes módulos, além de estar em conformidade com a LGPD.

## Stack Tecnológico Proposto

Para atender aos requisitos de modernidade, funcionalidade e escalabilidade, a seguinte stack tecnológica é proposta:

- **Backend:** Python com o framework Flask. Flask é leve, flexível e ideal para a construção de APIs RESTful. Utilizaremos SQLAlchemy para a modelagem de dados e Marshmallow para serialização/desserialização.
- **Banco de Dados:** PostgreSQL. Um banco de dados relacional robusto, de código aberto, conhecido por sua confiabilidade, integridade de dados e capacidade de lidar com grandes volumes de informações.
- **Frontend:** React. Uma biblioteca JavaScript popular para a construção de interfaces de usuário interativas e dinâmicas. Será utilizada para criar uma experiência de usuário fluida e responsiva.
- **Containerização:** Docker e Docker Compose. Para facilitar o desenvolvimento, a implantação e a escalabilidade do sistema, garantindo que o ambiente de execução seja consistente em diferentes máquinas.

## Arquitetura do Sistema

A arquitetura será baseada em um modelo cliente-servidor, com o frontend (React) consumindo dados e funcionalidades expostas por uma API RESTful (Flask).




### Detalhes da Arquitetura:

1.  **API RESTful (Backend - Flask):**
    *   Responsável por gerenciar a lógica de negócios, a interação com o banco de dados e a exposição dos dados para o frontend.
    *   Endpoints bem definidos para operações CRUD (Create, Read, Update, Delete) em cada entidade (Beneficiária, Declaração, Anamnese, etc.).
    *   Autenticação baseada em tokens (JWT) para proteger as rotas da API.
    *   Validação de dados de entrada para garantir a integridade.

2.  **Frontend (React):**
    *   Interface de usuário intuitiva e responsiva, adaptável a diferentes dispositivos (desktop, tablet, mobile).
    *   Componentes reutilizáveis para formulários, tabelas, modais e outros elementos da UI.
    *   Gerenciamento de estado eficiente (e.g., com React Context ou Redux).
    *   Consumo da API do backend para exibir e manipular dados.
    *   Geração de documentos preenchidos no lado do cliente ou através de chamadas à API para o backend.

3.  **Banco de Dados (PostgreSQL):**
    *   Armazenará todas as informações das beneficiárias, registros de formulários, histórico de evolução, etc.
    *   Relacionamentos bem definidos entre as tabelas para garantir a consistência dos dados.
    *   Índices para otimização de consultas.

4.  **Docker:**
    *   Um `Dockerfile` para o backend Flask, contendo todas as dependências e configurações necessárias.
    *   Um `docker-compose.yml` para orquestrar o backend, o frontend e o banco de dados, facilitando a configuração do ambiente de desenvolvimento e produção.

## Modelagem de Dados (Esquema do Banco de Dados)

A seguir, a modelagem de dados detalhada para as principais entidades do sistema. O GitHub Copilot deve usar essas definições para auxiliar na criação dos modelos SQLAlchemy no backend e na estrutura dos dados no frontend.

### Entidade: `Usuario`
Representa os usuários do sistema (profissionais, administradores).

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `nome`            | String        | Nome completo do usuário                      | Not Null          |
| `email`           | String        | Endereço de e-mail do usuário                 | Not Null, Único   |
| `senha_hash`      | String        | Hash da senha do usuário                      | Not Null          |
| `tipo_usuario`    | Enum          | Tipo de usuário (e.g., 'admin', 'profissional') | Not Null          |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |
| `data_atualizacao`| Timestamp     | Data e hora da última atualização             | Default: now()    |

### Entidade: `Beneficiaria`
Representa a beneficiária atendida pelo instituto.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `nome_completo`   | String        | Nome completo da beneficiária                 | Not Null          |
| `cpf`             | String        | CPF da beneficiária                           | Not Null, Único   |
| `rg`              | String        | RG da beneficiária                            |                   |
| `orgao_emissor_rg`| String        | Órgão emissor do RG                           |                   |
| `data_emissao_rg` | Date          | Data de emissão do RG                         |                   |
| `data_nascimento` | Date          | Data de nascimento da beneficiária            | Not Null          |
| `idade`           | Integer       | Idade da beneficiária (calculada)             |                   |
| `endereco`        | String        | Endereço completo                             |                   |
| `bairro`          | String        | Bairro                                        |                   |
| `nis`             | String        | Número de Identificação Social                |                   |
| `contato1`        | String        | Telefone de contato principal                 | Not Null          |
| `contato2`        | String        | Telefone de contato secundário                |                   |
| `referencia`      | String        | Referência (como chegou ao instituto)         |                   |
| `data_inicio_instituto`| Date          | Data de início no Instituto                   |                   |
| `programa_servico`| String        | Programa/Oficina/Serviço                      |                   |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |
| `data_atualizacao`| Timestamp     | Data e hora da última atualização             | Default: now()    |

### Entidade: `DeclaracaoComparecimento`
Corresponde ao formulário `declaraçao-modelo2.docx` (primeira parte).

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `data_comparecimento`| Date          | Data do comparecimento                        | Not Null          |
| `hora_entrada`    | Time          | Horário de entrada                            |                   |
| `hora_saida`      | Time          | Horário de saída                              |                   |
| `profissional_responsavel`| String        | Nome da profissional responsável              | Not Null          |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `ReciboBeneficio`
Corresponde ao formulário `declaraçao-modelo2.docx` (segunda parte).

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `tipo_beneficio`  | String        | Descrição do benefício recebido               | Not Null          |
| `data_recebimento`| Date          | Data de recebimento do benefício              | Not Null          |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `AnamneseSocial`
Corresponde ao formulário `ANAMNESESOCIAL.docx`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `data_anamnese`   | Date          | Data da anamnese                              | Not Null          |
| `observacoes_importantes`| Text          | Observações gerais                            |                   |
| `uso_alcool`      | Boolean       | Faz uso de álcool?                            | Default: False    |
| `uso_drogas_ilicitas`| Boolean       | Faz uso de drogas ilícitas?                   | Default: False    |
| `uso_cigarros`    | Boolean       | Faz uso de cigarros?                          | Default: False    |
| `uso_outros`      | String        | Outros usos (se aplicável)                    |                   |
| `transtorno_mental_desenvolvimento`| Boolean       | Alguém na família com transtorno mental/desenvolvimento? | Default: False    |
| `desafios_transtorno`| Text          | Desafios relacionados ao transtorno           |                   |
| `deficiencia`     | Boolean       | Alguém na família com deficiência?            | Default: False    |
| `desafios_deficiencia`| Text          | Desafios relacionados à deficiência           |                   |
| `idosos_dependentes`| Boolean       | Idosos ou pessoas dependentes na família?     | Default: False    |
| `desafios_idosos` | Text          | Desafios relacionados a idosos/dependentes    |                   |
| `doenca_cronica_degenerativa`| Boolean       | Alguém com doença crônica ou degenerativa?    | Default: False    |
| `desafios_doenca` | Text          | Desafios relacionados à doença                |                   |
| `vulnerabilidades`| Array de String| Lista de vulnerabilidades (NIS, Desemprego, etc.) |                   |
| `assinatura_beneficiaria`| Boolean       | Beneficiária assinou?                         | Default: False    |
| `assinatura_tecnica`| Boolean       | Técnica assinou?                              | Default: False    |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `MembroFamiliar`
Relacionada à `AnamneseSocial` para a seção de situação socioeconômica familiar.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `anamnese_id`     | UUID          | Chave estrangeira para `AnamneseSocial`       | FK, Not Null      |
| `nome`            | String        | Nome do membro familiar                       | Not Null          |
| `data_nascimento` | Date          | Data de nascimento                            |                   |
| `idade`           | Integer       | Idade (calculada)                             |                   |
| `trabalha`        | Boolean       | Trabalha?                                     | Default: False    |
| `renda`           | Numeric       | Renda mensal                                  |                   |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `FichaEvolucao`
Corresponde ao formulário `FICHADEEVOLUÇÃO.docx`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `data_evolucao`   | Date          | Data da evolução                              | Not Null          |
| `descricao`       | Text          | Descrição da evolução/movimentação            | Not Null          |
| `responsavel`     | String        | Nome do responsável pelo registro             | Not Null          |
| `assinatura_beneficiaria`| Boolean       | Beneficiária assinou?                         | Default: False    |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `TermoConsentimento`
Corresponde ao formulário `TCLE.docx`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `data_consentimento`| Date          | Data do consentimento                         | Not Null          |
| `nacionalidade`   | String        | Nacionalidade                                 |                   |
| `estado_civil`    | String        | Estado civil                                  |                   |
| `uso_imagem_autorizado`| Boolean       | Autorização para uso da imagem                | Not Null          |
| `tratamento_dados_autorizado`| Boolean       | Autorização para tratamento de dados (LGPD)   | Not Null          |
| `assinatura_voluntaria`| Boolean       | Voluntária assinou?                           | Default: False    |
| `assinatura_responsavel_familiar`| Boolean       | Responsável familiar assinou?                 | Default: False    |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `VisaoHolistica`
Corresponde ao formulário `VISÃOHOLÍSTICA.docx`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `historia_vida`   | Text          | História de vida da beneficiária              |                   |
| `rede_apoio`      | Text          | Rede de apoio da beneficiária                 |                   |
| `visao_tecnica_referencia`| Text          | Visão da técnica de referência                |                   |
| `encaminhamento_projeto`| Text          | Encaminhamento para o projeto                 |                   |
| `data_visao`      | Date          | Data da visão holística                       | Not Null          |
| `assinatura_tecnica`| Boolean       | Técnica assinou?                              | Default: False    |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `RodaVida`
Corresponde ao formulário `RODADAVIDAINDIVIDUAL.pdf`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `data_roda`       | Date          | Data da avaliação da Roda da Vida             | Not Null          |
| `espiritualidade_score`| Integer       | Pontuação de 1 a 10 para Espiritualidade      | 1-10              |
| `saude_score`     | Integer       | Pontuação de 1 a 10 para Saúde                | 1-10              |
| `lazer_score`     | Integer       | Pontuação de 1 a 10 para Lazer                | 1-10              |
| `equilibrio_emocional_score`| Integer       | Pontuação de 1 a 10 para Equilíbrio Emocional | 1-10              |
| `vida_social_score`| Integer       | Pontuação de 1 a 10 para Vida Social          | 1-10              |
| `relacionamento_familiar_score`| Integer       | Pontuação de 1 a 10 para Relacionamento Familiar | 1-10              |
| `recursos_financeiros_score`| Integer       | Pontuação de 1 a 10 para Recursos Financeiros | 1-10              |
| `amor_score`      | Integer       | Pontuação de 1 a 10 para Amor                 | 1-10              |
| `contribuicao_social_score`| Integer       | Pontuação de 1 a 10 para Contribuição Social  | 1-10              |
| `proposito_score` | Integer       | Pontuação de 1 a 10 para Propósito            | 1-10              |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `PlanoAcaoPersonalizado`
Corresponde ao formulário `PLANODEAÇÃOPERSONALIZADO.pdf`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `objetivos`       | Text          | Objetivos do plano de ação                    | Not Null          |
| `acoes`           | Text          | Ações a serem realizadas                      | Not Null          |
| `prazos`          | String        | Prazos para as ações                          |                   |
| `responsaveis`    | String        | Responsáveis pelas ações                      |                   |
| `resultados_esperados`| Text          | Resultados esperados                          |                   |
| `acompanhamento`  | Text          | Detalhes do acompanhamento                    |                   |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

### Entidade: `MatriculaProjetoSocial`
Corresponde ao formulário `MATRÍCULADEPROJETOSSOCIAIS.docx`.

| Campo             | Tipo de Dados | Descrição                                     | Restrições        |
| :---------------- | :------------ | :-------------------------------------------- | :---------------- |
| `id`              | UUID          | Chave primária, identificador único           | PK, Not Null      |
| `beneficiaria_id` | UUID          | Chave estrangeira para `Beneficiaria`         | FK, Not Null      |
| `nome_projeto`    | String        | Nome do projeto social                        | Not Null          |
| `data_inicio_projeto`| Date          | Data de início do projeto                     | Not Null          |
| `data_termino_projeto`| Date          | Data de término do projeto                    |                   |
| `carga_horaria`   | String        | Carga horária do projeto                      |                   |
| `escolaridade`    | String        | Escolaridade do participante                  |                   |
| `profissao`       | String        | Profissão do participante                     |                   |
| `renda_familiar`  | Numeric       | Renda familiar do participante                |                   |
| `observacoes_matricula`| Text          | Observações adicionais da matrícula           |                   |
| `assinatura_participante`| Boolean       | Participante assinou?                         | Default: False    |
| `assinatura_coordenador`| Boolean       | Coordenador assinou?                          | Default: False    |
| `data_criacao`    | Timestamp     | Data e hora de criação do registro            | Default: now()    |

## Funcionalidades Detalhadas

O sistema deve implementar as seguintes funcionalidades, com foco na usabilidade e na automação dos processos:

### 1. Autenticação e Autorização
- **Login de Usuários:** Permite que profissionais e administradores acessem o sistema.
- **Gerenciamento de Usuários:** Administradores podem criar, editar e desativar contas de usuários.
- **Controle de Acesso Baseado em Papéis (RBAC):** Diferentes níveis de acesso para 'admin' e 'profissional', garantindo que cada usuário veja e interaja apenas com as informações relevantes para sua função.

### 2. Gestão de Beneficiárias
- **Cadastro de Beneficiárias:** Formulário para inserir novas beneficiárias com todos os dados da entidade `Beneficiaria`.
- **Visualização de Beneficiárias:** Lista paginada e pesquisável de todas as beneficiárias cadastradas.
- **Edição de Beneficiárias:** Capacidade de atualizar as informações de uma beneficiária existente.
- **Exclusão de Beneficiárias:** Funcionalidade para remover registros de beneficiárias (com confirmação e, se necessário, arquivamento lógico).
- **PAEDI (Pasta de Atendimento e Desenvolvimento Individual):** Uma página dedicada para cada beneficiária, agregando todos os formulários e informações relacionadas a ela. Esta página deve ser a 


central para o acompanhamento individual, incluindo o número do PAEDI conforme a `CAPA.pdf`.

### 3. Preenchimento e Gestão de Formulários

Cada formulário será representado por uma interface de usuário dedicada, permitindo o preenchimento, edição e visualização dos dados. A integração entre os formulários deve ser automática, preenchendo campos comuns (como nome da beneficiária, CPF) sempre que possível.

-   **Declaração de Comparecimento:**
    *   Formulário para registro de comparecimentos com campos para nome, CPF, PAEDI, data, hora de entrada/saída e profissional responsável.
    *   Geração de PDF/DOCX da declaração preenchida.
-   **Recibo de Benefício:**
    *   Formulário para registro de recebimento de benefícios com campos para nome, CPF, PAEDI, tipo de benefício e data.
    *   Geração de PDF/DOCX do recibo preenchido.
-   **Anamnese Social:**
    *   Formulário completo com seções para identificação, situação socioeconômica familiar (tabela dinâmica para membros da família), biopsicossocial e vulnerabilidades.
    *   Campos de texto para observações e desafios.
    *   Opções de múltipla escolha para vulnerabilidades.
    *   Registro de assinaturas (beneficiária e técnica).
-   **Ficha de Evolução da Beneficiária:**
    *   Interface para adicionar novos registros de evolução com data, descrição e responsável.
    *   Visualização cronológica de todas as evoluções de uma beneficiária.
    *   Espaço para registro de assinatura da beneficiária/responsável.
-   **Termo de Consentimento Livre e Esclarecido (TCLE):**
    *   Formulário para autorização de uso de imagem e tratamento de dados pessoais (LGPD).
    *   Campos para dados pessoais, detalhes da autorização e registro de assinaturas (voluntária e responsável familiar).
-   **Visão Holística:**
    *   Formulário com campos de texto para história de vida, rede de apoio, visão da técnica de referência e encaminhamento para o projeto.
    *   Registro de assinatura da técnica e data.
-   **Roda da Vida Individual:**
    *   Interface para preenchimento da Roda da Vida, permitindo que o usuário insira pontuações de 1 a 10 para cada área (Espiritualidade, Saúde, Lazer, Equilíbrio Emocional, Vida Social, Relacionamento Familiar, Recursos Financeiros, Amor, Contribuição Social, Propósito).
    *   Visualização gráfica da Roda da Vida preenchida (idealmente um gráfico de radar ou similar).
    *   Geração de PDF/imagem da Roda da Vida preenchida.
-   **Plano de Ação Personalizado:**
    *   Formulário para definir objetivos, ações, prazos, responsáveis, resultados esperados e acompanhamento.
    *   Geração de PDF/DOCX do plano preenchido.
-   **Matrícula de Projetos Sociais:**
    *   Formulário para registro de matrícula em projetos sociais com dados do projeto e do participante.
    *   Campos para informações adicionais como escolaridade, profissão, renda familiar e observações.
    *   Registro de assinaturas (participante e coordenador).

### 4. Geração de Documentos e Relatórios

O sistema deve ser capaz de gerar os documentos preenchidos em formato PDF ou DOCX, utilizando os dados inseridos nos formulários. Isso inclui:

-   Declaração de Comparecimento
-   Recibo de Benefício
-   Anamnese Social
-   Ficha de Evolução da Beneficiária
-   Termo de Consentimento (Uso de Imagem e LGPD)
-   Visão Holística
-   Roda da Vida Individual (com representação gráfica)
-   Plano de Ação Personalizado
-   Matrícula de Projetos Sociais

Além disso, o sistema deve oferecer relatórios básicos, como:

-   **Relatório de Beneficiárias:** Lista de beneficiárias com filtros por status, programa, etc.
-   **Relatório de Atendimentos:** Sumário de comparecimentos e benefícios concedidos.
-   **Dashboard:** Visão geral com métricas importantes (e.g., número de beneficiárias ativas, formulários preenchidos, vulnerabilidades mais comuns).

### 5. Conformidade com a LGPD

O sistema deve ser projetado com a Lei Geral de Proteção de Dados (LGPD) em mente, garantindo:

-   **Consentimento Explícito:** O TCLE digitalizado deve ser o registro do consentimento.
-   **Segurança dos Dados:** Implementação de medidas de segurança para proteger os dados pessoais (criptografia, controle de acesso).
-   **Direitos do Titular:** Funcionalidades para permitir que o titular dos dados exerça seus direitos (acesso, correção, exclusão).
-   **Anonimização/Pseudonimização:** Considerar a possibilidade de anonimizar dados para relatórios e análises.

## Considerações de Design (UI/UX)

O sistema deve ser moderno, funcional e bonito, com foco em uma excelente experiência do usuário:

-   **Interface Intuitiva:** Navegação clara e fácil de usar, com um fluxo lógico para o preenchimento dos formulários.
-   **Design Responsivo:** O layout deve se adaptar perfeitamente a diferentes tamanhos de tela (desktops, laptops, tablets e smartphones).
-   **Paleta de Cores:** Sugere-se uma paleta de cores suave e profissional, com cores primárias que transmitam confiança e secundárias para destaque de elementos interativos. Evitar cores muito vibrantes ou que causem fadiga visual.
-   **Tipografia:** Escolha de fontes legíveis e modernas, com hierarquia clara para títulos, subtítulos e corpo de texto.
-   **Componentes UI:** Utilização de uma biblioteca de componentes UI (e.g., Material-UI, Ant Design, Chakra UI) para garantir consistência visual, agilizar o desenvolvimento e oferecer componentes pré-construídos de alta qualidade (botões, campos de entrada, tabelas, modais, etc.).
-   **Feedback Visual:** Mensagens claras de sucesso, erro e validação. Indicadores de carregamento (loaders) para operações demoradas.
-   **Acessibilidade:** Considerar padrões de acessibilidade (WCAG) para garantir que o sistema possa ser utilizado por pessoas com diferentes necessidades.

## Estrutura de Pastas (Sugestão para o GitHub Copilot)

```
. (raiz do projeto)
├── backend/
│   ├── app.py             # Aplicação Flask principal
│   ├── config.py          # Configurações da aplicação
│   ├── models.py          # Definições dos modelos de dados (SQLAlchemy)
│   ├── schemas.py         # Esquemas de serialização/desserialização (Marshmallow)
│   ├── routes/            # Módulos para rotas da API (separados por funcionalidade)
│   │   ├── auth.py
│   │   ├── beneficiarias.py
│   │   └── forms.py
│   ├── services/          # Lógica de negócio e interação com o banco de dados
│   ├── utils/             # Funções utilitárias (e.g., geração de PDF, helpers de data)
│   └── requirements.txt   # Dependências do backend
├── frontend/
│   ├── public/            # Arquivos estáticos (index.html)
│   ├── src/
│   │   ├── App.js         # Componente principal da aplicação
│   │   ├── index.js       # Ponto de entrada do React
│   │   ├── assets/        # Imagens, ícones, etc.
│   │   ├── components/    # Componentes React reutilizáveis (botões, inputs, cards)
│   │   ├── layouts/       # Layouts de página (sidebar, header, footer)
│   │   ├── pages/         # Páginas específicas para cada funcionalidade/formulário
│   │   │   ├── Auth/
│   │   │   ├── Beneficiarias/
│   │   │   ├── Forms/
│   │   │   └── Dashboard/
│   │   ├── services/      # Funções para chamadas à API (Axios ou Fetch API)
│   │   ├── contexts/      # Context API para gerenciamento de estado global
│   │   ├── hooks/         # Custom Hooks do React
│   │   ├── styles/        # Estilos globais e específicos de componentes
│   │   └── utils/         # Funções utilitárias do frontend
│   ├── package.json       # Dependências do frontend
│   └── .env               # Variáveis de ambiente do frontend
├── templates/             # Templates para geração de documentos (Jinja2, se usado no backend para HTML/PDF)
├── docker-compose.yml     # Orquestração de containers Docker
├── Dockerfile             # Dockerfile para o backend
├── .env                   # Variáveis de ambiente globais
├── README.md              # Documentação do projeto
└── .gitignore             # Arquivos a serem ignorados pelo Git
```

## Instruções para o GitHub Copilot

Com base na arquitetura, modelagem de dados e funcionalidades detalhadas acima, o GitHub Copilot deve ser capaz de auxiliar no desenvolvimento do sistema. O processo deve seguir as seguintes etapas:

1.  **Configuração Inicial:**
    *   Criar a estrutura de pastas sugerida.
    *   Configurar o `docker-compose.yml` para o backend (Flask), frontend (React) e banco de dados (PostgreSQL).
    *   Configurar o `Dockerfile` para o backend.
    *   Inicializar um projeto Flask básico no diretório `backend/`.
    *   Inicializar um projeto React básico no diretório `frontend/`.

2.  **Modelos de Dados (Backend):**
    *   Gerar os modelos SQLAlchemy em `backend/models.py` para cada entidade (`Usuario`, `Beneficiaria`, `DeclaracaoComparecimento`, `ReciboBeneficio`, `AnamneseSocial`, `MembroFamiliar`, `FichaEvolucao`, `TermoConsentimento`, `VisaoHolistica`, `RodaVida`, `PlanoAcaoPersonalizado`, `MatriculaProjetoSocial`), com base nas tabelas fornecidas.
    *   Incluir os relacionamentos entre os modelos (e.g., `Beneficiaria` com seus formulários).

3.  **Esquemas de Serialização (Backend):**
    *   Criar os esquemas Marshmallow em `backend/schemas.py` para cada modelo, permitindo a serialização de objetos Python para JSON e vice-versa.

4.  **Rotas da API (Backend):**
    *   Desenvolver as rotas da API RESTful em `backend/routes/` para cada funcionalidade CRUD (e.g., `/api/beneficiarias`, `/api/declaracoes`).
    *   Implementar a lógica de autenticação e autorização.

5.  **Serviços (Backend):**
    *   Criar a lógica de negócio em `backend/services/` para interagir com os modelos e o banco de dados.

6.  **Geração de Documentos (Backend/Utils):**
    *   Implementar funções em `backend/utils/` para gerar PDFs/DOCX preenchidos a partir de templates, utilizando bibliotecas Python (e.g., `python-docx`, `reportlab` ou `fpdf2`).

7.  **Componentes de UI (Frontend):**
    *   Desenvolver componentes React reutilizáveis em `frontend/src/components/` (e.g., `Input`, `Button`, `Table`, `Modal`).
    *   Integrar uma biblioteca de componentes UI (Material-UI, Ant Design, Chakra UI) conforme preferência.

8.  **Páginas (Frontend):**
    *   Criar as páginas React em `frontend/src/pages/` para cada formulário e funcionalidade (e.g., `BeneficiariasPage`, `AnamneseSocialForm`, `DashboardPage`).
    *   Implementar a lógica de formulários, validação e chamadas à API.

9.  **Serviços de API (Frontend):**
    *   Criar funções em `frontend/src/services/` para realizar chamadas à API do backend.

10. **Estilos (Frontend):**
    *   Definir estilos globais e específicos de componentes em `frontend/src/styles/`.

11. **Testes:**
    *   Escrever testes unitários e de integração para o backend e frontend.

12. **Documentação:**
    *   Manter o `README.md` atualizado com instruções de setup, uso e deploy.

O GitHub Copilot deve ser usado como um assistente inteligente, gerando sugestões de código para cada uma dessas etapas, desde a estrutura inicial até a implementação de funcionalidades complexas e a integração entre as partes do sistema. O foco deve ser em código limpo, modular e seguindo as melhores práticas de desenvolvimento.

---

# PLANO DE DESENVOLVIMENTO COMPLETO

## 📋 Visão Geral do Projeto

### Estimativa de Tempo Total: 16-20 semanas
### Metodologia: Desenvolvimento Ágil com Sprints de 2 semanas
### Equipe Recomendada: 3-4 desenvolvedores (1 Backend, 2 Frontend, 1 Fullstack/DevOps)

---

## 🚀 FASE 1: CONFIGURAÇÃO E INFRAESTRUTURA (Semanas 1-2)

### Sprint 1: Configuração do Ambiente de Desenvolvimento

#### 📦 1.1 Configuração Inicial do Projeto
**Tempo estimado: 2-3 dias**

- [ ] **Estrutura de Diretórios**
  - Criar estrutura de pastas conforme especificação
  - Configurar workspace para desenvolvimento colaborativo
  - Estabelecer convenções de nomenclatura

- [ ] **Controle de Versão**
  - Configurar repositório Git
  - Definir estratégia de branching (GitFlow)
  - Configurar hooks de pre-commit

#### 🐳 1.2 Containerização com Docker
**Tempo estimado: 3-4 dias**

- [ ] **Docker Configuration**
  - Criar `Dockerfile` para backend Flask
  - Criar `Dockerfile` para frontend React
  - Configurar `docker-compose.yml` para orquestração
  - Configurar volumes para desenvolvimento

- [ ] **Ambiente de Desenvolvimento**
  - Configurar hot-reload para backend e frontend
  - Configurar networking entre containers
  - Testar ambiente completo

#### 🗄️ 1.3 Configuração do Banco de Dados
**Tempo estimado: 2-3 dias**

- [ ] **PostgreSQL Setup**
  - Configurar container PostgreSQL
  - Criar schemas iniciais
  - Configurar backup automático
  - Configurar variáveis de ambiente

---

## 🏗️ FASE 2: BACKEND - API E MODELOS (Semanas 3-6)

### Sprint 2: Modelos de Dados e Configuração Base

#### 📊 2.1 Modelagem de Dados
**Tempo estimado: 5-6 dias**

- [ ] **Modelos SQLAlchemy**
  - [ ] Modelo `Usuario` com autenticação
  - [ ] Modelo `Beneficiaria` (entidade principal)
  - [ ] Modelo `DeclaracaoComparecimento`
  - [ ] Modelo `ReciboBeneficio`
  - [ ] Modelo `AnamneseSocial`
  - [ ] Modelo `MembroFamiliar`
  - [ ] Modelo `FichaEvolucao`
  - [ ] Modelo `TermoConsentimento`
  - [ ] Modelo `VisaoHolistica`
  - [ ] Modelo `RodaVida`
  - [ ] Modelo `PlanoAcaoPersonalizado`
  - [ ] Modelo `MatriculaProjetoSocial`

- [ ] **Relacionamentos e Constraints**
  - Definir relacionamentos entre modelos
  - Configurar foreign keys e constraints
  - Implementar validações de integridade
  - Configurar índices para performance

#### ⚙️ 2.2 Configuração Flask
**Tempo estimado: 3-4 dias**

- [ ] **App Configuration**
  - Configurar Flask app factory pattern
  - Configurar SQLAlchemy e Migrate
  - Configurar CORS para frontend
  - Configurar logging e error handling

- [ ] **Segurança**
  - Implementar JWT para autenticação
  - Configurar bcrypt para hash de senhas
  - Implementar middleware de segurança
  - Configurar rate limiting

### Sprint 3: APIs de Autenticação e Usuários

#### 🔐 3.1 Sistema de Autenticação
**Tempo estimado: 4-5 dias**

- [ ] **Authentication Routes**
  - POST `/api/auth/login` - Login de usuário
  - POST `/api/auth/register` - Registro (admin only)
  - POST `/api/auth/refresh` - Refresh token
  - POST `/api/auth/logout` - Logout
  - GET `/api/auth/me` - Dados do usuário atual

- [ ] **Authorization Middleware**
  - Middleware de verificação JWT
  - Decorators para controle de acesso
  - RBAC (Role-Based Access Control)

#### 👥 3.2 Gestão de Usuários
**Tempo estimado: 3-4 dias**

- [ ] **User Management Routes**
  - GET `/api/users` - Listar usuários
  - POST `/api/users` - Criar usuário
  - GET `/api/users/:id` - Obter usuário
  - PUT `/api/users/:id` - Atualizar usuário
  - DELETE `/api/users/:id` - Desativar usuário

### Sprint 4: APIs de Beneficiárias

#### 👩 4.1 CRUD de Beneficiárias
**Tempo estimado: 5-6 dias**

- [ ] **Beneficiarias Routes**
  - GET `/api/beneficiarias` - Listar com paginação/filtros
  - POST `/api/beneficiarias` - Criar beneficiária
  - GET `/api/beneficiarias/:id` - Obter beneficiária
  - PUT `/api/beneficiarias/:id` - Atualizar beneficiária
  - DELETE `/api/beneficiarias/:id` - Arquivar beneficiária

- [ ] **Advanced Features**
  - Busca por CPF, nome, NIS
  - Filtros por programa, data de cadastro
  - Cálculo automático de idade
  - Validação de CPF

#### 📋 4.2 PAEDI (Pasta Individual)
**Tempo estimado: 3-4 dias**

- [ ] **PAEDI Routes**
  - GET `/api/beneficiarias/:id/paedi` - Dados completos
  - GET `/api/beneficiarias/:id/formularios` - Lista formulários
  - GET `/api/beneficiarias/:id/historico` - Histórico de atendimentos

### Sprint 5: APIs de Formulários (Parte 1)

#### 📝 5.1 Formulários Básicos
**Tempo estimado: 6-7 dias**

- [ ] **Declaração de Comparecimento**
  - POST `/api/declaracoes` - Criar declaração
  - GET `/api/declaracoes` - Listar declarações
  - GET `/api/declaracoes/:id` - Obter declaração
  - PUT `/api/declaracoes/:id` - Atualizar declaração

- [ ] **Recibo de Benefício**
  - POST `/api/recibos` - Criar recibo
  - GET `/api/recibos` - Listar recibos
  - GET `/api/recibos/:id` - Obter recibo
  - PUT `/api/recibos/:id` - Atualizar recibo

- [ ] **Ficha de Evolução**
  - POST `/api/evolucoes` - Criar evolução
  - GET `/api/evolucoes` - Listar evoluções
  - GET `/api/evolucoes/:id` - Obter evolução
  - PUT `/api/evolucoes/:id` - Atualizar evolução

### Sprint 6: APIs de Formulários (Parte 2)

#### 📋 6.1 Formulários Complexos
**Tempo estimado: 7-8 dias**

- [ ] **Anamnese Social**
  - POST `/api/anamneses` - Criar anamnese
  - GET `/api/anamneses/:id` - Obter anamnese
  - PUT `/api/anamneses/:id` - Atualizar anamnese
  - POST `/api/anamneses/:id/membros` - Adicionar membro familiar
  - PUT `/api/membros/:id` - Atualizar membro familiar

- [ ] **Termo de Consentimento**
  - POST `/api/termos` - Criar termo
  - GET `/api/termos/:id` - Obter termo
  - PUT `/api/termos/:id` - Atualizar termo

- [ ] **Visão Holística**
  - POST `/api/visoes` - Criar visão
  - GET `/api/visoes/:id` - Obter visão
  - PUT `/api/visoes/:id` - Atualizar visão

#### 📊 6.2 Formulários Especiais
**Tempo estimado: 5-6 dias**

- [ ] **Roda da Vida**
  - POST `/api/roda-vida` - Criar avaliação
  - GET `/api/roda-vida/:id` - Obter avaliação
  - PUT `/api/roda-vida/:id` - Atualizar avaliação

- [ ] **Plano de Ação Personalizado**
  - POST `/api/planos` - Criar plano
  - GET `/api/planos/:id` - Obter plano
  - PUT `/api/planos/:id` - Atualizar plano

- [ ] **Matrícula em Projetos Sociais**
  - POST `/api/matriculas` - Criar matrícula
  - GET `/api/matriculas/:id` - Obter matrícula
  - PUT `/api/matriculas/:id` - Atualizar matrícula

---

## 🎨 FASE 3: FRONTEND - INTERFACE DE USUÁRIO (Semanas 7-12)

### Sprint 7: Configuração Frontend e Design System

#### ⚛️ 7.1 Setup React
**Tempo estimado: 3-4 dias**

- [ ] **React Configuration**
  - Configurar Create React App ou Vite
  - Configurar roteamento com React Router
  - Configurar gerenciamento de estado (Context API/Redux)
  - Configurar Axios para chamadas API

- [ ] **Development Tools**
  - Configurar ESLint e Prettier
  - Configurar Husky para hooks
  - Configurar ambiente de desenvolvimento

#### 🎨 7.2 Design System
**Tempo estimado: 4-5 dias**

- [ ] **UI Library Setup**
  - Escolher e configurar biblioteca UI (Material-UI/Ant Design/Chakra UI)
  - Configurar tema personalizado
  - Definir paleta de cores do projeto
  - Configurar tipografia

- [ ] **Base Components**
  - Criar componentes base reutilizáveis
  - Button, Input, Card, Modal, Table
  - Loading, Alert, Tooltip
  - Form components com validação

### Sprint 8: Autenticação e Layout

#### 🔐 8.1 Sistema de Autenticação Frontend
**Tempo estimado: 4-5 dias**

- [ ] **Auth Pages**
  - Página de Login
  - Página de Esqueci a Senha (futuro)
  - Proteção de rotas
  - Context de autenticação

- [ ] **Auth Services**
  - Service para login/logout
  - Interceptors para token
  - Refresh automático de token
  - Redirecionamento baseado em role

#### 🏗️ 8.2 Layout Principal
**Tempo estimado: 4-5 dias**

- [ ] **Layout Components**
  - Header com menu de usuário
  - Sidebar com navegação
  - Breadcrumbs
  - Footer

- [ ] **Navigation**
  - Menu lateral responsivo
  - Indicadores visuais de página ativa
  - Controle de acesso por role

### Sprint 9: Gestão de Beneficiárias

#### 👩 9.1 CRUD de Beneficiárias
**Tempo estimado: 6-7 dias**

- [ ] **Lista de Beneficiárias**
  - Tabela com paginação
  - Filtros avançados (nome, CPF, programa)
  - Busca em tempo real
  - Ordenação por colunas

- [ ] **Formulário de Beneficiária**
  - Formulário completo de cadastro
  - Validação em tempo real
  - Máscara para CPF, telefone
  - Cálculo automático de idade

- [ ] **Visualização Individual**
  - Card com dados principais
  - Histórico de atendimentos
  - Acesso rápido aos formulários

#### 📋 9.2 PAEDI (Pasta Individual)
**Tempo estimado: 5-6 dias**

- [ ] **Dashboard da Beneficiária**
  - Visão geral dos dados
  - Lista de formulários preenchidos
  - Cronologia de atendimentos
  - Indicadores visuais de progresso

- [ ] **Navegação entre Formulários**
  - Menu lateral com formulários
  - Indicação de formulários preenchidos
  - Navegação rápida entre seções

### Sprint 10: Formulários Básicos

#### 📝 10.1 Declaração e Recibo
**Tempo estimado: 5-6 dias**

- [ ] **Declaração de Comparecimento**
  - Formulário com seleção de beneficiária
  - Campos de data e hora
  - Seleção de profissional
  - Preview do documento

- [ ] **Recibo de Benefício**
  - Formulário de recibo
  - Seleção de tipo de benefício
  - Validação de dados
  - Histórico de benefícios

#### 📈 10.2 Ficha de Evolução
**Tempo estimado: 4-5 dias**

- [ ] **Formulário de Evolução**
  - Editor de texto rico
  - Campos obrigatórios
  - Assinatura digital
  - Histórico cronológico

- [ ] **Visualização de Histórico**
  - Timeline de evoluções
  - Filtros por data/responsável
  - Busca no conteúdo

### Sprint 11: Formulários Complexos (Parte 1)

#### 🏥 11.1 Anamnese Social
**Tempo estimado: 7-8 dias**

- [ ] **Formulário Principal**
  - Seções organizadas em abas/steps
  - Campos condicionais
  - Validação de seções
  - Auto-save

- [ ] **Gestão de Membros Familiares**
  - Tabela dinâmica de membros
  - Modal para adicionar/editar
  - Cálculo de renda total
  - Validações específicas

- [ ] **Seção de Vulnerabilidades**
  - Checkboxes organizados
  - Campos de observação condicionais
  - Indicadores visuais de risco

#### 📄 11.2 Termo de Consentimento
**Tempo estimado: 4-5 dias**

- [ ] **Formulário TCLE**
  - Texto do termo
  - Campos de autorização
  - Assinaturas digitais
  - Conformidade LGPD

### Sprint 12: Formulários Complexos (Parte 2)

#### 🎯 12.1 Visão Holística e Planos
**Tempo estimado: 6-7 dias**

- [ ] **Visão Holística**
  - Editor de texto rico para narrativas
  - Seções estruturadas
  - Assinatura da técnica
  - Templates predefinidos

- [ ] **Plano de Ação Personalizado**
  - Formulário estruturado por objetivos
  - Tabela de ações e prazos
  - Responsáveis e indicadores
  - Timeline visual

#### 📊 12.2 Roda da Vida
**Tempo estimado: 5-6 dias**

- [ ] **Interface da Roda da Vida**
  - Gráfico radar interativo
  - Sliders para pontuação (1-10)
  - Visualização em tempo real
  - Comparação histórica

- [ ] **Matrícula em Projetos**
  - Formulário de matrícula
  - Seleção de projetos disponíveis
  - Campos específicos do projeto
  - Assinaturas digitais

---

## 📄 FASE 4: GERAÇÃO DE DOCUMENTOS (Semanas 13-14)

### Sprint 13: Sistema de Geração de Documentos

#### 📄 13.1 Backend - Geração de PDFs
**Tempo estimado: 6-7 dias**

- [ ] **PDF Generation Service**
  - Configurar ReportLab ou WeasyPrint
  - Templates para cada formulário
  - Sistema de merge de dados
  - Formatação profissional

- [ ] **Document Routes**
  - GET `/api/documentos/declaracao/:id/pdf`
  - GET `/api/documentos/recibo/:id/pdf`
  - GET `/api/documentos/anamnese/:id/pdf`
  - GET `/api/documentos/termo/:id/pdf`
  - GET `/api/documentos/visao/:id/pdf`
  - GET `/api/documentos/roda-vida/:id/pdf`
  - GET `/api/documentos/plano/:id/pdf`
  - GET `/api/documentos/matricula/:id/pdf`

#### 🖼️ 13.2 Roda da Vida Gráfica
**Tempo estimado: 3-4 dias**

- [ ] **Chart Generation**
  - Gerar gráfico radar da Roda da Vida
  - Exportar como imagem (PNG/SVG)
  - Integrar no PDF
  - Personalização visual

### Sprint 14: Frontend - Download e Preview

#### 💾 14.1 Download de Documentos
**Tempo estimado: 4-5 dias**

- [ ] **Download Features**
  - Botões de download em cada formulário
  - Preview antes do download
  - Loading states
  - Error handling

- [ ] **Bulk Operations**
  - Download múltiplos documentos
  - Geração de ZIP
  - Progress indicators

#### 📱 14.2 Mobile Optimization
**Tempo estimado: 3-4 dias**

- [ ] **Responsive Design**
  - Otimização para tablets
  - Menu mobile
  - Formulários responsivos
  - Touch-friendly interface

---

## 📊 FASE 5: RELATÓRIOS E DASHBOARD (Semanas 15-16)

### Sprint 15: Dashboard e Métricas

#### 📈 15.1 Dashboard Principal
**Tempo estimado: 5-6 dias**

- [ ] **Dashboard Components**
  - Cards de estatísticas principais
  - Gráficos de atendimentos por mês
  - Top vulnerabilidades
  - Status dos formulários

- [ ] **Real-time Data**
  - Atualização automática de dados
  - WebSocket ou polling
  - Cache inteligente

#### 📊 15.2 Relatórios Básicos
**Tempo estimado: 4-5 dias**

- [ ] **Reports Backend**
  - GET `/api/relatorios/beneficiarias`
  - GET `/api/relatorios/atendimentos`
  - GET `/api/relatorios/vulnerabilidades`
  - Filtros avançados

- [ ] **Reports Frontend**
  - Interface de geração de relatórios
  - Filtros por data, programa, status
  - Export para Excel/PDF

### Sprint 16: Finalização e Polimento

#### 🔧 16.1 Otimizações e Performance
**Tempo estimado: 4-5 dias**

- [ ] **Performance Optimization**
  - Lazy loading de componentes
  - Otimização de queries SQL
  - Caching de dados
  - Compressão de assets

- [ ] **SEO e Acessibilidade**
  - Meta tags apropriadas
  - ARIA labels
  - Navegação por teclado
  - Contraste de cores

#### 🧪 16.2 Testes e QA
**Tempo estimado: 4-5 dias**

- [ ] **Testing**
  - Testes unitários (backend)
  - Testes de integração
  - Testes de componentes (frontend)
  - Testes end-to-end

- [ ] **Quality Assurance**
  - Code review completo
  - Teste de usabilidade
  - Verificação de segurança
  - Documentação final

---

## 🚀 FASE 6: DEPLOY E PRODUÇÃO (Semanas 17-18)

### Sprint 17: Preparação para Produção

#### 🏗️ 17.1 Infrastructure as Code
**Tempo estimado: 5-6 dias**

- [ ] **Production Setup**
  - Docker Compose para produção
  - Nginx como proxy reverso
  - SSL/HTTPS configuration
  - Environment variables

- [ ] **Database Production**
  - PostgreSQL otimizado
  - Backup automático
  - Monitoring
  - Migrations strategy

#### 🔒 17.2 Segurança e LGPD
**Tempo estimado: 3-4 dias**

- [ ] **Security Hardening**
  - Helmet.js para headers de segurança
  - Rate limiting production
  - Input sanitization
  - SQL injection protection

- [ ] **LGPD Compliance**
  - Auditoria de dados pessoais
  - Logs de acesso
  - Funcionalidades de direitos do titular
  - Política de privacidade

### Sprint 18: Deploy e Go-Live

#### 🌐 18.1 Deploy Strategy
**Tempo estimado: 3-4 dias**

- [ ] **Deployment Pipeline**
  - CI/CD com GitHub Actions
  - Automated testing
  - Staging environment
  - Blue-green deployment

- [ ] **Monitoring and Logging**
  - Application monitoring
  - Error tracking (Sentry)
  - Performance monitoring
  - Health checks

#### 📚 18.2 Documentação e Treinamento
**Tempo estimado: 4-5 dias**

- [ ] **Documentation**
  - API documentation (Swagger)
  - User manual
  - Admin guide
  - Development guide

- [ ] **Training Materials**
  - Video tutorials
  - User workflows
  - FAQ section
  - Support documentation

---

## 📋 CHECKLIST DE QUALIDADE

### 🔍 Code Quality Standards

- [ ] **Backend Standards**
  - [ ] PEP 8 compliance
  - [ ] Type hints em funções críticas
  - [ ] Docstrings em todas as funções
  - [ ] Error handling consistente
  - [ ] Logging apropriado
  - [ ] Testes com cobertura > 80%

- [ ] **Frontend Standards**
  - [ ] ESLint rules seguidas
  - [ ] Componentes documentados
  - [ ] PropTypes ou TypeScript
  - [ ] Performance optimization
  - [ ] Accessibility compliance
  - [ ] Mobile responsiveness

### 🛡️ Security Checklist

- [ ] **Authentication & Authorization**
  - [ ] JWT implementation secure
  - [ ] Password hashing (bcrypt)
  - [ ] Role-based access control
  - [ ] Session management
  - [ ] Rate limiting

- [ ] **Data Protection**
  - [ ] Input validation
  - [ ] SQL injection prevention
  - [ ] XSS protection
  - [ ] CSRF protection
  - [ ] HTTPS enforcement

### 📊 Performance Benchmarks

- [ ] **Backend Performance**
  - [ ] API response time < 200ms
  - [ ] Database queries optimized
  - [ ] N+1 queries avoided
  - [ ] Caching implemented
  - [ ] Memory usage monitored

- [ ] **Frontend Performance**
  - [ ] Page load time < 3s
  - [ ] Bundle size optimized
  - [ ] Images optimized
  - [ ] Lazy loading implemented
  - [ ] Core Web Vitals met

### 🧪 Testing Strategy

- [ ] **Testing Coverage**
  - [ ] Unit tests > 80% coverage
  - [ ] Integration tests for critical paths
  - [ ] End-to-end tests for user journeys
  - [ ] Performance tests
  - [ ] Security tests

### 📱 Compatibility Requirements

- [ ] **Browser Support**
  - [ ] Chrome (latest 2 versions)
  - [ ] Firefox (latest 2 versions)
  - [ ] Safari (latest 2 versions)
  - [ ] Edge (latest 2 versions)

- [ ] **Device Support**
  - [ ] Desktop (1920x1080+)
  - [ ] Tablet (768x1024+)
  - [ ] Mobile (375x667+)

---

## 🚦 MILESTONES E ENTREGAS

### 🎯 Milestone 1 (Semana 6): MVP Backend
- ✅ API completa funcionando
- ✅ Autenticação implementada
- ✅ CRUD de beneficiárias
- ✅ Formulários básicos

### 🎯 Milestone 2 (Semana 12): MVP Frontend
- ✅ Interface completa
- ✅ Todos os formulários funcionando
- ✅ Navegação entre telas
- ✅ Responsividade básica

### 🎯 Milestone 3 (Semana 16): Sistema Completo
- ✅ Geração de documentos
- ✅ Dashboard e relatórios
- ✅ Otimizações de performance
- ✅ Testes completos

### 🎯 Milestone 4 (Semana 18): Produção
- ✅ Deploy em produção
- ✅ Monitoramento ativo
- ✅ Documentação completa
- ✅ Treinamento realizado

---

## 🛠️ FERRAMENTAS E TECNOLOGIAS

### Backend Stack
- **Framework**: Flask 2.3+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+
- **Serialization**: Marshmallow 3.0+
- **Authentication**: Flask-JWT-Extended
- **Validation**: Flask-WTF
- **PDF Generation**: ReportLab ou WeasyPrint
- **Testing**: pytest
- **Migration**: Flask-Migrate

### Frontend Stack
- **Framework**: React 18+
- **Build Tool**: Vite ou Create React App
- **Router**: React Router 6+
- **State Management**: React Context API
- **UI Library**: Material-UI, Ant Design ou Chakra UI
- **HTTP Client**: Axios
- **Forms**: Formik ou react-hook-form
- **Charts**: Chart.js ou Recharts
- **Testing**: Jest + React Testing Library

### DevOps & Tools
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry + Custom dashboards
- **Documentation**: Swagger + JSDoc
- **Code Quality**: ESLint, Prettier, Black, flake8

### Development Environment
- **IDE**: VS Code com extensões específicas
- **API Testing**: Postman ou Insomnia
- **Database Client**: pgAdmin ou DBeaver
- **Version Control**: Git com GitFlow

---

## 📝 OBSERVAÇÕES IMPORTANTES

### 🔄 Metodologia de Desenvolvimento
- **Sprints de 2 semanas** com reuniões diárias
- **Code review obrigatório** para todas as funcionalidades
- **Testes automatizados** antes do merge
- **Deploy contínuo** no ambiente de staging

### 📞 Comunicação e Colaboração
- Reuniões diárias de 15 minutos
- Sprint planning no início de cada sprint
- Sprint review e retrospective ao final
- Documentação atualizada continuamente

### 🎯 Critérios de Sucesso
- **Funcionalidade**: Todos os formulários operacionais
- **Performance**: Tempo de carregamento < 3s
- **Usabilidade**: Interface intuitiva e responsiva
- **Segurança**: Conformidade com LGPD
- **Manutenibilidade**: Código limpo e documentado

### ⚠️ Riscos e Mitigações
- **Complexidade dos formulários**: Desenvolvimento incremental
- **Integração frontend/backend**: Definição clara de APIs
- **Performance**: Otimizações desde o início
- **Segurança**: Revisões de segurança regulares
- **Prazo**: Buffer de 2 semanas incluído

Este plano de desenvolvimento serve como guia detalhado para a implementação do Sistema Move Marias, garantindo que todas as funcionalidades sejam entregues com qualidade e dentro do prazo estabelecido.

