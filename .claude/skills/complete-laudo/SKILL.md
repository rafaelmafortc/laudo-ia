---
name: complete-laudo
description: Responde os quesitos e redige a discussão e a conclusão de um laudo pericial médico judicial (acidentária no TJRJ ou trabalhista no TRT) a partir de um rascunho .docx em que essas seções estão marcadas em amarelo. Use quando o usuário enviar ou apontar um laudo em rascunho e pedir para responder os quesitos, concluir o laudo, redigir a discussão ou "preencher o amarelo".
---

# Concluir laudo pericial

Recebe um laudo em rascunho e devolve, prontos para colar no documento, a **DISCUSSÃO E CONCLUSÃO** e a **RESPOSTA AOS QUESITOS**. Antes deles, devolve a lista do que falta ou está inconsistente.

A responsabilidade pelo laudo é do perito e não se transfere (Res. CFM 2.430/2025, art. 5º, §6º; Res. CFM 2.454/2026, art. 7º). O que esta skill produz é uma **minuta para revisão do perito**.

## Convenção do rascunho

- **Vermelho:** dado do caso preenchido pela assistente ou pelo perito (exame, antecedentes, partes condicionais do texto). É fato a usar, mas precisa ser checado quanto à coerência.
- **Amarelo:** seção a redigir. Hoje são "DISCUSSÃO E CONCLUSÃO" e "RESPOSTA AOS QUESITOS".
- **Texto sem cor:** texto fixo do modelo do perito, ou texto colado dos autos.

## Passo a passo

### 1. Extrair o rascunho

```bash
python3 .claude/skills/complete-laudo/scripts/extract_docx.py "<laudo.docx>" --images "<pasta temporária>"
```

- **Saída.** Texto com `[AMARELO]…[/AMARELO]` e `[VERMELHO]…[/VERMELHO]`, tabelas como `| a | b |`, checkboxes como ☐/☒, e `[IMAGEM: caminho]` onde há imagem.
- **Arquivo .doc:** converta antes com `textutil -convert docx`.
- **Pasta temporária:** use o scratchpad da sessão, nunca uma pasta do repositório, porque as imagens têm dados pessoais.
- **Imagens a ler:**
  - Documentos médicos digitalizados (linhas da tabela de documentos que só têm imagem, inclusive manuscritos): leia com a ferramenta de leitura de imagem e use o conteúdo como fato, citando a folha (fls.) ou o Id.
  - Fotos do exame e documento de identidade: não é preciso ler.

### 2. Identificar o tipo e carregar as regras

- Leia `references/dominio.md`. Identifique o tipo de processo (§1 da referência): acidentária ou trabalhista.
- Leia o laudo **finalizado** do mesmo tipo em `docs/laudos/` como referência de **estilo e formato**:
  - acidentária: `LAUDO MÉDICO TJRJ (FINALIZADO).docx`;
  - trabalhista: `LAUDO MÉDICO TRT (FINALIZADO).docx`.
- Imite o tom, a extensão, o formato "Resp.:" e o uso de ☒. **Não copie** os erros listados no §5 da referência.

### 3. Montar a ficha do caso

Antes de redigir, organize o que o laudo **efetivamente** contém, cada item com sua origem (seção do laudo, ou fls./Id):

- **Partes e processo:** número, vara, tipo.
- **Datas:** acidente ou início dos sintomas, internação, cirurgia, benefícios (espécie, DIB e DCB), documentos-chave, exame pericial, assinatura.
- **Atividade na data do acidente**, para acidentária (Decreto 3.048, art. 104, §8º), ou exposição por reclamada e período, para trabalhista.
- **Achados do exame:** só os que estão escritos, com os números.
- **Documentos médicos:** o que dizem, inclusive as imagens lidas.
- **Quesitos:** todos, por parte, na numeração original.

### 4. Checar lacunas e inconsistências

Liste, do mais grave para o menos grave:

- **Dados que faltam para responder um quesito ou sustentar a conclusão** (§6 da referência). Exemplo: o quesito pede flexão e extensão, e só a extensão foi medida.
- **Contradições internas:**
  - texto-padrão do exame × achado específico;
  - antecedentes × história da doença;
  - datas (assinatura antes do exame, versões diferentes do mecanismo do acidente);
  - conclusão pré-escrita no modelo × achados.
