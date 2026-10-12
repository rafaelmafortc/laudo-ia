# Modo C: revisar um laudo antes de protocolar

Leia o laudo inteiro (extract_docx.py) e `dominio.md`. Liste os problemas do mais grave para o menos grave, cada um com o ¶ (ou Tn.linha), o trecho e a correção proposta. Não reescreva o laudo; ofereça aplicar as correções aprovadas com `fill_docx.py` (`trocar`, `substituir`).

## Checklist

**Bloqueiam o protocolo**
- Quesito sem resposta, "Resp.:" vazio, ou resposta que não responde ao perguntado (CPC, art. 473, IV).
- Conclusão que os achados registrados não sustentam (cadeia de `dominio.md` §2.2 ou §3.2).
- Contradição entre o texto-padrão do exame e o achado específico (força 5/5 com muletas; "sem sinais inflamatórios" com fístulas; "musculatura simétrica" com perimetria assimétrica).
- Caixas incoerentes com a conclusão (4.2 marcado e 8.1 marcado; "Permanente" sem consolidação).
- "Não há divergência" com o INSS quando a conclusão diverge da decisão administrativa.
- Dados de outro caso: outro número de processo, outro nome, CRM com UF errada.
- Texto meta de IA ("Segue a versão…"), comentários, marcações [PENDENTE]/[REVISAR] ou realces esquecidos.
- Seção de raciocínio vazia com conclusão pronta (no modelo B, 15.1 e 15.2 vazios).
- Respostas não conclusivas ("depende", "pode") ou contraditórias entre quesitos.
- Exame do segmento da queixa não registrado (ex.: região inguinal numa hérnia), ou sinais vitais do modelo não conferidos.

**Graves**
- Datas incoerentes: assinatura antes do exame; preâmbulo e encerramento com datas diferentes; DIB antes do acidente; consolidação antes do fim do tratamento.
- Termos do tipo errado (Reclamante/Reclamada contra o INSS; Autor/Réu no TRT é aceitável, mas padronize).
- Percentual sem método (baremo sem item; concausa sem critério; concausa não aplicada ao déficit).
- Classe de Weliton durante incapacidade temporária; dano estético com escalas misturadas.
- "Vide item X" para item que não trata do assunto; "Repetido"/"Prejudicado" sem dizer qual quesito ou por quê.
- Juízo jurídico ("faz jus", culpa, responsabilidade, licitude da dispensa).
- Normas revogadas (tabela de `dominio.md` §5).
- Diagnóstico a partir de uma única medida (ex.: hipertensão por uma aferição).

**Forma**
- Número de laudas no encerramento desatualizado.
- Erros de digitação nos títulos ("ILUSTRTIVAS", "QUANTUN", "Hpa"), UF incompleta ("Rio de Janeiro - J").
- Literatura colada sobre outra lesão, com primeira pessoa do autor original, ou de site leigo.
- Exame mínimo ausente para o segmento (`dominio.md` §7): aponte o que faltou medir; não invente o valor.

## Resposta

1. Veredito em uma linha: "Pronto para protocolo", "Pronto após correções de forma" ou "Não protocolar: N problemas que bloqueiam".
2. A lista, por gravidade.
3. Pergunta: aplicar as correções de forma no .docx?
