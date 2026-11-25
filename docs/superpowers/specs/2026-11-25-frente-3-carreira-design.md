# Frente 3: Carreira (Trajetória & Objetivos): design

**Data:** 25/11/2026
**Escopo:** Frente 3 do *Plano de Divisão Analítica* (PRO3201, Grupo 10), em `context/`.
**Objetivo da frente:** mapear como a vivência no grupo de extensão se conecta ao horizonte profissional de curto prazo (estágio e objetivo atual) e de médio prazo (área pós-formatura).

## 1. Restrições herdadas

- **Só métodos da disciplina**, como na Frente 1 (changelog `20261125-frente-1-metodos-da-disciplina.md`):
  - qui-quadrado de associação com V de Cramér;
  - ANOVA de 1 fator com Bartlett, η² e Scheffé;
  - regressão linear múltipla com F parcial.

  Ficam de fora a regressão logística, o bootstrap e a validação cruzada.
- α = 0,05. Cada pergunta é registrada no bloco (a)–(e) do guia: hipóteses, método e premissas, estatística/p/efeito, gráfico ou tabela, conclusão em 3–4 linhas.
- Linguagem associativa, não causal. A amostra tem só participantes de extensão, sem grupo de controle.
- Convenções do README: código em EN-US e texto em PT-BR. O notebook só chama funções de `src/` e explica os métodos em quadros "Conceito".
- **Critério de validade do qui-quadrado:** no máximo cerca de 20% das caselas com frequência esperada abaixo de 5. Os agrupamentos abaixo foram escolhidos para atender esse critério.

## 2. Fatos dos dados que moldam o design (`clean_data.parquet` de 24/11, n = 187)

- **`anos_de_poli` estava desalinhado** no parquet de 24/11, que foi gerado antes do commit 59adcc2: 30 alunos tinham o ano errado. O parquet foi gerado de novo em 25/11 a partir do notebook 00 e agora está correto. Com o valor corrigido, objetivo × ano passa de p = 0,095 para p < 0,001. As outras frentes precisam usar o parquet novo.
- A amostra é jovem: 31 alunos no 1º ano, 93 no 2º e 63 no 3º ano ou depois (já corrigido). **`momento_estagio` mede intenção**, não um fato.
- `momento_estagio`: "Não pretendo realizar estágio" tem n = 1.
- `motivacao_ingresso`: Networking tem n = 6 e Amigos, n = 1.
- `objetivo_faculdade`: 7 respostas ausentes; IC / Pesquisa tem n = 6.
- `categoria_extensao`: Empreendedorismo tem n = 8.

## 3. Arquivos

| Arquivo | Papel |
|---|---|
| `src/carreira.py` (novo) | Constantes (ordens e rótulos), `prepare_front_data`, `check_data_quality`, tabela dos agrupamentos e construção dos cenários da P7 |
| `src/plotting/plots_carreira.py` (novo) | Gráficos da frente (barras empilhadas de 100%, composição por ano, médias com IC, cenários da P7 e resíduos) |
| `src/stats_tests.py` (alterado) | Acrescenta `standardized_residuals(observed)`: resíduos ajustados do qui-quadrado, para mostrar quais caselas puxam a associação |
| `src/regression.py` | Reaproveitado sem mudanças |
| `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb` (novo) | Análise completa, legível sem ler Python |
| `output/tables/f3_tabNN_*.csv`, `output/figures/f3_figNN_*.png` | Artefatos com prefixo `f3_`, numerados na ordem em que aparecem |
| `output/f3_resumo_para_relatorio.md` | Resumo de cerca de 6 páginas, no formato do `f1_resumo_para_relatorio.md` |
| `.changelog/YYYYMMDD-frente-3-carreira.md` (com a data da implementação) | Decisões, resultados e limitações |

## 4. Preparação (`carreira.prepare_front_data`)

As colunas originais não são alteradas. Colunas novas:

| Coluna | Regra |
|---|---|
| `anos_de_poli` (só verificada) | `raise` se for diferente de 2026 − `ano_ingresso` + 1, para não rodar sobre um parquet antigo |
| `ano_poli_grupo` | Valores {"1º ano", "2º ano", "3º ano ou mais"}, ordenado |
| `categoria_grupo` | Empreendedorismo entra em "Consultoria & Negócios". Ordem igual à da Frente 1 |
| `area_grupo` | Consultoria + Empreendedorismo viram "Consultoria & Empreendedorismo" (5 níveis) |
| `estagio_ate_3ano` | 1 = "Antes do 3º ano" ou "No 3º ano"; 0 = "No 4º ano" ou "A partir do 5º ano"; ausente = "Não pretendo" |
| `motivacao_grupo` | Networking + Amigos viram "Outros" (n = 7) |
| `objetivo_grupo` | "Desempenho acadêmico" + "IC / Pesquisa" viram "Desempenho & Pesquisa" |
| `log_horas_semanais` | ln(`horas_semanais_grupo_num`), mesmo critério da Frente 1 |

