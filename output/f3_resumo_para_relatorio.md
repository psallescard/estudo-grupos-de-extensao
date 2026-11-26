# Frente 3 — Carreira: trajetória e objetivos (resumo para o relatório)

Texto pronto para a Seção 4, pensado para cerca de 6 páginas. Os números vêm do notebook `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb`. As figuras estão em `output/figures/` e as tabelas em `output/tables/`, todas com o prefixo `f3_`.

## Sugestão de montagem (~6 páginas)

| Página | Conteúdo | Figura / tabela |
|---|---|---|
| 1 | Introdução da frente + descritiva + P1a | `f3_fig01` + `f3_fig02`, números da `f3_tab05` no texto |
| 2 | P1b + P2 | `f3_fig03` + `f3_fig04` |
| 3 | P3 + P4 | `f3_fig05` + `f3_fig06` |
| 4 | P6 | `f3_fig07` + `f3_tab18` (pode ficar só o contraste a priori e o par mais próximo) |
| 5 | Modelo explicativo (P7) | `f3_tab20` + `f3_tab21` + `f3_fig08` |
| 6 | Síntese + limitações | `f3_tab02` (agrupamentos) |
| Apêndice | Descritiva, tabelas de contingência, testes, resíduos, médias e cenários | `f3_tab01`, `f3_tab03`, `f3_tab04`, `f3_tab06` a `f3_tab17`, `f3_tab19`, `f3_tab22`, `f3_fig09` |

---

## 4.3 Frente 3 — Carreira: trajetória e objetivos

**Objetivo.** Avaliar como a vivência no grupo de extensão se conecta ao horizonte profissional de curto prazo (estágio e objetivo atual) e de médio prazo (área pretendida após a formatura).

**Base.** 187 alunos da Poli, todos participantes de grupos de extensão. Usamos α = 5%. A amostra é jovem: 31 alunos no 1º ano, 93 no 2º e 63 no 3º ano ou depois (só 9 no 4º ou 5º). Por isso, o momento do 1º estágio mede **intenção**, não um fato.

- **Área pretendida:** Mercado Financeiro é a mais citada (49 alunos; 26%), seguida de Indústria/Engenharia (42; 22%) e Consultoria (33; 18%); 20 alunos (11%) estão indefinidos (Figura f3_fig01).
- **Estágio:** 82 de 186 respondentes (44%) pretendem fazer o 1º estágio até o 3º ano.
- **Objetivo atual:** "Grupo de extensão" é o mais comum (77 de 180; 43%), à frente de Estágio (48; 27%).

**Agrupamentos** (Tabela f3_tab02). O qui-quadrado só é confiável com no máximo cerca de 20% das caselas com esperado abaixo de 5 (mesmo critério da Frente 1). Para cumpri-lo:

- **Categoria do grupo:** Empreendedorismo (n = 8) somado a Consultoria & Negócios, como na Frente 1;
- **Área pretendida:** Consultoria + Empreendedorismo nos testes qui-quadrado (com 6 áreas, 28% das caselas da P1a ficam abaixo de 5; com 5, 20%);
- **Objetivo atual:** Desempenho acadêmico + Iniciação científica (n = 6) em "Desempenho & Pesquisa";
- **Ano na Poli:** 3º, 4º e 5º anos somados em "3º ano ou mais";
- **Momento do estágio:** "Até o 3º ano" (antes do 3º ano ou no 3º ano) contra "4º ano ou depois";
- **Exclusões feitas teste a teste:** "Outros" na motivação (n = 7) fica fora da P2; "Indefinido" (n = 20) fica fora da P1b; as 7 respostas sem objetivo ficam fora dos testes com objetivo; a única resposta "Não pretendo realizar estágio" fica fora da P3 e da P7.

### P1 — A área pretendida está associada ao grupo de extensão e ao curso?

**Hipóteses.** Dois testes qui-quadrado de associação. P1a: $H_0$: a área pretendida é independente da categoria do grupo. P1b: $H_0$: a área pretendida é independente da grande área do curso (sem os 20 "Indefinido").

> V de Cramér: $V = \sqrt{\chi^2 / (n \cdot k)}$, com $k$ = min(linhas, colunas) − 1. As referências de Cohen dependem do $k$: para $k = 2$, 0,07 fraca, 0,21 moderada e 0,35 forte; para $k = 3$, 0,06, 0,17 e 0,29.

**Resultado** (Tabela f3_tab05).

