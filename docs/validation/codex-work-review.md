# Auditoria de Pipeline: skill `site-seo-release` (trabalho do Codex)

**Data:** 2026-09-12
**Input avaliado:** skill em Markdown (`SKILL.md`, 8 referências, template `SEO-SPEC.md`), 4 scripts Python com testes, plano de construção (`docs/BUILD_PLAN.md`), snapshots do upstream (`vendor/claude-seo/`) e arquivos de descoberta dos hosts.
**Escopo:** integridade do fluxo construção, incremental e fechamento; exatidão técnica das referências contra fontes oficiais; código dos scripts; fidelidade e licença do upstream; alegações sobre Claude Code, Codex e Gemini CLI.
**Método:** auditoria de fluxo pelo revisor principal mais quatro revisores independentes somente leitura (código Python com reprodução empírica, fact-check de 20 páginas oficiais via HTTP, fidelidade ao upstream com hashes, verificação das docs dos três hosts).

---

## Resumo Executivo

A skill é uma adaptação real e superior ao upstream `claude-seo`: troca notas subjetivas por um contrato de evidências (`pass` exige evidência, `na` exige motivo, `blocked` exige impedimento), adiciona o modo construção com `SEO-SPEC.md`, cobre entrega real de formulário, LGPD, SPF/DKIM/DMARC e 404 real, e é portátil de fato (stdlib Python, sem MCP ou runtime). O fact-check não encontrou nenhuma afirmação técnica errada ou desatualizada nas referências; a licença MIT viaja com a skill instalada; os hashes do snapshot conferem; todas as alegações sobre descoberta de skills nos hosts estão corretas ou incompletas, nunca erradas.

Os problemas estão na engenharia de borda e em lacunas de tradução entre documentos: o instalador falha em checkout Windows padrão (`core.autocrlf=true`), o validador do relatório não aplica a única regra determinística que o contrato lhe delega (`production-verification` em produção), o catálogo de IDs vive duplicado sem teste de deriva, e itens prometidos no plano de construção (acessibilidade) ou no briefing (conversão) não têm ID próprio no fechamento. Nada é crítico: nenhum achado perde dado de forma irreversível nem produz READY sem que o agente tenha declarado algo falso; o backup do MD global é criado antes de qualquer escrita, com `os.replace` atômico.

Pelo critério aritmético do template, a nota fica em 43/100 (REPROVADO). A leitura correta dessa nota: 2 achados altos com correção de menos de uma hora cada, 9 médios que são dívida técnica acionável, e 14 baixos que são precisões de texto. O conteúdo de SEO está certo; o que falta é fechar as arestas.

### Contagem de Findings

| Severidade | Quantidade |
| --- | --- |
| Crítico | 0 |
| Alto | 2 |
| Médio | 9 |
| Baixo | 14 |
| **Total** | **25** |

---

## Parte 1: Findings

### Findings Críticos

Nenhum.

### Findings Altos

#### [FA-001] Instalador quebra após checkout Windows com `autocrlf`

- **Categoria:** Pontos Cegos de Erro (critério dinâmico: portabilidade Windows)
- **Localização:** `skills/site-seo-release/scripts/install_skill.py:155` e `:204`
- **Evidência:** comparação byte a byte do bloco gerenciado (`text[start:end] != expected_block`) e da árvore instalada (`source_manifest != _tree_manifest(destination)`). Com `core.autocrlf=true` (padrão do Git for Windows, ativo nesta máquina), LF vira CRLF e toda reexecução falha com "differs; refusing overwrite". Reproduzido pelo revisor: exit 2 tanto para `AGENTS.md` quanto para o `SKILL.md` instalado.
- **Impacto:** `install_skill.py --platform both` deixa de ser idempotente no fluxo Windows padrão; a segunda execução (ou qualquer atualização da skill) é recusada em todo projeto clonado.
- **Sugestão de correção:** normalizar `\r\n` para `\n` e remover BOM antes de comparar o bloco e os arquivos de texto do manifesto; distinguir na mensagem "difere só em fim de linha" de "conteúdo divergente". Adicionar teste que instala, converte a cópia para CRLF e reexecuta esperando `unchanged`.

