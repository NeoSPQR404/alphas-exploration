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
