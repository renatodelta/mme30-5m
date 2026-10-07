"""
Calcula a MME (Média Móvel Exponencial) de 30 períodos sobre o fechamento do
arquivo WIN$M5.csv e mede a distância, em pontos, da Máxima, Mínima e
Fechamento até a MME30.

Saídas:
  - WIN_M5_MME30.csv : dados com MME30 e distâncias
  - mme30_data.js    : dados compactados para o gráfico (mme30.html)
"""
import csv
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
ENTRADA = BASE / "WIN$M5.csv"
SAIDA_CSV = BASE / "WIN_M5_MME30.csv"
SAIDA_JS = BASE / "mme30_data.js"
PERIODO = 30


def detectar_encoding(caminho: Path) -> str:
    inicio = caminho.read_bytes()[:4]
    if inicio.startswith((b"\xff\xfe", b"\xfe\xff")):
        return "utf-16"
    if inicio.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    return "utf-8"


def ler_csv(caminho: Path):
    linhas = []
    with caminho.open(encoding=detectar_encoding(caminho), newline="") as f:
        leitor = csv.reader(f)
        next(leitor)  # cabeçalho
        for r in leitor:
            if len(r) < 5 or not r[0].strip():
                continue
            dt = datetime.strptime(r[0].strip(), "%Y.%m.%d %H:%M")
            o, h, l, c = (float(x) for x in r[1:5])
            linhas.append((dt, o, h, l, c))
    return linhas


def calcular_mme(fechamentos, periodo):
    """MME clássica: semente = SMA dos primeiros N períodos, alpha = 2/(N+1)."""
    alpha = 2 / (periodo + 1)
    mme = [None] * len(fechamentos)
    if len(fechamentos) < periodo:
        return mme
    atual = sum(fechamentos[:periodo]) / periodo
    mme[periodo - 1] = atual
    for i in range(periodo, len(fechamentos)):
        atual = alpha * fechamentos[i] + (1 - alpha) * atual
        mme[i] = atual
    return mme


def resumo(valores):
    v = sorted(valores)
    n = len(v)
    pct = lambda p: v[min(n - 1, int(p * (n - 1)))]
    absv = sorted(abs(x) for x in v)
    return {
        "media": round(statistics.fmean(v), 1),
        "media_abs": round(statistics.fmean(absv), 1),
        "desvio": round(statistics.pstdev(v), 1),
        "min": round(v[0], 1),
        "max": round(v[-1], 1),
        "p05": round(pct(0.05), 1),
        "p50": round(pct(0.50), 1),
        "p95": round(pct(0.95), 1),
        "p99_abs": round(absv[min(n - 1, int(0.99 * (n - 1)))], 1),
    }


def main():
    dados = ler_csv(ENTRADA)
    fech = [d[4] for d in dados]
    mme = calcular_mme(fech, PERIODO)

    t, o, h, l, c, m = [], [], [], [], [], []
    dist_h, dist_l, dist_c = [], [], []

    with SAIDA_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["DATA/HORA", "OPEN", "HIGH", "LOW", "CLOSE", "MME30",
                    "DIST_HIGH", "DIST_LOW", "DIST_CLOSE"])
        for (dt, op, hi, lo, cl), e in zip(dados, mme):
            if e is None:
                continue
            dh, dl, dc = hi - e, lo - e, cl - e
            w.writerow([dt.strftime("%Y-%m-%d %H:%M"), op, hi, lo, cl,
                        f"{e:.2f}", f"{dh:.2f}", f"{dl:.2f}", f"{dc:.2f}"])
            # horário tratado como UTC para o gráfico exibir a hora local do arquivo
            t.append(int(dt.replace(tzinfo=timezone.utc).timestamp()))
            o.append(op); h.append(hi); l.append(lo); c.append(cl)
            m.append(round(e, 1))
            dist_h.append(dh); dist_l.append(dl); dist_c.append(dc)

    payload = {
        "ativo": "WIN$", "timeframe": "M5", "periodo": PERIODO,
        "inicio": dados[PERIODO - 1][0].strftime("%d/%m/%Y %H:%M"),
        "fim": dados[-1][0].strftime("%d/%m/%Y %H:%M"),
        "n": len(t),
        "t": t, "o": o, "h": h, "l": l, "c": c, "m": m,
        "stats": {
            "high": resumo(dist_h),
            "low": resumo(dist_l),
            "close": resumo(dist_c),
        },
    }
    SAIDA_JS.write_text(
        "window.MME_DATA = " + json.dumps(payload, separators=(",", ":")) + ";",
        encoding="utf-8",
    )

    print(f"Candles lidos: {len(dados)} | com MME30: {len(t)}")
    for k, s in payload["stats"].items():
        print(f"{k:>5}: {s}")
    print(f"Gerado: {SAIDA_CSV.name}, {SAIDA_JS.name}")


if __name__ == "__main__":
    main()
