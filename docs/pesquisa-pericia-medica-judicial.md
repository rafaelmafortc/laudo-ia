# Perícia médica judicial e o laudo pericial

Pesquisa de domínio para o laudo-ia. Revisão 2, fechada em 06/10/2026.

**Base:**
- Os seis laudos reais em `docs/laudos/`, de três peritos, do TJRJ e do TRT-1.
- Legislação, normas do CFM, do CNJ, do CSJT e do MTE.
- Jurisprudência, literatura médica e literatura médico-legal.
- Panorama do mercado de software para peritos.

**Convenção das marcas:**
- [V]: conferido no texto primário.
- [NC]: não confirmado em fonte primária.
- "Inferência": raciocínio nosso, sem fonte direta.

Os nomes de periciandos foram omitidos. Os peritos aparecem como A, B e C.

---

## 1. O essencial

1. **O laudo é uma prova técnica que o juiz avalia pelo método.** O juiz não fica preso ao laudo (CPC/2015, art. 479), mas precisa dizer por que o acolheu ou o afastou, "levando em conta o método utilizado pelo perito".
2. **A responsabilidade é do perito e não se transfere.**
   - O ato pericial é "personalíssimo" (Res. CFM 2.430/2025, art. 5º, §6º).
   - Só assina quem examinou pessoalmente (Código de Ética Médica, art. 92).
   - A Res. CFM 2.454/2026, sobre IA na medicina, vale também no contexto "pericial", está em vigor desde cerca de 26/08/2026 e diz que o médico "permanece integralmente" responsável (art. 7º) [V].
   - Consequência: a IA redige uma minuta, o perito decide e assina. A IA nunca inventa achado.
3. **O escopo é maior que o auxílio-acidente.** Os laudos cobrem dois tipos de processo, que fazem perguntas diferentes:
   - **Acidentária (TJRJ, contra o INSS):** há redução da capacidade para a atividade habitual? Desde quando a lesão está consolidada? O valor do benefício é fixo (50%), então o percentual de redução não importa.
   - **Trabalhista (TRT, contra o empregador):** nexo ou concausa, com percentual; incapacidade; déficit funcional em %; repercussão profissional; dano estético; *quantum doloris*; estabilidade. Os percentuais definem o valor da indenização (CC, art. 950) [V].
   - Há perícias ortopédicas, uma psiquiátrica e uma de medicina do trabalho.
4. **Não existe um modelo único de laudo.** Cada perito tem uma família de modelos, com estrutura, ordem e estilo próprios. A Perita C usa um software de mercado (MSLaudo). O produto precisa se adaptar ao modelo de cada perito, e não impor um.
5. **O maior risco é texto-padrão que parece achado.** Os modelos trazem, sem marcação de pendência:
   - sinais vitais fixos;
   - exame físico "normal";
   - conclusões já escritas ("NÃO há nexo", "Não há divergência", "AUMENTA O ESFORÇO").
   - Nos laudos finalizados, esse texto-padrão convive com achados que o contradizem.
6. **Os peritos já usam IA generativa sem controle.** Um laudo finalizado do TJRJ começa a discussão com o resíduo de um chatbot: "Segue a versão reescrita em linguagem médico-pericial formal, deixando expressamente caracterizada a redução funcional...". A demanda está validada. Os riscos também: texto meta vazado, prompt que já induz a conclusão e nenhuma rastreabilidade.
7. **Normas revogadas aparecem em laudos já protocolados.** Exemplos: CPC/1973, Res. CFM 1.851/2008, Res. CREMESP 126/2005, Res. CFM 2.183/2018 e o art. 104, II, do Decreto 3.048. A seção "literatura" é capítulo de livro ou texto de site colado, às vezes sobre outra lesão.
8. **No caso do vigilante (modelo original), a medida que decide não foi tomada.** O exame registra "bloqueio de extensão em 40°" sem medir a flexão. É a flexão que define se a lesão se enquadra no Anexo III do Decreto 3.048 (§4.2).

---

## 2. O conjunto de laudos analisado

| Arquivo | Perito | Justiça e tipo | Objeto | Estado |
|---|---|---|---|---|
| `LAUDO MÉDICO TJRJ ROSBERG.docx` | A, ortopedista | TJRJ (Vara Cível), acidentária: auxílio-acidente | Fratura do úmero distal E; vigilante | Rascunho com marcações (é o antigo "MODELO LAUDO PARA IA") |
| `LAUDO MÉDICO TJRJ (FINALIZADO).docx` | A | TJRJ, acidentária: auxílio-acidente | Fraturas de antebraço E e tíbia/joelho E; caminhoneiro reabilitado | Finalizado. Conclui por redução parcial e permanente. |
| `LAUDO MÉDICO TRT (FINALIZADO).docx` | A | TRT-1, acidente típico (desabamento de parede) | Fraturas de fêmur E e tíbia D exposta; infecção ativa | Finalizado. Nexo causal; incapacidade total e temporária; dano estético leve. |
| `LAUDO MÉDICO TRT ORTOPÉDICO BIANCA.docx` | B | TRT-1, doença ocupacional osteomuscular | Coluna, ombros, cotovelos; bancária | Modelo semipreenchido. Exame todo normal, "NÃO há nexo" já escrito, 64 quesitos sem resposta. |
| `LAUDO MÉDICO MENTAL BIANCA.docx` | B | TRT-1, doença ocupacional psíquica (F41.2); dispensa após retorno de afastamento | Transtorno misto ansioso e depressivo | Esqueleto. Anamnese psiquiátrica, PHQ-9, GAD-7 e exame do estado mental em branco; "NÃO há nexo" já escrito. |
| `LAUDO MÉDICO TRT TATIANA.doc` | C, medicina do trabalho | TRT-1, doença ocupacional, 4 reclamadas | Hérnia inguinal; promotor de vendas | Finalizado, gerado no MSLaudo. Concausa de cerca de 25%; Weliton classe 2. |

### 2.1 Três famílias de modelo

| | Perito A | Perita B | Perita C (MSLaudo) |
|---|---|---|---|
| Forma | Prosa e listas pergunta → "Nega/Sim". Mesmo esqueleto no TJRJ e no TRT. | Pesada em checkboxes do Word (96 a 310 por documento) e roteiros estruturados | Tabelas geradas por sistema (atitude, sinais vitais, exame geral) e linha do tempo de documentos |
| Blocos próprios | Qualificação longa; legislação; literatura; obs. normativas. No TRT acrescenta contestação, reclamada, histórico na reclamada, documentos de SST, nexo (Simonin) e valoração do dano. | Avaliação de dependência (autonomia física e intelectual); exame segmento a segmento com testes nomeados; módulo psiquiátrico (PHQ-9, GAD-7, exame do estado mental, risco suicida); conclusões por item; pedido de honorários | Profissiografia quantificada ("10 caixas de 20 kg, 2 a 3 vezes ao dia"); raciocínio técnico pericial; valoração por baremo mais classe de Weliton; quesitos complementares do juízo |
| Referência documental | "fls." no TJRJ; "fls." e Id no TRT | Id do PJe e fls. | fls. e Id |
| Marcações | Vermelho = dado do caso; amarelo = seção a redigir. Somem no laudo finalizado. | Amarelo = campo pendente. Mas sinais vitais e exame normal **não** são marcados. | Nenhuma |

- **Convenção de cores (confirmada no XML).** Os laudos finalizados não têm nenhum realce, o que confirma que as cores são marcações de trabalho.
- **Quem prepara os laudos (inferência).** Todos os arquivos foram salvos hoje pela mesma conta de usuário do Word, e o modelo original também. Hipótese: quem prepara é uma assistente que atende vários peritos. Isso define a persona do produto (ver §12).

