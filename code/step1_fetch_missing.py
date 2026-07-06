"""Step 1 — fetch the endpoints missing from tushare-data.

Probed on 2026-07-06: this token CAN access stk_limit, suspend_d, moneyflow,
hk_hold, margin_detail (limit_list_d is NOT licensed). These fill the gaps the
BARRA-input panel doesn't cover:

  stk_limit      涨跌停价格  -> tradability filter (can't enter at limit)
  suspend_d      停复牌      -> explicit suspension flag
  moneyflow      资金流向    -> order-size buy/sell flows (alpha raw material)
  hk_hold        北向持股    -> northbound holdings (alpha raw material)
  margin_detail  融资融券    -> margin balances (alpha raw material)

Fetched by trade_date for 2016-01-01..2025-12-31 (one year of lookback before
the 2017-2025 mining window) into tushare-data/data/raw/<endpoint>/YYYY/,
same resumable layout as the price base. Re-run to resume after interruption.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2] / "tushare-data"
sys.path.insert(0, str(REPO))

from tsbarra import config  # noqa: E402
from tsbarra.client import TushareClient  # noqa: E402
from tsbarra import fetch_prices  # noqa: E402
from tsbarra.logutil import setup  # noqa: E402

NEW_ENDPOINTS = ("stk_limit", "suspend_d", "moneyflow", "hk_hold", "margin_detail")
START, END = "20160101", "20251231"

# conservative per-minute budgets; client also backs off on server-side caps
config.RATE_LIMITS.update({ep: 190 for ep in NEW_ENDPOINTS})

if __name__ == "__main__":
    log = setup()
    client = TushareClient()
    fetch_prices.fetch_by_date(client, datasets=NEW_ENDPOINTS, start=START, end=END)
    log.info("step1 fetch done.")
