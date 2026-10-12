# Exemplo do modelo B: hérnia inguinal (TRT-2), antes e depois

Arquivos:
- `exemplo-modelo-B-hernia-1-inicial.docx`: o laudo como chega para preencher.
- `exemplo-modelo-B-hernia-2-finalizado.docx`: o mesmo laudo depois de preenchido pela perita.

Dados pessoais foram trocados ou omitidos. **É referência, não gabarito:** mostra onde as coisas entram e o tom do modelo B. A conclusão vale só para este caso, e o finalizado tem erros listados abaixo.

## O que muda do inicial para o finalizado

| Parte do laudo | No inicial | No finalizado | Quem preenche |
|---|---|---|---|
| Jornada (amarelo), dominância, peso, altura | Vazios | Preenchidos | Perita (dado da entrevista e do exame) |
| Caixas do perfil profissiográfico e do estado anterior | Desmarcadas | Marcadas, com complementos ("musculação, mas parou em 2023") | Perita |
| HISTÓRIA DA DOENÇA ALEGADA e tabelas de dependência | Vazias | Preenchidas (dependência com "x") | Perita |
| RESUMO DOS FATOS DA INICIAL | Vazio | Relato colhido na perícia (mecanismo do esforço, atendimento, situação atual) | Perita, ou a IA a partir das anotações dela |
| Sinais vitais | 130x80 mmHg (texto do modelo) | 140x100 mmHg (medido) | Perita |
| FUNDAMENTAÇÃO TEÓRICA e BIBLIOGRAFIA | Vazias | Texto sobre hérnia inguinal e 4 referências | IA pode redigir (texto técnico próprio) |
| 15.1 e 15.2 | Vazios | **Continuaram vazios** (erro) | IA deve redigir |
| 15.3 a 15.6 | Conclusões já escritas ("NÃO há nexo") | Mantidas | Conferir com os achados |
| Quesitos (24 + 12 + 22, das três partes) | "Resp.:" vazios | Respondidos | IA redige; perita revisa |
| Encerramento | "35 laudas" | "27 laudas" | Atualizar sempre |

## O que imitar

- Responder **todos** os quesitos de cada reclamada, na ordem e numeração originais, mesmo os repetidos.
- Usar o relato do ato pericial como fonte, dizendo que é relato ("segundo o Reclamante…").
- Basear a análise do mecanismo na carga efetivamente suportada (paciente transferido apoiado nos próprios pés).
- Respostas curtas e diretas quando a pergunta é simples ("Resp.: B31.").

## O que NÃO imitar

- **15.1 e 15.2 vazios** com a conclusão pronta em 15.6: o laudo não mostra como chegou à conclusão.
- **Nenhum exame da região inguinal** registrado (cicatriz, abaulamento, Valsalva), e ainda assim a resposta "totalmente restabelecido".
- **Respostas não conclusivas:** "depende de como são transportados", "pode", "todas", "quando se movimenta todo o corpo está envolvido".
- **Respostas que não respondem:** o quesito 8 pede elementos objetivos anteriores ao evento e a resposta é "a hérnia podia existir"; o quesito 14 pede datas e não há datas; o quesito 22 repete a alegação.
- **Contradição:** quesito 13 ("não" há compatibilidade com os afastamentos) × quesito 14 (houve incapacidade no pós-operatório).
- **Juízo e comentário pessoal:** "o benefício foi concedido de maneira correta"; "sendo o reclamante professor… ele mesmo sabe o limite".
- **Raciocínio técnico frágil:** explicar uma hérnia alegada como **direta** pelo não fechamento do conduto (mecanismo da **indireta**); dizer que hérnia não encarcerada "favorece a hipótese de que já estava lá".
- **"Vide item 5"**, item que não existe no laudo.
- **"Hipertensão detectada na perícia"** a partir de uma única aferição.
- **Fundamentação copiada de site leigo** ("Neste artigo vamos explicar…", "irritação e choro persistente nos bebês").
- Letra minúscula no início das respostas, erros de digitação ("poder, poderia", "pês").
- Caixa ambígua "Nega ser usuário de drogas ilícitas ☒ Sim": mantenha o que a perita marcou, mas não interprete sem confirmar.

## Como o Claude deve tratar um caso assim

1. Listar como pendência: o exame da região inguinal, a confirmação dos sinais vitais e o tipo da hérnia (direta ou indireta) no relatório cirúrgico.
2. Redigir 15.1 (síntese do caso) e 15.2 (doença, tipo, fatores individuais, exposição, LDRT K40, evento único segundo Simonin, cronologia) com as fontes.
3. Conferir se "NÃO há nexo" de 15.6 decorre dos achados. Se faltar dado decisivo, abrir CONFLITO DE CONCLUSÃO.
4. Responder os quesitos de forma conclusiva e coerente entre si, com datas quando pedidas: período de incapacidade documentado, da cirurgia ao ASO de retorno.
