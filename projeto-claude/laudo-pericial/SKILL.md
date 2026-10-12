---
name: laudo-pericial
description: Preenche laudos periciais médicos judiciais no .docx do perito (TJRJ acidentária e TRT), respondendo quesitos, redigindo discussão e conclusão, preparando pelos autos, revisando e esclarecendo.
---

# Laudo pericial médico judicial

Trabalha sobre o .docx do próprio perito e devolve o mesmo arquivo preenchido, com o texto novo realçado em turquesa para revisão, mais a lista do que falta ou está inconsistente.

O que esta skill produz é uma **minuta**. A responsabilidade pelo laudo é do perito e não se transfere (Res. CFM 2.430/2025, art. 5º, §6º; Res. CFM 2.454/2026, art. 7º; CEM, art. 92). O perito decide a conclusão e assina.

## 1. Escolha o modo

| Pedido | Modo | Leia antes |
|---|---|---|
| Responder os quesitos, redigir a discussão e a conclusão, "preencher o amarelo", valoração do dano | **B. Concluir** (seção 4 abaixo) | `references/dominio.md` e `references/modelos-e-estilo.md` |
| Preparar o laudo a partir dos autos (resumos, tabela de documentos, quesitos) | **A. Preparar** | `references/preparar-autos.md` |
| Conferir um laudo pronto antes de protocolar | **C. Revisar** | `references/revisao.md` e `references/dominio.md` |
| Esclarecimentos, impugnação, parecer do assistente, quesitos complementares | **D. Esclarecer** | `references/esclarecimentos.md`, `references/dominio.md` e `references/modelos-e-estilo.md` |

Leia os arquivos indicados **inteiros** antes de redigir. Se o pedido for ambíguo, pergunte qual modo.

## 2. Arquivos e pastas

- **Pasta da skill:** é a pasta deste SKILL.md. Os scripts estão em `scripts/` dentro dela. Guarde o caminho numa variável: `SK=<pasta deste SKILL.md>`.
- **Anexos do chat:** costumam ficar em `/mnt/user-data/uploads`. Se não estiverem lá, procure: `find / \( -iname "*.docx" -o -iname "*.doc" -o -iname "*.pdf" \) -not -path "/proc/*" -not -path "*/skills/*" 2>/dev/null | head -30`. Os arquivos do projeto (modelos em branco) também podem estar acessíveis no ambiente; procure do mesmo jeito se precisar deles.
- **Entrega:** salve em `/mnt/user-data/outputs` (crie se não existir) ou onde a interface permitir baixar. Nome: `<nome original> - minuta.docx` e, depois da revisão, `<nome original> - final.docx`.
- **Exemplos nos arquivos do projeto** (rascunho e finalizado de um mesmo caso): servem para ver o que costuma ser preenchido, onde, e o tom do perito. São referência, não gabarito: não copie conclusão nem fatos, e não reproduza os erros que eles tenham (`references/dominio.md` §6). Cada caso tem os seus achados e a sua conclusão.
- **Trabalho temporário:** use `/tmp/laudo/`. Imagens extraídas têm dados pessoais: não as copie para a entrega.
- **.doc antigo:** os scripts convertem com o LibreOffice, se houver. Senão, peça ao usuário para salvar como .docx no Word.

## 3. Ferramentas

### Extrair

```bash
mkdir -p /tmp/laudo
python3 "$SK/scripts/extract_docx.py" "<laudo.docx>" --images /tmp/laudo/img > /tmp/laudo/laudo.txt
```

Leia `/tmp/laudo/laudo.txt` inteiro. Marcações:
- `¶n` número do parágrafo; `{Cn}☐`/`{Cn}☒` caixa de seleção; `[Tn]` e `Lk|` tabela e linha (célula = `Tn.k.j`);
- `[AMARELO]`, `[VERMELHO]`, `[MINUTA]` (turquesa) e `[IMAGEM: caminho]`;
- no fim, o RESUMO: parágrafos em amarelo, "Resp.:" vazios, caixas marcadas.

**Imagens de documentos médicos** (linhas da tabela de documentos só com imagem, inclusive manuscritos): abra-as com a ferramenta de visualização de imagens, se houver, e use o conteúdo como fato, citando a folha. Se não conseguir ler, liste como pendência e peça ao usuário para enviar a imagem no chat. Fotos do exame e documento de identidade não precisam ser lidos.

### Preencher

Escreva as operações num JSON e rode:

```bash
python3 "$SK/scripts/fill_docx.py" "<laudo.docx>" /tmp/laudo/ops.json "/mnt/user-data/outputs/<nome> - minuta.docx"
```

