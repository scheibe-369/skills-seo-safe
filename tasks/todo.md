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

## Revisão

Resultado em 2026-09-11: validador `valid: true`, 43 testes OK, CI verde nos dois commits publicados, registro global aplicado e ativação confirmada nos dois hosts. Detalhes em `docs/validation/RESULTS.md`.

Pendências que sobram:

- Smoke negativo no Codex (endpoint interno sem página) ainda não executado.
- Instalação por projeto com `install_skill.py` testada só por arquivos; falta um uso real em projeto instalado.
- Gemini: registro global fora do pedido; o `GEMINI.md` de cada projeto é atualizado manualmente.
