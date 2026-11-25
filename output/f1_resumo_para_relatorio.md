# Frente 1 — Formação: extensão vs. disciplinas (resumo para o relatório)

Texto pronto para a Seção 4, pensado para cerca de 6 páginas. Os números vêm do notebook `notebooks/01_Formacao_Extensao_vs_Poli.ipynb`. As figuras estão em `output/figures/` e as tabelas em `output/tables/`, todas com o prefixo `f1_`.

## Sugestão de montagem (~6 páginas)

| Página | Conteúdo | Figura / tabela |
|---|---|---|
| 1 | Introdução da frente + P1 | `f1_fig01`, números da `f1_tab02` no texto |
| 2 | P2+P3: associação e ANOVA de 2 fatores | `f1_tab05` (pode ficar só a parte do ganho líquido) + `f1_fig02` |
| 3 | P2+P3: Scheffé + P4 | `f1_tab06` (linhas do ganho líquido) + `f1_fig03` + `f1_tab07` |
| 4 | P6 | `f1_fig04` + `f1_tab10` (pode ficar só o contraste-resumo e os pares) |
| 5 | Regressão | `f1_tab11` + `f1_tab12` + `f1_fig06` |
| 6 | Perfis + síntese + limitações | `f1_tab13` |
| Apêndice | Tabela de contingência, qui-quadrado, ANOVA da P4, resíduos | `f1_tab03`, `f1_tab04`, `f1_tab08`, `f1_fig05` |

---

## 4.1 Frente 1 — Formação: extensão vs. disciplinas

**Objetivo.** Avaliar o valor formativo que os alunos percebem na extensão, comparado às disciplinas obrigatórias, e como o perfil do grupo e a dedicação se associam a essa percepção.

**Base.** 187 alunos da Poli, todos participantes de grupos de extensão. Usamos α = 5%, e as escalas de 1 a 5 foram tratadas como numéricas.

- **Ganho líquido:** nota de preparo na extensão menos nota de preparo nas disciplinas.
- **Categorias de grupo:**
  - **Consultoria & Negócios:** Poli Júnior, GNP, Consulting Club e Liga de Empreendedorismo;
  - **Engenharia:** Thunder Ratz e Poli Racing;
  - **Mercado Financeiro:** Quant, Real State e Finance.
- **Agrupamento:** a Liga de Empreendedorismo (n = 8) foi somada à categoria Consultoria & Negócios, para atender às condições do teste qui-quadrado.

### P1 — A extensão prepara mais do que as disciplinas?

- **Hipóteses:** $H_0: \mu_d = 0$ contra $H_1: \mu_d > 0$, com $d$ = preparo na extensão − preparo nas disciplinas.
- **Teste:** t pareado, porque as duas notas vêm do mesmo aluno. A normalidade da média das diferenças vale pelo TCL, com n = 187.

**Resultado.**

- t(186) = 26,6, p < 0,001.
- Diferença média de **2,27 pontos** (IC 95%: 2,10 a 2,44).
- d de Cohen = 1,95 (efeito muito grande).
- 93% dão nota maior à extensão e só 1 aluno dá nota maior às disciplinas (Figura f1_fig01).

**Conclusão.** Os participantes de grupos de extensão percebem um preparo profissional muito maior na extensão do que nas disciplinas obrigatórias, e de forma quase unânime. Como todos os respondentes são de extensão, o resultado mede a percepção relativa desses alunos, e não um efeito causal da participação.

### P2 + P3 — As diferenças vêm da área do curso ou da categoria do grupo?

**Etapa 1: associação.** Um teste qui-quadrado mostra que a categoria do grupo e a grande área do curso são fortemente associadas: χ²(8) = 69,3, p < 0,001, V de Cramér = 0,43. A condição do teste foi atendida (7% das caselas com esperado abaixo de 5). Os grupos técnicos não têm alunos de Civil & Ambiental nem de Produção, e reúnem 25 dos 41 alunos de Mecânica, Mecatrônica & Naval.

**Etapa 2: ANOVA de 2 fatores** (categoria + área, sem interação, porque há combinações vazias), com F parcial para cada fator (Tabela f1_tab05).

- **Ganho líquido:**
  - a área é significativa sozinha (p = 0,038), mas deixa de ser controlada a categoria (F(4; 180) = 1,99; p = 0,098);
  - a categoria continua significativa controlada a área (F(2; 180) = 10,25; p < 0,001; η² parcial = 0,10).