- **Respostas pré-preenchidas no modelo que contrariam a conclusão.** Exemplo: "Não há divergência" com o INSS.
- **Termos e normas a corrigir fora do amarelo** (§4 da referência). Liste-os; não reescreva o resto do laudo.

### 5. Definir a conclusão

A conclusão é do perito. A skill confere ou propõe, nunca decide.

- **O rascunho ou o pedido já traz a conclusão** (ex.: "AUMENTA O ESFORÇO" em vermelho, "NÃO há nexo" no modelo):
  - Confira se os achados registrados a sustentam, passo a passo da cadeia do tipo de processo.
  - **Sustentam:** fundamente a conclusão.
  - **Não sustentam, ou falta um dado decisivo:** sinalize no topo das pendências como **CONFLITO DE CONCLUSÃO**. Diga o que diverge, ou que dado falta, e qual conclusão os achados sustentariam. Redija a discussão e os quesitos com a conclusão do perito, mas marque `[REVISAR: conflito com os achados]` nos pontos afetados. Não troque a conclusão por conta própria.
- **O rascunho não traz conclusão:**
  - Proponha uma, marcada como **CONCLUSÃO PROPOSTA**, com a alternativa mais próxima e o dado que faria mudar de uma para a outra.
  - Redija a discussão e os quesitos com a proposta. O perito confirma antes de usar.

### 6. Redigir a DISCUSSÃO E CONCLUSÃO

- **Ordem.** Siga a cadeia do tipo de processo (referência §2.2 ou §3.2). Cada passo cita o achado ou documento que o sustenta.
- **Repercussão.** Na acidentária, explicite a repercussão tarefa a tarefa. É o que separa "redução funcional" de "redução da capacidade laborativa".
- **Fecho.** Termine com a frase de conclusão no padrão do perito (ex.: "este Perito CONCLUI que…"), seguida das observações finais com as normas vigentes (texto pronto no §4 da referência).
- **Linguagem.** Formal, simples e com coerência lógica (CPC, art. 473, §1º). Terceira pessoa ("este Perito"). Termos corretos para o tipo (Autor/Réu ou Reclamante/Reclamada).

### 7. Responder os quesitos

- **Todos, sem exceção** (CPC, art. 473, IV): Juízo, autor e réu, na numeração original. Se o Juízo não apresentou quesitos, mantenha "Não encontrado quesitos nos autos."
- **Forma da resposta.** Conclusiva e curta, coerente com a discussão. Ao lado de uma resposta "Sim" ou "Não", uma frase de fundamento.
- **Checkboxes.** Reproduza as opções e marque com ☒ a escolhida. Não marque caixas de quesitos prejudicados.
- **"Prejudicado"** só com o motivo ("Prejudicado: não há incapacidade permanente").
- **"Vide item"** só se o item existir no laudo e responder ao que foi perguntado.
- **Quesito fora da medicina:** "Extrapola o objeto da perícia médica", mais o motivo.
- **Percentuais:** na acidentária, não são objeto desta perícia. Na trabalhista, informe o método e o valor.

## Regras invioláveis

- **Nunca inventar** achado, medida, data, documento ou fala do periciando. Se faltar, escreva `[PENDENTE: o que falta]` no ponto do texto e liste nas pendências.
- **Não contradizer o exame.** Se a conclusão exigir um achado que não foi registrado, não conclua como se ele existisse.
- **Neutralidade (CEM, art. 98).** Não escreva "para deixar caracterizado" um resultado. A conclusão decorre dos achados.
- **Sem juízo jurídico.** Nada de "faz jus", "tem direito", culpa ou responsabilidade da empresa.
- **Sem texto meta** no material para colar: nada de "segue a versão", "conforme solicitado", comentários sobre IA.
- **Literatura.** Não reproduza texto de livros ou sites. Se for preciso, resuma em poucas frases e cite a referência completa.
- **Dados pessoais.** Não repita CPF, RG, endereço ou dados bancários na resposta. Use apenas dados do laudo atual.

## Formato da resposta

1. **Pendências e inconsistências.** Lista curta, do mais grave para o menos grave, cada item com onde está e o que fazer. Comece pelos itens que bloqueiam a conclusão.
2. **DISCUSSÃO E CONCLUSÃO.** Texto pronto para colar.
3. **RESPOSTA AOS QUESITOS.** Por parte, com o enunciado do quesito resumido e "Resp.: …". Checkboxes com ☐/☒.
4. **Correções fora do amarelo.** Uma linha por item: termo errado, norma revogada, data incoerente.
