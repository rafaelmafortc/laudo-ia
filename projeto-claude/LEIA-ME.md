# Projeto "Laudos periciais" no Claude

Guia para montar, no claude.ai, um Projeto que prepara, conclui, revisa e esclarece laudos periciais médicos sobre o .docx de cada perito.

Conferido na Central de Ajuda da Anthropic em 11/10/2026. Os nomes dos menus mudam com frequência; se algum não bater, procure pelo nome do recurso.

## O que vai em cada lugar

| Peça | Arquivo | Onde entra | Para quê |
|---|---|---|---|
| Skill | `laudo-pericial.zip` (pasta `laudo-pericial/`) | Personalizar > Skills | Procedimento, regras de domínio, estilo dos peritos e os scripts que leem e preenchem o .docx. É carregada quando o pedido é sobre laudo. |
| Instruções do projeto | `instrucoes-do-projeto.md` | Projeto > Instruções | Papel, peritos atendidos e regras que valem em toda conversa do projeto. Mandam usar a skill. |
| Conhecimento do projeto | `docs/pesquisa-pericia-medica-judicial.md`, pares de exemplo (`exemplos/`) e modelos em branco | Projeto > Arquivos | Referência de normas e literatura, do que se preenche em cada modelo e da estrutura de cada perito. |

Por que essa divisão: as instruções ficam sempre no contexto, então são curtas e trazem o que não pode ser esquecido; a skill traz o procedimento longo e só entra quando é usada; o conhecimento é consulta.

## Passo a passo

### 1. Plano e privacidade (antes de enviar qualquer laudo)

Laudos têm dado de saúde, que é dado sensível pela LGPD (art. 11).

- **Melhor opção: plano Team ou Enterprise.** Os termos comerciais não usam as conversas para treinar modelos, e a retenção padrão é de 30 dias.
- **Plano Pro ou Max:** em Configurações > Privacidade, desligue a opção de ajudar a melhorar o Claude (uso para treino). Desligada, a retenção é de 30 dias; ligada, até 5 anos.
- **Memória:** temas de saúde não entram na memória por padrão. Deixe desligada a opção "Include sensitive topics in memory".
- **Arquivos do projeto:** não suba laudos com dados de periciandos como conhecimento do projeto, porque eles ficam disponíveis em todas as conversas. Envie cada laudo só na conversa do caso.
- **Declaração de uso de IA:** a Res. CFM 2.454/2026 exige que o médico permaneça responsável e, na assistência, que informe o paciente quando a IA for apoio relevante. A Política de Uso da Anthropic trata usos médicos e jurídicos como de alto risco e, nesses casos, exige revisão por profissional qualificado e aviso a quem é afetado de que houve uso de IA (que o laudo pericial se enquadre aí é leitura nossa, não da Anthropic). Se o laudo vai declarar o uso de IA é decisão do perito; a skill não acrescenta essa declaração por conta própria.

### 2. Ligar a execução de código

A skill e o preenchimento do .docx precisam dela.

- **Free, Pro e Max:** Configurações > Capacidades (Settings > Capabilities) > ligar **"Execução de código e criação de arquivos"** (Code execution and file creation).
- **Team e Enterprise:** o administrador liga em Configurações da organização > Plugins e skills > Política: "Code execution" e "Skills".

### 3. Enviar a skill

1. Abra **Personalizar > Skills** (claude.ai/customize/skills).
2. Clique em **"+"** > **Criar skill** > **Enviar uma skill** (Upload a skill) e escolha `laudo-pericial.zip`.
3. Ligue a skill no botão ao lado do nome.

O ZIP já está no formato exigido: a pasta `laudo-pericial/` na raiz, com `SKILL.md` dentro, e o nome da pasta igual ao nome da skill. A descrição tem 193 caracteres; a Central de Ajuda fala em limite de 200.

No Team e no Enterprise, a skill pode ser compartilhada com outras pessoas da organização (fica só leitura para elas e atualiza sozinha).

### 4. Criar o projeto

1. Em **claude.ai/projects**, clique em **"+ Novo projeto"**. Nome sugerido: "Laudos periciais".
2. Em **Instruções do projeto** (Set project instructions), cole **todo** o conteúdo de `instrucoes-do-projeto.md` e salve.
3. Revise o bloco `<peritos>`: apague quem você não atende e acrescente outros peritos no mesmo formato.

### 5. Conhecimento do projeto

Suba em **Arquivos** do projeto:
- `docs/pesquisa-pericia-medica-judicial.md`: normas, jurisprudência, critérios de nexo e valoração, com fontes. Não tem nome de periciando.
- **Pares de exemplo** (o mesmo laudo antes e depois de preenchido), **anonimizados**. Já há um do modelo B em `projeto-claude/exemplos/`: os dois .docx e a nota `exemplo-modelo-B-hernia-LEIA.md`, que diz o que imitar e o que não imitar. Suba os três juntos. Para novos pares, troque nome, CPF, RG, CNH, endereço, número do processo e empresas, e tire as imagens de documentos.
- **Opcional:** o modelo em branco de cada perito, sem dados de nenhum caso, com nome descritivo (ex.: `modelo-A-TJRJ.docx`).