---

## 3. A profissão

### 3.1 Quem é o perito médico judicial

- **Função.** Auxiliar da Justiça (CPC, arts. 149 e 156). O juiz o nomeia quando a prova depende de conhecimento técnico. A perícia é ato privativo de médico (Lei 12.842/2013, art. 4º, XII) [V].
- **Exigências.** Basta CRM ativo. O RQE em Medicina Legal e Perícia Médica não é exigido (Parecer CFM 45/2016) [V]. O CPC pede "perito especializado no objeto" (art. 465). Nos laudos analisados, há ortopedista em caso ortopédico e médica do trabalho em hérnia. A especialidade da Perita B não aparece nos laudos.
- **A especialidade existe.** Medicina Legal e Perícia Médica é a nº 36 da Res. CFM 2.380/2024 [V]. As siglas que aparecem nos laudos são CRM, RQE, TEOT (título da SBOT) e ABMLPM (a associação da especialidade).

| Papel | Quem | Base |
|---|---|---|
| Perito do juízo | Médico cadastrado no tribunal. Sujeito a impedimento e suspeição. | CPC 156–158, 465–480 |
| Assistente técnico | Médico de confiança da parte. Acompanha a perícia e dá parecer. No laudo TRT do Perito A, a reclamada indicou uma assistente. | CPC 466 §1º, 477 §1º |
| Perito oficial (legista) | Concursado, área criminal | Lei 12.030/2009 |
| Perito Médico Federal | Servidor do INSS, autor da perícia administrativa | Lei 11.907/2009, art. 30 |

- **Cadastro.**
  - CPTEC (Res. CNJ 233/2016). É vedado nomear quem não está cadastrado.
  - Quem foi assistente técnico de uma das partes nos 3 anos anteriores não pode ser perito no caso [V].
  - Na Justiça do Trabalho, o cadastro e o pagamento passam pelo sistema AJ-JT.

### 3.2 Áreas de atuação

| Área | Justiça | O que se discute | Particularidades |
|---|---|---|---|
| Previdenciária comum (B31, B32, B36, BPC) | Federal | Incapacidade, DID/DII, reabilitação | Laudo no **Sisperjud** (Res. CNJ 595/2024), obrigatório desde 01/09/2025 |
| **Acidentária (B91, B92, B94)** | Estadual (CF 109, I; Súm. 15 STJ) | Sequela, consolidação, redução da capacidade | O INSS antecipa os honorários. Pela Res. 595, também vai para o Sisperjud. Não confirmamos se o TJRJ já aplica [NC]. |
| **Trabalhista** | Justiça do Trabalho | Nexo e concausa, incapacidade, dano corporal, estabilidade | "Reclamante/Reclamada"; documentos de SST; honorários pelo art. 790-B da CLT |
| Cível | Estadual | Erro médico, DPVAT, seguro, interdição | Baremos |

### 3.3 Fluxo do processo

1. **Nomeação.** O juiz nomeia o perito e fixa o prazo (CPC, art. 465). As partes têm 15 dias para impedimento ou suspeição, assistentes e quesitos.
2. **Proposta.** O perito apresenta proposta de honorários, currículo e contatos (§2º). O juiz arbitra o valor.
3. **Agendamento.** As partes são cientificadas (art. 474). Os assistentes são avisados com 5 dias de antecedência (art. 466, §2º). Nos laudos, o exame é feito no fórum (TJRJ) ou no consultório do perito (TRT).
4. **Ato pericial.** Autos, anamnese, exame e documentos (art. 473, §3º). Filmagem só com anuência das partes; terceiros só com autorização do perito (Res. CFM 2.430/2025, arts. 14 e 15).
5. **Laudo.** Protocolo pelo menos 20 dias antes da audiência (art. 477).
6. **Depois do laudo.** As partes se manifestam em 15 dias. O perito presta esclarecimentos em 15 dias (art. 477, §§1º e 2º).
7. **Pagamento.** Alvará ou mandado de pagamento.
8. **Sanções.** Informação inverídica gera inabilitação de 2 a 5 anos (art. 158). Perícia deficiente pode ter os honorários reduzidos (art. 465, §5º).

### 3.4 Honorários: dois regimes

**Acidentária (TJRJ).**
- O INSS antecipa (Lei 13.876/2019, art. 1º, §7º, II) [V].
- Se o autor perde, o Estado paga (STJ, Tema 1044).
- Por isso o Perito A informa dados bancários e pede "liberação do alvará".

**Trabalhista (TRT).**
- Paga quem perde no objeto da perícia (CLT, art. 790-B) [V].
- É proibido exigir adiantamento (§3º; Res. CSJT 247/2019, art. 15) [V].
- Se o beneficiário da gratuidade perder, quem paga é a União (STF, ADI 5766; Súm. 457 TST) [V], até **R$ 1.500 a partir de 01/01/2026** (Ato CSJT 97/2025) [V]. Pode haver acréscimo de até 30% se houver vistoria (Res. CSJT 247, art. 21, §5º, red. Res. 436/2026) [V].
- A Perita B pede no próprio laudo o arbitramento de R$ 4.000 e R$ 9.500. Esses valores só são exigíveis da parte que não tem gratuidade e que perdeu.

**Gratuidade na Justiça Estadual (demais casos).** Teto de R$ 370 na Res. CNJ 232/2016, com possibilidade de até 5 vezes esse valor [V].

### 3.5 Ética

Código de Ética Médica, Capítulo XI [V]:

- **Art. 92:** só assina quem examinou.
- **Art. 93:** o perito não pode periciar o próprio paciente. Daí o quesito "é ou foi paciente do perito?".
- **Art. 94:** não comenta o trabalho de outro médico na frente do examinado.
- **Art. 96:** sem remuneração ligada ao resultado da causa.
- **Art. 97:** não altera o tratamento instituído.
- **Art. 98:** "absoluta isenção" e respeito aos limites da designação.
- **CPC, art. 473, §2º:** nenhuma opinião além do exame técnico.
- **Protocolo da ABMLPM para a Justiça do Trabalho:** veda especular sobre tratamentos alternativos, infrações éticas e atribuição de responsabilidade [V].
- **Perito × médico assistente.** O perito tem autonomia técnica (Res. CFM 2.430/2025, art. 6º; Res. CFM 2.323/2022, art. 9º).

---

## 4. Perícia acidentária: auxílio-acidente

### 4.1 O benefício

- **Requisito (Lei 8.213/91, art. 86)** [V]: sequela, "após consolidação das lesões", que implique "redução da capacidade para o trabalho que habitualmente exercia".
- **Valor e regras.**
  - Indenização de 50%, devida a partir do dia seguinte à cessação do auxílio-doença.
  - Continua sendo paga com o retorno ao trabalho e cessa na véspera da aposentadoria.
  - Não exige carência.
- **Quem tem direito.** Empregado, doméstico, avulso e segurado especial. **Contribuinte individual e facultativo não têm** (art. 18, §1º; TNU, Tema 201) [V].
- **Espécie.** B94 para acidente do trabalho, inclusive de trajeto (art. 21, IV, "d", vigente) [V]. B36 para os demais.
- **Decreto 3.048/99, art. 104 (red. Decreto 10.410/2020)** [V]:
  - caput: sequela que, "**a exemplo** das situações discriminadas no Anexo III", reduza a capacidade. O Anexo III é exemplificativo.
  - **Incisos I a III revogados**, inclusive o "maior esforço".
  - §4º, I: não dá direito o "dano funcional sem repercussão na capacidade laborativa".
  - §8º: conta a atividade na **data do acidente**.