#### [FA-002] Gate não aplica a regra de produção do contrato e aceita `production-verification` dispensado

- **Categoria:** Gaps de Tradução (contrato em Markdown para o script)
- **Localização:** `skills/site-seo-release/scripts/release_gate.py:165-177`; `references/report-contract.md:37`
- **Evidência:** o contrato diz "Em produção, `production-verification` não pode ser dispensado num lançamento público solicitado", mas `na` nunca conta como item aberto. Reproduzido: `environment: production` com `production-verification: na` retorna `READY` e exit 0. A variante inversa também passa: em `local` ou `preview`, o script aceita `pass` para uma verificação que só pode existir em produção, e o contrato não diz que nesses ambientes o status correto é `pending`, nunca `na`.
- **Impacto:** é a única regra determinística que o contrato delega ao script e ela não existe; um agente pode obter READY em produção sem smoke real, e o texto ambíguo permite `na` em pré-publicação.
- **Sugestão de correção:** em `validate_report`, levantar `SchemaError` quando `environment == "production"` e o check `production-verification` estiver `na`; levantar `SchemaError` quando `environment != "production"` e o mesmo check estiver `pass`. Em `report-contract.md:37`, acrescentar: "Em `local` e `preview`, `production-verification` fica `pending`, nunca `na` nem `pass`." Cobrir com dois testes.

### Findings Médios

#### [FM-001] `register_global.py` não valida a codificação do MD global

- **Categoria:** Pontos Cegos de Erro
- **Localização:** `scripts/register_global.py:184`, `:191-194`
- **Evidência:** alvo em UTF-16 é aceito e recebe bloco UTF-8. Reproduzido: `STATUS: insert`, exit 0, e o arquivo deixa de decodificar como um todo. `install_skill.py:139` já exige UTF-8; o script de maior raio de impacto não.
- **Impacto:** o MD global inteiro fica ilegível para o host. Há backup, mas o usuário não é avisado onde ele está (ver FB-014).
- **Sugestão de correção:** `original.decode("utf-8")` em `plan_registration` com `RegistrationError` em falha; rejeitar bytes NUL. Teste com alvo UTF-16 esperando exit diferente de 0 e arquivo intacto.

#### [FM-002] Crash de codificação em stdout reutiliza o exit 1 de NOT_READY

- **Categoria:** Pontos Cegos de Erro
- **Localização:** `scripts/release_gate.py:298-300`
- **Evidência:** `ensure_ascii=False` e o Markdown vão para um stdout cp1252 (pipe no Windows sem `PYTHONUTF8`); qualquer `action` ou `project` com caractere fora do cp1252 lança `UnicodeEncodeError` com traceback e exit 1. Reproduzido com U+2192 nos dois modos.
- **Impacto:** exit 1 é o sinal contratual de NOT_READY; uma falha de infraestrutura passa a parecer decisão de gate.
- **Sugestão de correção:** `sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")` no início de `main`, ou capturar a exceção e retornar 2 com mensagem de erro.

#### [FM-003] Catálogo de IDs duplicado sem teste de deriva

- **Categoria:** Critério Dinâmico: determinismo entre documento e script
- **Localização:** `scripts/release_gate.py:27-54`; `tests/test_release_gate.py:35`; `references/release-checklist.md:5-32`
- **Evidência:** `REQUIRED_CHECK_IDS` replica os 26 IDs da tabela (hoje iguais, mesma ordem). `valid_report()` gera fixtures a partir da própria constante e `validate_skill.py` não confere a tabela; uma edição só no Markdown passa em silêncio.
- **Impacto:** o script aprova relatórios incompletos ou exige IDs que o catálogo já não descreve.
- **Sugestão de correção:** teste que parseia a coluna ID da tabela de `release-checklist.md` e assere igualdade ordenada com `REQUIRED_CHECK_IDS`; opcionalmente a mesma checagem em `validate_skill.py`.