- **P1a (n = 187):** χ²(8) = 95,0, p < 0,001, V de Cramér = 0,50 (forte). Condição atendida no limite (20% das caselas com esperado abaixo de 5). Pelos resíduos ajustados (|r| > 2):
  - grupos de Mercado Financeiro: 64,7% miram Mercado Financeiro (r = 5,64);
  - Consultoria & Negócios: 39,8% miram Consultoria & Empreendedorismo (r = 4,28);
  - Engenharia: 60,0% miram Indústria/Engenharia (r = 6,92) e nenhum mira Mercado Financeiro (r = −4,59) (Figura f3_fig02).
- **P1b (n = 167):** χ²(12) = 60,4, p < 0,001, V de Cramér = 0,35 (forte). Condição atendida (10%). Destaques:
  - Mecânica, Mecatrônica & Naval: 56,4% miram Indústria/Engenharia (r = 5,14);
  - Elétrica & Computação: 35,7% miram Tecnologia (r = 4,56);
  - Produção: 52,0% miram Mercado Financeiro (r = 2,70) e nenhum mira Indústria/Engenharia (r = −3,14) (Figura f3_fig03).

**Conclusão.** A área pretendida está fortemente associada tanto à categoria do grupo quanto à grande área do curso. Há possível autosseleção: o aluno pode ter escolhido o grupo pela área que já mirava, então a associação não mostra que o grupo molda a área pretendida. Como grupo e curso se sobrepõem, os dois testes não separam os dois efeitos.

### P2 — A motivação para entrar no grupo se reflete na área pretendida?

**Hipóteses.** $H_0$: a área pretendida é independente da motivação de ingresso. Qui-quadrado sem a linha "Outros" (com ela, 40% das caselas ficam abaixo de 5; sem ela, 20%), n = 180.

**Resultado.** χ²(12) = 22,2, p = 0,035, V de Cramér = 0,20, entre as referências moderada (0,17) e forte (0,29) para $k = 3$. Condição atendida no limite (20%). As caselas com |r| > 2 estão todas em Mercado Financeiro (Figura f3_fig04):

- aprendizado técnico (hardskills): 42,6% miram Mercado Financeiro (r = 2,99);
- experiência prática em projetos reais: só 13,0% (r = −2,34);
- desenvolvimento pessoal, comunicação e liderança: só 12,5% (r = −2,22).

**Conclusão.** Há associação significativa e moderada entre a motivação de ingresso e a área pretendida, mas o p-valor fica perto do limite de 5%, então o resultado deve ser lido com cautela. A diferença está em Mercado Financeiro: quem entrou por aprendizado técnico mira essa área com mais frequência (43%) do que quem entrou por experiência prática ou por desenvolvimento pessoal (13%).

### P3 — Alunos de alguma categoria de grupo pretendem antecipar o 1º estágio?

**Hipóteses.** $H_0$: pretender o 1º estágio até o 3º ano é independente da categoria do grupo. Qui-quadrado numa tabela 3 × 2, n = 186; nenhuma casela com esperado abaixo de 5.

**Resultado.** χ²(2) = 3,79, p = 0,15, V de Cramér = 0,14. Não se rejeita $H_0$. Pretendem estagiar até o 3º ano (Figura f3_fig05):

- Consultoria & Negócios: 50,0% (54 de 108);
- Mercado Financeiro: 38,2% (13 de 34);
- Engenharia: 34,1% (15 de 44).

**Conclusão.** Não há evidência de associação entre a categoria do grupo e a intenção de fazer o 1º estágio até o 3º ano. As diferenças entre 34% e 50% são apenas descritivas e podem ser acaso amostral. O resultado fala de intenção, não de quem de fato estagiou mais cedo.

### P4 — O objetivo principal muda ao longo da graduação?

**Hipóteses.** $H_0$: o objetivo principal atual é independente do ano na Poli. Qui-quadrado com 4 objetivos × 3 anos, n = 180 (Tabela f3_tab14).

**Resultado.** χ²(6) = 28,0, p < 0,001, V de Cramér = 0,28, entre as referências moderada (0,21) e forte (0,35) para $k = 2$. Condição atendida (8%). Caselas com |r| > 2 (Figura f3_fig06):

- 3º ano ou mais: "Estágio" sobe para 46,0% (r = 4,31) e "Grupo de extensão" cai para 19,0% (r = −4,72);
- 2º ano: "Grupo de extensão" 55,1% (r = 3,29) e "Estágio" só 15,7% (r = −3,28).

Com a coluna `anos_de_poli` antiga (arquivo de 24/11, desalinhada para 30 alunos), o mesmo teste daria χ²(6) = 12,28 e p = 0,056 (calculado fora do notebook); daí a nova geração do arquivo em 25/11.