Cuidados:
- O conhecimento do projeto lê só o texto: imagens dentro de .docx são ignoradas.
- .doc não é aceito; salve como .docx.
- Quando o volume de arquivos cresce, o projeto passa a buscar trechos (modo RAG) em vez de ler tudo. Nomes de arquivo descritivos ajudam.

### 6. Modelo e esforço

- Escolha o modelo mais capaz disponível (hoje, Opus 5.5) no seletor ao lado do botão de enviar.
- Para concluir e revisar laudos, use esforço **Alto** ou **Extra alto**: a Anthropic recomenda esforço maior para análise detalhada de documentos.

## Como usar

Abra **uma conversa por processo** dentro do projeto e anexe os arquivos.

| Quero… | Anexe | Peça, por exemplo |
|---|---|---|
| Concluir o laudo | O rascunho .docx | "Conclua este laudo: responda os quesitos e redija a discussão e a conclusão." |
| Concluir com a conclusão já decidida | O rascunho .docx | "Conclua. A conclusão é redução da capacidade com maior esforço." |
| Preparar o laudo pelos autos | O PDF dos autos e o modelo do perito | "Prepare o laudo a partir dos autos: alegação, contestação, tabela de documentos e quesitos." |
| Revisar antes de protocolar | O laudo pronto | "Revise este laudo antes do protocolo." |
| Esclarecimentos | O laudo protocolado e a impugnação | "Prepare os esclarecimentos à impugnação da reclamada." |
| Preencher o exame com minhas anotações | O rascunho e as anotações (texto ou foto) | "Preencha o exame físico com estas anotações." |

**Ciclo de revisão:**
1. O Claude devolve `<nome> - minuta.docx`: texto novo em **turquesa**, pendências em **amarelo**. No chat vêm as pendências, a conclusão adotada e a discussão.
2. O perito revisa no Word e pede ajustes no chat ("no quesito 14, acrescente…"), ou envia as medidas que faltavam.
3. Quando estiver tudo certo: **"pode finalizar"**. O Claude gera `<nome> - final.docx`, sem o turquesa e sem o vermelho. Se ainda houver pendência, o Claude avisa e não finaliza.

**Teste recomendado:** comece pelo rascunho do vigilante (`docs/laudos/LAUDO MÉDICO TJRJ ROSBERG.docx`). O esperado é o Claude apontar, entre outras coisas:
- **conflito de conclusão**: a flexão do cotovelo não foi medida, e é ela que define o enquadramento no Anexo III;
- três versões do mecanismo do acidente;
- datas diferentes no preâmbulo e no encerramento;
- "Reclamante" num processo contra o INSS;
- "Não há divergência" com o INSS pré-preenchido.

## Limites

- **A minuta não substitui a revisão.** Leia todo o texto em turquesa antes de finalizar.
- **Documentos só em imagem** (manuscritos, digitalizados): o Claude tenta ler. Se não conseguir, lista como pendência e pede a imagem no chat.
- **Autos grandes:** PDFs de até 100 páginas são lidos com imagens. Acima disso, só o texto; páginas digitalizadas passam pela extração da skill.
- **Sem execução de código** (ou com o recurso desligado pela organização), a skill entrega o texto para colar, sem o .docx.

## Atualizar a skill

1. Edite os arquivos em `projeto-claude/laudo-pericial/`.
2. Gere o ZIP de novo:
   ```bash
   cd projeto-claude && rm -f laudo-pericial.zip && zip -r laudo-pericial.zip laudo-pericial -x "*/__pycache__/*"
   ```
3. Em Personalizar > Skills, substitua a skill pelo novo ZIP.

Outra opção é editar no próprio chat, com "Editar com o Claude" na página da skill.

A pasta `.claude/skills/complete-laudo/` é a versão para o Claude Code (terminal) e continua valendo lá. Para o claude.ai, use esta.

## Arquivos

```
projeto-claude/
├── LEIA-ME.md                  este guia
├── instrucoes-do-projeto.md    texto para colar nas instruções do projeto
├── laudo-pericial.zip          skill pronta para enviar
├── exemplos/                   par antes/depois anonimizado (modelo B, hérnia) e nota de uso
└── laudo-pericial/             fonte da skill
    ├── SKILL.md                procedimento e regras
    ├── references/
    │   ├── dominio.md          acidentária, trabalhista, psiquiatria, normas, exame mínimo
    │   ├── modelos-e-estilo.md modelos dos peritos A, B e C, estilo e exemplos corrigidos
    │   ├── preparar-autos.md   modo A: preparar pelos autos
    │   ├── revisao.md          modo C: checklist antes do protocolo
    │   └── esclarecimentos.md  modo D: esclarecimentos e quesitos complementares
    └── scripts/
        ├── extract_docx.py     lê o .docx com ¶, caixas, tabelas, cores e imagens
        ├── fill_docx.py        preenche o .docx (minuta e versão final)
        └── laudo_docx.py       funções comuns
```
