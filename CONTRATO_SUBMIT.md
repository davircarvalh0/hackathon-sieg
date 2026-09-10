# Contrato do `POST /api/submit`

Endpoint de submissão do resultado. **A SIEG não executa o seu código** — você
roda o Selenium na sua máquina e envia apenas o payload JSON abaixo.

## Requisição

`POST https://talkabit-z3eg.onrender.com/api/submit`
`Content-Type: application/json`

```json
{
  "teamToken": "SEU-TOKEN",
  "itens": [
    { "chave": "00000000000000000000000000000000000000000000", "valor": 1234.56 },
    { "chave": "1111...44 dígitos", "valor": "1.234,56" }
  ]
}
```

- **teamToken** (string, obrigatório): identifica sua equipe. É a sua credencial
  de submissão — **não compartilhe**. No placar você aparece por um *alias*
  (ex.: `Equipe-15VTY`), nunca pelo token.
- **itens** (array, obrigatório): os pares extraídos.
  - **chave**: a chave de acesso (44 dígitos). Pontuação/espacos são ignorados.
  - **valor**: número (`1234.56`) ou string BR (`"1.234,56"`, `"R$ 1.234,56"`).
    O servidor normaliza para centavos.

## Resposta (sucesso)

```json
{
  "accepted": true,
  "alias": "Equipe-15VTY",
  "bestScore": 240,
  "rank": 1,
  "attemptsLeft": 9
}
```

> Não há feedback por item (não dizemos quais você acertou) — de propósito.
> O `/api/submit` não é um oráculo para adivinhar o gabarito.

## Limites e erros

- **400** — payload inválido (faltou `teamToken` ou `itens` não é lista).
- **403** — `teamToken` não reconhecido (confira o token do credenciamento).
- **429** — limite de tentativas atingido (**10 por equipe**) **ou** cooldown
  ativo (**30 s**; `retryAfterSeconds` no corpo). Vale sempre o **melhor score**.

## Pontuação (resumo)

`score = corretos×pontos − incorretos×penalidade − penalidade_de_tempo
         − penalidade_honeypot + bônus_N5 + bônus_N6`

O score **nunca fica negativo**: se as penalidades passarem dos pontos, o placar
mostra `0`. Os pesos exatos ficam com a organização — o que amarra você está no
enunciado (https://talkabit-z3eg.onrender.com/enunciado). O relógio de tempo começa no seu **primeiro
login bem-sucedido** no portal.
