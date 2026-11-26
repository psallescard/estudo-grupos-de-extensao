# 20261125 - Frente 3: carreira, trajetória e objetivos

## Objetivo

Registrar a implementação da Frente 3 (`notebooks/02_Carreira_Trajetoria_Objetivos.ipynb`): como a vivência no grupo de extensão se conecta ao horizonte profissional de curto prazo (estágio e objetivo atual) e de médio prazo (área pretendida após a formatura). Só métodos da disciplina: qui-quadrado de associação com V de Cramér, ANOVA de 1 fator com Bartlett, η² e Scheffé, e regressão linear múltipla com F parcial. α = 5%.

## O que foi feito

- **Base de dados: `clean_data.parquet` gerado de novo em 25/11**, a partir do notebook 00:
  - no arquivo de 24/11, `anos_de_poli` estava errado para 30 alunos (o arquivo tinha sido gerado antes da correção do commit 59adcc2). Agora `anos_de_poli` = 2026 − `ano_ingresso` + 1, e `prepare_front_data` confere isso e interrompe a execução se receber um arquivo antigo;
  - nas outras colunas, mudaram só arredondamentos: `media_ponderada_num` (4,64 → 4,65; 9,42 → 9,41) e `horas_semanais_grupo_num` (70,37 → 70,36);
  - **as outras frentes devem usar o arquivo novo.** A Frente 2 é afetada nas perguntas 5 e 7, que usam o ano na Poli.
- **Código novo em `src/`:**
  - `carreira.py`: preparação dos dados e agrupamentos da frente (`prepare_front_data`, `analysis_sample`, `category_distribution`, `grouping_table`, `build_scenarios`), ordens das categorias, contraste a priori da P6 (`CAREER_CONTRASTS`) e blocos da regressão (`REGRESSION_BLOCKS`, `REGRESSION_COLUMNS`, `REGRESSION_LABELS`);
  - `stats_tests.py`, duas funções novas: `standardized_residuals` (resíduos padronizados ajustados de uma tabela de contingência) e `row_percentages` (% por linha);
  - `plotting/plots_carreira.py`: `plot_category_distribution`, `plot_stacked_shares`, `plot_means_panels` e `plot_scenario_probabilities` (os resíduos usam `plot_residual_diagnostics`, reexportado da Frente 1);
  - testes: `tests/test_carreira.py`, `tests/test_plots_carreira.py` e os novos casos de `tests/test_stats_tests.py` (11 testes no total, sem avisos). O teste de gráficos troca `plt.show` por uma função vazia, porque o `_save` da Frente 1 chama `plt.show` e geraria aviso fora do Jupyter.
  - `prepare_front_data` transforma "Excluído (sem valor)" em ausente (NaN) antes de criar a coluna categórica `estagio_antecipado`. O plano criava a categórica direto, o que gerava um `Pandas4Warning` (valor fora das categorias), que versões futuras do pandas tratarão como erro. Os resultados não mudam.
- **Execução do notebook:** o comando precisa de `--with ipykernel` além de `--with nbconvert`: `cd notebooks && uv run --with nbconvert --with ipykernel jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`.
- **Notebook** com 40 células: preparação, dados e cuidados gerais, descritiva, P1, P2, P3, P4, P6, P7 (modelo explicativo) e a seção 9 (síntese e limitações). Cada pergunta segue os itens (a) a (e) do guia.
- **Arquivos com prefixo `f3_`:**
  - tabelas `output/tables/f3_tab01` a `f3_tab22`;
  - figuras `output/figures/f3_fig01` a `f3_fig09`, adicionadas ao git com `git add -f` (a pasta `figures/` está no `.gitignore`, mas as figuras da Frente 1 são versionadas do mesmo jeito);
  - resumo `output/f3_resumo_para_relatorio.md`, montado para cerca de 6 páginas.
