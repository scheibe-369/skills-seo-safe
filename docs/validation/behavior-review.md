# Revisão comportamental independente da skill `site-seo-release`

## Escopo e método

Esta revisão simula o comportamento descrito pela skill contra os casos de `skills/site-seo-release/tests/behavior-cases.json`. Ela não executa site, navegador, HTTP, DNS, formulário, envio, registro global nem smoke real em Claude, Codex ou Gemini.

Cada conclusão abaixo usa somente os fatos declarados no caso. `pending` significa teste ou trabalho não realizado. `blocked` exige um impedimento identificado. A decisão do gate só é indicada quando os fatos permitem uma revisão de fechamento. Nos demais casos, a coluna informa que o gate não se aplica ou ainda não pode ser calculado.

## Resultado resumido

| Caso | Ativação e modo | Decisão operacional | Gate de release |
| --- | --- | --- | --- |
| `new-landing` | Ativar, construção | Prosseguir com especificação e marcar dependências externas | Ainda não aplicável |
| `local-finish` | Ativar, revisão final local | Não declarar lançamento pronto | `NOT_READY` |
| `production-observations` | Ativar, revisão final de produção | Corrigir bloqueios observados antes de aprovar | `NOT_READY` |
| `narrow-edit` | Ativar, incremental | Limitar a revisão à imagem e dependências afetadas | Não recalcular o gate completo |
| `explicit-exclusion` | Não ativar | Executar somente a tarefa de endpoint fora desta skill | Não aplicável |
| `private-campaign` | Ativar, revisão final privada | Preservar autenticação e `noindex`; não afirmar fechamento | `NOT_READY` com os fatos disponíveis |
| `global-registration` | Ativar, instalação e portabilidade | Preparar alterações, registrar bloqueio de escrita global | Não aplicável |

## Casos detalhados

### 1. `new-landing`

**Ativação e modo:** ativação implícita esperada. O pedido é criação de landing page, portanto o modo é construção.

**Decisão operacional:** prosseguir nas partes independentes. Não inventar domínio, provedor de e-mail, dados de pesquisa ou volume de busca. A intenção comercial, a região Curitiba e o CTA de orçamento são fatos do briefing. Qualquer termo principal derivado desses fatos deve ser rotulado como hipótese de briefing, não como resultado de pesquisa.

**Arquivos que o fluxo criaria ou atualizaria:**

- `SEO-SPEC.md`, a partir do template da skill.
- Arquivos modulares da landing page conforme a stack, ainda não informada.
- Implementação nativa de `robots.txt`, `sitemap.xml` e `llms.txt`, mas URLs absolutas finais ficam pendentes até existir domínio.
- Favicon, imagem social e imagens de página quando os ativos forem fornecidos ou autorizados.
- Formulário de orçamento e sua integração quando o destino for definido.
- Política de privacidade baseada na coleta e nos fornecedores reais, após os dados faltantes serem confirmados.
- Referência curta em `AGENTS.md` e `CLAUDE.md` locais somente se a configuração desses MDs estiver autorizada.
- `tasks/site-release.json` e `tasks/site-release.md` apenas na revisão final.

**Evidências disponíveis:** negócio, serviço, região, CTA, ausência de código, ausência de domínio final, ausência de provedor de e-mail, escrita limitada ao projeto e indisponibilidade de pesquisa de volume.

**Pendências:** stack, rotas, nome público do negócio, oferta detalhada, público, provas e diferenciais, ativos, domínio, destino do lead, controlador e contato de privacidade, inventário de cookies, provedor e fluxo de e-mail. SPF, DKIM e DMARC não podem ser configurados ou aprovados sem domínio e provedor. Pesquisa de volume não é condição para avançar, mas nenhuma métrica pode ser atribuída ao termo.

### 2. `local-finish`

**Ativação e modo:** ativar em revisão final, ambiente `local`.

**Decisão operacional:** gerar o relatório completo de fechamento, preservar as evidências locais e declarar que o lançamento não está confirmado.

**Gate:** `NOT_READY`. `production-verification` permanece aberto para um pedido que pergunta se o site está pronto, pois não há URL publicada. A entrega do formulário também não foi comprovada. O código contém uma chamada a `/api/leads` e uma condição visual de sucesso, mas isso não prova que a requisição foi executada nem que o lead chegou ao destino.

