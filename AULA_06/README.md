# 1.1 Descrição do Problema

### Qual é o problema que você deseja resolver?
Resgatar dados de antigos prontuários para identificar doenças pré-existentes que possam resultar em complicações durante a consulta odontológica. Por exemplo: se o paciente é cardiopata e hipertenso, é fundamental mapear os medicamentos em uso contínuo e as possíveis interações medicamentosas decorrentes da administração de determinados tipos de anestésicos.

---

### Quem utilizaria a aplicação?
* **Cargo:** Cirurgião-Dentista.
* **Contexto de uso:** Consultório odontológico, antes de iniciar o plano de tratamento durante a anamnese e procedimentos cirúrgicos.
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
* **Privacidade e LGPD:** Modelos pré-treinados não possuem acesso a dados clínicos privados e sensíveis dos pacientes.
* **Prevenção de Alucinações:** Em contexto de saúde, alucinações sobre dosagens e contraindicações podem causar danos irreversíveis; o RAG garante ancoragem estrita aos documentos recuperados.
* **Rastreabilidade e Validação:** O RAG fornece a citação da fonte exata (prontuário ou diretriz clínica) para que o dentista confirme a conduta antes da intervenção.

---

### Como o usuário vai utilizar o sistema?
* **Interface:** Aplicação integrada diretamente ao Prontuário Eletrônico do Paciente.
* **Consumo de Serviços:** A interface consome uma API REST para envio das consultas e recuperação contextual das respostas.

---

### Perguntas Reais de Usuários (Exemplos Práticos)
> 1. *"Existe interação medicamentosa entre o medicamento Losartana e o anestésico Mepivacaína?"*
> 2. *"Qual seria o anestésico mais apropriado para paciente com histórico de cardiopatia isquêmica?"*
> 3. *"Quais antibióticos são indicados para tratar abscesso periapical agudo neste paciente alérgico a penicilina?"*

---

# Por que RAG é adequado para esse problema?
Para poder mesclar informações sigilosas de pacientes e informações públicas sem que as informações sensíveis sejam expostas.

# Que tipo de conhecimento precisa ser fornecido ao modelo?
Diretrizes e doocumentos oficiais, publicações em sites do Conselho Federal de Odontologia, regulamentações.

# Esse conhecimento muda com que frequência? (diariamente, mensalmente, quase nunca?)
O conhecimento pode mudar com variadas frequência, por exemplo, diariamente através de alertas que podem ser emitidos, mensalmente por meio de novas publicações incluídas nas bases de dados e anualmente por atualizações Normas e Resoluções feitas pelo CFO ou outros órgãos.

# Existe necessidade de utilizar documentos privados ou específicos da organização?
Sim, utilizar os dados sensíveis de prontuários eletrônicos sendo muito importante respeitar a LGPD.

# Que problemas poderiam ocorrer se o LLM respondesse apenas com seu conhecimento pré-treinado? Dê um exemplo concreto de resposta errada que ele daria no seu cenário.
Um dos problemas seria a defasagem temporal dos estudos. 
Pergunta: Existe alguma restrição da ANVISA para o uso de amálgama de prata para restaurações em crianças?
Resposta errada: Não, o amálga de prata, composto de limalha de prata e mercúrio é amplamente utilizado em restaurações de dentes decíduos.

* **O amálga de prata é um materia usado há décadas dentro da odontologia, porém, atualmente, há diretrizes globais que banem o uso deste tipo de material em crianças.**
