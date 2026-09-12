# Arquivos públicos, indexação e HTTP

## Antes de criar arquivos

Inspecione rotas de metadata, plugins do CMS, saída de build e regras da hospedagem. Uma rota dinâmica que responde `/sitemap.xml` já pode cumprir o requisito. Verifique a resposta efetiva, não apenas a existência de arquivo no disco. Diferencie produção, preview e origem de assets.

## robots.txt

Nome correto: `robots.txt`. Disponibilize em `/robots.txt`, UTF-8 e texto simples, com regras deliberadas e referência absoluta ao sitemap. O exemplo abaixo só serve para um site público integralmente rastreável e precisa do domínio real antes de publicação:

```text
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Não aplique esse exemplo a um site que já tenha exclusões necessárias. Teste URLs por grupo de user-agent, inclusive regras específicas mais restritivas. Verifique CSS, JS, imagens e favicon necessários à renderização. Não imponha bloqueio de todos os crawlers de IA sem a decisão do proprietário.

Robots controla rastreamento. Para desindexação use mecanismos apropriados, como `noindex` em resposta que o crawler possa ler. Para conteúdo privado use autenticação. Bloquear crawling e depender do `noindex` da página pode impedir que o buscador o veja.

A ausência de robots não bloqueia crawling por si só. Sua existência é padrão de entrega solicitado aqui; ausência é pendência do projeto, sem alegar penalidade automática do Google. Em preview, não remova proteções de forma global ao preparar produção.

## sitemap.xml

Nome convencional: `sitemap.xml`. Gere a partir do inventário canônico, não de uma lista de todas as rotas indiscriminadamente.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc></url>
</urlset>
```

Use URLs absolutas, escape XML corretamente e inclua apenas páginas públicas que devam ser indexadas, com canonical consistente e resposta 200. Exclua redirects, erros, páginas privadas, `noindex`, parâmetros descartáveis e duplicatas. Teste XML com parser, compare com a matriz de páginas e verifique as URLs; informe amostragem se não verificar todas.

Se incluir `lastmod`, use a data real de alteração substancial. Não atualize por compilação sem mudança de conteúdo. Respeite 50.000 URLs e 50 MB descompactados por sitemap; use índice acima disso. O Google ignora `priority` e `changefreq`. Em sites multilíngues, verifique as alternâncias reais de idioma e hreflang conforme documentação atual.

Registrar ou enviar sitemap ao Search Console é uma etapa de descoberta após acesso autorizado. Sua ausência não transforma testes locais em falha de XML nem garante que um envio resulte em indexação. Se pendente, deixe como ação operacional separada.

## llms.txt

Nome correto: `llms.txt`, proposta comunitária em Markdown. O padrão desta skill inclui sua criação para sites públicos. Pode ser dispensado por motivo contextual documentado, por exemplo conteúdo privado ou decisão explícita do usuário. Não usar como autorização para treinamento, bloqueio de bots ou substituição de HTML, robots e sitemap.

```markdown
# Nome público do negócio

> Descrição factual e curta da oferta, público e região atendida.

## Informações principais

- [Serviços](https://example.com/servicos): o que é oferecido e suas condições.
- [Contato](https://example.com/contato): canais públicos de atendimento.
- [Privacidade](https://example.com/privacidade): como os dados são tratados.
```

Substitua todo exemplo por fatos e links reais. Não publique credenciais, dados internos, instruções para burlar agentes ou promessas não presentes no site. Mantenha os links atualizados. Se disponibilizar versões `.md` de páginas, gere do mesmo conteúdo para evitar divergência e só aponte para URLs existentes.

Verifique HTTP 200, Markdown legível e todos os links. A presença do arquivo não comprova adoção pelos buscadores ou agentes. Consulte a proposta vigente nas fontes antes de acrescentar convenções novas.

## Canonical, redirects e 404

Decida protocolo, hostname e slash finais. Teste canonical absoluto por rota, variantes e redirecionamentos permanentes reais. Não mande todos os canonicals para a home. Páginas indexáveis não podem ter `noindex` acidental em meta ou `X-Robots-Tag`.

Peça uma URL inexistente de verdade, inclusive rota aninhada, e examine o status HTTP servido pela hospedagem. Exiba 404 útil com home e navegação. Uma SPA com fallback 200 não satisfaz esse teste. Não redirecione toda URL desconhecida para a home. Se houver substituição real, use redirect para o conteúdo equivalente. Exclua páginas de erro do sitemap.

Confira conteúdo essencial no HTML servido e no renderizado, rotas acessíveis diretamente, links com `href`, HTTPS e recursos quebrados. Não imponha migração de framework como única solução de SEO sem evidência de falha de renderização.

