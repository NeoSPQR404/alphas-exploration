"""Mining pipeline configuration. All thresholds live here and are
'subject to change' per the mining prompt."""

HORIZON = 10                       # primary label: fwd_ret_10d

# windows (trade_date strings, inclusive)
IS_START, IS_END = "20170101", "20211231"      # in-sample: stages 1-3
OOS_START, OOS_END = "20220101", "20231231"    # stage-4 coverage gate
HOLDOUT_START, HOLDOUT_END = "20240101", "20251231"
# 2024-2025 is a final holdout: metrics are computed and written to
# results/mining/holdout/ but never used for accept/reject decisions and
# never fed back into experience memory, so repeated rounds don't burn it.

# stage 1: quick IC screen (in-sample, full-A)
# 2026-07-07: user raised the IC standard to 0.03 (both IS and OOS);
# 34 factors purged from the set at the same time.
S1_MIN_ABS_IC = 0.03
S1_MIN_ABS_ICIR = 0.30
S1_MIN_COVERAGE = 0.60

# stage 2: correlation vs accepted alpha set
S2_MAX_ABS_CORR = 0.70
S2_REPLACE_IC_RATIO = 1.30   # replace incumbent if new |IS IC| >= 1.3x old

# stage 3: intra-round duplication removal
S3_MAX_ABS_CORR = 0.70

# stage 4: coverage / robustness (OOS 2022-2023 + sub-universes + years)
S4_MIN_OOS_IC_RATIO = 0.40   # |OOS IC| >= 0.4 * |IS IC|, same sign
S4_MIN_OOS_ABS_IC = 0.03     # raised from 0.01 with the 0.03 standard
S4_UNIVERSES = ("hs300", "csi500", "csi1000")
S4_MIN_UNIVERSES_PASS = 2    # sub-universes with same-sign full-period IC
S4_UNIVERSE_MIN_ABS_IC = 0.005
S4_MIN_YEAR_SIGN_RATE = 0.60  # share of 2017-2023 years with same-sign IC

# stage 4 addition (2026-07-20): decile-monotonicity gate. Guards against
# factors that "work" only in the extreme deciles (the failure mode behind
# the 2026 extreme-decile inversion). Requires the decile mean-return curve
# to be monotone in the factor's own direction: Spearman(decile_mean, rank)
# same sign as IS IC and |.| >= threshold, on the IS+OOS window.
S4_MIN_MONOTONICITY = 0.60

# stage 4 additions (2026-07-09): rolling-window + bootstrap tests,
# both on the oriented daily rank-IC series over IS_START..OOS_END
S4_ROLL_WINDOW = 120          # rolling window length (trading days)
S4_ROLL_STEP = 20             # step between window starts
S4_ROLL_MIN_SIGN_RATE = 0.70  # share of windows with same-sign mean IC
S4_BOOT_B = 1000              # bootstrap resamples
S4_BOOT_BLOCK = 10            # moving-block length (= label horizon,
                              #   preserves overlap autocorrelation)
S4_BOOT_MAX_P = 0.05          # one-sided p-value: H0 mean oriented IC <= 0
S4_BOOT_SEED = 11

QUANTILES = 10

# ---------------------------------------------------------------- construction
# 2026-07-20: size+industry neutralization halved the 2026 long-short loss at
# zero historical cost (results/mining/NEUTRALIZE_REPORT.md). Adopted as the
# default construction. When True, the S1/S4 gates score the *neutralized*
# factor (residual alpha on [SW-L1 industry, log circ_mv]) so future rounds
# are judged on residual alpha, not a size/industry style tilt. Registry
# still stores the raw factor; neutralization is a construction-time transform.
# NOTE: the existing corpus was gated on raw IC — factors accepted before this
# flag are not directly comparable to ones accepted after.
GATE_ON_NEUTRALIZED = True

# Investable filter (backtest/eval layer). Status-only by default: drop ST and
# names listed < FILTER_MIN_DAYS trading days. The micro-cap size cut
# (FILTER_SIZE_DROP) is opt-in — it was shown to subtract signal out-of-sample
# (the edge lives partly in small caps) without fixing the regime risk.
FILTER_STATUS_ONLY = True
FILTER_MIN_DAYS = 250
FILTER_SIZE_DROP = 0.30
