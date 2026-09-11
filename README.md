# Skills SEO Safe

Skill para orientar a construção e o fechamento de sites e landing pages no Codex e Claude Code. Inclui registro de ativação em MD global para Codex, Claude e Gemini, com leitura sob demanda.

Repositório de destino: [scheibe-369/skills-seo-safe](https://github.com/scheibe-369/skills-seo-safe).

## Uso

Leia [SKILL.md](skills/site-seo-release/SKILL.md), ou instale a pasta no projeto. A fonte canônica é `skills/site-seo-release/`.

- Início: gera `SEO-SPEC.md` com intenção, termos, metadados, páginas, integrações e critérios de aceite.
- Alteração: revisa a parte afetada e suas dependências.
- Fechamento: gera `tasks/site-release.json` e `tasks/site-release.md`, com 26 áreas de verificação, evidências e pendências.

Inclui robots, sitemap, llms, títulos, descriptions, palavras-chave, perguntas e conversão, imagem OG, favicon, compressão de imagens, formulários, 404, privacidade, cookies e SPF/DKIM/DMARC. `llms.txt` é experimental, sem promessa de ranking. E-mail é avaliado quando existe envio no escopo.

## Instalação por projeto

Requer Python 3.10+ e nenhuma dependência de terceiros. Substitua o caminho pelo projeto desejado:

```powershell
python skills/site-seo-release/scripts/install_skill.py --project "D:/caminho/do/projeto" --platform both --dry-run
python skills/site-seo-release/scripts/install_skill.py --project "D:/caminho/do/projeto" --platform both
```

O instalador cria cópias para Codex e Claude, acrescenta regras locais e preserva configurações existentes. Recusa conteúdo divergente para permitir revisão antes de atualizar. Consulte [portabilidade](skills/site-seo-release/references/portability.md).

Codex: `$site-seo-release`. Claude Code: `/site-seo-release`. Gemini: leia o caminho indicado no registro de GEMINI.md. A ativação precisa das instruções carregadas no host; este repositório sozinho não instala a skill globalmente.

## Registro global

A primeira leitura orienta a criação de um índice curto no MD global do host. O índice informa quando ativar e o que produzir. O conteúdo completo só é lido na ativação ou mudança relevante de fase/contexto.

A atualização preparada especificamente para este computador está em [GLOBAL_SETUP.md](docs/GLOBAL_SETUP.md). O script preserva conteúdo fora do bloco, cria backup privado no diretório do MD e é idempotente. Sem `--apply`, não grava.

## Verificação

```text
python skills/site-seo-release/scripts/validate_skill.py
python -m unittest discover -s skills/site-seo-release/tests -v
python skills/site-seo-release/scripts/release_gate.py CAMINHO_DO_RELATORIO.json
```

O validador do relatório verifica completude e consistência; não executa auditoria do site nem comprova a verdade das evidências. Exit 0: pronto ou pronto com ressalvas. Exit 1: não pronto. Exit 2: relatório inválido. O agente realiza as verificações de código, HTTP, navegador e integração conforme os recursos disponíveis.

O workflow de CI está preparado para Windows, Linux e macOS, Python 3.10 e 3.12. Ele só poderá executar no GitHub após publicação dos arquivos.

## Origem e situação

Base: [claude-seo](https://github.com/AgriciDaniel/claude-seo), MIT. Foram importados snapshots textuais selecionados, com licença, versões declaradas e hashes. Isso não é clone integral nem comprovação de um commit upstream. Veja [atribuição](THIRD_PARTY_NOTICES.md), [plano](docs/BUILD_PLAN.md) e [resultado dos testes](docs/validation/RESULTS.md).

O `origin` local está configurado. O remoto não foi verificado pelo Git, e não há commit/push realizado. O registro global real ficou pendente pela restrição de escrita da sessão que construiu esta versão.

<a href="https://methodgrowthhub.com.br" target="_blank" rel="noopener">Desenvolvido por Method Growth Hub</a>

