# Registro global preparado

Os arquivos reais foram lidos e a prévia passou em 2026-09-11:

- Codex: `C:/Users/Helinho Filhão/.codex/AGENTS.md`.
- Claude: `C:/Users/Helinho Filhão/.claude/CLAUDE.md`.
- Skill: `D:/Projetos-vibeocding/skill-seo/skills/site-seo-release/SKILL.md`.

Nenhum bloco da skill existia nos dois MDs. Não havia `AGENTS.override.md` na pasta global do Codex. A sessão permite escrita somente no workspace, portanto os arquivos globais não foram alterados. Não é necessário pedir novamente autorização para a finalidade solicitada, mas a aplicação precisa ocorrer num ambiente que permita gravar nesses caminhos.

Execute no PowerShell fora da sessão restrita:

```powershell
python "D:/Projetos-vibeocding/skill-seo/skills/site-seo-release/scripts/register_global.py" --target "C:/Users/Helinho Filhão/.codex/AGENTS.md" --apply
python "D:/Projetos-vibeocding/skill-seo/skills/site-seo-release/scripts/register_global.py" --target "C:/Users/Helinho Filhão/.claude/CLAUDE.md" --apply
```

Para verificar, rode os mesmos comandos sem `--apply`: devem retornar `STATUS: unchanged`. O script só mostra o caminho, o status e o bloco gerenciado no modo prévia. Não mostra instruções privadas existentes.

Cada aplicação que altera um MD cria um backup exclusivo `.site-seo-release.<identificador>.bak` ao lado dele. Mantenha o backup privado. A restauração consiste em comparar o backup com o MD atual e restaurar o conteúdo anterior, preservando mudanças posteriores do usuário.

Inicie novas sessões de Claude e Codex para recarregar suas instruções globais. Teste “vou criar uma landing page” e confirme leitura da skill e criação do SEO-SPEC. Em uma tarefa de API isolada, confirme que a skill não é carregada.

O suporte a GEMINI.md está na skill e no registrador, mas o pedido de aplicação neste computador especificou Claude e Codex. Nenhuma alteração global do Gemini foi aplicada.

