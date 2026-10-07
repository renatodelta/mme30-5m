# MME30 · WIN$ M5

Análise da distância, em pontos, entre o fechamento do mini índice (WIN$, 5 minutos) e a Média Móvel Exponencial de 30 períodos.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `WIN$M5.csv` | Dados brutos (OHLC M5) exportados do MT5 |
| `calc_mme30.py` | Calcula a MME30 e as distâncias; gera os arquivos abaixo |
| `WIN_M5_MME30.csv` | Dados com `MME30`, `DIST_HIGH`, `DIST_LOW`, `DIST_CLOSE` |
| `mme30_data.js` | Dados compactados usados pelos gráficos |
| `close_mme30.html` | Oscilador **Close − MME30** em torno do zero |
| `mme30.html` | Candles + MME30 e distâncias de Máx/Mín/Fech |

## Uso

```bash
python calc_mme30.py
```

Depois abra `close_mme30.html` no navegador (precisa de internet para carregar a biblioteca Lightweight Charts).

## Cálculo

- MME30 sobre o fechamento: α = 2/31, semente = SMA dos 30 primeiros candles, série contínua.
- Distância = Close − MME30 (positivo: acima da média; negativo: abaixo).
- Linhas P5/P95: percentis 5% e 95% da distância em todo o histórico (90% dos candles ficam entre elas).
