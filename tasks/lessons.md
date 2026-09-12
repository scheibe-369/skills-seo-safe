# Lições do projeto

## 2026-09-11

- Correção: a origem `claude-seo` é centrada no Claude, mas a nova skill precisa funcionar tanto no Claude Code quanto no OpenAI Codex.
- Regra preventiva: toda decisão de estrutura, metadados, comandos e ferramentas deve ter um caminho portátil ou uma adaptação explícita para os dois ambientes.
- Validação obrigatória: testar descoberta por `AGENTS.md` no Codex, por `CLAUDE.md` no Claude Code e por frontmatter portátil em `skills/*/SKILL.md`.
- Ampliação de requisito: o primeiro uso deve registrar no MD global do host um resumo curto de ativação e funcionamento, também para Gemini. Não confundir esse índice global com carregar o checklist inteiro a cada mensagem.
- Regra preventiva: alterações globais exigem preservar conteúdo, usar bloco idempotente e respeitar os limites de escrita da sessão. Preparar uma atualização não equivale a aplicá-la.

## 2026-09-11 (fechamento pelo Claude Code)

- Correção de processo: o snapshot de `git status` do início da sessão ficou obsoleto porque outra sessão commitou e publicou no mesmo diretório enquanto esta rodava. Antes de afirmar "sem commits" ou "pendente", reconferir `git log`, `git worktree list` e `tasks/ai-handoff.md` no momento da afirmação.
- Regra preventiva: os arquivos de `tasks/` também seguem a regra de copy sem U+2013 e U+2014. O validador cobre só a skill, então rodar uma busca nos `.md` do repositório antes de cada commit.

## 2026-09-12 (revisão do trabalho do Codex)

- Regra preventiva: fixtures de teste que comparam bytes usam `write_bytes`, nunca `write_text`, porque no Windows o modo texto converte `\n` em `\r\n` e o teste falha por motivo alheio ao código.
- Regra preventiva: toda constante que replica uma tabela de documento (IDs, enums) precisa de um teste que leia o documento e compare; sem isso a deriva é silenciosa.
