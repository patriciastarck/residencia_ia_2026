# 1.1 Descrição do Problema

### Qual é o problema que você deseja resolver?
Resgatar dados de antigos prontuários para identificar doenças pré-existentes que possam resultar em complicações durante a consulta odontológica. Por exemplo: se o paciente é cardiopata e hipertenso, é fundamental mapear os medicamentos em uso contínuo e as possíveis interações medicamentosas decorrentes da administração de determinados tipos de anestésicos.

---

### Quem utilizaria a aplicação?
* **Cargo:** Cirurgião-Dentista (Clínico Geral ou Especialista).
* **Contexto de uso:** Consultório odontológico, antes de iniciar o plano de tratamento ou *chairside* (ao lado da cadeira clínica) durante a anamnese e procedimentos cirúrgicos.
* **Nível técnico:** Usuário final sem conhecimento avançado de programação; familiarizado com interfaces web e prontuários eletrônicos padrão.

---

### Que tipo de informação o usuário gostaria de consultar?
* Reações adversas a medicamentos administrados no consultório.
* Riscos de hemorragia e protocolos de hemostasia.
* Indicações e contraindicações de anestésicos locais (ex.: pacientes com trombofilia em uso de anticoagulantes).
* Protocolos clínicos para pacientes sistemicamente comprometidos.

---

### De onde vêm essas informações?
* **Dados proprietários/clínicos:** Prontuários médicos e odontológicos dos pacientes (fichas de anamnese, evoluções clínicas e laudos prévios).
* **Bases de conhecimento e órgãos oficiais:**
  * ANVISA (Bulário Eletrônico e monografias)
  * Conselho Federal de Odontologia (CFO)
  * Sociedade Brasileira de Cardiologia (SBC) e demais sociedades de especialidades médicas
  * BVS Odontologia / PubMed / SciELO

---

### Por que utilizar um LLM sozinho não seria suficiente?
* **Privacidade e LGPD:** Modelos pré-treinados não possuem acesso a dados clínicos privados e sensíveis dos pacientes, que exigem armazenamento seguro e sigilo.
* **Prevenção de Alucinações:** Em contexto de saúde, alucinações sobre dosagens e contraindicações podem causar danos irreversíveis; o RAG garante ancoragem estrita aos documentos recuperados.
* **Rastreabilidade e Validação:** O RAG fornece a citação da fonte exata (prontuário ou diretriz clínica) para que o dentista confirme a conduta antes da intervenção.

---

### Como o usuário vai utilizar o sistema?
* **Interface:** Aplicação Web responsiva integrada diretamente ao Prontuário Eletrônico do Paciente (PEP).
* **Consumo de Serviços:** A interface consome uma **API REST** para envio das consultas e recuperação contextual das respostas.

---

### Perguntas Reais de Usuários (Exemplos Práticos)
> 1. *"Existe interação medicamentosa entre o medicamento Losartana e o anestésico Mepivacaína?"*
> 2. *"Qual seria o anestésico mais apropriado para paciente com histórico de cardiopatia isquêmica?"*
> 3. *"Quais antibióticos são indicados para tratar abscesso periapical agudo neste paciente alérgico a penicilina?"*