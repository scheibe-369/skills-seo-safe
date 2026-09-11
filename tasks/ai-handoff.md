# Handoff mútuo Claude ⇄ Codex — skill-seo

Canal de retomada entre Claude Code e OpenAI Codex CLI para este projeto. Ver a seção
"Orquestração Multi-IA" nos MDs globais (`~/.claude/CLAUDE.md` e `~/.codex/AGENTS.md`) para o
protocolo completo. Resumo: para retomar, precisa só do nome do projeto (`skill-seo`) e da tag
entre aspas da entrada desejada, ou usar o bloco `Estado atual` abaixo se não vier tag.

## Estado atual

- Tag: "HANDOFF-skill-seo-20260911-201100-claude"
- Status: concluído
- Resumo: protocolo de handoff mútuo Claude⇄Codex configurado nos MDs globais e validado neste
  projeto; nenhuma tarefa de produto em andamento no momento.

## Log

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
