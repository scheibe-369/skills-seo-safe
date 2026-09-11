# Índice global de ativação

Na primeira leitura da skill, identifique o MD global efetivamente usado pelo host e cadastre um bloco curto. O objetivo é manter os gatilhos sempre disponíveis e carregar o conteúdo completo somente na tarefa relevante.

| Host | Caminho padrão de instruções globais | Observação |
| --- | --- | --- |
| Codex | diretório Codex configurado, `AGENTS.md` | Se existir `AGENTS.override.md` não vazio, ele prevalece. Identifique a fonte efetiva antes de escrever. |
| Claude Code | diretório pessoal `.claude/CLAUDE.md` | Respeite diretório/configuração personalizada quando existir. |
| Gemini CLI | diretório pessoal `.gemini/GEMINI.md` | O nome pode estar configurado em `context.fileName`; verifique quando não for o padrão. |

Não adivinhe o diretório pessoal a partir de caminhos de outro computador. Use o host/configuração observados e confirme acesso ao arquivo da skill. O registro só funcionará onde esse caminho existir. Para cloud ou outra máquina, instale no projeto ou registre um caminho disponível naquele ambiente.

## Procedimento

1. Leia o MD global existente sem copiar suas instruções privadas, tokens ou dados para o repositório ou logs de saída.
2. Procure o bloco `<!-- site-seo-release:global:start -->` até `<!-- site-seo-release:global:end -->`.
3. Se já estiver atualizado para a skill acessível, reutilize. Não regrave a cada tarefa. Se a skill local do projeto for uma cópia temporária, não substitua um caminho global estável válido por ela.
4. Se faltar ou precisar de atualização, insira/atualize só esse bloco. Preserve todo o restante e a codificação. Marcadores duplicados/incompletos exigem resolver o conflito, sem sobrescrever o arquivo inteiro.
5. Use `scripts/register_global.py` para preparar a alteração e, havendo permissão de escrita, aplicar com backup. O pedido de registro global do usuário já autoriza essa finalidade; não peça confirmação repetida. Restrições do ambiente continuam valendo.
6. Releia apenas o bloco e confirme presença única, caminho e conteúdo. Registre o resultado: aplicado, já atualizado ou bloqueado. Se bloqueado, entregue o bloco/comando e continue a tarefa que independe dele.

O cadastro é do host ativo. Não altere os MDs dos demais hosts apenas por encontrá-los no disco. Um pedido explícito para vários hosts, como Codex e Claude, autoriza os alvos nomeados.

## Conteúdo mínimo

O bloco registra versão do índice, nome da skill, caminho absoluto verificado, gatilhos e exclusões. Explica os modos construção (`SEO-SPEC.md`), alteração incremental e fechamento (`tasks/site-release.json` e `.md` com evidências/pendências). Instrui leitura do núcleo ao ativar e de referências sob demanda, reutilizando contexto atual. Não use uma diretiva de importação incondicional do arquivo inteiro.

```text
python CAMINHO_DA_SKILL/scripts/register_global.py --target CAMINHO_DO_MD_GLOBAL --skill CAMINHO_DA_SKILL/SKILL.md
python CAMINHO_DA_SKILL/scripts/register_global.py --target CAMINHO_DO_MD_GLOBAL --skill CAMINHO_DA_SKILL/SKILL.md --apply
```

Substitua os caminhos e mantenha aspas em caminhos com espaços. Sem `--apply`, apenas mostra o novo bloco e o estado, sem modificar o MD. O backup da aplicação permanece ao lado do MD global e deve ser tratado como privado. Nunca publique esse backup no repositório da skill.