**Arquivos que o fluxo criaria ou atualizaria:**

- `tasks/site-release.json` com todos os IDs do catálogo.
- `tasks/site-release.md` com decisão, evidências, limitações e pendências.
- `SEO-SPEC.md` apenas se existir e precisar refletir o fechamento; o caso não informa sua existência.

**Evidências disponíveis:** build local com exit code 0; title e description presentes nas três páginas do build; código da home chama `fetch('/api/leads')`; a interface exibe sucesso quando recebe HTTP 200.

**Pendências:** navegador, URL de produção, smoke HTTP, teste da interface do formulário, resposta real do endpoint, confirmação no destino do lead, mobile, 404 efetivo, arquivos públicos, canonicals, favicon, imagens, performance, privacidade, cookies, segurança, crédito e demais checks sem resultado. Acesso DNS ausente é impedimento apenas para checks de e-mail que sejam aplicáveis após inventariar o fluxo de envio. A skill não permite converter ausência de resultado em `pass`.

### 3. `production-observations`

**Ativação e modo:** ativar em revisão final, ambiente `production`.

**Decisão operacional:** não aprovar a versão publicada. Registrar as falhas observadas, corrigir somente se a tarefa autorizar implementação e repetir os testes afetados.

**Gate:** `NOT_READY` pelos seguintes observáveis:

- `robots`: `fail`, pois `Disallow: /` bloqueia todo rastreamento no escopo observado de um site publicado.
- `sitemap`: `fail`, pois contém `/obrigado`, que tem `noindex`, e `/nao-existe`, que representa página inexistente.
- `not-found`: `fail`, pois `/nao-existe` responde HTTP 200 apesar de exibir texto de página não encontrada.
- `forms-delivery`: `fail`, pois a submissão respondeu 200 e exibiu sucesso, mas nenhum registro foi encontrado no CRM.
- `email-dkim`: `blocked`, pois o domínio usa e-mail próprio, mas o seletor não foi fornecido.
- `email-dmarc`: `fail`, pois `_dmarc` retorna NXDOMAIN para um domínio de envio informado.

Esses achados incluem falhas de indexação e de conversão que impedem `READY` independentemente dos checks sem resultado.

**Arquivos que o fluxo criaria ou atualizaria:**

- `tasks/site-release.json` com todos os IDs e as evidências fornecidas.
- `tasks/site-release.md` com bloqueios em ordem de impacto e procedimento de reteste.
- Arquivos do site somente em uma tarefa posterior que autorize correção.

**Evidências disponíveis:** códigos HTTP e conteúdos declarados de `/`, `/robots.txt`, `/sitemap.xml` e `/nao-existe`; `noindex` em `/obrigado`; resposta e toast do formulário; ausência do lead no CRM; uso de domínio próprio para e-mail; ausência de seletor DKIM; NXDOMAIN de `_dmarc`.

**Pendências:** investigar a perda do lead antes de alterar o estado visual; obter o seletor e uma mensagem recebida com cabeçalhos sanitizados para validar DKIM; definir DMARC após inventariar remetentes e alinhamento; executar todos os demais checks sem resultado. SPF não pode receber `pass`, `fail` ou recomendação de valor específico sem observação do registro e dos remetentes.

### 4. `narrow-edit`

**Ativação e modo:** ativar no modo incremental. A solicitação explícita limita a mudança à foto do hero e dispensa a auditoria inteira neste momento.

**Decisão operacional:** respeitar o escopo estreito, mas revalidar imagem e dependências diretamente afetadas. A evidência anterior de mídia e performance fica antiga para esses objetos. Os demais achados do relatório anterior devem ser preservados.

**Gate:** não recalcular o gate completo. O caso não pede fechamento e não fornece o estado integral do catálogo.

**Arquivos que o fluxo criaria ou atualizaria:**

- Variante otimizada e responsiva da imagem fornecida, preservando o original, se a tarefa real autorizasse a edição.
- Arquivo modular que referencia a imagem do hero.
- Linhas de mídia, LCP e decisão da imagem em `SEO-SPEC.md`.
- Apenas os registros afetados do relatório anterior, caso ele siga o contrato atual.

