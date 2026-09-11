# Plano de construção da Site SEO Release

## 1. Objetivo

Criar uma skill portátil para Claude Code e OpenAI Codex que oriente a construção e execute a revisão final de sites, páginas e landing pages. A skill deve converter requisitos de SEO, conversão, acessibilidade, privacidade, entrega de e-mail e qualidade operacional em verificações observáveis.

O resultado principal de cada revisão será um relatório local em Markdown com status, evidência, impacto, correção recomendada, responsável sugerido e condição de aceite para cada item.

## 2. Princípios de produto

1. A skill atua em dois momentos: durante a construção e antes da entrega.
2. Nenhum item pode ser aprovado por suposição. Todo aprovado precisa de evidência.
3. Itens que dependem de domínio, DNS, produção, credenciais ou decisão jurídica devem ficar como pendência ou bloqueio, nunca como aprovado.
4. Recomendações devem respeitar o framework e a arquitetura do projeto analisado.
5. A palavra-chave principal deve refletir a intenção real da página e aparecer de forma natural, sem repetição artificial.
6. `llms.txt` será tratado como proposta emergente e opcional, não como fator confirmado de ranking.
7. A política de privacidade será tecnicamente verificada, mas a skill não substituirá revisão jurídica.
8. A skill não fará deploy, mudanças de DNS, envio de formulários reais ou publicação sem autorização compatível com o projeto.

## 3. Arquitetura prevista

```text
.
|-- AGENTS.md
|-- CLAUDE.md
|-- LICENSE
|-- THIRD_PARTY_NOTICES.md
|-- skills/
|   `-- site-seo-release/
|       |-- SKILL.md
|       |-- agents/
|       |   `-- openai.yaml
|       |-- references/
|       |   |-- build-guidelines.md
|       |   |-- release-checklist.md
|       |   |-- report-contract.md
|       |   |-- portability.md
|       |   `-- sources.md
|       `-- scripts/
|           `-- validate_skill.py
|-- tests/
|   `-- test_skill_contract.py
`-- tasks/
    |-- todo.md
    `-- lessons.md
```

Cada responsabilidade fica no módulo `skills/site-seo-release`. Arquivos na raiz existem apenas para descoberta multiplataforma, licença e atribuição.

## 4. Modos da skill

### 4.1 Construção

Ativa durante a criação ou alteração de um site, página ou landing page. Define requisitos antes da implementação:

- intenção de busca e palavra-chave principal por página;
- título, descrição, URL canônica, cabeçalhos e conteúdo de resposta;
- arquivos públicos de descoberta;
- favicon e metadados sociais;
- imagens e desempenho;
- formulários e estados de interação;
- privacidade e consentimento;
- página 404 e rotas inválidas;
- configuração de autenticação de e-mail quando o domínio envia mensagens;
- crédito de produção exigido pelo projeto.

### 4.2 Revisão final

Ativa obrigatoriamente quando o usuário disser que o projeto está pronto, pedir revisão, QA, fechamento, lançamento, publicação ou deploy. A revisão deve:

1. identificar o framework, a saída de build e a URL de produção, quando disponível;
2. mapear páginas indexáveis e a intenção de cada uma;
3. executar verificações locais e remotas adequadas;
4. classificar cada item como aprovado, pendente, bloqueado ou não aplicável;
5. produzir o relatório de fechamento;
6. impedir a afirmação de que o projeto está pronto quando houver falhas críticas abertas.

## 5. Cobertura funcional

### 5.1 Descoberta e indexação

- `robots.txt` na raiz pública, sintaxe válida, sem bloqueio acidental de páginas ou recursos necessários.
- referência ao sitemap por URL absoluta quando aplicável.
- `sitemap.xml` ou índice de sitemaps com URLs canônicas, indexáveis e bem formadas.
- exclusão de páginas 404, redirecionadas, privadas, duplicadas ou com `noindex`.
- canonical consistente, HTTPS e hostname final.
- `llms.txt` enxuto, factual, sem segredos, com links canônicos relevantes.

### 5.2 SEO por página

- um título único, claro e coerente com o conteúdo visível;
- uma meta description específica e orientada ao clique, sem promessas falsas;
- um título principal claro e hierarquia de subtítulos coerente;
- palavra-chave principal e variações semânticas usadas naturalmente;
- conteúdo que responde perguntas reais cedo e conduz à próxima ação;
- links internos descritivos;
- metadados Open Graph e sociais quando a página será compartilhada;
- dados estruturados somente quando representam conteúdo visível e um tipo atual.