**Conclusão.** O objetivo principal atual se associa ao ano na Poli, com magnitude moderada a forte. "Grupo de extensão" pesa mais no 1º e no 2º ano (57% e 55%), e "Estágio" passa a ser o objetivo mais citado no 3º ano ou mais (46%, contra 18% no 1º e 16% no 2º). Os dados são de um único momento: é uma comparação entre turmas, não o acompanhamento das mesmas pessoas.

### P6 — Quem mira Mercado Financeiro ou Consultoria valoriza mais a média e tem média maior?

**Hipóteses.** Duas ANOVAs de 1 fator pelas 6 áreas pretendidas: importância da média ponderada (1–5) e média ponderada (ponto médio da faixa). $H_0$: as médias das 6 áreas são iguais. A hipótese do guia vira um contraste definido a priori: média simples de {Mercado Financeiro, Consultoria} menos a média simples das outras 4 áreas, com $H_1$: contraste positivo.

**Resultado** (Tabelas f3_tab16 a f3_tab19, Figura f3_fig07).

- **Importância da média (n = 187):** F(5; 181) = 2,74, p = 0,021, η² = 0,07 (a área está associada a 7% da variação; efeito pequeno a moderado). Bartlett: p = 0,43.
  - Médias: Mercado Financeiro 2,59 (a menor) e Consultoria 2,73; Indústria/Engenharia 3,29 (a maior) e Indefinido 3,25.
  - Contraste a priori: −0,45 ponto (IC de Scheffé: −0,98 a 0,07; p = 0,14), negativo e não significativo.
  - Scheffé nos 15 pares: nenhum difere; o mais próximo é Mercado Financeiro × Indústria/Engenharia (−0,69; p = 0,071).
- **Média ponderada (n = 184):** F(5; 178) = 0,34, p = 0,89, η² = 0,009; médias entre 7,16 e 7,44. Contraste a priori −0,11 (p = 0,99).
- **Checagem ordinal** (3 faixas de média × área): χ²(8) = 8,43, p = 0,39.

**Conclusão.** A área pretendida se associa à importância dada à média, mas no sentido contrário ao da hipótese do guia: quem mira Mercado Financeiro ou Consultoria dá, em média, menos importância à média do que quem mira Indústria/Engenharia. O contraste a priori não é significativo e o Scheffé não aponta nenhum par. A média ponderada em si não difere entre as áreas. A associação é bem menor que a do objetivo atual na Frente 1 (η² = 0,27).

### Modelo explicativo (P7) — o que se associa à intenção de antecipar o 1º estágio?

**Objetivo.** Juntar os fatores num só modelo para estimar a associação de cada um com a intenção de estagiar até o 3º ano, mantidos os demais constantes. O foco é explicativo, não preditivo.

**Modelo.** Regressão linear múltipla com resposta $Y$ = 1 (pretende o 1º estágio até o 3º ano) ou 0, o **modelo de probabilidade linear**: cada β é uma diferença em pontos percentuais. Modelo completo definido a priori, com 6 blocos: categoria do grupo, grande área do curso, ano na Poli, objetivo atual, tempo no grupo e ln(horas semanais). n = 179.

**Efeito mecânico do ano.** Só quem já está no 4º ano ou depois e ainda não estagiou fica impedido de pretender estagiar "até o 3º ano". São 9 alunos no 4º ou 5º ano: 7 responderam "4º ano ou depois" e 2 responderam "No 3º ano" (provavelmente já estagiaram; para os mais velhos, a variável é em parte retrospectiva, não só intenção). Para quem está no 3º ano, "No 3º ano" continua sendo uma resposta possível. A restrição explica, portanto, parte da queda em "3º ano ou mais", mas não a diferença entre o 1º e o 2º ano, que é uma associação entre turmas. O ano entra principalmente como **controle**. Proporção que pretende estagiar até o 3º ano: 75% no 1º ano, 53% no 2º e 14% no 3º ano ou mais.

**Eliminação por F parcial** (Tabela f3_tab20), nesta ordem:

1. sai o objetivo atual (p = 0,283);
2. sai o tempo no grupo (p = 0,179);
3. sai a categoria do grupo (p = 0,089);
4. saem as horas semanais (p = 0,051);
5. ficam a grande área do curso (F(4; 172) = 3,42; p = 0,010) e o ano na Poli.

**F parcial conjunto** (completo contra final): F(9; 163) = 1,98, p = 0,045. Os blocos retirados, em conjunto, acrescentam algo ao modelo final, e o R² ajustado cai de 0,275 para 0,238. A exclusão de categoria e horas é, portanto, limítrofe.