- **Jurisprudência** [V]:
  - STJ, Tema 416: devido "ainda que mínima a lesão".
  - STJ, Tema 862, e TNU, Tema 315: termo inicial no dia seguinte à cessação do auxílio-doença.
  - STJ, Tema 156: a reversibilidade é irrelevante.
  - TNU, Tema 395: conceito de "consolidação das lesões", **ainda sem tese**.
  - TNU, Tema 343: DII na data da perícia só em caso excepcional.
- **"Maior esforço" hoje.** A expressão continua no Tema 416 e no quesito VI-c da Recomendação Conjunta CNJ/AGU/MTPS 1/2015. Pode ser usada como achado técnico, com fundamento no art. 86 mais o caput do art. 104.
  - O Perito A, no laudo TJRJ finalizado, respondeu corretamente que a porcentagem de redução "não [é] objeto dessa perícia": o benefício é fixo.
- **Reabilitação profissional e auxílio-acidente.** No laudo TJRJ finalizado, o segurado foi reabilitado para auxiliar de escritório. As Diretrizes do INSS mandam, ao fim da reabilitação, "sempre avaliar a indicação de auxílio-acidente" [V].

### 4.2 Anexo III, Quadro 6

- **Alínea "d":** "redução em grau médio ou superior dos movimentos das articulações do ombro ou do cotovelo" [V].
- **Graus (Nota 1)** [V]:
  - mínimo: redução de até 1/3 da amplitude normal;
  - médio: mais de 1/3 até 2/3;
  - máximo: acima de 2/3.
- **Referência.** O anexo não fixa a amplitude normal. O laudo precisa declarar a referência que usou (AAOS 150°, AMA 140°, TNI 145°) ou, de preferência, o lado contralateral.

Caso do vigilante, conta nossa com referência de 145°:

| Achado | Arco | Perda | Grau | Quadro 6 "d" |
|---|---|---|---|---|
| Extensão −40°, flexão 145° | 105° | 27,6% | mínimo | não enquadra |
| Extensão −40°, flexão 136° | 96° | 33,8% | médio | enquadra |
| Extensão −40°, flexão 130° | 90° | 37,9% | médio | enquadra |
| Arco 45°–90° (laudo do assistente) | 45° | 69,0% | máximo | enquadra |

- **Limiar.** Com a extensão travada em 40°, a lesão vira grau médio se a flexão ficar abaixo de cerca de 137° (referência de 145°) ou de cerca de 140° (referência de 150°).
- **Fora do Anexo III.** Mesmo sem enquadrar, pode haver direito pelo caput e pelo Tema 416, se o laudo demonstrar repercussão na atividade habitual.

### 4.3 Conceitos

| Sigla | Significado | Regra |
|---|---|---|
| DID | Início da doença | Em acidente, é a data do evento (Manual Técnico do INSS, 2018) |
| DII | Início da incapacidade | Quando a doença impediu a atividade habitual |
| DIB / DCB | Início e cessação do benefício | Começar no 16º dia após o acidente é coerente com o art. 60 da Lei 8.213 |
| Consolidação | Estabilização da lesão, quando a sequela vira definitiva | Sem definição legal (TNU, Tema 395 pendente) |
| Espécies | B31/B91 incapacidade temporária; B32/B92 incapacidade permanente; B36/B94 auxílio-acidente; B87 BPC | Nomes atuais pós-EC 103/2019 |

### 4.4 Quesitos

- **Do Juízo.** A Res. CNJ 595/2024 manda usar a quesitação mínima unificada do Sisperjud, "inclusive [nos] acidentários" [V].
  - O Sisperjud é um formulário web no PDPJ-Br, com rascunho, anexos e PDF assinado [V].
  - Não há API pública para terceiros [NC].
  - Já está em uso em TRF3, SJRJ, TJBA e TJSC [V].
- **Do autor.** Escritos para provar o direito: nexo, consolidação na data de cessação, goniometria, "ainda que mínima", "maior esforço".
- **Do INSS.** "Rol de Quesitos Padronizados" da PGF/AGU [V]. Pedem:
  - causa provável;
  - DID, DII e data de consolidação;
  - grau de capacidade e se é temporária ou permanente;
  - reabilitação;
  - assistência de terceiros;
  - profissiografia;
  - **divergência com o laudo administrativo** (Lei 8.213, art. 129-A, §1º: obrigação de fundamentar a divergência) [V];
  - capacidade civil;
  - doenças da Portaria Interministerial MTP/MS 22/2022.
- **Regra (CPC, art. 473, IV).** Resposta conclusiva a todos os quesitos.

---

## 5. Perícia trabalhista

### 5.1 Por que os percentuais importam

- **Fundamentos** [V]:
  - CF 7º, XXVIII: indenização por dolo ou culpa do empregador.
  - CC 927, parágrafo único: responsabilidade objetiva em atividade de risco (STF, Tema 932).
  - CC 949: tratamento e lucros cessantes até o fim da convalescença.
  - **CC 950:** "pensão correspondente à importância do trabalho para que se inabilitou, ou da depreciação que ele sofreu".
  - CLT 223-G: faixas de dano extrapatrimonial, que o STF trata como "critério orientador", não teto (ADIs 6050/6069/6082).
- **Fórmula prática.** Pensão ≈ remuneração × % de redução da capacidade × % de contribuição do trabalho (concausa).
  - O TST considerou violação manter 100% de pensão quando há concausa (8ª Turma, RR-945-02.2012.5.09.0095) [V].
  - Por isso os quesitos trabalhistas pedem percentual, e os acidentários não.
- **Estabilidade** [V]:
  - Lei 8.213, art. 118: 12 meses após a cessação do auxílio-doença acidentário.
  - Súmula 378, II, do TST: exige afastamento maior que 15 dias e B91, "salvo se constatada, após a despedida, doença profissional" com nexo.
  - **TST, Tema 125** (IRR, acórdão de 07/05/2025): "não é necessário o afastamento por período superior a 15 dias ou a percepção de auxílio-doença acidentário, desde que reconhecido, após a cessação do contrato, o nexo causal ou concausal".
  - Daí os quesitos "havia incapacidade na data da dispensa?".
  - Súmula 443 do TST (dispensa discriminatória em doença grave que gere estigma): o TST diverge sobre aplicá-la a transtornos psiquiátricos. Lei 9.029/95.

### 5.2 Nexo e concausa: métodos

- **Norma com força obrigatória: Res. CFM 2.323/2022, art. 2º** [V]. Além da anamnese e do exame presencial, o perito deve considerar:
  - história clínica e ocupacional;
  - **estudo do local de trabalho**;
  - organização do trabalho;
  - dados epidemiológicos;
  - literatura;
  - quadro em outros trabalhadores expostos;
  - identificação de riscos;
  - depoimento dos trabalhadores;
  - outras disciplinas.
- **Vistoria (art. 14, II).** A redação é condicional e não obriga a vistoria [V]. Mas um laudo que diz "perito desconsidera a necessidade de vistoria" (os dois da Perita B) sem explicar como supriu o estudo do local de trabalho (PGR, AET, PPP, depoimentos) fica fraco perante o CPC, art. 473, §1º.
- **Critérios de Simonin** (Müller e Cordonnier, 1925) [V, em Vieira e Corte-Real 2008]:
  - realidade e intensidade do evento;
  - certeza diagnóstica;
  - integridade prévia da região (estado anterior);
  - concordância de lugar;
  - adequação temporal;
  - encadeamento anátomo-clínico;
  - exclusão de causa estranha.
  - O Perito A os cita no laudo TRT. Prevalecem na medicina legal e na escola de Coimbra.