#### [FM-004] Helpers duplicados com garantias divergentes; escrita não atômica em projetos

- **Categoria:** Pontos Cegos de Erro
- **Localização:** `scripts/install_skill.py:68-91`, `:160-164` versus `scripts/register_global.py:47-73`, `:142-152`, `:212-226`
- **Evidência:** `_is_link` e `_reject_*chain` copiados nos dois scripts; `_append_managed_block` faz `write_bytes` direto (trunca e escreve, sem temporário, `os.replace` ou backup) e cola bloco LF em arquivo CRLF, enquanto `register_global` preserva fim de linha e escreve de forma atômica.
- **Impacto:** o mesmo conceito (bloco gerenciado) tem dois comportamentos, e o mais fraco é o que escreve em `AGENTS.md`/`CLAUDE.md` de projetos do usuário.
- **Sugestão de correção:** extrair `_is_link`, `_newline_for` e `_write_atomic` para `scripts/_fsutil.py` e usar nos dois; ao menos replicar temporário mais `os.replace` e preservação de EOL no instalador.

#### [FM-005] Markdown do gate não cobre o contrato do relatório

- **Categoria:** Gaps de Tradução
- **Localização:** `scripts/release_gate.py:215-251`; `references/report-contract.md:50-54`
- **Evidência:** `render_markdown` imprime só decisão, contagens e a tabela de checks abertos (id, status, severidade, required, ação). O contrato exige tabela completa, resumo das evidências, responsável sugerido, dependência, bloqueio, como retestar, ações externas destacadas e limitações. O contrato chama a saída de "base", mas não diz o que o agente precisa completar.
- **Impacto:** um agente salva a base como `tasks/site-release.md` final e o documento não satisfaz o próprio contrato; o usuário recebe uma lista de pendências sem responsável nem reteste.
- **Sugestão de correção:** renderizar também a tabela completa e as colunas recomendadas quando presentes (`owner`, `dependencies`, `limitations`, `verified_at`), ou listar em `report-contract.md` as seções que o agente deve acrescentar à base antes de salvar.

#### [FM-006] Sem `verified_at` obrigatório, o modo incremental não distingue evidência antiga

- **Categoria:** Gaps de Tradução
- **Localização:** `references/report-contract.md:25`, `:29`; `references/build-guidelines.md:37`; `SKILL.md:19`
- **Evidência:** o modo incremental manda "sinalizar evidências antigas" e "manter a data de cada evidência", mas `verified_at` é apenas recomendado e o script não o valida. Sem data por check, não há como saber qual evidência a mudança invalidou.
- **Impacto:** um `pass` de semanas atrás sobrevive a uma alteração que o invalidou, sem sinal mecânico.
- **Sugestão de correção:** tornar `verified_at` obrigatório (ISO 8601 com timezone) quando `status == "pass"`, validar no script e citar no contrato; no modo incremental, o agente compara `verified_at` com a data da mudança.

#### [FM-007] Acessibilidade prometida no plano sem ID próprio no catálogo

- **Categoria:** Gaps de Tradução (plano para catálogo)
- **Localização:** `docs/BUILD_PLAN.md` seções 5.3 e 5.4 e `tasks/todo.md` item 5 ("acessibilidade"); `references/release-checklist.md:20-21`
- **Evidência:** o plano lista labels, foco, teclado e contraste; no catálogo isso aparece diluído em `navigation-mobile` (teclado) e `forms-ui` (labels, erros). Não há critério para contraste AA, alt de imagens fora do contexto de SEO, nomes acessíveis, hierarquia de headings ou zoom a 200%.
- **Impacto:** uma landing page pode fechar READY com contraste ilegível ou botões sem nome acessível, sem nenhuma linha do relatório apontar isso.
- **Sugestão de correção:** adicionar o ID `accessibility` (contraste AA em texto e CTA, foco visível, nomes acessíveis, headings, zoom 200%, alt) na tabela, em `REQUIRED_CHECK_IDS` e nos testes (o catálogo é hardcoded, ver FM-003).