**Evidências disponíveis:** existência de `SEO-SPEC.md` e relatório anterior; imagem nova de 4200 por 2800 pixels e 7 MB; hero atual usa `loading=lazy`.

**Pendências:** inspecionar formato e conteúdo da imagem, licença ou autorização, propor dimensões e compressão adequadas ao layout, registrar bytes antes e depois, revisar corte mobile e desktop, alt contextual e comportamento LCP. O fato de ser hero não prova sozinho que a imagem é o elemento LCP, mas exige retirar ou manter lazy loading com base no teste do elemento crítico, não por suposição.

### 5. `explicit-exclusion`

**Ativação e modo:** não ativar. O pedido exclui SEO explicitamente e o endpoint não produz página nem interface pública.

**Decisão operacional:** tratar somente o endpoint pela disciplina técnica apropriada. Não criar `SEO-SPEC.md`, arquivos públicos, relatório de release da skill ou adaptadores locais por causa deste pedido.

**Evidências disponíveis:** endpoint interno, sem página e sem interface pública; exclusão explícita de SEO.

**Pendências da skill:** nenhuma. A correção do endpoint pertence a outro fluxo.

### 6. `private-campaign`

**Ativação e modo:** ativar em revisão final de uma página privada. Embora não deva ser otimizada para busca pública, o corpo da skill contém regras explícitas para campanha `noindex` e conteúdo autenticado.

**Decisão operacional:** preservar login e `noindex`. Não recomendar indexação, remoção da autenticação ou inclusão em sitemap e `llms.txt`. `robots.txt` não deve ser tratado como controle de acesso.

**Gate:** `NOT_READY` com os fatos disponíveis, pois o pedido é finalizar e só há evidência de autenticação e `noindex`. Não existem resultados para build, acesso direto, navegação, formulário, privacidade, cookies, segurança, crédito ou outros requisitos aplicáveis. Checks de descoberta pública podem ser `na` com o motivo de página privada, mas ausência de teste dos demais checks não pode virar dispensa.

**Arquivos que o fluxo criaria ou atualizaria:**

- `SEO-SPEC.md` com `/convite`, intenção privada, `Indexar? não` e motivo.
- `tasks/site-release.json` e `tasks/site-release.md` com todos os IDs, usando `na` somente quando a privacidade demonstrar inaplicabilidade.
- Arquivos da página apenas se a tarefa de finalização autorizar alterações e houver falhas observadas.

**Evidências disponíveis:** `/convite` exige login; `noindex` é intencional; o usuário não autorizou torná-la pública.

**Pendências:** testar se o acesso realmente exige autenticação, se a resposta privada mantém `noindex`, se a rota não aparece no sitemap ou `llms.txt`, e executar os demais checks aplicáveis à página privada.

### 7. `global-registration`

**Ativação e modo:** ativação explícita, modo instalação e portabilidade, com alvos Codex e Claude nomeados pelo usuário.

**Decisão operacional:** não escrever nos MDs globais porque o ambiente permite somente leitura fora do projeto. Ler os arquivos sem reproduzir conteúdo privado, preparar os dois blocos ou comandos e registrar a pendência. Não contornar a restrição e não escrever uma cópia dos globais dentro do repositório.

**Gate:** não aplicável, pois não é revisão de um site.

**Arquivos que o fluxo alteraria se houvesse permissão:** o MD global efetivo do Codex e `.claude/CLAUDE.md` efetivo, preservando todo conteúdo existente e inserindo um único bloco delimitado por host. Nesta simulação, nenhum deles pode ser alterado.

**Evidências disponíveis:** ambos os arquivos possuem instruções preexistentes; nenhum bloco da skill existe; leitura global é permitida; escrita é limitada ao projeto.

**Pendências:** identificar os caminhos efetivos, gerar preview dos blocos com `register_global.py` sem `--apply`, obter um ambiente com escrita permitida, aplicar com backup e confirmar presença única. Depois, iniciar nova sessão em cada host e executar um prompt positivo e um negativo. A validação de arquivos não comprova ativação nos aplicativos.