- **Classificação de Schilling** (Manual MS/OPAS 2001) [V]:
  - Grupo I: o trabalho é causa necessária.
  - Grupo II: o trabalho é fator contributivo. Inclui o aparelho locomotor.
  - Grupo III: o trabalho é provocador ou agravador, ou seja, concausa. Inclui as doenças mentais.
- **Critérios de Hill** (1965) [V]. Base epidemiológica, não é um checklist.
- **Penteado** [V]:
  - 10 critérios de nexo e 7 de concausa, publicados no Jusbrasil desde 2014.
  - Metodologia de pontos de 2020 (Penteado e Saladini, Rev. TST 86(2):195-209): fatores extralaborais e laborais pontuados de 0 a 3; % laboral = pontos laborais / (laborais + extralaborais).
  - Muito usada na Justiça do Trabalho, mas publicada em revista jurídica e sem validação empírica.
- **Gradação da concausa.**
  - Oliveira (Rev. TRT-2, 2013) propõe graus I, II e III **sem percentuais** [V].
  - Os pontos 25/50/75% vêm do 7º quesito de Penteado (2017), segundo TCC da UnB de 2019 [V no TCC].
  - É convenção pericial, sem base científica. "Aproximadamente 25%" (Perita C) é o grau I por convenção. O laudo deveria declarar isso ou mostrar a pontuação.
- **Presunções epidemiológicas.**
  - **NTEP** (Lei 8.213, art. 21-A; Lista C do Anexo II do Decreto 3.048, sem atualização desde 2009) [V]. Para bancos (CNAE 6422), cobre F30–F48 e M60–M79, ou seja, F41, M65 e M75. **Não cobre M54.** A hérnia (K40–K46) depende do CNAE do empregador.
  - **LDRT** (Portaria GM/MS 1.999/2023) [V]. Inclui:
    - F32, F41, F43 e Z73.0 (burnout), ligados a fatores psicossociais;
    - K40 (hérnia inguinal), ligado à manipulação de carga;
    - M54, M65 e M75.
    - Tem finalidade de vigilância e não cria presunção de nexo individual (inferência).
  - Ambas são fatos que o laudo precisa enfrentar, não conclusões automáticas.

### 5.3 Documentos de SST que o laudo cita

| Documento | Norma | Observação |
|---|---|---|
| PGR (inventário de riscos + plano de ação) | NR-1, em vigor desde 03/01/2022 (Portaria SEPRT 6.730/2020) [V] | **Substituiu o PPRA.** Citar PPRA só vale para períodos anteriores a 2022. |
| Riscos psicossociais no GRO | NR-1, item 1.5.3.1.4 (Portaria MTE 1.419/2024) [V] | Em vigor desde **26/05/2026**, com fiscalização inicialmente orientativa [V]. Para fatos anteriores, não havia exigência expressa. |
| PCMSO e ASO (admissional, periódico, retorno após 30 dias ou mais, mudança de risco, demissional) | NR-7 (Portaria SEPRT 6.734/2020) [V] | Os três peritos listam os ASOs com folha, data e "APTO" |
| AEP e AET | NR-17 (Portaria MTP 423/2021) [V] | A AET só é exigida em certas hipóteses |
| LTCAT e PPP | Lei 8.213, art. 58 [V] | PPP só eletrônico (eSocial) para períodos a partir de 2023 [V] |
| CAT | Lei 8.213, art. 22 | Também pode ser emitida pelo sindicato ou pelo médico (houve CAT de sindicato num dos laudos) |

### 5.4 Valoração do dano corporal

- **Referência nacional atual:** **Diretriz da ABMLPM para avaliação do dano pessoal (2025)** e **Tabela Brasileira para a Apreciação do Dano Corporal** (ABMLPM, 2024) [V a diretriz; a tabela só como citação].
- **Parâmetros temporários:**
  - déficit funcional temporário, total e parcial, em dias;
  - repercussão temporária na atividade profissional, em dias;
  - ***quantum doloris*** em 7 graus: 1 muito ligeiro, 2 ligeiro, 3 moderado, 4 médio, 5 considerável, 6 importante, 7 muito importante (escala francesa de 1971) [V].
- **Parâmetros permanentes:**
  - déficit funcional permanente, pela Tabela Brasileira;
  - repercussão permanente na atividade profissional;
  - dano estético em 7 graus;
  - repercussão em atividades sociais, desportivas e de lazer;
  - repercussão na atividade sexual;
  - dependências futuras.
- **Regras.** Sem nexo, não se valora. Se houve cura, só os temporários.
- **AIPE.** Instrumento de Cobo Plana validado no Brasil (Fernandes et al., *Saúde Debate* 2016;40(108):118-130), com graus de leve a muito importante (0–50 pontos) [V]. **Não é a escala de 1 a 7.** Citar o AIPE e dar nota "x/7" mistura as escalas. O Perito A usa "leve", que é coerente com o AIPE.
- **Classes de Weliton Barbosa Santos** (RBMT 2012;10(1)) [V]: nove classes de repercussão profissional permanente.
  - Classe 1 (0–5%): compatível.
  - **Classe 2 (6–15%): esforço acrescido**, sem afetar produção ou ganho.
  - Classes intermediárias: de esforço que afeta o posto até reabilitação em nível inferior.
  - Classe 9 (**80**–100%): insuscetível de reabilitação.
  - Não tem validação. A classe 2 é a ponte conceitual com o "maior esforço" do auxílio-acidente.
- **Baremos estrangeiros:**
  - TNI de Portugal (DL 352/2007);
  - Mélennec (1997);
  - AMA Guides;
  - **Argentina, Decreto 659/1996** [V]. Hérnia inguinal operada: sem sequelas, 0%; com sequelas, 6%. **Não existe 8%.** O Anexo I foi substituído pelo Decreto 549/2025 [V].

### 5.5 Estrutura recomendada

- **Protocolo da ABMLPM para laudo na Justiça do Trabalho (2025)** [V]. Seções obrigatórias: as do CPC, art. 473, mais as da Res. CFM 2.056/2013, art. 58.
- **A fundamentação deve cobrir:**
  - documentação;
  - exame;
  - condições de trabalho;
  - profissiografia;
  - nexo;
  - dano;
  - literatura.
- **Documentos imprestáveis.** Documento sem data, sem identificação ou ilegível não serve como prova, e a exclusão deve constar do laudo.
- **Vistoria.** Só com método e objetivo definidos.

---

## 6. Perícia psiquiátrica

- **Roteiro.** A Res. CFM 2.056/2013, art. 58, exige história psiquiátrica e exame do estado mental (alíneas g e k). A Res. CFM 2.057/2013, arts. 34–36, trata dos atos periciais em psiquiatria [V].
- **CSJT.** A Res. 247/2019, art. 14-A (red. Res. 436/2026), prevê perícia psiquiátrica quando a controvérsia envolve diagnóstico, nexo ou incapacidade por transtorno mental [V]. Ou seja, há preferência por psiquiatra.
- **Instrumentos do modelo da Perita B: PHQ-9 e GAD-7.**
  - Referências: Kroenke 2001; Spitzer 2006. Validação brasileira: Santos 2013; Moreno 2016 [V].
  - São **autorrelato e rastreio, não diagnóstico**, sem escala de validade e não validados em quem está em litígio. O PHQ-9 ≥ 10 superestima a prevalência (Levis, *BMJ* 2019) [V].
  - Medem intensidade nas últimas duas semanas, não a etiologia.
  - No laudo, servem como complemento do exame do estado mental, nunca como fundamento único.