- **Perguntas do guia cortadas:**
  - **P5** (o estágio derruba as horas no grupo): o questionário não pergunta se o aluno estagia hoje, e a maior parte da amostra (124 de 187 alunos, no 1º ou 2º ano) ainda não chegou à idade usual de estágio, então o efeito de começar a estagiar não pode ser testado;
  - **P8** (prever a área pretendida): com 6 áreas, n = 187 e sem regressão logística, a previsão não se sustenta.

## Decisões analíticas

- **Critério do qui-quadrado:** no máximo cerca de 20% das caselas com esperado abaixo de 5, o mesmo da Frente 1.
- **Agrupamentos** (tabela `f3_tab02`):

  | Variável | Categorias originais | Nova categoria | n | Motivo |
  |---|---|---|---|---|
  | `categoria_extensao` | Consultoria & Negócios + Empreendedorismo | Consultoria & Negócios | 108 | Empreendedorismo tem n = 8; mesma decisão da Frente 1 |
  | `area_pretendida` | Consultoria + Empreendedorismo | Consultoria & Empreendedorismo | 52 | Com 6 áreas, 28% das caselas da P1a ficam com esperado < 5; com 5 áreas, 20% |
  | `motivacao_ingresso` | Networking e contato com empresas + Indicação ou influência de amigos | Outros | 7 | Aparece na descritiva, mas fica fora do qui-quadrado da P2 |
  | `objetivo_faculdade` | Desempenho acadêmico + IC / Pesquisa | Desempenho & Pesquisa | 33 | IC / Pesquisa tem n = 6; com 5 objetivos, 33% das caselas da P4 ficam com esperado < 5; com 4, 8% |
  | `anos_de_poli` | 3 + 4 + 5 | 3º ano ou mais | 63 | Só 9 alunos estão no 4º ou 5º ano |
  | `momento_estagio` | Antes do 3º ano + No 3ºano | Até o 3º ano | 82 | Corte da P3 e da P7; mede intenção |
  | `momento_estagio` | No 4ºano + A partir do 5ºano | 4º ano ou depois | 104 | Idem |
  | `momento_estagio` | Não pretendo realizar estágio | Excluído (sem valor) | 1 | n = 1 |
  | `media_ponderada` | Menor que 5,0 + 5,0 a 5,9 + 6,0 a 6,9 | Abaixo de 7,0 | 71 | Checagem ordinal da P6 |
  | `media_ponderada` | 8,0 a 8,9 + 9,0 a 10,0 | 8,0 ou mais | 41 | Idem |

  Na P6, as ANOVAs usam as 6 áreas pretendidas sem agrupar (a ANOVA não tem a restrição de caselas).
- **Exclusões, teste a teste, sem apagar linhas da base:**
  - P1b: sem os 20 "Indefinido" na área pretendida (com eles, 28% das caselas abaixo de 5; sem eles, 10%), n = 167;
  - P2: sem "Outros" na motivação (com essa linha, 40%; sem ela, 20%), n = 180;
  - P3: sem a resposta "Não pretendo realizar estágio", n = 186;
  - P4: sem as 7 respostas sem objetivo, n = 180;
  - P6: média ponderada com n = 184 (3 sem resposta); checagem ordinal com n = 184;
  - P7: casos completos nas 7 colunas do modelo, n = 179.
