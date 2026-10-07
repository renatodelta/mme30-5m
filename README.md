# MME30 Â· WIN$ M5

AnÃ¡lise da distÃ¢ncia, em pontos, entre o fechamento do mini Ã­ndice (WIN$, 5 minutos) e a MÃ©dia MÃ³vel Exponencial de 30 perÃ­odos.

## Arquivos

| Arquivo | DescriÃ§Ã£o |
|---|---|
| `WIN$M5.csv` | Dados brutos (OHLC M5) exportados do MT5 |
| `calc_mme30.py` | Calcula a MME30 e as distÃ¢ncias; gera os arquivos abaixo |
| `WIN_M5_MME30.csv` | Dados com `MME30`, `DIST_HIGH`, `DIST_LOW`, `DIST_CLOSE` |
| `mme30_data.js` | Dados compactados usados pelos grÃ¡ficos |
| `index.html` | Oscilador **Close âˆ’ MME30** em torno do zero |
| `mme30.html` | Candles + MME30 e distÃ¢ncias de MÃ¡x/MÃ­n/Fech |

## Uso

```bash
python calc_mme30.py
```

Depois abra `index.html` no navegador (precisa de internet para carregar a biblioteca Lightweight Charts).

## CÃ¡lculo

- MME30 sobre o fechamento: Î± = 2/31, semente = SMA dos 30 primeiros candles, sÃ©rie contÃ­nua.
- DistÃ¢ncia = Close âˆ’ MME30 (positivo: acima da mÃ©dia; negativo: abaixo).
- Linhas P5/P95: percentis 5% e 95% da distÃ¢ncia em todo o histÃ³rico (90% dos candles ficam entre elas).
