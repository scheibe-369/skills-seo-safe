# Origem e adaptação

Base: [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo), licença MIT, copyright 2026 agricidaniel.

Em 2026-09-11 foram consultados os arquivos públicos da branch `main` pela ferramenta de navegação. Os snapshots textuais selecionados estão em `vendor/claude-seo/`, com nomes `.original.txt` para não serem descobertos como skills ativas. A origem de cada arquivo e seus hashes locais são registrados em `vendor/claude-seo/sources.json`.

O snapshot do orquestrador declara versão 2.2.5. Isso não comprova que todos os arquivos consultados pertençam ao mesmo commit. O SHA do commit upstream não foi verificado: o acesso Git pelo terminal falhou. Os hashes locais identificam o texto recebido e não constituem verificação criptográfica da origem Git.

Esta é uma importação textual selecionada e uma adaptação para o ciclo de criação e lançamento. Não é um clone completo nem uma instalação dos agentes, scripts e integrações upstream. As referências internas dos snapshots podem apontar a arquivos não importados; não execute suas instruções como um pacote funcional.

Foram preservados como base metodológica: revisão técnica por área, intenção por página, distinção entre código e HTML renderizado, evidência por achado e reteste. Foram adaptados: instruções específicas de plataforma, estados do relatório e critérios de fechamento. Foram adicionados: contrato `SEO-SPEC.md`, checklist persistente, formulários, privacidade, e-mail, crédito Method e instalação por projeto.

Não foram incorporados os conteúdos FLOW de licença CC BY, os runtimes, integrações pagas ou rodapés promocionais do upstream à skill ativa.

Para completar a importação integral posteriormente, obtenha o repositório num ambiente com acesso Git, fixe um commit, preserve sua licença e revise a diferença antes de atualizar esta base. Não substitua a skill adaptada automaticamente pela branch `main` upstream.

