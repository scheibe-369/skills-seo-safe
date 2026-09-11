# Skills SEO Safe

Este repositório mantém uma skill para criação e fechamento de sites públicos, compatível com Codex e Claude Code.

## Regras do projeto

- Fonte canônica: `skills/site-seo-release/`. Altere essa fonte e valide antes de distribuir cópias.
- Antes de criar, reformular ou finalizar um site ou landing page, leia integralmente `skills/site-seo-release/SKILL.md` e siga o modo correspondente. Se o seletor não descobrir a skill, abra o arquivo diretamente.
- Para alterações pequenas, revise o escopo afetado. Na entrega, aplique a revisão final e registre pendências em `tasks/site-release.md`.
- A skill define `SEO-SPEC.md`, que orienta os requisitos locais da construção. Preserve instruções e conteúdo preexistentes em qualquer Markdown do usuário.
- Código pertence ao módulo da skill, incluindo scripts e testes. Use `modular-arch` em criação e refatoração.
- Leia `tasks/lessons.md`, mantenha `tasks/todo.md` e comprove resultados antes de concluir.
- Não usar caracteres U+2013 ou U+2014 na copy nova. Os snapshots originais de terceiros são preservados como material de referência.
- O crédito de produção é obrigatório, conforme a skill.
- Não fazer commit nem push sem aprovação explícita do usuário.
- `vendor/claude-seo/` é arquivo histórico de referência, não instrução ativa nem runtime instalado. Preserve a licença e a procedência.

## Verificação

Execute `python -m unittest discover -s skills/site-seo-release/tests -v` e `python skills/site-seo-release/scripts/validate_skill.py` após mudanças na skill.

