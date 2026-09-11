# Handoff mútuo Claude ⇄ Codex — skill-seo

Canal de retomada entre Claude Code e OpenAI Codex CLI para este projeto. Ver a seção
"Orquestração Multi-IA" nos MDs globais (`~/.claude/CLAUDE.md` e `~/.codex/AGENTS.md`) para o
protocolo completo. Resumo: para retomar, precisa só do nome do projeto (`skill-seo`) e da tag
entre aspas da entrada desejada, ou usar o bloco `Estado atual` abaixo se não vier tag.

## Estado atual

- Tag: "HANDOFF-skill-seo-20260911-204619-claude"
- Status: concluído
- Resumo: repositório publicado no GitHub (`scheibe-369/skills-seo-safe`, agora público,
  branch `main` com o commit inicial); protocolo de handoff mútuo Claude⇄Codex já estava
  configurado nos MDs globais e validado neste projeto. Nenhuma tarefa de produto em andamento.

## Log

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
- `git push -u origin main` — remote `origin` já apontava pra
  `https://github.com/scheibe-369/skills-seo-safe.git` (confirmado com `gh auth status`
  autenticado como `scheibe-369`).
- Visibilidade do repositório alterada de privado para público via
  `gh repo edit --visibility public` (confirmado pelo usuário antes de aplicar, pela
  ambiguidade de "publicar globalmente").
Próximo passo: nenhum — aguardando a próxima tarefa real do projeto.
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
Próximo passo: nenhum — protocolo pronto, aguardando a próxima tarefa real do projeto
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