- **V de Cramér pelas referências do $k$ de cada tabela** (Cohen: V = w/√k, com $k$ = min(linhas, colunas) − 1). Para $k = 1$: 0,10/0,30/0,50; $k = 2$: 0,07/0,21/0,35; $k = 3$: 0,06/0,17/0,29. Por isso a P2 (V = 0,20, $k = 3$) é lida como associação moderada, e não fraca como dizia o plano.
- **P6:** a hipótese do guia virou um contraste definido a priori ({Mercado Financeiro, Consultoria} − demais áreas), testado por Scheffé. Como a ANOVA da importância foi significativa e o contraste não, o Scheffé também foi aplicado aos 15 pares (como na Frente 1). η² = 0,07 é lido como efeito pequeno a moderado pelas referências de Cohen para η² (0,01/0,06/0,14).
- **P7, modelo de probabilidade linear:** a regressão logística está fora da disciplina. O modelo completo tem 6 blocos definidos a priori (categoria, grande área, ano, objetivo, tempo no grupo e ln(horas)), e a eliminação para trás retira o bloco de maior p enquanto p ≥ 0,05. Limitações declaradas: previsões fora de 0–100%, variância não constante e resíduos não normais.
- **Efeito mecânico do ano na P7:** a resposta vale 1 para "antes do 3º ano" ou "no 3º ano". Só fica impedido de responder "até o 3º ano" quem está no 4º ano ou depois e ainda não estagiou. São 9 alunos no 4º ou 5º ano: 7 responderam "4º ano ou depois" e 2 responderam "No 3º ano" (provavelmente já estagiaram; para os mais velhos, a variável é em parte retrospectiva, não só intenção). Para quem está no 3º ano, "No 3º ano" continua sendo uma resposta possível. A restrição explica, portanto, parte da queda em "3º ano ou mais", e a diferença entre o 1º e o 2º ano (−26 pontos; p = 0,007) não é mecânica: é uma associação entre turmas. O ano entra principalmente como controle (o texto do plano, que tratava toda a queda como mecânica, foi corrigido).
- **Linguagem:** associativa, não causal. O momento do estágio mede intenção, e a P4 compara turmas, não acompanha as mesmas pessoas.

## Resultados

- **P1:**
  - área pretendida × categoria do grupo: χ²(8) = 95,0, p < 0,001, V = 0,50; 20% das caselas com esperado abaixo de 5;
  - área pretendida × grande área do curso (sem Indefinido): χ²(12) = 60,4, p < 0,001, V = 0,35; 10%;
  - 64,7% dos alunos de grupos de Mercado Financeiro miram Mercado Financeiro; 60,0% dos de Engenharia miram Indústria/Engenharia.
- **P2:** χ²(12) = 22,2, p = 0,035, V = 0,20 (moderada, perto do limite); 20%. Aprendizado técnico: 42,6% miram Mercado Financeiro (r = 2,99).
- **P3:** χ²(2) = 3,79, p = 0,15, V = 0,14; 0%. Até o 3º ano: Consultoria & Negócios 50,0%, Mercado Financeiro 38,2%, Engenharia 34,1%.
- **P4:** χ²(6) = 28,0, p < 0,001, V = 0,28; 8%. "Estágio": 17,9% no 1º ano, 15,7% no 2º e 46,0% no 3º ano ou mais.
  - Com a coluna antiga de 24/11 e o mesmo agrupamento, o teste daria χ²(6) = 12,28, p = 0,056 (calculado fora do notebook, porque a preparação atual recusa o arquivo antigo).
- **P6:**
  - importância da média: F(5; 181) = 2,74, p = 0,021, η² = 0,07, Bartlett p = 0,43; Mercado Financeiro 2,59, Consultoria 2,73, Indústria/Engenharia 3,29;
  - contraste a priori −0,45 (IC de Scheffé −0,98 a 0,07; p = 0,14); nenhum dos 15 pares é significativo (o mais próximo: Mercado Financeiro − Indústria/Engenharia, −0,69, p = 0,071);
  - média ponderada: F(5; 178) = 0,34, p = 0,89, η² = 0,009; ordinal: χ²(8) = 8,43, p = 0,39.
- **P7 (n = 179):**
  - eliminados, nesta ordem: objetivo (p = 0,283), tempo no grupo (p = 0,179), categoria (p = 0,089) e horas (p = 0,051); ficam grande área (p = 0,010) e ano;
  - modelo final: R² = 0,264 (ajustado 0,238), F(6; 172) = 10,28, p < 0,001; 2º ano −26 pontos (p = 0,007), 3º ano ou mais −62, Mecânica, Mecatrônica & Naval −23 (vs. Civil & Ambiental). Só parte da queda em "3º ano ou mais" é mecânica; a do 1º para o 2º ano é uma associação entre turmas;
  - **o F parcial conjunto rejeita por pouco:** F(9; 163) = 1,98, p = 0,045, e o R² ajustado cai de 0,275 (completo) para 0,238 (final). A exclusão de categoria e horas é limítrofe;
  - perfis de −6% (3º ano ou mais, Mecânica) a 93% (1º ano, Produção); proporções observadas: 75%, 53% e 14% por ano.

