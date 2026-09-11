# Lições do projeto

## 2026-09-11

- Correção: a origem `claude-seo` é centrada no Claude, mas a nova skill precisa funcionar tanto no Claude Code quanto no OpenAI Codex.
- Regra preventiva: toda decisão de estrutura, metadados, comandos e ferramentas deve ter um caminho portátil ou uma adaptação explícita para os dois ambientes.
- Validação obrigatória: testar descoberta por `AGENTS.md` no Codex, por `CLAUDE.md` no Claude Code e por frontmatter portátil em `skills/*/SKILL.md`.
- Ampliação de requisito: o primeiro uso deve registrar no MD global do host um resumo curto de ativação e funcionamento, também para Gemini. Não confundir esse índice global com carregar o checklist inteiro a cada mensagem.
- Regra preventiva: alterações globais exigem preservar conteúdo, usar bloco idempotente e respeitar os limites de escrita da sessão. Preparar uma atualização não equivale a aplicá-la.