- **Validade de sintomas.** Testes como SIMS (Smith e Burger 1997) e o consenso AACN 2021 [V].
  - No Brasil, testes psicológicos são privativos de psicólogo (SATEPSI) [NC].
  - Referência nacional: *Psiquiatria forense de Taborda*, 3ª ed., 2016 [V].
- **Nexo em transtorno mental.**
  - Schilling III (concausa).
  - LDRT 2023 (F41, F32, F43, Z73.0).
  - CID-11: burnout como "fenômeno ocupacional", não como doença.
  - NR-1 psicossocial só a partir de 26/05/2026.
  - Fatores extralaborais precisam ser pesados com cronologia e dose de exposição. Exemplos alegados pela defesa no caso: nascimento de filho após perdas gestacionais.
- **Problemas no modelo psiquiátrico da Perita B:**
  - a conclusão "não há nexo, não há incapacidade, não há dano psíquico" está pronta antes do exame;
  - a "fundamentação teórica" é texto leigo de site, escrito em segunda pessoa, que inclui **depressão pós-parto** para um periciando homem e não trata de F41.2;
  - os sinais vitais fixos (130x80) foram herdados do modelo ortopédico;
  - o roteiro tem campos de "risco suicida", o que exige protocolo para achado positivo (inferência).

---

## 7. O laudo: requisitos e esqueleto comum

### 7.1 Requisitos formais

- **CPC, art. 473** [V]:
  - objeto;
  - análise técnica;
  - método "predominantemente aceito";
  - resposta conclusiva a todos os quesitos;
  - §1º: linguagem simples e coerência lógica, "indicando como alcançou suas conclusões";
  - §2º: nada além da designação;
  - §3º: anexos, fotos e documentos.
- **Res. CFM 2.430/2025** [V]:
  - art. 8º: são obrigatórios metodologia, objeto, análise e quesitos;
  - art. 9º: avaliar todos os documentos, examinar e fundamentar a escolha do método.
- **Res. CFM 2.056/2013, art. 58, roteiro básico** [V]:
  - preâmbulo e individualização;
  - circunstâncias do exame e identificação;
  - HDA e histórias pessoal, psiquiátrica, médica e familiar;
  - exame físico, estado mental e exames complementares;
  - diagnóstico pela CID;
  - comentários médico-legais e conclusão;
  - respostas aos quesitos.
  - O art. 55 traz o princípio *visum et repertum*: o que não foi visto e registrado não existe.

### 7.2 Esqueleto comum dos três modelos

Legenda de origem: **F** = fixo do perito; **A** = autos; **E** = exame/entrevista; **R** = raciocínio.

| Bloco | Origem | Variações observadas |
|---|---|---|
| Cabeçalho (vara, número CNJ, partes) | A | O segmento do número (8 = Estadual; 5 = Trabalho) deve bater com a classe e os termos (Autor/Réu × Reclamante/Reclamada) |
| Preâmbulo, qualificação e honorários | F | TJRJ: alvará e banco. TRT: pedido de arbitramento. |
| Objetivo/objeto | A | Acidentária: auxílio-acidente. TRT: nexo, redução, incapacidade, patologias citadas. |
| Síntese da inicial e da contestação | A | Contestação só no TRT. Às vezes há várias reclamadas. |
| Metodologia | F | Genérica nos três. Não diz quais instrumentos usou (goniômetro, MRC, escalas). |
| Diligências (data, local, assistentes) | E | |
| Identificação do periciando e da reclamada | A+E | TRT: CNPJ, CNAE, ramo (relevante para o NTEP) |
| Histórico laboral, profissiografia e ASOs | A+E | TRT: jornada, EPIs, ASOs por folha ou Id, carga manuseada |
| Histórico previdenciário | A | Espécie, número e período |
| Documentos médicos | A | Tabela data/tipo/CRM/CID/transcrição/folha. Várias linhas só com imagem, inclusive documentos manuscritos (precisa de OCR com visão). |
| Documentos de SST | A | PGR/PPRA, PCMSO, AET, LTCAT, PPP com Id, ou "não encontrado nos autos" |
| Antecedentes / estado anterior | E | A pergunta "possui sequela de fraturas?" é ambígua: fala do estado anterior ou de hoje? |
| HDA / história ocupacional | E | Perita C cita o periciando entre aspas |
| Exame físico (e estado mental) | E | Texto-padrão normal + linhas específicas do caso (ver §8.2) |
| Discussão / raciocínio | R | Nexo (TRT), repercussão na atividade (acidentária) |
| Valoração do dano | R | Só no TRT (Peritos A e C) |
| Conclusão | R | Na Perita B, já vem escrita no modelo |
| Quesitos (juízo, autor, réu, complementares) | A+R | De 5 a 64 quesitos por parte |
| Legislação, literatura e bibliografia | F/R | Coladas e genéricas |
| Anexos e encerramento | E/F | Fotos, identidade, documentos |

### 7.3 A cadeia de raciocínio esperada

**Acidentária:**
1. Evento e nexo.
2. Lesão e tratamento.
3. Consolidação (data justificada).
4. Sequela medida.
5. Tarefas da atividade na data do acidente.
6. Repercussão tarefa a tarefa (para afastar o art. 104, §4º, I).
7. Anexo III (com a referência declarada).
8. Divergência com o INSS (art. 129-A).
9. Conclusão.

**Trabalhista:**
1. Diagnóstico pela CID, com certeza diagnóstica.
2. Exposição: profissiografia, documentos de SST, período e réu.
3. Estado anterior e fatores extralaborais.
4. Critérios de nexo declarados (Res. 2.323, art. 2º, mais Simonin, Schilling ou Penteado).
5. Conclusão de nexo: causal, concausal (grau e método) ou ausente.
6. Incapacidade (atual e na dispensa).
7. Valoração: temporários e permanentes, com o baremo e a versão citados.
8. Dano estético (com a escala declarada).
9. Dependências.

---

## 8. Problemas encontrados no conjunto de laudos

### 8.1 Normas

| Ocorrência | Onde | Correção |
|---|---|---|
| "art. 436 / art. 131 do CPC" (CPC/1973, revogado) | Perito A, nos 3 laudos, inclusive os finalizados | CPC/2015, arts. 479 e 371 |
| Res. CFM 1.851/2008 (alterava a 1.658/2002, revogada pela 2.381/2024) e CREMESP 126/2005 (revogada, só SP) | Perito A, nos 3 | Res. CFM 2.430/2025 (arts. 6º e 9º) e 2.323/2022 (art. 9º) |
| Res. CFM 2.183/2018 na bibliografia, mas 2.323/2022 na metodologia | Perito A, TRT | 2.323/2022 (a 2.183 foi revogada) |
| IN INSS 31/2008 e 98/2003 na bibliografia | Perito A, TRT | Vigência não confirmada [NC]. Evitar. |
| "Lei 6.514/1977 (Consolidação das Leis do Trabalho)" | Perito A, TRT | A Lei 6.514 alterou o capítulo de SST da CLT; não é a CLT |
| Texto do art. 20 da Lei 8.213 (doença profissional/do trabalho) colado num acidente típico | Perito A, TRT | Citar o art. 19 (acidente típico) |
| "AUMENTA O ESFORÇO" com fundamento implícito no art. 104, II (revogado) | Perito A, TJRJ | Art. 86 mais caput do art. 104 e Tema 416 |
| "ATSum" | Perito A: correto no TRT (número com segmento 5); copiado nos dois do TJRJ (segmento 8) | Usar a classe da capa do processo |
| "Reclamante/Reclamada" num processo contra o INSS | Perito A, TJRJ (também na discussão do finalizado) | Autor / Réu |
| PPRA tratado como documento atual | Peritas B e C | PGR desde 2022; PPRA só para períodos anteriores |
| CBO entre aspas com texto parafraseado | Perito A | Descrição oficial (mtecbo.gov.br) |
| Dano estético citando AIPE | Perito A, TRT ("leve": coerente) | Não misturar com escala de 7 graus |
| "Baremo Argentino 8%" para hérnia | Perita C | A tabela dá 0% ou 6%; o Anexo foi substituído em 2025 |