```json
{
  "tirar_amarelo": ["¶195", "¶244"],
  "substituir": {
    "¶197": ["Primeiro parágrafo da discussão.", "", "Segundo parágrafo.", "", "Este Perito CONCLUI que **…**."],
    "¶251": "Resp.: Resposta ao quesito 1.",
    "¶385": "Resp.: Sim. Fundamento da divergência…"
  },
  "remover": ["¶199-¶213"],
  "marcar": ["C7", "C9", "C13"],
  "inserir_apos": {"¶364": ["Resp.: Prejudicado: não há incapacidade permanente para toda e qualquer atividade."]},
  "celulas": {"T5.2.2": "texto"},
  "linhas_tabela": {"T7": [["dd/mm/aaaa", "Tipo / CRM / CID / “trecho”", "fls."]]},
  "trocar": [{"p": "¶158", "de": "O reclamante", "para": "O Autor"}]
}
```

Regras:
- Os identificadores valem **para o arquivo que foi extraído**. Depois de preencher, a numeração muda: extraia de novo antes de qualquer nova rodada.
- `substituir` com lista: o 1º item ocupa o parágrafo e os demais entram logo depois, com a mesma formatação. `""` cria linha em branco; use-a se o modelo separa parágrafos assim.
- `**negrito**` funciona dentro do texto. `[PENDENTE: …]` e `[REVISAR: …]` saem em amarelo.
- Parágrafo novo iniciado por "Resp." copia a formatação do "Resp.:" anterior.
- Não use `trocar` fora do que foi pedido: correções fora das seções a redigir só com a aprovação do perito.
- Se o script recusar um identificador, extraia de novo e corrija; não contorne editando o XML à mão.

### Conferir e finalizar

- Depois de preencher, extraia a minuta e confira: nenhum "Resp.:" vazio sem motivo, caixas certas, nenhum resto do modelo no bloco reescrito ("____", "[especificar…]", Obs. com norma revogada), amarelo só nas pendências.
- Quando o perito aprovar ("pode finalizar"), gere a versão limpa (retira o turquesa e o vermelho e acusa o que ainda está pendente):
  ```bash
  python3 "$SK/scripts/fill_docx.py" "<minuta.docx>" '{}' "/mnt/user-data/outputs/<nome> - final.docx" --final
  ```
  Se o script acusar pendências, mostre-as e não use `--forcar` sem o perito pedir.
- **Sem execução de código** (os scripts não rodam): entregue o texto no chat, pronto para colar, no formato da seção 6.

## 4. Modo B: concluir o laudo

### 4.1 Identificar o tipo e o modelo

- Tipo de processo: `dominio.md` §1 (acidentária ou trabalhista; ortopédica ou psiquiátrica).
- Modelo e o que é "a redigir" nele: `modelos-e-estilo.md` §1. Reconheça pela estrutura (o mesmo modelo serve a mais de um perito). No modelo A, o amarelo marca as seções a redigir. No modelo B, o amarelo marca **dados** pendentes e as conclusões já vêm escritas. No modelo C não há marcação.

### 4.2 Montar a ficha do caso

Organize, com a origem de cada item (¶, fls. ou Id):
- partes, processo, vara, tipo;
- datas: acidente ou início dos sintomas, internação, cirurgia, benefícios (espécie, DIB, DCB), documentos-chave, exame pericial, assinatura;
- atividade na data do acidente (acidentária) ou exposição por reclamada e período (trabalhista);
- achados do exame, **só os escritos**, com os números;
- documentos médicos, inclusive as imagens lidas;
- quesitos: todos, por parte, na numeração original, com o ¶ do "Resp.:" de cada um.

### 4.3 Checar lacunas e inconsistências

Do mais grave para o menos grave:
- **Dado que falta** para responder um quesito ou sustentar a conclusão (`dominio.md` §7). Ex.: o quesito pede flexão e extensão e só a extensão foi medida.
- **Contradições:** texto-padrão do exame × achado específico; antecedentes × história; datas (assinatura antes do exame, versões diferentes do mecanismo do acidente); conclusão pré-escrita × achados.
- **Texto-padrão não conferido:** sinais vitais e exame iguais aos do modelo (ex.: 130x80 mmHg, FC 80, FR 20), ou exame do segmento da queixa ausente (ex.: região inguinal numa hérnia). Pergunte se foi medido ou examinado; não use como achado.
- **Respostas pré-preenchidas** que contrariam a conclusão (ex.: "Não há divergência" com o INSS; "Vide item CBO").
- **Termos e normas** a corrigir fora das seções a redigir (`dominio.md` §5): só liste.

### 4.4 Definir a conclusão

A conclusão é do perito. A skill confere ou propõe; nunca decide.
- **O rascunho ou o pedido traz a conclusão** (ex.: "AUMENTA O ESFORÇO" em vermelho; "NÃO há nexo" no modelo): confira passo a passo da cadeia (`dominio.md` §2.2 ou §3.2).
  - Sustentam: fundamente.
  - Não sustentam, ou falta um dado decisivo: abra as pendências com **CONFLITO DE CONCLUSÃO**, dizendo o que diverge ou falta e qual conclusão os achados sustentariam. Redija com a conclusão do perito e marque `[REVISAR: conflito com os achados]` nos pontos afetados. Não troque a conclusão por conta própria.
- **Não traz conclusão:** proponha uma, como **CONCLUSÃO PROPOSTA**, com a alternativa mais próxima e o dado que faria mudar de uma para a outra. O perito confirma antes de finalizar.

