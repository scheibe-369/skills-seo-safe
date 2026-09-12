# Conteúdo, conversão e mídia

## Intenção e metadados

Mapeie intenção, termo principal, variações e CTA por rota em `SEO-SPEC.md`. Identifique a origem do termo: briefing, conteúdo existente ou pesquisa. Não estime volume ou concorrência sem dados. Se duas páginas visarem a mesma consulta, explique a diferença de intenção antes de criar outra página quase idêntica.

Cada página indexável precisa de title descritivo e description própria como padrão de entrega. Verifique unicidade no inventário, idioma e correspondência com a página renderizada. Use preview de resultados para legibilidade. Faixas de caracteres são heurísticas editoriais, não limites oficiais rígidos; títulos e snippets podem ser reescritos pelo buscador.

Use um título principal claro e hierarquia semântica de subtítulos. Não declare que uma quantidade específica de H1 é fator isolado de ranking. Revise links internos, textos âncora e fatos verificáveis. Não invente avaliações, certificações, depoimentos, endereços ou garantias.

## Resposta e conversão

Transforme uma seção explicativa em pergunta e resposta quando isso refletir uma dúvida real do visitante. Dê a resposta principal cedo, acrescente condições e prova verificável, e direcione a um CTA coerente. A pergunta não deve esconder a oferta nem repetir o mesmo termo artificialmente.

Esqueleto sugerido por bloco: subtítulo em forma de pergunta; resposta direta em uma ou duas frases; condições ou exceções; prova verificável (número, prazo, caso ou certificação real); imagem ou foto com legenda quando ela acrescentar contexto; CTA coerente com a pergunta. Na revisão final, o ID `headings-content` confere se as perguntas principais da página seguem essa estrutura.

Imagem e legenda devem ajudar a entender a promessa, processo ou resultado. Para uma seção sobre prazo, prefira explicar etapas e condições reais do prazo. Só use uma foto se ela acrescentar contexto. Registre melhorias de conversão como hipóteses a medir, sem prometer aumento de taxa.

Use schema apenas quando corresponder ao conteúdo visível e a tipos adequados. Confira a documentação atual de rich results antes de prometer elegibilidade. Não use FAQPage indiscriminadamente nem transforme uma FAQ editorial em QAPage sem perguntas e respostas de usuários.

## Imagem social e favicon

Interprete pedidos de “imagem OG” como preview social: `og:title`, `og:description`, `og:url`, `og:type` e `og:image`, com URLs públicas finais, imagem representativa e texto alternativo social quando suportado. Confira formato, recorte e dimensões aceitos pela plataforma pretendida; 1200 por 630 é um ponto de partida comum, não requisito universal. Teste acesso HTTP e visualização, incluindo cache do compartilhador.

Publique favicon quadrado, representativo, estável e referenciado na home. O Google Search aceita apenas BMP, GIF, ICO, PNG, JPEG, PPM e TIFF, nunca SVG: forneça ICO ou PNG quadrado, de preferência acima de 48x48 px, em URL estável referenciada no head da home; SVG fica como complemento para navegadores. Confira acesso ao arquivo, MIME e aparência em tamanho pequeno. Adicione apple-touch-icon ou manifest somente quando fizer sentido ao uso. Não crie um PWA só para cumprir favicon.

## Imagens e desempenho

- Inspecione o original antes de comprimir; preserve o original e registre bytes/dimensões antes e depois.
- Entregue formato e dimensões adequados ao papel da imagem. Priorize WebP/AVIF quando suportados, mantenha SVG vetorial e fallback quando necessário.
- Use `srcset`/`sizes` ou o componente otimizado da stack para imagens responsivas.
- Reserve espaço por dimensões ou aspect-ratio. Revise corte em mobile e desktop.
- Não aplique lazy loading à imagem LCP. Use prioridade alta somente quando a imagem realmente for crítica; lazy loading é adequado às imagens fora da primeira tela.
- Escreva alt informativo e contextual. Imagens decorativas usam `alt=""`; imagem-link precisa de nome acessível que descreva o destino ou ação. Não repetir palavras-chave por obrigação.
- Não remova indiscriminadamente metadados de autoria ou direitos durante a compressão.
- Ferramentas portáteis para comprimir e redimensionar: `cwebp`, `sharp`, Pillow ou o otimizador da própria stack; registre a ferramenta e os parâmetros usados.

Meça LCP, INP e CLS quando houver dados de campo. Os limiares de referência são LCP até 2,5 s, INP até 200 ms e CLS até 0,1 no percentil 75, separando mobile/desktop. Sem tráfego suficiente, registre ausência de campo e apresente resultados de laboratório com suas limitações. Uma nota Lighthouse não comprova INP real nem é garantia de ranking.

