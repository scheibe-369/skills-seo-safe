# Handoff mútuo Claude ⇄ Codex: skill-seo

Canal de retomada entre Claude Code e OpenAI Codex CLI para este projeto. Ver a seção
"Orquestração Multi-IA" nos MDs globais (`~/.claude/CLAUDE.md` e `~/.codex/AGENTS.md`) para o
protocolo completo. Resumo: para retomar, precisa só do nome do projeto (`skill-seo`) e da tag
entre aspas da entrada desejada, ou usar o bloco `Estado atual` abaixo se não vier tag.

## Estado atual

- Tag: "HANDOFF-skill-seo-20260912-030650-claude"
- Status: concluído
- Resumo: revisão completa do trabalho do Codex na skill (`docs/validation/codex-work-review.md`)
  e correções aprovadas aplicadas: gate aplica a regra de produção, `verified_at` obrigatório,
  catálogo com 28 IDs (`accessibility`, `conversion-tracking`), instalador tolerante a CRLF e com
  escrita atômica, registro global exige UTF-8 e imprime backup. 52 testes OK. Backlog em
  `tasks/todo.md`: FM-005 e FM-009.

## Log

## [HANDOFF · skill-seo · 2026-09-12T03:06:51-03:00 · claude]
Status: concluído
Objetivo: revisar o trabalho do Codex na skill `site-seo-release` e aplicar as correções que o
usuário aprovou.
Feito:
- Auditoria de fluxo (pipeline-auditor) mais quatro revisores independentes: código Python com
  reprodução empírica, fact-check de 20 fontes oficiais, fidelidade ao upstream com hashes,
  docs de descoberta dos três hosts. Relatório em `docs/validation/codex-work-review.md`
  (0 críticos, 2 altos, 9 médios, 14 baixos; nenhuma afirmação de SEO errada).
- Correções aplicadas: FA-001 (CRLF/BOM no instalador), FA-002 (regra de produção no gate),
  FM-001 (UTF-8 no registro global), FM-002 (stdout UTF-8), FM-003 (teste de deriva do
  catálogo), FM-004 parcial (escrita atômica no instalador), FM-006 (`verified_at`
  obrigatório), FM-007 e FM-008 (IDs `accessibility` e `conversion-tracking`), baixos de texto,
  FB-009, FB-010, FB-014. Nove testes novos, 52 no total.
- `RESULTS.md`, `todo.md` e `lessons.md` atualizados. Registro global segue `unchanged`.
Próximo passo:
- Commit e push desta leva; conferir o run de CI.
- Backlog: FM-005 (Markdown completo do gate), FM-009 (paridade HTML/JS, mobile, security
  headers, crawlers de IA), `license: MIT` no frontmatter, testes de falha em `os.replace`.
- Usar a skill num projeto real para validar construção e fechamento ponta a ponta.
Arquivos tocados: docs/validation/codex-work-review.md (novo), docs/validation/RESULTS.md,
README.md, THIRD_PARTY_NOTICES.md, skills/site-seo-release/assets/seo-spec.md,
skills/site-seo-release/references/{build-guidelines, content-media, forms-privacy-email,
global-registration, portability, release-checklist, report-contract, sources,
technical-files}.md, skills/site-seo-release/scripts/{install_skill, register_global,
release_gate, validate_skill}.py, skills/site-seo-release/tests/{test_install_skill,
test_register_global, test_release_gate}.py, tasks/todo.md, tasks/lessons.md,
tasks/ai-handoff.md.
Decisões/contexto: escopo definido pelo usuário (altos, médios de código, `verified_at`, os dois
IDs novos, baixos). `valid_report()` dos testes passou a usar `environment: production` porque
`production-verification` só pode ser `pass` em produção. Helpers do instalador não foram
extraídos para módulo comum para manter cada script autossuficiente na cópia instalada. Dois
revisores caíram no limite de sessão e foram relançados com o mesmo briefing.
Tag: "HANDOFF-skill-seo-20260912-030650-claude"

## [HANDOFF · skill-seo · 2026-09-11T23:03:31-03:00 · claude]
Status: concluído
Objetivo: fechar a task de construção da skill iniciada pelo Codex e interrompida, a partir do
briefing original do usuário.
Feito:
- Registro global aplicado com `register_global.py --apply` em `~/.claude/CLAUDE.md` e
  `~/.codex/AGENTS.md` (bloco v2, um por arquivo, backup privado ao lado de cada MD). Gemini
  ficou fora do pedido.
- Achados 1 a 4 de `docs/validation/behavior-review.md` aplicados em `SKILL.md` e
  `references/release-checklist.md`.
- Três agentes paralelos de validação (portabilidade, cobertura do briefing, comportamento).
  Divergências de gatilho entre bloco global, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e
  `install_skill.py` corrigidas; esqueleto de bloco pergunta, resposta, prova e CTA em
  `content-media.md`; resíduo "7 map.xml" removido; DMARC alinhado à RFC 9989.
- Smoke real: `claude -p` positivo ativou a skill e o negativo não carregou; `codex exec`
  positivo ativou. Ver `docs/validation/RESULTS.md`.