## Ambiguidades observadas

1. **Página privada e descrição de ativação:** a descrição exclui telas internas sem superfície pública, mas o corpo instrui como finalizar campanha privada ou `noindex`. O caso `private-campaign` deve ativar para preservar exclusão da busca e revisar qualidade de release. A descrição deveria explicitar essa exceção para aumentar o recall implícito.
2. **Obrigatoriedade sem `SEO-SPEC.md`:** o contrato determina que `required` seja definido antes do teste no `SEO-SPEC.md`. Os casos de fechamento não informam esse arquivo. É possível concluir `NOT_READY` quando há falha critical/high ou pendência clara de produção, mas não preencher todos os booleanos contextuais de forma auditável sem primeiro recuperar ou estabelecer o contrato.
3. **Severidade contextual:** o catálogo fornece importância usual, mas não fixa severidade por ID. Isso é correto para adaptação, porém permite divergência entre agentes. Exemplos mínimos de severidade para bloqueio total de rastreamento, perda do lead e falso 404 reduziriam variação sem transformar heurísticas em regras universais.
4. **Arquivos previstos em modo construção:** a entrega menciona artefatos implementados e relatórios, mas não define exatamente em que momento o relatório inicial nasce. A referência de fechamento diz para criar o relatório antes de corrigir. Uma frase explícita distinguindo checklist de construção em `SEO-SPEC.md` e relatório de auditoria em `tasks/` evitaria criação prematura de relatórios vazios.
5. **Registro global na primeira leitura:** esse efeito colateral pode ocorrer durante auditoria somente leitura ou avaliação isolada. A skill contém fallback seguro quando a escrita é bloqueada, mas deveria deixar explícito que testes e avaliações em workspace temporário apenas registram a pendência, sem tentar modificar o ambiente do avaliador.
6. **`blocked` versus `pending`:** o contrato define bem os estados. Ainda assim, a falta de um resultado sem informação sobre disponibilidade de ferramenta deve ser `pending`; só deve ser `blocked` quando o caso identifica o impedimento. Essa regra poderia aparecer em uma frase direta no contrato.

## Achados acionáveis

1. Ajustar a descrição para incluir finalização de páginas privadas ou `noindex` quando o objetivo é preservar a exclusão da busca.
2. Acrescentar ao checklist exemplos de severidade observacional para bloqueio total em robots, perda comprovada de lead e falso 404, mantendo decisão contextual.
3. Explicitar que, se um fechamento começa sem `SEO-SPEC.md`, o agente precisa registrar o contrato contextual antes de atribuir `required` e não pode reduzir obrigações após observar falhas.
4. Declarar que avaliações isoladas, dry runs e auditorias somente leitura não tentam registro global; elas apenas registram a pendência ou fornecem o preview solicitado.
5. Fixar no contrato a distinção: sem teste e sem impedimento conhecido é `pending`; sem teste por impedimento identificado é `blocked`.
6. Adicionar estes sete casos ao conjunto de regressão comportamental e comparar invariantes, não redação: ativação, modo, decisão, artefatos, evidências aceitas e pendências.

## Aplicação dos achados

Em 2026-09-11 os achados 1 a 4 foram aplicados: a descrição em `SKILL.md` passou a cobrir a finalização de páginas privadas ou `noindex`; a seção de registro global em `SKILL.md` exclui avaliações isoladas, dry runs e auditorias somente leitura; `references/release-checklist.md` ganhou exemplos observacionais de severidade e a regra de registrar o contrato de `required` quando o fechamento começa sem `SEO-SPEC.md`. Os achados 5 e 6 já estavam cobertos por `references/report-contract.md` (definição de `pending` e `blocked`) e por `tests/behavior-cases.json` (os sete casos).

## Resultado final

A skill se comporta de forma conservadora nos casos centrais: não inventa pesquisa, não confunde sucesso visual com entrega, não aprova DNS sem mensagem autenticada, preserva `noindex` intencional e não transforma teste local em publicação comprovada. Os principais riscos restantes estão na descoberta implícita do caso privado, na atribuição contextual de `required` e severidade quando falta `SEO-SPEC.md`, e no efeito colateral de registro global durante avaliações isoladas.
