# Catálogo de fechamento

Inclua uma linha para cada ID abaixo em toda revisão final. Um ID pode agregar testes de várias rotas, mas seu resultado reflete o pior caso não resolvido; vincule o inventário completo. `na` exige motivo contextual, nunca ausência de ferramenta. `required` representa obrigação do escopo do projeto, definida em `SEO-SPEC.md` antes do teste. Se o fechamento começar sem `SEO-SPEC.md`, registre primeiro o contrato contextual de `required` por ID, com base no briefing e no escopo observado, e só depois teste. Nunca reduza obrigações depois de observar falhas.

| ID | Critério e evidência esperada | Aplicabilidade e importância usual |
| --- | --- | --- |
| context | SEO-SPEC atualizado, stack, ambiente, domínio, briefing e inventário real | Obrigatório, high se contexto impede auditoria |
| page-intent | Intenção, termo principal com origem e CTA por página | Obrigatório para páginas comerciais |
| titles | Title próprio, presente no HTML e coerente em cada página indexável | Obrigatório |
| descriptions | Description específica por página, sem promessa infundada | Obrigatório nas páginas de entrada |
| headings-content | Título principal, blocos de pergunta e resposta com prova e CTA, links, fatos e schema quando usado | Obrigatório, schema pode ser dispensado |
| canonical-indexing | Canonical correto, status, HTTPS, renderização e indexação deliberada | Obrigatório, critical se bloqueia objetivo de busca |
| robots | Resposta de /robots.txt e avaliação de regras por user-agent/URL | Obrigatório para site público no padrão local |
| sitemap | XML válido, inventário canônico e URLs elegíveis verificadas | Obrigatório quando indexação pública é desejada |
| llms | Markdown público factual, links válidos e decisão experimental registrada | Padrão solicitado; low salvo requisito contratual |
| social | Preview OG e imagem compartilhável reais, sem URL de staging | Obrigatório quando compartilhamento faz parte da entrega |
| favicon | Referência na home, arquivo público e visual em tamanho pequeno | Obrigatório |
| images | Compressão comparada, dimensões, alt, formatos, LCP sem lazy e mobile | Obrigatório quando usa imagens |
| performance | Resultado de lab e/ou campo com dispositivo, data e condições | Obrigatório medir o disponível; não inventar campo |
| navigation-mobile | Navegação, CTAs, links, teclado e viewports testados | Obrigatório |
| forms-ui | Validação cliente/servidor, loading, erro, sucesso e reenvio testados | Obrigatório quando há formulário |
| forms-delivery | Registro de chegada ao destino e notificações esperadas | Obrigatório quando há formulário, critical se conversão depende dele |
| privacy | Política coerente com coleta, fornecedores e informações reais | Obrigatório quando há tratamento de dados; inventariar mesmo sem formulário |
| cookies | Comportamento de scripts, escolha, rejeição e revogação conforme base definida | Condicional ao inventário, não dispensar sem inspecionar |
| not-found | URL inexistente retorna HTTP 404 e apresenta recuperação útil | Obrigatório |
| email-spf | Registro único, remetentes, consultas e teste autenticado | Condicional a envio de e-mail no escopo |
| email-dkim | Seletor do provedor e assinatura validada em mensagem | Condicional a envio de e-mail no escopo |
| email-dmarc | Registro, alinhamento e mensagem, política contextual registrada | Condicional a envio de e-mail no escopo |
| security | Sem segredo público, HTTPS, validação e controles pertinentes ao formulário | Obrigatório no escopo, sem alegar auditoria de segurança integral |
| credit | Crédito Method Growth Hub com o HTML definido em SKILL.md, concordância, URL, target e rel, visual discreto | Obrigatório |
| build | Build/testes da stack concluídos, comandos e resultados registrados | Obrigatório; site estático sem build documenta teste equivalente |
| production-verification | Smoke HTTP/navegador e integração na URL final após publicação | Obrigatório para fechamento de produção; pending em pré-publicação |

## Execução e decisão

Leia também [report-contract.md](report-contract.md). Não classifique todas as falhas como críticas: severidade depende do impacto observado. Ausência de llms, description ou favicon não é prova de desindexação. Um erro no fluxo de conversão principal pode bloquear lançamento mesmo com ótimo SEO.

Exemplos observacionais, que orientam sem substituir a decisão contextual: `Disallow: /` em `robots.txt` de site público que pretende indexar é critical; perda comprovada de lead (sucesso na tela, nada no destino) é critical quando a conversão principal depende do formulário; página inexistente que responde HTTP 200 com texto de erro é high.

Crie o relatório antes de corrigir, resolva as falhas autorizadas e reteste. Não faça testes de carga, varredura invasiva, disparo de e-mails em massa ou submissões a serviços sem relação com o projeto. Ferramentas indisponíveis deixam pendências específicas com teste de recuperação.

Em pré-publicação, separe “implementação local verificada” de “lançamento verificado”. A pendência de produção não proíbe um deploy solicitado necessário para testá-la; impede apenas afirmar que o lançamento já está confirmado. Um deploy autorizado pode ser seguido do smoke e atualização do relatório.

