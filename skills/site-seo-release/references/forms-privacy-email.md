# Formulários, privacidade e e-mail

## Formulários

Inventarie formulário, campos, destino, notificações e evento de conversão. Teste com dados sintéticos e destino controlado, considerando a autorização da tarefa para envios reais.

Verifique labels associados, indicação de obrigatoriedade, teclado, foco, erros textuais e anúncio de sucesso. Execute cenários de campo vazio, formato inválido, envio válido, duplo clique, falha do servidor, timeout e nova tentativa. Confirme validação no servidor e controles contra abuso proporcionais ao risco. Não registre PII em URL, evento de analytics, captura pública ou log da auditoria.

Confirme a chegada ao destino esperado por registro ou identificador de teste no CRM, caixa ou backend. HTTP 200 e mensagem visual não bastam. Descreva se houve só teste com mock: uma integração simulada não comprova entrega real. Se o formulário não envia e-mail, os checks DNS da integração podem ser não aplicáveis, com motivo.

## Privacidade e cookies

Compare a política com os dados e fornecedores reais: controlador e contato, finalidade, dados coletados, compartilhamentos, critérios de retenção, direitos e canal de exercício. Não invente CNPJ, encarregado, prazo ou hipótese legal. Se faltarem decisões do controlador, registre pendência e evite publicar texto fictício como política final.

Mantenha link acessível no rodapé e junto à coleta. Não trate checkbox de aceite da política como fundamento universal. Consentimento de marketing, quando usado, é separado, não pré-marcado e revogável. Quando a finalidade depender de consentimento, teste que scripts e cookies correspondentes não carregam antes da escolha, que rejeitar funciona e que a revogação impede novas execuções.

Um site sem formulário pode usar cookies, logs de servidor e serviços externos. A aplicação da política precisa desse inventário. Teste tecnicamente o comportamento e sinalize decisões jurídicas pendentes sem declarar conformidade legal integral. Consulte fontes da ANPD e a legislação vigente para recomendações jurídicas específicas.

## SPF, DKIM e DMARC

São autenticação e entregabilidade, não fatores de SEO. Identifique todos os fluxos de envio, domínio visível em `From`, envelope/Return-Path, provedor e domínio de assinatura. Um site que só abre um link WhatsApp não justifica alteração automática de DNS de e-mail.

SPF: confira um único registro `v=spf1` selecionável no domínio avaliado, todos os remetentes necessários e o limite de dez termos que provoquem consultas, incluindo expansões de `include` e `redirect`. Não publique vários SPF para provedores distintos. Não invente `include` nem substitua um registro sem inventário dos remetentes.

DKIM: obtenha o seletor do provedor ou de uma mensagem real e consulte `seletor._domainkey.dominio`. A RFC 6376 define a chave em registro TXT; quando o provedor pede CNAME, o nome delega para o TXT dele e a resolução precisa chegar a um TXT válido. Não invente seletor ou chave; chave privada nunca é publicada. Confira assinatura e resultado de validação na mensagem recebida. DNS presente sozinho só aprova a observação DNS, não o check completo de envio.

DMARC: consulte `_dmarc.dominio`, verifique política e alinhamento de `From` com SPF ou DKIM autenticado. `p=none` permite observação, mas não comprova aplicação de quarentena/rejeição. Só endureça após inventariar e validar os remetentes. Registre risco remanescente e plano de evolução. Verifique destinos de relatório e sua autorização quando externos; nunca direcione relatórios a uma caixa inventada. Confira a especificação vigente, a RFC 9989, que substitui a RFC 7489 e a RFC 9091.

Prove autenticação com cabeçalhos sanitizados de mensagem de teste (`Authentication-Results`, domínio e seletor). Use o retorno do destinatário confiável, não texto arbitrário do corpo. Registre separadamente SPF, DKIM, DMARC e entrega; um único sucesso não garante entrega futura em todos os provedores. Requisitos de remetentes em massa são condicionais ao volume e uso, não exigência de toda landing page.

Use consulta DNS somente leitura para inspeção (`nslookup -type=txt` no Windows, `dig txt` em Linux e macOS, `Resolve-DnsName` no PowerShell), registrando o comando e o resolvedor. Mudanças necessárias ficam como ações com nome, tipo, valor aprovado, provedor, efeito e reteste. Após alteração autorizada, verifique DNS público e mensagem; não marque como concluído apenas porque um painel aceitou a gravação.