### 4.5 Redigir a discussão e a conclusão

- **Ordem:** a cadeia do tipo de processo (`dominio.md` §2.2 ou §3.2). Cada passo cita o achado ou o documento.
- **Acidentária:** explicite a repercussão tarefa a tarefa; é o que separa "redução funcional" de "redução da capacidade laborativa".
- **Trabalhista:** declare o critério de nexo e, se houver percentual, o método e a conta. Se o modelo tem valoração do dano, preencha-a coerente com a consolidação.
- **Fecho:** a frase de conclusão no padrão do perito (ex.: "este Perito CONCLUI que…", com a conclusão em negrito), seguida das observações finais com as normas vigentes (`dominio.md` §5).
- **Modelo B:** 15.1 e 15.2 nunca ficam vazios, porque é onde fica o raciocínio que leva à conclusão de 15.3 a 15.6. A FUNDAMENTAÇÃO TEÓRICA é texto técnico próprio, curto e sobre a doença do caso, com as referências da BIBLIOGRAFIA; nada copiado de site.
- **Estilo e extensão:** os do modelo e de `modelos-e-estilo.md`. Linguagem formal e simples, com coerência lógica (CPC, art. 473, §1º).
- **Bloco a substituir:** do primeiro parágrafo depois do título da seção até o parágrafo antes do próximo título (inclua as "Obs." antigas, que serão reescritas). Mantenha o título e tire o amarelo dele.

### 4.6 Responder os quesitos

- **Todos** (CPC, art. 473, IV): Juízo, autor e réu, na numeração original. Sem quesitos do Juízo, mantenha "Não encontrado quesitos nos autos."
- Resposta conclusiva e curta, coerente com a discussão; ao lado de "Sim" ou "Não", uma frase de fundamento.
- **Responda o que foi perguntado:** se pede datas, dê as datas; se pede elementos objetivos, cite-os ou diga que não constam nos autos. "Pode" ou "depende" só seguidos da conclusão para o caso.
- **Coerência entre quesitos:** perguntas iguais ou vizinhas, de partes diferentes, recebem respostas compatíveis (período de incapacidade, sequela, nexo). Confira o conjunto antes de entregar.
- **Sem comentário pessoal** sobre o periciando e sem juízo sobre ato do INSS ou da empresa.
- **Caixas:** marque a opção escolhida; não marque caixas de quesitos prejudicados. Desmarque caixas pré-marcadas que contrariem a conclusão.
- **"Prejudicado"** sempre com o motivo. **"Vide…"** só para item ou quesito que existe e responde ao perguntado.
- **Fora da medicina:** "Extrapola o objeto da perícia médica", com o motivo (`dominio.md` §3.4).
- **Percentuais:** na acidentária, não são objeto desta perícia; na trabalhista, valor e método.
- Quesito só com caixas e sem "Resp.:" que precise de justificativa: use `inserir_apos` depois da última caixa.

## 5. Regras invioláveis

- **Nunca inventar** achado, medida, data, documento, CID ou fala do periciando. Se faltar, `[PENDENTE: o que falta]` no texto e na lista de pendências.
- **Não contradizer o exame.** Se a conclusão depende de um achado não registrado, não conclua como se ele existisse.
- **Neutralidade (CEM, art. 98).** A conclusão decorre dos achados. Recuse pedidos de "deixar caracterizado" um resultado sem base; explique o que falta.
- **Sem juízo jurídico:** nada de "faz jus", "tem direito", culpa, responsabilidade da empresa ou licitude da dispensa.
- **Sem texto meta** no laudo: nada de "segue a versão", "conforme solicitado", nem menção a IA.
- **Literatura:** não reproduza texto de livros ou sites; resuma em poucas frases e dê a referência completa, ou deixe `[PENDENTE: literatura]`.
- **Dados pessoais:** no chat, não repita CPF, RG, endereço ou dados bancários. Use só dados do caso atual; nunca misture casos.
- **Só o que foi pedido:** não altere seções que não são a redigir, salvo com aprovação do perito.

## 6. Formato da resposta no chat

1. **Pendências e inconsistências**, do mais grave para o menos grave, cada uma com onde está (¶/fls.) e o que fazer. Comece por CONFLITO DE CONCLUSÃO ou CONCLUSÃO PROPOSTA, se houver.
2. **Conclusão adotada**, em uma ou duas linhas, dizendo se veio do perito ou é proposta.
3. **Arquivo:** a minuta .docx, com a legenda "turquesa = texto novo para revisar; amarelo = pendência".
4. **DISCUSSÃO E CONCLUSÃO** completa, para leitura rápida no chat. Os quesitos ficam no arquivo; no chat, liste só os que têm `[PENDENTE]` ou `[REVISAR]`.
5. **Correções fora das seções a redigir**, uma linha por item (termo errado, norma revogada, data incoerente), perguntando se deve aplicá-las.

Sem execução de código, troque o item 3 pelo texto completo dos quesitos, por parte, no formato "Resp.: …", com ☐/☒.