Exclusões feitas em cada teste, e não na base:
- "Outros" fica fora do qui-quadrado da P2, mas aparece na descritiva;
- "Indefinido" fica fora só da P1b;
- objetivo ausente fica fora dos testes que usam objetivo.

## 5. Análises

**Descritiva** (tab01, fig01): distribuição das variáveis principais e das colunas agrupadas, com n, e uma tabela dos agrupamentos com a justificativa de cada um.

**P1: área pretendida × categoria do grupo e × grande área do curso.**
- H0: não há associação.
- P1a: `area_grupo` × `categoria_grupo`. Valores prévios: 20% de caselas abaixo de 5, χ²(8) ≈ 95, V ≈ 0,50.
- P1b: `area_grupo` × `grande_area_curso`, sem "Indefinido". Valores prévios: 10% de caselas abaixo de 5, χ²(12) ≈ 60, V ≈ 0,35.
- Para cada teste: tabela observada, percentuais em linha, resíduos padronizados e figura de barras empilhadas de 100%.

**P2: motivação × área pretendida.**
- `motivacao_grupo`, sem "Outros", × `area_grupo`.
- Valores prévios: 20% de caselas abaixo de 5, χ²(12) ≈ 22, p ≈ 0,035, V ≈ 0,20.
- Inclui resíduos. O texto destaca que o efeito é fraco.

**P3: categoria × intenção de antecipar o estágio.**
- `categoria_grupo` × `estagio_ate_3ano`, com a proporção de cada categoria.
- Resultado prévio não significativo (p ≈ 0,15). É reportado como ausência de evidência e fala de intenção.

**P4: objetivo × ano na Poli.**
- `objetivo_grupo` × `ano_poli_grupo`.
- Valores prévios: 8% de caselas abaixo de 5, χ²(6) ≈ 28, p < 0,001, V ≈ 0,28.
- Inclui resíduos e uma figura da composição por ano.
- Ressalva: compara turmas diferentes, não acompanha as mesmas pessoas.

**P6: área pretendida × importância da média e × média ponderada.**
- Duas ANOVAs de 1 fator com `area_pretendida` (6 níveis), uma para `importancia_media` e outra para `media_ponderada_num`.
- Cada uma com Bartlett, η² e médias com IC 95%.
- Contraste de Scheffé definido antes dos resultados: {Mercado Financeiro, Consultoria} − {demais}.
- Checagem ordinal: qui-quadrado de `media_ponderada` (faixas, agrupando se necessário) × área.
- O efeito do objetivo na importância da média é citado a partir da Frente 1, P6, sem repetir a análise.
- Os dados prévios contrariam H1: Mercado Financeiro tem 2,59 e Indústria, 3,29.

**P7: modelo explicativo da intenção de antecipar o estágio.**
- Modelo de probabilidade linear: OLS de `estagio_ate_3ano`.
- Modelo completo, com cada bloco testado por F parcial:
  - `categoria_grupo`;
  - `grande_area_curso`;
  - `ano_poli_grupo`;
  - `objetivo_grupo` (o mesmo agrupamento da P4; IC / Pesquisa sozinho, com n = 6, deixaria o coeficiente impreciso);
  - `tempo_grupo`;
  - `log_horas_semanais`.
- Procedimento: eliminação por F parcial com `backward_elimination`, F parcial conjunto entre o modelo completo e o final, tabela de coeficientes e cenários a priori com probabilidade prevista e IC.
- Figuras: cenários e diagnóstico de resíduos.
- Limitações declaradas: previsões podem sair de [0, 1], a variância é heterogênea por construção e β é lido como diferença em pontos percentuais.

**Cortadas:**
- P5: ninguém na amostra está estagiando, então não há como testar.
- P8: prever 6 áreas com n = 187 sem logística não se sustenta.

## 6. Verificação

- `prepare_front_data` checa invariantes com `raise`, como a Frente 1:
  - n = 187;
  - `anos_de_poli` ∈ {1..5} e coerente com `ano_ingresso`;
  - `estagio_ate_3ano` ausente só onde a resposta é "Não pretendo".
- Cada qui-quadrado mostra o "% de caselas com esperado < 5" na própria tabela de resultado.
- O notebook roda do início ao fim (`uv run jupyter nbconvert --execute`) a partir da raiz.
- Os valores prévios desta spec servem de referência: um desvio grande indica erro de preparação.
- Revisão de legibilidade: alguém que não lê Python consegue entender a análise só pelo texto, pelas tabelas e pelos gráficos.