#### [FM-008] Evento de conversão inventariado mas nunca verificado

- **Categoria:** Gaps de Tradução (briefing para catálogo)
- **Localização:** `references/forms-privacy-email.md:5` ("inventarie ... evento de conversão"); `references/build-guidelines.md:12` ("analytics, pixels e cookies"); `references/release-checklist.md` sem ID correspondente
- **Evidência:** o briefing do usuário centra a skill em conversão; o inventário pede o evento, mas nenhum check confirma que o evento de lead dispara no sucesso do formulário, só após consentimento, sem PII nos parâmetros.
- **Impacto:** o site converte e ninguém mede, ou mede antes do consentimento; a skill declara READY.
- **Sugestão de correção:** adicionar o ID `conversion-tracking` (evento disparado no sucesso real, gate de consentimento, sem PII, destino do dado) ou ampliar `forms-delivery` com esse critério explícito.

#### [FM-009] Checks técnicos do upstream dispensados sem substituto

- **Categoria:** Critério Dinâmico: fidelidade ao upstream
- **Localização:** `vendor/claude-seo/seo-technical.original.txt:152-159`, `:114-122`, `:98-106`, `:39-66`; `references/technical-files.md:18`, `:67`; `references/release-checklist.md:20`, `:29`
- **Evidência:** quatro blocos concretos do upstream não têm equivalente: paridade entre HTML bruto e renderizado (canonical divergente, `noindex` removido por JS ainda honrado, sem render em não-200); critérios de mobile (alvos de toque 48 px, fonte base 16 px, sem scroll horizontal, interstitials intrusivos, paridade mobile/desktop); security headers (CSP, HSTS, X-Content-Type-Options, mixed content), que o próprio `BUILD_PLAN.md` 5.4 prometia; e a distinção entre crawlers de treino e de citação (GPTBot versus OAI-SearchBot, ClaudeBot versus Claude-SearchBot, Google-Extended) para a decisão do dono sobre `robots.txt`.
- **Impacto:** perda de capacidade real em Next/SPA (canonical injetado por JS), em landing pages com popup, e na decisão informada sobre bots de IA que a skill pede ao proprietário.
- **Sugestão de correção:** reincorporar em poucas linhas, sem copiar afirmações datadas do upstream sem fonte: um parágrafo de paridade em `technical-files.md:67`; critérios mobile em `navigation-mobile`; headers e mixed content no ID `security`; tabela curta de crawlers com finalidade em `technical-files.md:18`, citando as páginas de suporte de cada fornecedor em `sources.md`.

### Findings Baixos

#### [FB-001] Favicon: SVG não é formato aceito pelo Google Search
- **Categoria:** Alucinações Arquiteturais (imprecisão)
- **Localização:** `references/content-media.md:25`
- **Evidência:** "Forneça PNG ou ICO compatível além de SVG quando necessário". A página oficial lista BMP, GIF, ICO, PNG, JPEG, PPM e TIFF; mínimo 8x8 px, recomendado acima de 48x48 px.
- **Sugestão de correção:** "O Google Search aceita apenas BMP, GIF, ICO, PNG, JPEG, PPM e TIFF: forneça ICO ou PNG quadrado, de preferência acima de 48x48 px, em URL estável referenciada no head da home; SVG fica como complemento para navegadores."

#### [FB-002] 404: faltam as alternativas oficiais quando a hospedagem não devolve 404 real
- **Localização:** `references/technical-files.md:65`
- **Sugestão de correção:** acrescentar: "Quando a hospedagem não permitir status 404 real, aceite as alternativas documentadas pelo Google: redirecionar via JavaScript para uma URL que responda 404 no servidor, ou injetar meta robots noindex na página de erro, registrando a limitação."

