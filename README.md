# Kit do Participante — Desafio de Automação (Talk a Bit)

Bem-vindo(a)! Este kit tem o mínimo para você começar rápido e focar no que
importa: **automação resiliente com Selenium**.

## Conteúdo

| Arquivo | O que é |
|---------|---------|
| `CONTRATO_SUBMIT.md` | Contrato do `POST /api/submit` (formato do payload) |
| `sample_data.json` | Amostra **ilustrativa** de como os dados aparecem |

> Não há bot de exemplo: a automação, do zero, é o desafio. 😉

## O que você precisa saber

- **Objetivo:** extrair, de **todas as notas «Autorizada»**, a `chave` (44
  dígitos) e o `valor`. Cada equipe tem dados próprios. Atenção: nem toda
  «Autorizada» está na listagem principal — e as que não estão contam igual.
- **Selenium é obrigatório.** Linguagem livre (diferencial C#).
- Você roda na **sua máquina**; a SIEG só valida o payload que você envia.
- O **portal-alvo** tem mecânicas anti-automação (N1..N6) — trate cada uma.
- **Sem ferramentas de IA.** A habilidade do time é o que vale — e os finalistas
  **defendem o código ao vivo** (explicam + fazem uma alteração pedida na hora).

## Credenciais de teste

- **URL:** https://talkabit-z3eg.onrender.com (local: `http://localhost:3000`)
- **Enunciado completo:** https://talkabit-z3eg.onrender.com/enunciado
- **Token da equipe:** entregue no **credenciamento** (é a sua credencial de
  submissão — não compartilhe).
- **Senha do portal:** `talkabit`

## Por onde começar

1. Faça login no portal com o token da equipe e a senha de teste.
2. Navegue até a busca, liste as notas e abra o detalhe de uma «Autorizada».
3. Extraia `chave` + `valor` e envie ao `/api/submit` (veja `CONTRATO_SUBMIT.md`).
4. Automatize tudo isso com Selenium — o portal foi feito para resistir.

## Sobre o desafio

O portal foi construído para resistir a robôs ingênuos. Espere resistência em
várias frentes e em dificuldade crescente — identidade dos elementos, tempo,
estrutura da página, ruído na tela e cantos menos óbvios da navegação. Descobrir
onde estão as pegadinhas e contorná-las com uma automação resiliente é
exatamente o que o desafio mede.

Boa sorte! 🚀