Por outro lado, as Peritas B e C citam corretamente a Res. CFM 2.056/2013 (art. 58) e a 2.323/2022.

### 8.2 Padrões de falha que se repetem

1. **Texto-padrão sem marcação vira achado:**
   - os sinais vitais "130x80 mmHg, FC 80, FR 20" são fixos nos dois modelos da Perita B;
   - o exame "amplitude preservada, sem atrofias, força 5/5" está nos três peritos;
   - conclusões vêm prontas (Perita B);
   - quesitos do INSS vêm pré-respondidos (Perito A, nos dois laudos do TJRJ; o finalizado manteve "Não há divergência" apesar de concluir por redução, o que tende a contrariar a perícia do INSS).
2. **O texto-padrão contradiz o achado específico, sem que isso seja resolvido:**
   - TJRJ finalizado: "ADM preservada de quadris, joelhos…" ao lado de "limitação importante de arco de movimento de joelho esquerdo".
   - TRT finalizado (A): "sem sinais inflamatórios" ao lado de "sinais inflamatórios… fístulas"; "musculatura simétrica" com perimetria de coxa D 46 cm × E 49 cm; amplitude preservada e força 5/5 num periciando que anda de muletas.
3. **Faltam medidas.** Nenhum laudo ortopédico traz goniometria completa da articulação afetada; só há "bloqueio de extensão em 40°" no caso do vigilante. O modelo da Perita B mostra o valor de referência (0–150°), mas não tem campo para o valor medido.
4. **IA generativa usada sem controle:**
   - preâmbulo de chatbot colado na discussão (TJRJ finalizado);
   - respostas a quesitos no estilo "O laudo não especifica…" e "O laudo registra…" (TRT finalizado).
   - O prompt revelado pede para "deixar expressamente caracterizada" uma conclusão. Isso é escrever a favor de um resultado, o que conflita com a isenção (CEM, art. 98).
5. **Literatura colada e fora do caso:**
   - o mesmo capítulo de livro-texto sobre **fratura diafisária da tíbia** aparece nos dois finalizados do Perito A (um caso de joelho/antebraço, outro de fêmur/tíbia);
   - esse capítulo tem trechos em **primeira pessoa do autor original** ("Há três anos desenvolvemos técnicas…", "acho razoável"), sem citação, e parece obra do perito;
   - na Perita B, o texto vem de site leigo.
   - Problema de pertinência, credibilidade e direito autoral.
6. **Quesitos:**
   - respostas em branco (TJRJ finalizado: quesito 14 do INSS, sobre a repercussão na profissão, que é justamente o central do auxílio-acidente);
   - "vide item X" apontando para conteúdo que não existe (Perita C: dano estético e CIF remetem à "Valoração", que não trata deles);
   - "Repetido" e "Prejudicado" sem explicar;
   - checkbox incoerente (TJRJ finalizado: 8.1 marcado "Sim" sem incapacidade permanente);
   - "Vide item CBO" como resposta à profissiografia.
7. **Dados de outro caso.** O modelo psiquiátrico da Perita B tem **dois números de processo e dois reclamantes** no cabeçalho (resíduo de outro caso) e "CRM/SP" num CRM do RJ. É risco de sigilo e LGPD, além de erro de identificação.
8. **Concausa e valoração sem coerência interna:**
   - Perita C: concausa de 25% não aplicada ao déficit de 8%. A reclamada no caso da Perita B pergunta exatamente "se [a concausa] foi aplicada adequadamente à redução funcional".
   - Perito A: classe 1 de Weliton atribuída durante incapacidade temporária, quando as classes são para sequela permanente.
   - Perita C: classe 2 ("esforço acrescido") ao lado de "recuperação funcional suficiente para retorno" e de exame sem hérnia, sem justificar.
9. **Exposição por empregador.** Com 4 reclamadas e sintomas desde 2012 (Perita C), a concausa é atribuída à "função de promotor desde 2010", sem separar períodos e empregadores. A defesa questiona o "período imprescrito".
10. **Erros de digitação e forma:** "QUANTUN/PRETIUN DOLORIS", "Hpa", "ILUSTRTIVAS", "Rio de Janeiro - J", jornada "7h30 às 22h" (que precisa ser verificada).

### 8.3 Caso do vigilante (modelo original)

- **Datas.** O preâmbulo diz 05/10/2026; o encerramento diz 05/09/2026.
- **Mecanismo do acidente em três versões:** queda de moto após choque com ônibus; atropelamento; queda com diferença de nível. O acidente de trajeto não está tipificado.
- **HDA e discussão com lacunas:** "_____", "saindo do joa", "[especificar o evento danoso]", "____".
- **Medicamentos.** Antecedentes dizem "Nega"; a HDA fala em "sintomáticos". A pergunta "sequela de fraturas: Nega" é ambígua (ver §7.2).
- **Exame.** Falta a flexão; falta a prono-supinação; falta o lado direito em números; o nervo ulnar não foi avaliado (neuropatia em 15–19% dos casos após fixação); os testes específicos não são nomeados.
- **Quesito 16 do INSS** vem pré-preenchido "Não há divergência", embora a perícia administrativa nas fls. 196 e 210 provavelmente tenha negado o benefício.
- **Quesito 13** responde com a CBO.

---

## 9. Base médica do caso do vigilante

- **Fratura do úmero distal (AO 13; S42.4)** [V]:
  - 5,7/100.000/ano, com 90,6% de consolidação em 12 semanas (Robinson 2003).
  - Dupla placa (paralela ≈ perpendicular, Wang 2020); as vias de acesso não diferem (Lu 2021; Jeong 2022).
  - Resultados: arco médio de 110°, complicações em 53%, reoperação em 21% (Yetter 2021).
  - Contratura média de 25°, na faixa de 5–65° (McKee 2000).
  - Rigidez em 46,5%; neuropatia ulnar em 15,3% (Han 2022).
- **Estabilização** [V]: o arco melhora até 6 meses e pouco depois, até 12 meses (Giannicola 2014). Inferência: a alta em 10/2022, 4 meses após o acidente, foi precoce.
- **Amplitude normal e funcional** [V]:
  - normal: 0–145/150° (Zwerus 2019: 146°);
  - funcional: 30–130° (Morrey 1981) ou 27–149° (Sardelli 2011);
  - as Diretrizes do INSS aceitam perder os últimos 45° de extensão. É o argumento do INSS.
- **Goniometria** [V]: só há mudança real acima de cerca de 10° entre examinadores (Armstrong 1998). A AMA usa a melhor de 3 medidas.
- **Força** [V]: o teste MRC tem sensibilidade de no máximo 75% para déficits de 15–30% (Bohannon 2005). A dinamometria seria a medida objetiva.
- **Baremos** (extensão −40° com flexão completa × arco 45–90°):