#### [FB-003] DKIM: nuance de CNAME
- **Localização:** `references/forms-privacy-email.md:25`
- **Sugestão de correção:** "A RFC 6376 define a chave em registro TXT; quando o provedor pede CNAME, o nome delega para o TXT dele e a resolução precisa chegar a um TXT válido."

#### [FB-004] Fonte da ANPD aponta para a notícia, não para o guia
- **Localização:** `references/sources.md:31`
- **Sugestão de correção:** adicionar o PDF do Guia Orientativo Cookies e Proteção de Dados Pessoais (out. 2022) como fonte primária.

#### [FB-005] Gemini CLI já descobre `.agents/skills/` nativamente
- **Categoria:** Alucinações Arquiteturais (informação incompleta)
- **Localização:** `references/portability.md:8`, `:28`; `README.md:28`
- **Evidência:** a doc do Gemini CLI lista skills de workspace em `.gemini/skills/` ou no alias `.agents/skills/`, ativadas pela tool `activate_skill`. A skill trata Gemini só via índice em `GEMINI.md`.
- **Sugestão de correção:** documentar que a cópia do Codex em `.agents/skills/` é descoberta pelo Gemini sem cópia extra; manter `GEMINI.md` como índice complementar.

#### [FB-006] Limites do padrão Agent Skills não citados
- **Localização:** `references/portability.md:3`
- **Sugestão de correção:** registrar que `name` tem até 64 caracteres, minúsculo com hífens, igual ao diretório, e `description` até 1.024 caracteres (Claude Code trunca em 1.536). Hoje a skill está dentro dos limites.

#### [FB-007] Atribuição: sem ponteiro para o texto de permissão e sem `license` no frontmatter
- **Localização:** `THIRD_PARTY_NOTICES.md:3`; `SKILL.md:1-4`; `vendor/claude-seo/seo.original.txt:6`
- **Evidência:** o aviso reproduz o copyright, mas não aponta onde está o texto MIT (está em `skills/site-seo-release/LICENSE:6-22`, correto). O upstream declarava `license: MIT` no frontmatter; a nova skill não, e `validate_skill.py:29-30` só aceita `name` e `description`.
- **Sugestão de correção:** ponteiro em `THIRD_PARTY_NOTICES.md` para `vendor/claude-seo/LICENSE.original.txt` e para o `LICENSE` da skill; avaliar permitir `license: MIT` no frontmatter (o padrão Agent Skills prevê o campo) e ajustar o validador.

#### [FB-008] Hashes provam consistência local, não equivalência com o upstream
- **Localização:** `vendor/claude-seo/sources.json:8`; `THIRD_PARTY_NOTICES.md:7`
- **Evidência:** os arquivos foram reconstruídos da saída renderizada; `LICENSE.original.txt` tem 19 linhas contra 21 do template MIT (texto igual, sem duas linhas em branco).
- **Sugestão de correção:** frase explícita em `THIRD_PARTY_NOTICES.md`: "os hashes garantem a integridade da cópia local, não a igualdade byte a byte com o repositório de origem".

#### [FB-009] Reparse points comuns são recusados como symlink
- **Localização:** `scripts/register_global.py:58-61`; `scripts/install_skill.py:75-78`
- **Evidência:** qualquer `FILE_ATTRIBUTE_REPARSE_POINT` (placeholder do OneDrive, Dev Drive) vira "symlink or junction".
- **Sugestão de correção:** filtrar por `st_reparse_tag` ou ajustar a mensagem para orientar o usuário.

#### [FB-010] Cobertura do validador estático
- **Localização:** `scripts/validate_skill.py:75`, `:99`
- **Evidência:** cobre frontmatter, `openai.yaml`, links locais, UTF-8 e U+2013/U+2014 em `.md`, `.yaml` e `.py`. Não cobre placeholders (`[...]`, TODO), arquivos `.json` (`tests/behavior-cases.json` escapa), referências não linkadas, e `main()` sem `argv` impede testar a CLI.