- Validador `valid: true`, 43 testes OK, zero travessão fora de `vendor/`.
Próximo passo:
- Commit e push deste fechamento; conferir o run de CI.
- Opcional: smoke negativo no Codex; uso real de `install_skill.py` em um projeto.
Arquivos tocados: AGENTS.md, CLAUDE.md, GEMINI.md, README.md, docs/GLOBAL_SETUP.md,
docs/validation/behavior-review.md, docs/validation/RESULTS.md (novo),
skills/site-seo-release/SKILL.md, skills/site-seo-release/references/{content-media,
forms-privacy-email, portability, release-checklist, technical-files}.md,
skills/site-seo-release/scripts/{install_skill, register_global}.py, tasks/todo.md,
tasks/lessons.md, tasks/ai-handoff.md.
Decisões/contexto: o snapshot inicial de git desta sessão dizia "sem commits", mas outra sessão
do Claude já tinha publicado o repo no mesmo diretório (tag 204619); o estado real foi
reconferido antes de agir. Travessões no cabeçalho e em três linhas deste arquivo foram trocados
por dois-pontos e vírgula, pela regra de copy do projeto. `REGISTRY_VERSION` subiu para 2 porque
o texto do bloco global mudou (inclui páginas privadas ou noindex e exclusões explícitas).
Tag: "HANDOFF-skill-seo-20260911-230331-claude"

## [HANDOFF · skill-seo · 2026-09-11T20:46:19-03:00 · claude]
Status: concluído
Objetivo: publicar o repositório no GitHub a pedido explícito do usuário ("vc tem que
publicar bora, globalmente").
Feito:
- Commit inicial (root-commit `6da3579`) com os 43 arquivos existentes: AGENTS.md, CLAUDE.md,
  GEMINI.md, LICENSE, README.md, THIRD_PARTY_NOTICES.md, docs/, skills/site-seo-release/,
  tasks/, vendor/claude-seo/, .github/workflows/validate.yml.
- Verificação prévia de segredos no conteúdo staged (grep por token/secret/api-key): nenhum
  encontrado, só menções em texto de orientação/testes.
- `git push -u origin main`; o remote `origin` já apontava pra
  `https://github.com/scheibe-369/skills-seo-safe.git` (confirmado com `gh auth status`
  autenticado como `scheibe-369`).
- Visibilidade do repositório alterada de privado para público via
  `gh repo edit --visibility public` (confirmado pelo usuário antes de aplicar, pela
  ambiguidade de "publicar globalmente").
Próximo passo: nenhum, aguardando a próxima tarefa real do projeto.
Arquivos tocados: todos os 43 arquivos do commit inicial (ver lista completa via
`git show --stat 6da3579`); mais este próprio `tasks/ai-handoff.md`.
Decisões/contexto: "globalmente" foi interpretado, com confirmação explícita do usuário, como
"tornar o repositório público no GitHub" e não como "aplicar o protocolo de handoff em todos
os workspaces" (isso já tinha sido tratado antes, na tag anterior).
Tag: "HANDOFF-skill-seo-20260911-204619-claude"

## [HANDOFF · skill-seo · 2026-09-11T20:10:59-03:00 · claude]
Status: concluído
Objetivo: criar o protocolo de handoff mútuo Claude ⇄ Codex/"ChatGPT" e documentá-lo nos MDs
globais, com este arquivo como primeira instância real.
Feito:
- Nova seção "Orquestração Multi-IA (Handoff Claude ⇄ Codex)" adicionada em
  `~/.claude/CLAUDE.md` e espelhada (com ajustes de perspectiva) em `~/.codex/AGENTS.md`.
- Este arquivo (`tasks/ai-handoff.md`) criado como formato de referência.
- Mecanismo validado num segundo workspace (`D:/Projetos-vibeocding/tyvo/tasks/ai-handoff.md`)
  para confirmar que não depende de nada específico deste projeto.
- Memória `reference` criada no Claude Code apontando pra este arquivo e pra seção global.
Próximo passo: nenhum, protocolo pronto, aguardando a próxima tarefa real do projeto
(retomar via `tasks/todo.md` / `SEO-SPEC.md` / `skills/site-seo-release/SKILL.md` conforme o
fluxo já documentado em `AGENTS.md`/`CLAUDE.md` deste repositório).
Arquivos tocados: `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `tasks/ai-handoff.md` (aqui),
`D:/Projetos-vibeocding/tyvo/tasks/ai-handoff.md`, memória
`ai-handoff-protocol` (Claude Code, escopo deste projeto).
Decisões/contexto: memória privada de cada ferramenta (Claude e Codex) não é compartilhada
entre elas, então o canal mútuo tinha que ser um arquivo no próprio repositório, não a memória
de nenhuma das duas. Tag usa timestamp real + iniciais da IA em vez de contador sequencial,
para nunca colidir quando as duas ferramentas gravam de forma independente.
Tag: "HANDOFF-skill-seo-20260911-201100-claude"
