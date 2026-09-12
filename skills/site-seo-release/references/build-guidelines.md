# Contrato local de construção

Use `SEO-SPEC.md` como fonte de requisitos SEO do projeto. `AGENTS.md` e `CLAUDE.md` contêm somente a regra de uso e o caminho da skill; o catálogo de requisitos permanece nesta skill. Não sobrescreva o plano geral, arquitetura ou instruções locais com um template SEO.

## Preparação

Inspecione o briefing e as páginas existentes para registrar:

- negócio, oferta, público, região, idioma, diferencial comprovável e objetivo de conversão;
- domínio e URL pública previstos, ambiente atual e responsável pela publicação;
- stack, convenções de metadata, sistema de rotas e fontes de conteúdo;
- formulários, destinos de lead, domínio remetente, provedores de e-mail, analytics, pixels e cookies;
- ativos reais disponíveis, imagens autorizadas, logo, favicon e dados legais do controlador.

Reutilize informação confirmada. Quando um dado faltar, marque `A confirmar`, indique impacto e quem pode resolvê-lo. Avance nas partes independentes. Uma hipótese sobre palavra-chave deve ser rotulada e revisada antes da entrega, sem inventar pesquisa de demanda.

## Escrever e manter o MD

Adapte [seo-spec.md](../assets/seo-spec.md) ao projeto. Se o arquivo já existe, leia inteiro e altere só o bloco da skill, delimitado por `<!-- site-seo-release:spec:start -->` e `<!-- site-seo-release:spec:end -->`. Preserve conteúdo humano fora dele. Se os marcadores estiverem duplicados ou incompletos, reporte o conflito antes de modificar esse bloco e continue apenas trabalho independente.

Preencha uma linha por rota planejada. O mapa inclui páginas não indexáveis e explica sua exclusão. Em sites grandes, use grupos por template mais inventário completo em arquivo vinculado. Não classifique uma amostra como revisão de todas as URLs.

Fixe os itens obrigatórios de fechamento antes dos testes. Não reduza `required` ou severidade depois de uma falha apenas para aprovar. Mudanças de escopo precisam de motivo registrado.

## Planejar implementação

Crie `robots.txt`, `sitemap.xml` e `llms.txt` usando os mecanismos nativos da stack. Não duplique arquivos estáticos se rotas de metadata já geram a mesma URL. Documente o que exige domínio final e reteste em produção.

Planeje páginas com intenção própria, títulos, descriptions, H1 e canonical coerentes. Use imagens e seções para responder dúvidas reais da oferta; uma imagem deve reforçar o que a seção explica. Perguntas e respostas são um recurso editorial, sem garantia automática de conversão.

Defina o orçamento de imagens e desempenho adequado ao layout. As metas precisam distinguir medição de laboratório e dados reais. Documente formulário, estados, validação, destino e teste esperado. Inclua privacidade e e-mail conforme o uso real.

## Revisão incremental

Alterou domínio, rota ou indexação: revalide canonical, sitemap, robots, llms e links. Alterou hero: revalide LCP, dimensões, alt e copy. Alterou formulário/provedor: revalide entrega, erros, privacidade e autenticação de e-mail. Alterou conteúdo: revalide intenção, títulos, descriptions e schema.

Atualize o MD e apenas as linhas afetadas do relatório, mantendo o `verified_at` das evidências não afetadas. A revisão final repassa o catálogo completo e deixa explícitos os testes ainda não executados.

