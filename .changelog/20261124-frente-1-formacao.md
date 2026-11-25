# 20261124 - Frente 1: Formação (Extensão vs. Poli)

## Objetivo

Registrar a análise da Frente 1 do guia de divisão analítica (PRO3201, Grupo 10): o valor formativo percebido da extensão frente às disciplinas obrigatórias e como o perfil do grupo e a dedicação moldam esse preparo. A análise está em `notebooks/01_Formacao_Extensao_vs_Poli.ipynb`.

## Arquivos criados

- `notebooks/01_Formacao_Extensao_vs_Poli.ipynb`: diagnóstico descritivo, testes P1–P6, modelos P7–P8, correção de Holm, síntese e limitações. Cada pergunta segue o bloco (a)–(e) do guia.
- `src/inference.py`: funções reutilizáveis.
  - comparação pareada (Wilcoxon, teste do sinal e t pareado, com rank-bisserial e d_z);
  - Kruskal-Wallis com ε², ANOVA de Welch com ω², teste de Dunn com correção de empates;
  - ajuste de Holm/BH;
  - τ-b de Kendall com IC bootstrap, médias por grupo com IC bootstrap, intervalo de Wilson;
  - qui-quadrado com p de Monte Carlo;
  - logit ordinal com checagem de convergência e teste da razão de verossimilhança;
  - validação cruzada K-fold estratificada repetida e AUC.
- `src/plotting/plots_formacao.py`: figuras da frente, com rótulos em PT-BR.
- `output/tables/frente1/*.csv`: tabelas de resultados.
- `output/figures/frente1/*.png`: figuras 01 a 11. A pasta é ignorada pelo Git (`figures/` no `.gitignore`), mas as figuras também ficam embutidas no notebook.

O ambiente não ganhou dependência nova. A validação cruzada e a AUC foram implementadas em `src/inference.py` justamente para não exigir o scikit-learn, que não está no `pyproject.toml`.

## Decisões metodológicas

- **Testes primários não paramétricos** (Wilcoxon, Kruskal-Wallis, τ-b de Kendall) e modelos logísticos/ordinais, porque as variáveis principais são escalas Likert de item único. t pareado, Welch e MQO entram como robustez.
- **Efeito teto em `preparo_extensao`** (63,6% de notas 5; nenhuma nota 1 ou 2): os modelos usam também a indicadora `preparo_ext_maximo` (nota 5) e a "saturação" é tratada como indistinguível do teto da escala.
- **`delta_preparo` é dominado pelas disciplinas** (ρ = −0,88): toda diferença de delta foi decomposta em `preparo_extensao` e `preparo_disciplinas`.
- **Confundimento categoria × área × horas**: os grupos de Engenharia não têm alunos de Civil nem de Produção, e Consultoria & Negócios concentra quem declara mais horas. Os controles foram:
  - análise estratificada por área;
  - teste LR no logit ordinal;
  - τ das horas dentro de cada categoria.
- **Comparações múltiplas**: cada pergunta tem teste(s) primário(s); Holm aplicado à família de 11 testes. Post-hocs com Dunn + Holm.
- **Escores ordinais (`horas_ord`, `tempo_ord`)** em vez das colunas `_num`. Para testes de postos o resultado é idêntico, e evita-se a alavancagem da faixa aberta "Mais de 40h" (regra 3 do guia).
- **Bootstrap** com B = 5.000 e semente 42, apenas para ICs.
- **`objetivo_faculdade`**: análise de casos completos (n = 180).

## Resultados principais (testes que sobrevivem a Holm)

- **P1:** extensão > disciplinas. Wilcoxon p = 7 × 10⁻³¹, r_rb ≈ 1; 93% com d > 0; diferença média de 2,27 (IC 2,10–2,44). Vale em todas as áreas e categorias.
- **P3:** o ganho líquido varia por categoria (ε² = 0,12). A diferença acompanha o preparo nas **disciplinas**: Engenharia 2,89 contra Consultoria 2,08, robusto dentro da mesma grande área. No preparo na extensão, a diferença entre categorias não é significativa.
- **P4a/P7a:** as horas semanais se associam ao preparo na extensão (τ-b = 0,32; 85% de nota 5 acima de 20 h contra 38% até 5 h), também dentro de cada categoria.
- **P6:** o objetivo atual se associa à importância da média (ε² = 0,27; intercâmbio/IC/desempenho > grupo/estágio) e o preparo nas disciplinas (ε² = 0,09).
- **P8:** o objetivo domina o modelo ordinal da importância da média (R² de McFadden = 0,14), com previsão individual fraca.

**Não significativos:**

- P2 (área): p = 0,047, que vira 0,19 com Holm e perde significância ao controlar a categoria (p = 0,12);
- P3 com o preparo na extensão;
- P4b (tempo de grupo);
- P5 (importância × preparo na extensão).

## Achados exploratórios (não corrigidos)

- A turma de ingresso se associa à nota máxima de preparo na extensão (80% em 2024, 60% em 2025, 45% em 2026; τ-b = −0,21). Dentro das turmas de 2024 e 2025, o tempo de grupo não se associa de forma consistente à nota. Gancho para a Frente 3.
- A importância da média acompanha o preparo percebido nas disciplinas (τ-b = 0,22), não o da extensão.

## Problemas encontrados nos dados (não corrigidos na origem)

- **`anos_de_poli` está errado em 30 linhas** do `clean_data.parquet` (a partir do índice 143). No `00_Data_Processing.ipynb`, a coluna é calculada com `df_renamed["ano_ingresso"]` (193 linhas, ainda com as 6 linhas de fora da Poli) e atribuída a `df_clean` (187 linhas, índice reiniciado). A correção é usar `df_clean["ano_ingresso"]` e regenerar o parquet. O notebook 01 recalcula a coluna localmente. **Isso afeta as Frentes 2 e 3.**
- Uma resposta tem ingresso em 2026 e "1 a 2 anos" de grupo (índice 49). Foi mantida; removê-la não altera nenhum resultado.

## Revisão

Uma auditoria independente conferiu cada número das conclusões contra as saídas do notebook e as funções de `src/inference.py`. As correções foram incorporadas: OR do modelo correto na P7, redação não causal, "mesma grande área" no lugar de "mesmo curso", IC t para grupos pequenos e números citados agora exibidos em células.

## Pontos de atenção para quem reutilizar

- Não há grupo de não participantes: nenhum resultado é efeito causal da extensão; são percepções entre participantes.
- A Poli Júnior é 40% da amostra e 75% de Consultoria & Negócios.
- Empreendedorismo (n = 8) e IC / Pesquisa (n = 6) têm estimativas instáveis. Na P8, o efeito "significativo" da categoria vem só de Empreendedorismo.
- Para reproduzir: `uv sync` e executar o notebook 01 inteiro, depois do notebook 00. O notebook encontra a raiz do projeto tanto se rodado da raiz quanto de `notebooks/`.