| Sistema | Extensão −40°, flexão completa | Arco 45°–90° |
|---|---|---|
| Decreto 3.048, Quadro 6 | grau mínimo | grau máximo |
| MEPS (pontos de movimento) | 20 | 5 |
| TNI, lado não dominante | 0,00–0,07 | 0,15–0,26 |
| Lei 6.194/74 (DPVAT) | 6,25% | 18,75% |

- **Vigilante.**
  - A Lei 14.967/2024 exige aptidão física e mental e prevê porte de arma [V].
  - A formação inclui tiro com empunhadura dupla e defesa pessoal [V na IN DG/PF 340/2026 e na Portaria 22-CGCSP/2026, via fontes secundárias].
  - Na postura isósceles, o braço de apoio (o esquerdo, num destro) precisa de extensão quase completa (inferência).
  - Pendência: ele era vigilante armado na data do acidente?

---

## 10. Mercado

| Produto | Foco | IA | Preço/mês | Observação |
|---|---|---|---|---|
| **MSLaudo** (MedSafe, Londrina) | Gestão de perícias + laudo por formulário; baremos (europeu, espanhol, português, Mélennec, argentino, SUSEP, DPVAT); NTEP | Não | Não publicado | Usado pela Perita C. Antigo (desde ~2016). Sem PJe. [V] |
| Perícia Today | Só médico. Gera o laudo completo, cronologia, transcrição de áudio. | Sim | R$ 99–449 | Concorrente mais direto; diz "zero alucinação" [V] |
| Peritia | Médico. Minuta pelo CPC, trilha de auditoria. | Sim, "assistiva, não decisória" | R$ 197–797 | Em validação comercial [V] |
| Perícia.AI | Todas as áreas. OCR de até 4.000 páginas, extrai quesitos, cita a página dos autos. | Sim | R$ 197 | Rastreabilidade [V] |
| PeríciaIA | Gestão + editor com IA | Sim | R$ 75–187 | Diz ter integração com o Sisperjud [NC] |
| MaisPerícia, Fluxo Pericial, eXpert, Radar Perito | Gestão (prazos via DataJud/DJEN) + minutas com IA | Sim | R$ 50–300 | Generalistas [V/NC] |

**Leitura do mercado:**
- **Ninguém baixa os autos inteiros automaticamente.** Os produtos extraem de PDF enviado pelo perito. O DataJud só dá metadados [NC].
- **Ninguém combina IA generativa com valoração estruturada por baremos e coerência interna.** O MSLaudo tem baremos e não tem IA; os produtos de IA não mostram baremos.
- **Nenhum exporta comprovadamente para o Sisperjud.**
- **Diferenciais possíveis:**
  - adaptar-se ao modelo de cada perito;
  - validar coerência (datas, exame × conclusão, quesitos × checkboxes, concausa × déficit);
  - lista branca de normas vigentes;
  - literatura citada e pertinente ao caso.

---

## 11. Implicações para o laudo-ia

### 11.1 Limites que não se negociam

- **Quem decide.** A IA redige; o perito decide e assina.
  - CEM, art. 92.
  - Res. CFM 2.430/2025, art. 5º, §6º.
  - Res. CFM 2.454/2026, arts. 4º e 7º: IA só como apoio, julgamento crítico, responsabilidade integral.
  - A Res. 2.454 manda informar o paciente quando a IA é apoio relevante (art. 5º, §1º). Aplicá-la ao periciando é analogia ainda não pacífica [V a norma; interpretação nossa].
  - No RS, a Res. CREMERS 6/2025 exige identificar o software nos documentos quando a IA for determinante [V].
- **Nada inventado.** Nunca inventar achado, medida, data ou transcrição. Campo ausente vira **pendência visível**, nunca texto plausível (CPC, art. 158).
- **Neutralidade.** O sistema não aceita instruções do tipo "deixe caracterizado X" sem achados que sustentem X. Se o perito escolhe uma conclusão que os achados não sustentam, o sistema sinaliza a lacuna (CEM, art. 98).
- **Rastreabilidade.** Toda afirmação aponta sua origem: folha ou Id dos autos, campo do exame ou referência bibliográfica.
- **Nada oculto no documento.** Nenhum texto oculto ou meta no documento final.
  - Há relatos de laudo com *prompt injection* dirigido à IA do juízo (TJRN, 09/2026) [NC].
  - A Res. CNJ 615/2025 classifica como alto risco a IA do tribunal que avalia provas [V].

### 11.2 Arquitetura que o conjunto de laudos sugere

1. **Modelo do perito como entrada.** Importar o .docx de cada perito, com seções, ordem, texto fixo, checkboxes (`w14:checkbox`), cabeçalho e rodapé com imagem, e preencher. Não impor um modelo canônico.
2. **Módulos por tipo de perícia,** cada um com sua cadeia de raciocínio (§7.3) e seus quesitos típicos:
   - acidentária;
   - trabalhista com trauma;
   - trabalhista com doença osteomuscular;
   - psiquiátrica;
   - depois, previdenciária federal (Sisperjud).
3. **Modelo de pendências.** Todo valor-padrão do modelo (sinais vitais, exame normal, conclusão, quesito pré-respondido) vira campo pendente explícito. O texto "normal" só entra para segmentos efetivamente examinados e confirmados.
4. **Ficha de exame com números,** conforme a lesão:
   - goniometria bilateral (ativa e passiva), com a referência;
   - força por grupo muscular;
   - perimetria;
   - testes nomeados com resultado;
   - neurológico do território em risco;
   - escalas psiquiátricas apenas como complemento.
5. **Extração dos autos.** OCR com visão para documentos digitalizados e manuscritos. Referência por fls. (TJRJ) ou Id (PJe-JT). Extração dos quesitos de cada parte.
6. **Validadores:**
   - datas (assinatura ≥ exame; DID ≤ DII; DIB no 16º dia);
   - identidade (número CNJ × classe × termos; nomes e números só do caso atual; UF do CRM);
   - normas por lista branca com vigência (§8.1);
   - exame completo para o tipo de lesão;
   - texto-padrão × achado específico (contradições do §8.2);
   - quesitos: nenhum em branco, "vide item" só para item que existe, checkboxes coerentes com a conclusão;
   - valoração: concausa aplicada, escala declarada, baremo e versão vigentes, classe de Weliton só para sequela permanente;
   - escopo: nada de "faz jus" ou responsabilidade civil no texto do perito.
7. **Cálculos:** % de redução no Anexo III, fórmula de Penteado, pensão × concausa (apenas como dado para o perito), conversões de escala.
8. **Literatura.** Biblioteca curta, por lesão ou patologia, com referência completa, sem reproduzir texto de terceiros.
9. **LGPD e segurança.**
   - Dado de saúde é sensível (LGPD, art. 11).
   - A Res. CFM 2.454/2026, art. 6º, §3º, veda IA sem segurança mínima para dados sensíveis [V].
   - Evitar contaminação entre casos.
   - Os seis arquivos em `docs/laudos/` têm dados reais de periciandos, empresas e peritos (CPF, RG, endereço, dados bancários, fotos).

---

## 12. Perguntas em aberto