#### [FB-011] Lacunas de teste
- **Localização:** `tests/test_install_skill.py:29`; `tests/test_register_global.py:14`
- **Evidência:** sem teste para falha em `os.replace` (alvo intacto e backup presente), guarda "Target changed after planning", alvo não UTF-8, reexecução após CRLF, exit 0 via CLI para READY_WITH_RESERVATIONS, `audited_at` sem timezone, arquivo inexistente com exit 2, casos negativos do validador. Testes patcham `tempfile._os.mkdir` (API privada) e fixam o layout do repositório via `parents[3]`, então a cópia instalada dos testes não roda.

#### [FB-012] Matriz de páginas do `SEO-SPEC.md` sem campos para pergunta principal, imagem social e idioma
- **Localização:** `assets/seo-spec.md:17`
- **Evidência:** `content-media.md` pede blocos de pergunta e resposta e preview social por página; `technical-files.md:37` fala em hreflang; a matriz não tem coluna para nenhum dos três.
- **Sugestão de correção:** colunas opcionais "Pergunta principal", "Imagem social" e "Idioma/hreflang".

#### [FB-013] Ferramentas de DNS, HTTP e imagem sem exemplo
- **Categoria:** Dependências Fantasma (leve)
- **Localização:** `references/forms-privacy-email.md:31`; `references/content-media.md:27`; `SKILL.md:55`
- **Evidência:** "consulta DNS somente leitura", "comprima" e "teste HTTP" sem nenhum comando de referência por sistema operacional.
- **Sugestão de correção:** uma linha por área com opções portáteis (`nslookup -type=txt` / `dig txt`, `curl -sI`, `cwebp` / `sharp` / Pillow), sem torná-las obrigatórias.

#### [FB-014] Backup do MD global invisível e acumulativo
- **Localização:** `scripts/register_global.py:246`, `:296-297`
- **Evidência:** `.site-seo-release.<uuid>.bak` nunca é impresso; cada update deixa uma cópia integral do MD privado; em `create` grava backup vazio (consagrado pelo teste da linha 89).
- **Sugestão de correção:** imprimir `BACKUP: <caminho>` no apply; pular backup quando `status == "create"`; documentar limpeza em `global-registration.md`.

---

## Parte 2: Interrogatório Estratégico

Estas perguntas cobrem zonas que a análise do material não resolve sozinha. As respostas mudam a prioridade de alguns findings.

### Área: catálogo de fechamento

**P1:** Acessibilidade deve ser um ID obrigatório do fechamento (contraste AA, foco, nomes acessíveis, zoom 200%) ou continua diluída em formulários e navegação?
- **Contexto:** o plano de construção prometia acessibilidade; entregas comerciais da Growth Hub costumam ter CTA sobre imagem e texto secundário claro, onde contraste falha com frequência.
- **Findings relacionados:** FM-007, FM-003

**P2:** Os projetos usam evento de conversão (GA4, Meta Pixel, tag no CRM) no sucesso do formulário? Ele deve ser verificado no fechamento e ficar condicionado ao consentimento?
- **Contexto:** o briefing centra a skill em conversão, mas nada mede a conversão hoje.
- **Findings relacionados:** FM-008

### Área: portabilidade e instalação

**P3:** A instalação em outros projetos vai acontecer por `git clone` em Windows (autocrlf ligado) ou sempre pelo `install_skill.py` a partir deste repositório?
- **Contexto:** define se FA-001 é bloqueante no seu fluxo real ou só em máquinas de terceiros.
- **Findings relacionados:** FA-001, FM-004

**P4:** Gemini CLI entra no escopo de uso real? Se sim, prefere confiar na descoberta nativa em `.agents/skills/` ou manter o índice em `GEMINI.md`?
- **Contexto:** hoje a skill documenta só o índice; a doc oficial já descobre a pasta do Codex.
- **Findings relacionados:** FB-005

### Área: contrato do relatório

**P5:** O relatório deve exigir data por evidência (`verified_at` obrigatório em `pass`)? Isso aumenta o custo de preencher, mas é o que faz o modo incremental funcionar.
- **Findings relacionados:** FM-006