- **Preparo nas disciplinas:** o padrão se repete (categoria p < 0,001; área p = 0,065).
- **Preparo na extensão:** nenhum fator é significativo (p = 0,24 e 0,32).
- **Premissa:** o teste de Bartlett não rejeita a homogeneidade das variâncias.

**Etapa 3: contrastes de Scheffé** sobre as médias de cada categoria (Tabela f1_tab06).

- **Ganho líquido:** Consultoria & Negócios supera Engenharia em 0,94 ponto (IC de Scheffé: 0,46 a 1,43).
- **Disciplinas:** os grupos técnicos dão nota maior que Consultoria (+0,81; IC 0,41 a 1,20) e que Mercado Financeiro (+0,57; IC 0,06 a 1,07).

**Conclusão.** As diferenças de ganho entre cursos parecem refletir, em boa parte, a composição dos grupos de extensão. Controlada a categoria, a área deixa de ser significativa (p = 0,10), mas os dois fatores se sobrepõem tanto que os dados não separam totalmente os efeitos. Os membros de grupos técnicos têm ganho cerca de 0,9 ponto menor que os de Consultoria & Negócios. Não há evidência de que valorizem menos a extensão (p = 0,24); a diferença está na avaliação das disciplinas, maior entre eles (2,89 contra 2,08) (Figura f1_fig02).

### P4 — Intensidade (horas semanais) ou tempo de casa?

**Variável analisada.** Como 64% dos alunos deram nota 5 à extensão (efeito teto), testamos quem dá a nota máxima, com o qui-quadrado de associação (Tabela f1_tab07).

**Resultado.**

- **Horas semanais:** associação significativa. χ²(4) = 26,15, p < 0,001, V de Cramér = 0,37 (moderada).
  - A proporção de nota 5 sobe de 38% (1–5 h) para 85% (mais de 20 h) (Figura f1_fig03).
- **Tempo no grupo:** não significativo. χ²(3) = 7,37, p = 0,061.
- **ANOVA de 2 fatores (confirmação):**
  - horas continuam significativas controlando o tempo (F(4; 179) = 7,79; p < 0,001);
  - tempo não é significativo controlando as horas (p = 0,062).
  - Ressalva: o teste de Bartlett indica variâncias desiguais, efeito do próprio teto. Por isso, a ANOVA serve só como confirmação.

**Conclusão.** O que se associa à percepção de preparo na extensão é a intensidade da dedicação. Entre quem dedica mais de 20 h por semana, 85% dão nota máxima, contra 38% de quem dedica até 5 h. Não encontramos evidência de associação com o tempo de permanência no grupo. Os dados não dizem a direção causal: mais horas podem gerar mais aprendizado, ou quem percebe mais retorno pode dedicar mais tempo.

### P6 — O objetivo atual se associa à importância dada à média?

**Teste.** ANOVA de 1 fator com n = 180 (7 objetivos não agrupáveis foram excluídos), teste de Bartlett e contrastes de Scheffé.

**Resultado.**

- **ANOVA:** F(4; 175) = 15,82, p < 0,001, η² = 0,27. O objetivo explica 27% da variação. Bartlett: p = 0,44.
- **Médias** (Figura f1_fig04):
  - Grupo de extensão 2,52 e Estágio 2,60;
  - Desempenho acadêmico 3,48, Iniciação científica 3,83 (n = 6) e Intercâmbio 3,91.
- **Scheffé** (Tabela f1_tab10):
  - todos os 6 pares entre esses dois blocos diferem (p ≤ 0,048), e nenhum dos 4 pares dentro de um mesmo bloco difere (p ≥ 0,61);
  - a média simples do primeiro bloco supera a do segundo em 1,18 ponto (IC: 0,64 a 1,72).

**Conclusão.** O objetivo atual se associa fortemente à importância dada à média ponderada. Quem mira intercâmbio, iniciação científica ou desempenho acadêmico atribui, em média, cerca de 1,2 ponto a mais de importância à média do que quem foca no grupo de extensão ou no estágio. Isso é coerente com seleções de intercâmbio e de iniciação científica que usam a média como critério. A alta importância no grupo "Desempenho acadêmico" é esperada, porque o próprio objetivo fala da média.

### Modelo explicativo — regressão linear múltipla do ganho líquido

**Objetivo.** Juntar os fatores num só modelo para estimar a associação de cada um com o ganho, mantidos os demais constantes, e comparar perfis definidos a priori. O foco é explicativo, não preditivo.