1. **Persona.** Quem redige hoje: o perito ou uma assistente que atende vários peritos? Muda o fluxo de revisão e assinatura.
2. **Escopo.** TJRJ acidentária e TRT (ortopedia, psiquiatria, medicina do trabalho) desde o início? E previdenciária federal (Sisperjud)?
3. **Modelos.** Cada perito mantém o seu, ou haverá um modelo padrão do produto?
4. **Uso atual de IA.** Como o ChatGPT é usado hoje (que prompts, em que seções)? É a linha de base a superar.
5. **Autos.** Existem os PDFs dos autos dos seis casos? Permitiriam testar a extração e comparar a saída com os laudos finalizados.
6. **Vigilante.** Ele era armado na data do acidente? O que diz a perícia do INSS (fls. 196 e 210)?
7. **Declarar IA.** O laudo vai declarar o uso de IA? A norma não obriga expressamente fora do RS.

---

## 13. Glossário

| Termo | Significado |
|---|---|
| Autos / fls. / Id | O processo; folha (TJRJ); identificador de documento no PJe |
| Quesito | Pergunta do juiz ou das partes ao perito |
| Assistente técnico | Médico da parte que acompanha a perícia |
| CAT | Comunicação de Acidente de Trabalho |
| CNIS / INFBEN | Vínculos e contribuições / benefícios do INSS |
| CBO / CNAE | Classificação de ocupações / de atividades econômicas (o CNAE define o NTEP) |
| ASO / PCMSO / PGR / AET / LTCAT / PPP | Documentos de saúde e segurança do trabalho (§5.3) |
| Profissiografia | Tarefas reais e exigências físicas da função |
| Nexo / concausa | Relação causal / fator que contribui sem ser a causa única (Lei 8.213, art. 21, I) |
| NTEP / LDRT | Nexo epidemiológico previdenciário / lista de doenças relacionadas ao trabalho |
| Consolidação | Estabilização da lesão, quando a sequela vira definitiva |
| Déficit funcional | Perda de função independente da profissão (baremo) |
| Repercussão profissional | Efeito da sequela na profissão (por exemplo, classes de Weliton) |
| *Quantum doloris* | Sofrimento físico e psíquico, em 7 graus |
| Baremo | Tabela de valoração de incapacidade |
| Goniometria / perimetria / MRC | Ângulo articular / circunferência do membro / escala de força de 0 a 5 |
| PHQ-9 / GAD-7 | Escalas de rastreio de depressão e de ansiedade, por autorrelato |
| Sisperjud | Sistema de perícias do CNJ (formulário estruturado) |

---

## 14. Fontes principais

- **Leis:**
  - CPC: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm
  - Lei 8.213/91: https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm
  - Decreto 3.048/99: https://www.planalto.gov.br/ccivil_03/decreto/d3048.htm
  - Anexos II e III do Decreto 3.048: https://www.planalto.gov.br/ccivil_03/decreto/D3048anexoii-iii-iv.htm
  - CLT: https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm
  - Código Civil: https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm
  - Lei 13.876/2019: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13876.htm
  - LGPD: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- **CFM:**
  - Código de Ética Médica: https://portal.cfm.org.br/images/PDF/cem2019.pdf
  - Res. 2.430/2025: https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2025/2430_2025.pdf
  - Res. 2.454/2026 (IA): https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2026/2454_2026.pdf
  - Res. 2.323/2022: https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2022/2323_2022.pdf
  - Res. 2.056/2013: https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2013/2056_2013.pdf
  - Res. 2.381/2024: https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2024/2381_2024.pdf
- **CNJ:**
  - Res. 595/2024 (compilada): https://atos.cnj.jus.br/files/compilado17170020250731688ba50c0cafa.pdf
  - Manual do Sisperjud: https://www.tjba.jus.br/portal/wp-content/uploads/2025/11/MANUAL-DO-USUARIO-SISPERJUD.pdf
  - Res. 615/2025 (IA no Judiciário): https://atos.cnj.jus.br/files/original1555302025031467d4517244566.pdf
- **CSJT:**
  - Res. 247/2019 (7ª republicação): https://juslaboris.tst.jus.br/bitstream/handle/20.500.12178/164654/2019_res0247_csjt_rep07.pdf
  - Ato 97/2025: https://juslaboris.tst.jus.br/bitstream/handle/20.500.12178/258471/2025_ato0097_csjt.pdf
- **TST:**
  - Tema 125: https://portal.trt3.jus.br/internet/jurisprudencia/incidentes-suscitados-irr-iac-arginc-tst/downloads/tema-125-irr-0020465-17-2022-5-04-0521-acordao-publicado-09-05-2025.pdf
  - Súmulas (Livro TST 2025): https://www.tst.jus.br/documents/10157/63003/LivroInternet(11)pdf.pdf
- **MTE:**
  - NR-1: https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1
  - Portaria 765/2025 (prorrogação psicossocial): https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/2025/portaria-mte-no-765-prorroga-inicio-de-vigencia-cap-1-5-da-nr-01.pdf
- **Ministério da Saúde:**
  - LDRT (Portaria GM/MS 1.999/2023): https://bvsms.saude.gov.br/bvs/saudelegis/gm/2023/prt1999_29_11_2023.html
  - Manual "Doenças Relacionadas ao Trabalho" (Schilling): https://bvsms.saude.gov.br/bvs/publicacoes/doencas_relacionadas_trabalho1.pdf
- **ABMLPM:**
  - Diretriz de dano pessoal (2025): https://amb.org.br/wp-content/uploads/2026/01/DIRETRIZ-PARA-VERIFICACAO-DO-DANO-CORPORAL-ABMLPM_FINAL.pdf
  - Protocolo de laudo na Justiça do Trabalho: https://amb.org.br/wp-content/uploads/2025/03/07.02.25_PROTOCOLO-PARA-A-ELABORACAO-DE-LAUDO-MEDICO-PERICIAL-NA-JUSTICA-DO-TRABALHO_ABMLPM.docx.pdf
- **Nexo e valoração:**
  - Vieira e Quintero, *Aspectos práticos da avaliação do dano corporal* (Coimbra, 2008): https://dl.uc.pt/rest/bitstreams/11383588/retrieve
  - Penteado e Saladini, Rev. TST 2020: https://hdl.handle.net/20.500.12178/176095
  - Oliveira, Rev. TRT-2 2013: https://hdl.handle.net/20.500.12178/77838
  - Santos WB, RBMT 2012: https://www.rbmt.org.br/details/84/pt-BR/proposta-para-a-valoracao-da-repercussao-laboral-em-direito-do-trabalho-e-direito-civil
  - AIPE, *Saúde Debate* 2016 (doi:10.1590/0103-1104-20161080010)
  - Decreto argentino 659/1996: http://servicios.infoleg.gob.ar/infolegInternet/anexos/35000-39999/37573/norma.htm
- **Psiquiatria:**
  - Kroenke 2001 (doi:10.1046/j.1525-1497.2001.016009606.x)
  - Spitzer 2006 (doi:10.1001/archinte.166.10.1092)
  - Levis 2019 (doi:10.1136/bmj.l1476)
  - *Psiquiatria forense de Taborda*, 3ª ed., 2016
- **Ortopedia (PMID):**
  - Robinson 2003 (12499966)
  - Yetter 2021 (33711499)
  - McKee 2000 (11130643)
  - Han 2022 (36045372)
  - Morrey 1981 (7240327)
  - Sardelli 2011 (21368079)
  - Zwerus 2019 (31210794)
  - Armstrong 1998 (9883416)
  - Bohannon 2005 (16180603)
  - Giannicola 2014 (24380536)
- **Mercado:**
  - MSLaudo: https://www.medsafesolution.com.br/mslaudo/
  - Perícia Today: https://pericia.today/
  - Peritia: https://www.sistemaperitia.com/
  - Perícia.AI: https://pericia.ai/
  - PeríciaIA: https://www.periciaia.com.br/