**P6:** O `tasks/site-release.md` deve sair pronto do script (tabela completa, responsável, reteste) ou o agente completa a base? Hoje o contrato pede o completo e o script entrega a base.
- **Findings relacionados:** FM-005

---

## Parte 3: Scorecard

### Nota Geral de Integridade

**43/100** pelo critério aritmético do template (2 altos a 8 pontos, 9 médios a 3, 14 baixos a 1). Classificação mecânica: REPROVADO. Leitura qualitativa: zero críticos, conteúdo técnico 100% verificado, melhoria real sobre o upstream; os dois altos e os médios de código cabem em uma sessão de correção. Recomendação prática: **APROVADO COM RESSALVAS após FA-001, FA-002, FM-001, FM-002 e FM-003**.

### Score por Categoria

| Categoria | Score | Observação |
| --- | --- | --- |
| Gaps de Tradução | 55/100 | Contrato para script (FA-002, FM-005, FM-006) e plano/briefing para catálogo (FM-007, FM-008) |
| Saltos Lógicos | 90/100 | Só ferramentas não exemplificadas (FB-013); o fluxo tem pré-requisitos claros |
| Alucinações Arquiteturais | 95/100 | 20 fontes verificadas, nenhuma afirmação errada; duas imprecisões (FB-001, FB-005) |
| Dependências Fantasma | 90/100 | Python opcional documentado; DNS e imagem sem ferramenta sugerida |
| Loops sem Saída | 100/100 | Corrigir e retestar é limitado pelo humano; sem retry automático |
| Pontos Cegos de Erro | 60/100 | autocrlf (FA-001), codificação (FM-001, FM-002), escrita não atômica no instalador (FM-004) |
| Critérios Dinâmicos | 75/100 | Deriva do catálogo (FM-003), upstream (FM-009); privacidade de evidência, autorização e copy corretos |

### Áreas Não Avaliadas

- Execução ponta a ponta em um projeto real (construção com `SEO-SPEC.md` até `tasks/site-release.json` e gate). Os smokes provaram ativação, não execução.
- `install_skill.py` em um projeto real; só testes de arquivo.
- Ativação no Gemini CLI; smoke negativo no Codex.
- Comportamento com sites multilíngues e com múltiplos domínios, descritos superficialmente nas referências.

### Critérios Dinâmicos Aplicados

- Determinismo entre documento e script: catálogo de IDs e decisão devem ser os mesmos em qualquer host. Justificativa: a skill promete decisão determinística.
- Privacidade das evidências: nenhum token, lead ou conteúdo global no relatório. Resultado: coberto (`report-contract.md:29`, `forms-privacy-email.md:7`).
- Limites de autorização: nenhum deploy, DNS ou envio sem autorização. Resultado: coberto (`SKILL.md:57`).
- Regras de copy do projeto: sem U+2013/U+2014, crédito Method Growth Hub. Resultado: coberto e validado.
- Portabilidade Windows: autocrlf, cp1252, reparse points. Resultado: FA-001, FM-002, FB-009.
- Fidelidade ao upstream e licença MIT: hashes, permissão, perdas. Resultado: licença correta, FM-009 e FB-007/FB-008.
- Exatidão das alegações sobre hosts: docs oficiais dos três. Resultado: correto, FB-005 e FB-006 como complementos.
- Exatidão jurídica LGPD/ANPD: guia oficial lido. Resultado: correto, FB-004.
- Economia de contexto: núcleo curto, referências sob demanda. Resultado: adequado (5 KB, 600 caracteres de descrição).

---

## Aplicação das correções (2026-09-12)

Escopo aprovado pelo usuário: altos, médios de código, `verified_at` obrigatório, IDs `accessibility` e `conversion-tracking`, baixos.

Aplicado:

