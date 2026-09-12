# Relatório e critério de liberação

Saídas: `tasks/site-release.json` como registro estruturado e `tasks/site-release.md` como documento legível, ambos relativos ao projeto analisado. Na auditoria somente leitura de um site externo, salve no diretório de relatório autorizado, nunca altere o site auditado.

## Estrutura JSON

Objeto principal:

- `schema_version`: inteiro 1.
- `project`: nome não vazio.
- `environment`: `local`, `preview` ou `production`.
- `audited_at`: ISO 8601 com timezone.
- `scope`: lista não vazia de URLs ou caminhos testados.
- `checks`: registros únicos de todos os IDs em [release-checklist.md](release-checklist.md). Extras são permitidos quando relevantes.

Cada check:

- `id`: ID estável.
- `status`: `pass`, `fail`, `pending`, `blocked` ou `na`.
- `severity`: `critical`, `high`, `medium` ou `low`, segundo impacto contextual.
- `required`: booleano JSON, definido antes da execução pelo contrato do projeto.
- `evidence`: lista de strings; em `pass` deve conter evidência não vazia, com local, método, resultado e data suficientes para repetir.
- `reason`: obrigatório em `pending`, `blocked` e `na`.
- `action`: obrigatório em `fail`, `pending` e `blocked`, com correção e reteste.
- `verified_at`: obrigatório em `pass`, ISO 8601 com timezone, data da verificação que sustenta a evidência.
- Recomendados: `location`, `expected`, `owner`, `dependencies` e `limitations`.

`pass` significa teste executado com resultado aceitável. `fail` significa falha observada. `pending` significa trabalho/teste ainda não realizado. `blocked` significa impedimento identificado. `na` significa fora do escopo por motivo demonstrável, não algo que faltou verificar.

Evidências devem ser sanitizadas: nunca inclua tokens, registros completos de lead, e-mail privado ou cópia de arquivos globais. Link local para log sanitizado, comando e trecho do resultado são suficientes. Evidência de uma versão anterior precisa ser revalidada se a mudança afetou seu objeto. No modo incremental, compare o `verified_at` de cada check com a data da mudança para decidir o que revalidar.

## Decisão determinística

- `NOT_READY`: qualquer item aberto (`fail`, `pending`, `blocked`) obrigatório, ou qualquer item aberto de severidade critical/high.
- `READY_WITH_RESERVATIONS`: só restam itens abertos não obrigatórios de severidade medium/low.
- `READY`: nenhum item aberto relevante ao critério acima.

Itens `na` precisam de justificativa e revisão humana da aplicabilidade. O script valida consistência, não a veracidade das evidências, a legitimidade de uma dispensa ou a cobertura real das URLs. Não altere required, severity ou status para obter aprovação artificial. Em produção, `production-verification` não pode ser dispensado num lançamento público solicitado. Em `local` e `preview`, `production-verification` fica `pending`, nunca `na` nem `pass`; o validador rejeita essas combinações e também `na` em produção.

## Rodar o validador

Resolva `scripts/release_gate.py` a partir da pasta desta skill, não da raiz presumida do site. No repositório de desenvolvimento:

```text
python skills/site-seo-release/scripts/release_gate.py tasks/site-release.json
python skills/site-seo-release/scripts/release_gate.py tasks/site-release.json --markdown
```

O segundo comando imprime uma base Markdown para o agente salvar pelo mecanismo de edição disponível. Exit 0: READY ou READY_WITH_RESERVATIONS. Exit 1: NOT_READY. Exit 2: relatório inválido ou erro de leitura. Sem Python, aplique o mesmo contrato manualmente e registre que o validador não foi executado.

## Conteúdo do MD

Inclua projeto, data, ambiente, escopo, decisão, resumo das evidências, tabela completa e pendências em ordem de dependência e impacto. Para cada pendência informe ID, local, ação, responsável sugerido (sem atribuir pessoa desconhecida como confirmada), bloqueio e como retestar. Destaque ações externas: domínio, DNS, credenciais, conteúdo e decisão jurídica. Liste limitações de ferramentas, amostragem e o que não foi observado em produção.

Separe “pronto no escopo local” de “lançamento confirmado”. Nunca use a saída do validador como prova de deploy realizado. A revisão deve registrar fatos mesmo quando o usuário aceitar publicar com pendências.

