# Plano de trabalho

## Construção (Codex, 2026-09-11)

- [x] Conectar o workspace ao repositório `scheibe-369/skills-seo-safe`.
- [x] Pesquisar a base `AgricIDaniel/claude-seo`, sua licença e orientações oficiais atuais.
- [x] Definir a arquitetura modular da skill e seus gatilhos obrigatórios.
- [x] Implementar a skill de criação e revisão final de sites e landing pages.
- [x] Incluir checklist de SEO, conversão, acessibilidade, segurança, e-mail e operação.
- [x] Incluir formato de relatório com evidências, pendências e bloqueios.
- [x] Configurar instruções locais para invocação automática e obrigatória.
- [x] Validar a skill e executar testes de consistência.
- [x] Documentar resultados nesta página.

## Fechamento (Claude Code, 2026-09-11)

- [x] Aplicar o registro global em `~/.claude/CLAUDE.md` e `~/.codex/AGENTS.md` com backup e verificação.
- [x] Aplicar os achados 1 a 4 da revisão comportamental na skill.
- [x] Rodar três agentes paralelos de validação (portabilidade, cobertura do briefing, comportamento) e corrigir as divergências apontadas.
- [x] Smoke real de ativação em sessão nova do Claude Code (positivo e negativo) e do Codex (positivo).
- [x] Criar `docs/validation/RESULTS.md` e corrigir o link do README.
- [x] Atualizar `tasks/ai-handoff.md`, `tasks/lessons.md` e esta página.
- [x] Commit e push do fechamento; o run de CI é conferido após o push.

## Correções da revisão do trabalho do Codex (Claude Code, 2026-09-12)

Relatório: `docs/validation/codex-work-review.md`. Escopo aprovado pelo usuário: altos, médios de código, `verified_at` obrigatório, IDs `accessibility` e `conversion-tracking`, baixos. Backlog: FM-005 (Markdown completo do gate) e FM-009 (checks do upstream).

- [x] FA-001: instalador normaliza CRLF e BOM antes de comparar bloco e árvore; teste de reexecução após CRLF.
- [x] FA-002: gate rejeita `production-verification` `na` em produção e `pass` fora de produção; contrato explicita `pending` em local/preview; testes.
- [x] FM-001: `register_global.py` exige alvo UTF-8 sem NUL; teste com UTF-16.
- [x] FM-002: `release_gate.py` reconfigura stdout para UTF-8; teste com caractere fora do cp1252.
- [x] FM-003: teste de deriva entre a tabela do `release-checklist.md` e `REQUIRED_CHECK_IDS`.
- [x] FM-004: instalador escreve bloco gerenciado com temporário, `os.replace` e fim de linha preservado (helpers não extraídos, por decisão).
- [x] FM-006: `verified_at` obrigatório em `pass` (script, contrato, testes).
- [x] FM-007 e FM-008: IDs `accessibility` e `conversion-tracking` na tabela, no script, no template e nos testes.
- [x] FB-001 a FB-008, FB-012, FB-013: precisões de texto nas referências, fontes, template, portabilidade, README e avisos de terceiros.
- [x] FB-009, FB-010, FB-014: mensagem de reparse point, `.json` no scan do validador, `main(argv)`, `BACKUP:` impresso e sem backup vazio em `create`.
- [x] Validador `valid: true`, 52 testes OK, zero travessão, resultado registrado no relatório e em `RESULTS.md`.
- [ ] Backlog: FM-005 (Markdown completo do gate), FM-009 (checks do upstream), `license: MIT` no frontmatter, testes de falha em `os.replace`.

## Revisão

Resultado em 2026-09-11: validador `valid: true`, 43 testes OK, CI verde nos dois commits publicados, registro global aplicado e ativação confirmada nos dois hosts. Detalhes em `docs/validation/RESULTS.md`.

Pendências que sobram:

- Smoke negativo no Codex (endpoint interno sem página) ainda não executado.
- Instalação por projeto com `install_skill.py` testada só por arquivos; falta um uso real em projeto instalado.
- Gemini: registro global fora do pedido; o `GEMINI.md` de cada projeto é atualizado manualmente.