- FA-001: `install_skill.py` normaliza CRLF e BOM na comparação de bloco e de árvore; teste de reinstalação após conversão para CRLF.
- FA-002: `release_gate.py` rejeita `production-verification` `na` em produção e `pass` ou `na` fora de produção; contrato atualizado; testes para os três casos e para `pending` em `local`.
- FM-001: `register_global.py` exige alvo UTF-8 sem bytes NUL; teste com alvo UTF-16 e arquivo intacto.
- FM-002: stdout e stderr reconfigurados para UTF-8 no gate; teste com U+2192 em stdout cp1252 nos dois modos.
- FM-003: teste que parseia a coluna ID da tabela de `release-checklist.md` e compara, em ordem, com `REQUIRED_CHECK_IDS`.
- FM-004 (parcial): bloco gerenciado do instalador escrito com temporário exclusivo, `os.replace`, modo preservado e fim de linha do arquivo existente; os helpers não foram extraídos para módulo comum, para manter cada script autossuficiente na cópia instalada.
- FM-006: `verified_at` obrigatório em `pass` (script, contrato, guia incremental, testes).
- FM-007 e FM-008: IDs `accessibility` e `conversion-tracking` na tabela, no script, no template `SEO-SPEC.md` e nos testes; o catálogo passa a 28 IDs.
- FB-001 a FB-006, FB-008, FB-012, FB-013: textos corrigidos nas referências, fontes, template, portabilidade, README e avisos de terceiros.
- FB-009: mensagens de symlink citam junction e reparse point. FB-010: `.json` incluído no scan de travessão e `main(argv)` testável. FB-011 (parcial): nove testes novos, 52 no total. FB-014: `BACKUP:` impresso no apply e sem backup vazio em `create`.

Backlog:

- FM-005: Markdown completo do gate (tabela integral, responsável, reteste, limitações).
- FM-009: reincorporar paridade HTML bruto e JS, critérios mobile, security headers e taxonomia de crawlers de IA.
- FB-007 (parcial): ponteiros de licença adicionados; `license: MIT` no frontmatter não aplicado, porque o validador e os hosts só garantem `name` e `description`.
- FB-011 (parcial): faltam testes para falha em `os.replace` e para a guarda "Target changed after planning".

Estado após as correções: 0 críticos, 0 altos, 2 médios abertos (FM-005, FM-009) e 2 parciais. Pela aritmética do template, 100 menos 6 menos 2 resulta em 92, APROVADO. Verificação: validador `valid: true`, 52 testes OK, zero travessão fora de `vendor/`, registro global inalterado (`STATUS: unchanged` nos dois hosts).

---

## Apêndice: Grafo do Pipeline

```mermaid
flowchart TD
  A[Ativação: bloco global ou MD local] --> B[Lê SKILL.md]
  B --> R[Registro global na 1a leitura<br/>register_global.py]
  B --> M{Modo}
  M -->|construção| C1[build-guidelines + template]
  C1 --> C2[SEO-SPEC.md: contexto, matriz, plano de aceite]
  C2 --> C3[Implementa: robots, sitemap, llms, páginas, forms, privacidade, e-mail]
  M -->|incremental| I1[Lê SEO-SPEC + referência da área]
  I1 --> I2[Revalida mudança e dependências<br/>FM-006: sem verified_at]
  M -->|revisão final| F1[release-checklist + report-contract]
  F1 --> F2[Executa checks: código, build, HTTP, navegador, DNS, entrega]
  F2 --> F3[tasks/site-release.json 26 IDs<br/>FM-007 FM-008: sem accessibility e conversion]
  F3 --> F4[release_gate.py<br/>FA-002: production-verification na/pass<br/>FM-003: catálogo duplicado]
  F4 --> F5[tasks/site-release.md<br/>FM-005: base incompleta]
  F5 --> D[Entrega: SEO-SPEC, artefatos, relatório, pendências]
  M -->|instalação| N1[install_skill.py<br/>FA-001: autocrlf<br/>FM-004: escrita não atômica]
  R -.-> G[(MD global do host)<br/>FM-001: codificação<br/>FB-014: backup invisível]
```
