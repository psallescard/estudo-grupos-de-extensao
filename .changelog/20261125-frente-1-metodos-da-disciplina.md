# 20261125 - Frente 1 refeita com os métodos da disciplina

## Objetivo

Registrar a revisão da Frente 1 (`notebooks/01_Formacao_Extensao_vs_Poli.ipynb`) após o alinhamento do grupo. Este registro substitui, na prática, o de `20261124-frente-1-formacao.md`: os métodos e as tabelas descritos lá não existem mais.

## O que mudou e por quê

- **Base de dados:** passa a ser o `clean_data.parquet` atualizado, enviado em 24/11. Em relação à versão anterior, mudam só os arredondamentos de `horas_semanais_grupo_num` (70,37 → 70,36) e `media_ponderada_num`. A coluna `anos_de_poli` desse arquivo ainda tem o desalinhamento já corrigido no código do notebook 00; ela não é usada na Frente 1.
- **Somente métodos dos slides:**
  - teste t pareado;
  - qui-quadrado de associação;
  - ANOVA de 1 e 2 fatores, com Bartlett e Scheffé;
  - regressão linear múltipla com F parcial.

  Saíram Wilcoxon, Kruskal-Wallis, Dunn, Kendall, logit ordinal, validação cruzada, bootstrap, HC3 e correção de Holm.
- **Perguntas:**
  - mantidas: P1, P4 e P6;
  - P2 e P3 fundidas numa ANOVA de 2 fatores (categoria + área);
  - excluídas: P5, P7a (logística da nota máxima) e P8 (predição da importância da média).
  - A regressão do ganho líquido foi refeita como **modelo explicativo**: modelo completo com base teórica, eliminação por F parcial e simulação de cenários a priori.
- **Notebook legível:** toda a lógica está em `src/`:
  - `stats_tests.py`: testes da disciplina, com tabelas em PT-BR;
  - `regression.py`: OLS, F parcial, eliminação, coeficientes e cenários;
  - `formacao.py`: preparação dos dados e constantes da frente;
  - `plotting/plots_formacao.py`: gráficos.

  As células do notebook só chamam funções, e quadros "Conceito" explicam cada método. `src/inference.py` foi removido.
- **Arquivos com prefixo `f1_`:**
  - tabelas `output/tables/f1_tab01` a `f1_tab13`;
  - figuras `output/figures/f1_fig01` a `f1_fig06`;
  - resumo `output/f1_resumo_para_relatorio.md`, montado para cerca de 6 páginas.

  As pastas `output/tables/frente1/` e `output/frente1_resumo_para_relatorio.md` foram removidas.

## Decisões analíticas

- **Empreendedorismo (n = 8) somado a "Consultoria & Negócios"** na coluna `categoria_grupo`, por afinidade temática e pela condição do qui-quadrado: com 4 categorias, 30% das caselas ficam com esperado abaixo de 5; com 3, ficam 7%.
- **ANOVA de 2 fatores aditiva** (sem interação), porque há combinações vazias: não há alunos de Civil & Ambiental nem de Produção em grupos de Engenharia. Cada fator é testado por F parcial (modelo com os dois fatores contra o modelo sem aquele fator).
- **P4 usa o qui-quadrado** de "deu nota 5 ou não" contra horas e contra tempo de grupo como teste principal, por causa do efeito teto. A ANOVA de 2 fatores entra só como confirmação, porque o teste de Bartlett rejeita variâncias iguais entre as faixas de horas e nem pode ser calculado para o tempo de grupo (o grupo "Mais de 2 anos" tem variância zero).
- **Regressão:** horas em logaritmo (`log_horas_semanais` = ln de `horas_semanais_grupo_num`). O ganho médio é quase plano até 20 h e sobe nas faixas altas, e o valor de "Mais de 40h" (70,36 h) dominaria uma escala linear. Interpretação: o dobro de horas corresponde a 0,69·β. Um F parcial contra o modelo com as 5 faixas como fator confirma que o log basta (F(3; 180) = 1,49; p = 0,22).
- **Objetivo renomeado:** o valor "IC / Pesquisa" foi renomeado para "Iniciação científica" em `objetivo_faculdade`, para que "IC" signifique só intervalo de confiança no texto.
- **Linguagem:** associativa, não causal. Os β descrevem associações mantidos os demais fatores constantes, e os perfis da regressão servem para comparar, não para prometer resultado.

## Resultados

- **P1:** t(186) = 26,6, p < 0,001; diferença média 2,27 (IC 2,10 a 2,44); d = 1,95; 93% dão nota maior à extensão.
- **P2+P3:**
  - categoria × área associadas: χ²(8) = 69,3, p < 0,001, V = 0,43;
  - no ganho líquido, a área tem p = 0,038 sozinha e p = 0,098 controlada a categoria; a categoria tem p < 0,001 controlada a área;
  - Scheffé: Consultoria − Engenharia = 0,94 (IC 0,46 a 1,43). A diferença vem das disciplinas.
- **P4:**
  - horas × nota 5: χ²(4) = 26,15, p < 0,001, V = 0,37;
  - tempo × nota 5: χ²(3) = 7,37, p = 0,061.
- **P6:** ANOVA F(4; 175) = 15,82, p < 0,001, η² = 0,27, Bartlett p = 0,44; contraste {Intercâmbio, IC, Desempenho} − {Grupo, Estágio} = 1,18 (IC 0,64 a 1,72).
- **Regressão:**
  - eliminados, nesta ordem: tempo no grupo, deslocamento e área. F parcial conjunto: p = 0,19;
  - modelo final: R² = 0,20; β(ln horas) = 0,40; β(Engenharia) = −0,67;
  - decomposição (mesmos preditores em cada parte do ganho):
    - horas: +0,24 na extensão (p < 0,001) e −0,17 nas disciplinas (p = 0,035);
    - Engenharia: +0,70 nas disciplinas (p < 0,001) e +0,02 na extensão (p = 0,84);
  - Engenharia tem −0,94 na comparação bruta (P2+P3) e −0,67 na regressão, porque os grupos técnicos dedicam menos horas (44% na faixa de 6–10 h, contra 12% em Consultoria).

## Revisão de legibilidade

Um leitor independente, sem conhecimento de Python, conferiu o notebook pelo critério do grupo (aprender a análise lendo só texto, tabelas, gráficos e nomes de funções). As correções aplicadas:

- **Rótulos:** em PT-BR nas tabelas.
- **Conceitos explicados:**
  - fórmula e referências do V de Cramér;
  - variáveis indicadoras na regressão;
  - notação científica dos p-valores.
- **Tabelas novas:**
  - composição das categorias;
  - cursos em "Outras Engenharias";
  - médias das três variáveis por categoria e por área;
  - contagens da P4;
  - valores representativos das faixas de horas;
  - distribuição de horas por categoria.
- **Scheffé da P6:** cobre os 10 pares.
- **Figuras:** a de resíduos virou `f1_fig05` e a de perfis `f1_fig06`, na ordem em que aparecem.

## Pontos de atenção

- Todas as conclusões são associações entre participantes de extensão (não há grupo de controle).
- IC / Pesquisa (n = 6) e "Mais de 2 anos" de grupo (n = 10) têm estimativas imprecisas.
- O ganho líquido é discreto (−1 a 4); a regressão linear é uma aproximação, aceitável para fins explicativos (resíduos verificados em `f1_fig06`).