## Revisão de legibilidade

Um revisor independente leu o notebook sem ler Python (passo 5 do plano) e confirmou a estrutura, as decisões e todos os números do texto. As correções aplicadas:

- **Efeito do ano na P7:** o texto dizia que a queda com o ano era "sobretudo mecânica". Foi corrigido no notebook (quadro "Conceito" da P7, item "Efeito do ano" e conclusão (e)), no resumo e neste registro: a restrição explica parte da queda em "3º ano ou mais" (dos 9 alunos do 4º ou 5º ano, 7 responderam "4º ano ou depois" e 2 "No 3º ano"), e a diferença entre o 1º e o 2º ano (−26 pontos; p = 0,007) é uma associação entre turmas.
- **Rótulos em PT-BR nas tabelas impressas:**
  - `f3_tab02`: a coluna "Variável" mostra nomes legíveis ("Categoria do grupo", "Área pretendida", "Motivação de ingresso", "Objetivo atual", "Ano na Poli", "Momento do 1º estágio", "Faixa da média ponderada") no lugar dos nomes de coluna crus, por um dicionário `GROUPING_LABELS` em `src/carreira.py`;
  - tabelas de contingência, percentuais e resíduos (P1, P2, P3, P4 e checagem ordinal da P6): os eixos ganharam nomes em PT-BR, o que muda só o cabeçalho de `f3_tab03`, `f3_tab04`, `f3_tab06` a `f3_tab08`, `f3_tab10`, `f3_tab11`, `f3_tab13` e `f3_tab15` (nenhum número muda);
  - P7: a tabela de proporções por ano mostra "Proporção que pretende estagiar até o 3º ano", "n" e "Ano na Poli";
  - `display.max_colwidth` sem limite, para que "Motivo" e os rótulos dos coeficientes não apareçam cortados.
- **Revisão final da branch (só texto, nenhum número mudou):** a restrição do ano descrita com os 9 alunos do 4º ou 5º ano (7 "4º ano ou depois", 2 "No 3º ano"); validade aproximada dos testes F da P7 justificada pela faixa dos valores previstos, não só pelo n; "de magnitude modesta" removido da P2; "pequena (0,07)" → "fraca (0,07)" na checagem ordinal da P6; motivo do corte da P5 reescrito (o questionário não pergunta sobre estágio atual e 124 de 187 alunos estão no 1º ou 2º ano); os −23 pontos da P7 descritos como probabilidade de pretender estagiar até o 3º ano.
- Antes da revisão, também foram aplicadas as correções de texto acumuladas nas revisões anteriores: base dos percentuais da `f3_tab01` explicada no texto; conclusões (e) da P1, P6 e P7 encurtadas; η² = 0,07 lido como efeito pequeno a moderado ("está associada a 7% da variação"); "não diferem de Civil & Ambiental" trocado por "não se distinguem significativamente".

## Pontos de atenção

- Todas as conclusões são associações entre participantes de extensão (não há grupo de controle), com possível autosseleção.
- Categoria do grupo e grande área do curso se sobrepõem fortemente (Frente 1: V = 0,43), então os dois testes da P1 não separam os dois efeitos.
- P1a e P2 ficam exatamente no limite do critério (20% das caselas com esperado abaixo de 5), e a P2 tem p perto de 5%.
- A eliminação da P7 é sensível: categoria e horas saem com p = 0,089 e 0,051, e o F conjunto rejeita (p = 0,045).
- n pequeno em Mercado Financeiro como categoria de grupo (34) e em Indefinido como área pretendida (20).
- A `f3_tab01` usa os 187 alunos como base dos percentuais; o texto e a `f3_fig01` usam as respostas válidas (a diferença está explicada no notebook).
