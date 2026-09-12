# Resultados de validação

Data: 2026-09-11. Ambiente: Windows 11, Python 3.12, repositório `scheibe-369/skills-seo-safe`, branch `main`.

## Validação estática

- `python skills/site-seo-release/scripts/validate_skill.py`: `{"valid": true, "errors": []}`.
- `python -m unittest discover -s skills/site-seo-release/tests`: 43 testes, OK.
- Busca por U+2013 e U+2014 fora de `vendor/`: zero ocorrências.
- CI (`.github/workflows/validate.yml`, matriz Windows, Linux e macOS com Python 3.10 e 3.12): runs `34659266068` e `34659351460` em `success` no GitHub. O run do commit de fechamento é conferido após o push.

## Registro global

- `~/.claude/CLAUDE.md` e `~/.codex/AGENTS.md`: bloco aplicado por `register_global.py --apply`, versão do registro 2, um bloco por arquivo, prévia posterior com `STATUS: unchanged`, backup privado criado ao lado de cada MD.
- Gemini: fora do pedido. `~/.gemini/GEMINI.md` não foi alterado.

## Smoke de ativação real

Sessões novas, sem ferramentas, em diretório temporário fora deste repositório, para testar somente as instruções globais:

| Host | Prompt | Resultado |
| --- | --- | --- |
| Claude Code (`claude -p`) | landing page nova para clínica em Curitiba | ativou `site-seo-release` pelo registro global e planejou `SEO-SPEC.md`, `tasks/site-release.md` e `tasks/site-release.json` |
| Claude Code (`claude -p`) | endpoint interno sem página | declarou explicitamente que não carrega a skill nem `SEO-SPEC.md` |
| Codex CLI 0.154.0 (`codex exec`) | landing page nova para clínica em Curitiba | ativou pela instrução global Site SEO Release, planejou `SEO-SPEC.md`, os relatórios de fechamento e o crédito Method Growth Hub |

O prompt negativo não foi executado no Codex; fica como reteste sugerido.

## Revisão comportamental

`behavior-review.md` simulou sete casos. Os achados 1 a 4 foram aplicados em 2026-09-11; 5 e 6 já estavam cobertos. Um recheque independente pós-edição dos casos `private-campaign` e `global-registration` confirmou as duas ambiguidades resolvidas e pediu dois ajustes de redação, aplicados em `SKILL.md`.

## Agentes paralelos de validação

Três revisores independentes, somente leitura, sobre o estado pós-edição:

- Portabilidade: nenhuma dependência exclusiva do Claude ou do Codex; frontmatter só com `name` e `description`; caminhos do instalador coerentes com `portability.md`. Seis divergências de texto entre gatilhos (bloco global, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `install_skill.py`) foram corrigidas, com o bloco global na versão 2.
- Cobertura do briefing: 21 itens mapeados para arquivo e linha; 20 adequados e 1 fino (bloco pergunta, resposta, prova, imagem e CTA), corrigido com esqueleto em `content-media.md` e critério em `headings-content`. Resíduo de transcrição em `technical-files.md` removido; referência de DMARC alinhada à RFC 9989, verificada no rfc-editor.
- Comportamento: ver a seção anterior.

## Limitações

- Os smokes provam ativação por instrução global em uma resposta de texto; não provam execução completa de construção ou fechamento em um projeto real.
- A instalação por projeto (`install_skill.py`) foi coberta por testes de arquivo, não por sessão real em projeto instalado.