**Modelo completo, com base teórica.** Cinco variáveis candidatas:

- categoria do grupo;
- grande área do curso;
- horas semanais, em logaritmo, porque o ganho só cresce nas faixas altas e o valor de "Mais de 40h" (70 h) dominaria uma escala linear;
- tempo no grupo;
- tempo de deslocamento (min).

**Eliminação por F parcial** (Tabela f1_tab11), nesta ordem:

1. sai o tempo no grupo (p = 0,50);
2. sai o tempo de deslocamento (p = 0,22);
3. sai a área do curso (p = 0,11);
4. ficam a categoria do grupo e as horas.

**Testes de suficiência:**

- o F parcial conjunto confirma que o modelo reduzido basta: F(8; 175) = 1,43, p = 0,19;
- usar as 5 faixas de horas como fator não melhora o ajuste em relação ao logaritmo: F(3; 180) = 1,49, p = 0,22.

**Modelo final** (Tabela f1_tab12): R² = 0,20, F(3; 183) = 14,9, p < 0,001.

- **ln(horas):** β = 0,40 (IC 95%: 0,22 a 0,59; p < 0,001). **Quem dedica o dobro de horas tem, em média, ganho 0,28 ponto maior.** Cerca de 60% disso vem de mais preparo percebido na extensão (β = +0,24) e 40% de nota menor às disciplinas (β = −0,17).
- **Grupo técnico:** β = −0,67 (IC 95%: −1,06 a −0,29) em relação a Consultoria & Negócios, com as mesmas horas. A diferença está inteiramente nas disciplinas.
  - O valor é menor que o −0,94 da P2+P3 porque os membros de grupos técnicos dedicam menos horas: 44% estão na faixa de 6–10 h, contra 12% em Consultoria.
- **Mercado Financeiro:** não difere de Consultoria (p = 0,52).
- **Premissas:** os resíduos não mostram padrão e são aproximadamente normais (Figura f1_fig05, apêndice).

**Perfis definidos a priori** (Tabela f1_tab13, Figura f1_fig06):

| Perfil | Ganho médio estimado | IC 95% da média |
|---|---|---|
| Consultoria & Negócios, 21–40 h | 2,69 | 2,48 a 2,90 |
| Consultoria & Negócios, 6–10 h | 2,16 | 1,88 a 2,43 |
| Engenharia, 21–40 h | 2,02 | 1,66 a 2,38 |
| Engenharia, 6–10 h | 1,48 | 1,17 a 1,80 |

O intervalo de predição de um aluno individual tem cerca de ±2,1 pontos, bem mais largo que o IC da média. Isso confirma que o modelo compara perfis, como a escolha de grupo e dedicação de um calouro, mas não prevê a resposta de uma pessoa.

**Conclusão.** Das cinco candidatas, o F parcial manteve só a categoria do grupo e as horas semanais. Área do curso, tempo no grupo e tempo de deslocamento não acrescentam informação significativa. Mantida a categoria, quem dedica o dobro de horas tem ganho 0,28 ponto maior. Mantidas as horas, membros de grupos técnicos têm ganho 0,67 ponto menor, por avaliarem melhor as disciplinas. O modelo explica 20% da variação.

### Síntese da frente

1. A extensão é vista como a principal fonte de preparo profissional, de forma quase unânime.
2. As diferenças entre cursos parecem refletir, em boa parte, a composição dos grupos de extensão. Grupos técnicos valorizam mais as disciplinas e, por isso, têm ganho líquido menor.
3. Dentro da extensão, pesa a intensidade (horas semanais); não encontramos associação com o tempo de casa.
4. A importância dada à média se associa ao objetivo atual: é alta para intercâmbio, iniciação científica e desempenho, e baixa para grupo e estágio.

Os testes principais significativos têm p ≤ 0,003. Continuam significativos mesmo com a correção de Bonferroni para os 10 testes principais (limite de 0,005).

### Limitações

- **Sem grupo de comparação:** os resultados são associações entre participantes, não efeitos causais. Há provável viés de seleção e de sobrevivência.
- **Amostra por conveniência,** com a Poli Júnior em 40% das respostas.
- **Autoavaliação de item único:** pode haver viés de desejabilidade social.
- **Efeito teto** na nota de preparo da extensão.
- **Grupos pequenos:** iniciação científica (n = 6) e mais de 2 anos de grupo (n = 10).
- **Desenho transversal.**