**Modelo final** (Tabela f3_tab21): R² = 0,264 (ajustado 0,238), F(6; 172) = 10,28, p < 0,001.

- 2º ano vs. 1º ano: −26 pontos (IC 95%: −46 a −7; p = 0,007);
- 3º ano ou mais vs. 1º ano: −62 pontos (IC 95%: −82 a −43; p < 0,001);
- Mecânica, Mecatrônica & Naval vs. Civil & Ambiental: −23 pontos (IC 95%: −43 a −4; p = 0,018);
- Elétrica & Computação (+4; p = 0,63), Produção (+14; p = 0,21) e Outras Engenharias (−2; p = 0,90) não se distinguem significativamente de Civil & Ambiental.

**Perfis definidos a priori** (Tabela f3_tab22, Figura f3_fig08): os 15 perfis (ano × grande área) vão de −6% (3º ano ou mais, Mecânica, Mecatrônica & Naval) a 93% (1º ano, Produção). Uma estimativa sai de 0–100% e os intervalos de predição individuais saem do intervalo em todos os perfis: o modelo compara perfis, mas não prevê pessoas. Os resíduos formam duas faixas, como esperado para $Y$ 0/1 (Figura f3_fig09, apêndice).

**Conclusão.** Dado o ano na Poli, a grande área do curso é o único bloco, além do ano, mantido pelo critério de eliminação: alunos de Mecânica, Mecatrônica & Naval têm, em média, 23 pontos percentuais a menos de probabilidade de pretender estagiar até o 3º ano que os de Civil & Ambiental. A exclusão da categoria do grupo (p = 0,089, coerente com a P3) e das horas (p = 0,051) é limítrofe, pois o F conjunto rejeita por pouco (p = 0,045). O ano entra sobretudo como controle: a restrição mecânica explica parte da queda no 3º ano ou mais (−62 pontos), mas não a do 1º para o 2º ano (−26 pontos), que é uma associação entre turmas. O modelo explica 26% da variação, e os resultados são associações aproximadas.

### Síntese da frente

1. A área pretendida está fortemente associada à categoria do grupo (V = 0,50) e à grande área do curso (V = 0,35): 65% dos alunos de grupos de Mercado Financeiro miram Mercado Financeiro e 60% dos de Engenharia miram Indústria/Engenharia.
2. A motivação de ingresso se associa de forma moderada à área pretendida (p = 0,035), sobretudo em Mercado Financeiro: 43% de quem entrou por aprendizado técnico miram essa área, contra 13% nas motivações de experiência prática e desenvolvimento pessoal.
3. Não há evidência de que a categoria do grupo se associe à intenção de estagiar até o 3º ano (p = 0,15; 50%, 38% e 34%).
4. O objetivo atual se associa ao ano (p < 0,001; V = 0,28): "Estágio" passa de 16–18% no 1º e 2º ano para 46% no 3º ano ou mais.
5. Quem mira Mercado Financeiro ou Consultoria dá menos importância à média (2,59 e 2,73 contra 3,29 em Indústria/Engenharia; ANOVA p = 0,021), o contrário da hipótese do guia; a média em si não difere entre as áreas (p = 0,89).
6. No modelo explicativo, dado o ano, só a grande área do curso se mantém (p = 0,010; Mecânica −23 pontos); categoria e horas saem no limite (F conjunto p = 0,045).

### Limitações

- **Sem grupo de controle:** os resultados são associações entre participantes de extensão, não efeitos causais. Há possível autosseleção (o aluno pode escolher o grupo pela área que já mira).
- **Grupo e curso se sobrepõem** (Frente 1: χ²(8) = 69,3; V = 0,43), então os dois testes da P1 não separam o efeito do grupo do efeito do curso.
- **Momento do estágio = intenção:** a maioria ainda está no 1º ou 2º ano.
- **Comparação entre turmas, não acompanhamento:** o desenho é transversal (P4 e efeito do ano na P7).
- **Agrupamentos feitos para cumprir o critério do qui-quadrado;** a P1a e a P2 ficam exatamente no limite de 20%.
- **Modelo de probabilidade linear:** variância não constante, resíduos não normais e uma previsão fora de 0–100%. A regressão logística está fora dos métodos da disciplina.
- **Média ponderada aproximada pelo ponto médio das faixas** (checada na versão ordinal).
- **n pequeno** em Mercado Financeiro como categoria de grupo (34 alunos) e em Indefinido como área pretendida (20).
