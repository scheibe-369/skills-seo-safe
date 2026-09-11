# Portabilidade e instalação

O núcleo usa frontmatter `name` e `description`, instruções por capacidade e Python 3.10+ com biblioteca padrão. `agents/openai.yaml` é metadado opcional do Codex. Claude Code pode ignorá-lo. O funcionamento não depende de subagentes ou do runtime upstream.

## Escopos distintos

- Desenvolvimento: `skills/site-seo-release/` é a fonte de verdade neste repositório. `AGENTS.md` e `CLAUDE.md` locais apontam para ela explicitamente.
- Instalação por projeto: o instalador copia a mesma skill para `.agents/skills/site-seo-release/` no Codex e `.claude/skills/site-seo-release/` no Claude Code. Acrescenta uma regra curta ao MD local de cada host.
- Registro global: [global-registration.md](global-registration.md) explica como cadastrar somente o índice de ativação no MD do usuário, inclusive Gemini. Ele aponta para um caminho acessível; não é cópia automática da skill nem instalação de plugin.

## Instalar em outro projeto

Execute a partir deste repositório, usando um caminho real de projeto existente:

```text
python skills/site-seo-release/scripts/install_skill.py --project CAMINHO_DO_PROJETO --platform both --dry-run
python skills/site-seo-release/scripts/install_skill.py --project CAMINHO_DO_PROJETO --platform both
```

Substitua `CAMINHO_DO_PROJETO` e use aspas quando houver espaços. A primeira chamada mostra o plano. A segunda aplica a instalação quando autorizada e permitida. `codex` ou `claude` selecionam um host. Não há download nem dependência externa.

O instalador não sobrescreve árvores diferentes ou blocos locais conflitantes. Uma atualização de versão exige inspecionar o diff da cópia instalada e aplicar uma atualização deliberada. Erros de permissão durante aplicação podem deixar uma instalação parcial; inspecione os arquivos e repita após resolver, sem apagar dados do usuário.

## Ativação e economia de contexto

No Codex instalado, use `$site-seo-release`. No Claude instalado, use `/site-seo-release`. O nome e descrição permitem seleção implícita, mas a regra local/global é o que estabelece o uso obrigatório no fluxo do usuário. Não afirme que a presença de `skills/` isoladamente instala ou garante autoativação em qualquer host.

No Gemini, use o registro em GEMINI.md como índice e leia a skill pelo caminho indicado quando houver gatilho; esta entrega não inclui empacotamento de extensão Gemini.

Após mudar instruções globais, inicie nova sessão no host ou use seu mecanismo de recarga documentado. Teste uma solicitação positiva e uma negativa; registre host, versão e resultado. Testes de arquivos/cópias não substituem esse smoke real.

Sem ferramenta de navegador, entregue análise de código/HTTP disponível e registre os testes visuais pendentes. Sem Python, aplique manualmente o contrato de relatório, registrando a limitação.