### 5.3 Conversão e formulários

- proposta de valor, prova, chamada para ação e redução de objeções;
- perguntas respondidas com estrutura direta: resposta, contexto, prova e ação;
- labels, mensagens de erro, foco, teclado e contraste;
- validação no cliente e no servidor;
- estado de carregamento, sucesso, falha, repetição e prevenção de envio duplicado;
- destino real do lead ou mensagem verificado sem expor dados pessoais;
- proteção contra spam adequada ao risco;
- política e consentimento próximos ao ponto de coleta quando necessários.

### 5.4 Experiência e operação

- favicon quadrado, rastreável e estável;
- imagens em formato e tamanho adequados, dimensões reservadas, `alt` contextual, carregamento responsivo e lazy load fora da primeira dobra;
- página 404 útil que retorna status HTTP 404;
- links, navegação, responsividade e estados vazios;
- segurança básica de cabeçalhos e ausência de segredos no cliente;
- crédito de produção no local equivalente ao rodapé.

### 5.5 Privacidade e e-mail

- aviso ou política de privacidade coerente com a coleta real;
- finalidade, categorias de dados, compartilhamentos, retenção, direitos e canal de contato;
- cookies não necessários desativados antes do consentimento quando a base aplicável exigir;
- SPF com apenas um registro válido e dentro dos limites de consulta;
- DKIM publicado e assinatura observável em mensagem de teste;
- DMARC alinhado a SPF ou DKIM, com política e relatórios definidos de forma segura;
- mudanças DNS sempre ficam pendentes até propagação e verificação pública.

## 6. Contrato do relatório

O relatório final terá:

- contexto do projeto e escopo revisado;
- resumo executivo;
- decisão de liberação: pronto, pronto com ressalvas ou não pronto;
- tabela de verificações com status e evidência;
- pendências ordenadas por criticidade e dependência;
- itens que exigem ação humana, DNS, credencial, conteúdo ou revisão jurídica;
- comandos ou passos de reteste;
- data, ambiente e limitações da auditoria.

Criticidades:

- crítica: impede indexação, conversão principal, privacidade essencial ou funcionamento;
- alta: risco relevante de busca, entrega ou confiança;
- média: perda provável de qualidade ou oportunidade;
- baixa: melhoria sem bloqueio de lançamento.

## 7. Compatibilidade

### Claude Code

- `CLAUDE.md` aponta para `skills/site-seo-release/SKILL.md`.
- O frontmatter usa somente campos portáveis.
- Ferramentas são descritas por capacidade, não por nomes exclusivos quando houver alternativa.

### OpenAI Codex

- `AGENTS.md` exige a skill na criação e no fechamento de sites.
- `agents/openai.yaml` fornece nome, descrição curta e prompt inicial.
- As instruções deixam explícita a prioridade da solicitação do usuário e os limites de autorização.

## 8. Validação

### Validação estática

- frontmatter válido e nome da pasta consistente;
- nenhuma referência quebrada;
- ausência de placeholders;
- ausência de travessão e hífen longo em toda copy criada;
- presença do crédito obrigatório nas instruções de entrega;
- cobertura de todos os tópicos solicitados.

### Validação comportamental

Executar cenários representativos:

1. criação de landing page local sem domínio configurado;
2. revisão final de site com build local e sem URL pública;
3. revisão de site em produção com formulário;
4. domínio com envio de e-mail, mas sem DMARC;
5. site com `robots.txt` que bloqueia a raiz;
6. página inexistente que responde 200 e exibe erro;
7. solicitação que dispensa SEO explicitamente, para confirmar prioridade da instrução do usuário.

## 9. Critérios de aceite

- descoberta clara em Claude Code e Codex;
- todos os arquivos e verificações solicitados estão cobertos;
- relatório sempre separa evidência de inferência;
- pendências nunca são ocultadas;
- falhas críticas impedem a classificação de pronto;
- referências técnicas apontam para fontes oficiais ou para a especificação identificada como proposta;
- licença e atribuição da base MIT estão preservadas;
- testes automatizados passam e a validação manual não encontra conflitos.

## 10. Limites desta entrega

- O repositório remoto será configurado localmente, mas não haverá commit ou push sem instrução explícita.
- A skill não será instalada globalmente nesta etapa. O repositório ficará pronto para instalação ou distribuição posterior.
- Nenhuma alteração DNS ou publicação em produção será realizada durante a construção da skill.
