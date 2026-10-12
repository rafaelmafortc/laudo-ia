# Modo A: preparar o laudo a partir dos autos

Objetivo: a partir do PDF do processo e do modelo do perito (.docx), preencher as seções que vêm dos autos, antes do exame. O exame, a discussão e os quesitos ficam para depois (modo B).

## 1. Ler os autos

- **Texto com página:** extraia página a página, para citar a folha.
  ```bash
  python3 - "$PDF" <<'EOF'
  import sys, pdfplumber
  with pdfplumber.open(sys.argv[1]) as pdf:
      for i, page in enumerate(pdf.pages, 1):
          print(f"\n=== PÁGINA {i} ===\n{page.extract_text() or '[SEM TEXTO: página digitalizada]'}")
  EOF
  ```
  Sem pdfplumber, use `pdftotext -layout` ou pypdf. Salve a saída em arquivo e procure nela (grep) em vez de ler tudo de uma vez.
- **Folha e Id:**
  - TJRJ: use o número de folha carimbado na página ("fls. 123"), se houver; senão, o número da página do PDF, e avise que é a página do PDF.
  - PJe (TRT): use o Id do documento ("Id 60c9064"), que aparece no rodapé ou no cabeçalho; acrescente a folha se o modelo do perito usar as duas.
- **Páginas digitalizadas ou manuscritas:** gere a imagem (`pdftoppm -r 150 -png -f N -l N`) e leia-a com a ferramenta de visualização de imagens, se houver. Se não conseguir ler, liste a folha como `[PENDENTE: documento ilegível ou só imagem, fls. N]`. Se houver OCR (`tesseract -l por`), use-o só como apoio e confira o resultado.

## 2. O que extrair, por seção do modelo

| Seção | Fonte nos autos | Como escrever |
|---|---|---|
| Cabeçalho (vara, número, partes) | Capa, petição inicial | Exatamente como na capa. Classe processual da capa (não copie "ATSum" de outro caso). |
| Objetivo | Despacho que nomeou o perito; pedidos da inicial | Acidentária: "CONCESSÃO DE AUXÍLIO-ACIDENTE". TRT: nexo, redução da capacidade, incapacidade, patologias citadas. |
| Alegação da parte autora | Petição inicial | Resumo fiel, entre aspas, em terceira pessoa, 120 a 250 palavras: função, evento ou adoecimento, datas, tratamento, benefício, sequelas alegadas, pedido. Sem adjetivos que não estejam na inicial. |
| Contestação (TRT) | Cada contestação | Um resumo por reclamada, entre aspas, 100 a 200 palavras: tese médica e fática (aptidão nos ASOs, causa degenerativa, culpa da vítima…). |
| Identificação | Inicial, documentos pessoais, CTPS | Só o que consta. Campo sem dado: "não encontrado nos autos". |
| Histórico trabalhista | CNIS, CTPS | Tabela Empresa / Função / Período, em ordem cronológica. |
| CBO | CTPS/CNIS (código) | Código e título. A descrição deve ser a oficial (mtecbo.gov.br); se não tiver acesso, `[PENDENTE: descrição oficial da CBO]`. Não invente paráfrase entre aspas. |
| Histórico previdenciário | CNIS, INFBEN, cartas do INSS | Tabela Número / Benefício (espécie) / Período, com o CID quando constar. |
| Histórico laboral na reclamada (TRT) | Ficha de registro, ASOs, PPP, contestação | Admissão, demissão, ASOs (fls. ou Id – data – resultado), jornada, função, EPIs (ficha de EPI). |
| Documentos médicos | Atestados, laudos, exames, prontuários, CAT | Uma linha por documento, em ordem de data: DATA / "Tipo / CRM nº / CID / “transcrição literal do trecho relevante”" / FLS. Exame de imagem: tipo, região e conclusão literal. CRM ilegível: "CRM ilegível". |
| Outros documentos | Demais peças médicas | "Tipo – juntado às fls. …" (boletim de ocorrência, fisioterapia, prontuário, perícia do INSS, dossiê). |
| Documentos de SST (TRT) | Juntadas das reclamadas | PPP, PCMSO, PGR (PPRA só para períodos antes de 2022), AET, LTCAT: Id ou "não encontrado nos autos". |
| Quesitos | Petições de quesitos, despacho | Transcrição **literal**, por parte, na numeração original, com fls./Id no título ("QUESITOS MÉDICOS – DO RECLAMANTE (fls. 410)"). Sem quesitos do Juízo: "Não encontrado quesitos nos autos." Deixe "Resp.:" vazio abaixo de cada um. |

## 3. Regras

- Transcrição entre aspas é **literal**; resumo não leva aspas de citação, exceto nos blocos de alegação e contestação, que o modelo já usa entre aspas.
- Não deduza CID, data ou CRM que não estejam escritos.
- Registre divergências entre documentos (datas, mecanismo do acidente, lado do corpo) numa lista de pendências; não escolha uma versão.
- Dados pessoais (CPF, RG, endereço) vão para o .docx porque o modelo os exige; não os repita no chat.

## 4. Preencher o modelo

Use `fill_docx.py`:
- parágrafos de texto: `substituir`;
- tabela de documentos, histórico trabalhista e previdenciário: `linhas_tabela` (copia a formatação da última linha) e `remover_linhas` para linhas de exemplo vazias;
- células isoladas: `celulas`.

Entregue o .docx e, no chat: o que foi preenchido, as pendências (documentos ilegíveis, folhas não identificadas, divergências) e a lista de quesitos por parte, com o total.
