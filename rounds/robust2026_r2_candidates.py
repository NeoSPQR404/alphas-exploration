"""robust_2026 Round 2 — the core activity-CV / liquidity-shape vein is now
saturated in the curated set (R1 was mostly S2-locked), so target less-covered
territory: lottery/peak forms (R1's relvol_peak cleared), peak-timing (HighDay),
and downside/tail asymmetry. Still no overnight-gap.
"""
SET_NAME = "robust_2026"

CANDIDATES = [
    # lottery / peak (R1 relvol_peak_60 accepted -> mine the family on fresh quantities)
    {"name": "relturnf_peak_60", "family": "lottery", "logic_score": 0.6,
     "expr": "-TsMax(TURN_F / TsMean(TURN_F, 20), 60)",
     "rationale": "Peak relative turnover (attention lottery)."},
    {"name": "relamount_peak_60", "family": "lottery", "logic_score": 0.55,
     "expr": "-TsMax(AMOUNT / TsMean(AMOUNT, 20), 60)",
     "rationale": "Peak relative dollar volume (liquidity lottery)."},
    {"name": "vr_peak_60", "family": "lottery", "logic_score": 0.55,
     "expr": "-TsMax(VR, 60)",
     "rationale": "Peak volume ratio."},
    {"name": "ret_max_20", "family": "lottery", "logic_score": 0.6,
     "expr": "-TsMax(RET, 20)",
     "rationale": "Classic MAX lottery: extreme up-day, reverses."},
    {"name": "amp_max_20", "family": "lottery", "logic_score": 0.55,
     "expr": "-TsMax(AMP, 20)",
     "rationale": "Peak amplitude (range lottery)."},

    # peak-timing / recency (days since a quantity's peak)
    {"name": "vol_peak_recency_60", "family": "timing", "logic_score": 0.55,
     "expr": "HighDay(VOLUME, 60)",
     "rationale": "Days since volume peak (attention recency/duration)."},
    {"name": "turnf_peak_recency_120", "family": "timing", "logic_score": 0.55,
     "expr": "HighDay(TURN_F, 120)",
     "rationale": "Days since turnover peak (attention duration, long band)."},
    {"name": "amp_peak_recency_60", "family": "timing", "logic_score": 0.5,
     "expr": "HighDay(AMP, 60)",
     "rationale": "Days since range peak (volatility recency)."},

    # downside / tail asymmetry (fresh forms vs the one resident asymmetry)
    {"name": "downsemivol_60", "family": "asymmetry", "logic_score": 0.55,
     "expr": "-TsStd(RET * (RET < 0), 60)",
     "rationale": "Downside semivol (crash-risk); low downside vol names steadier."},
    {"name": "semivol_asym_ret_60", "family": "asymmetry", "logic_score": 0.6,
     "expr": "TsStd(RET * (RET > 0), 60) - TsStd(RET * (RET < 0), 60)",
     "rationale": "Up-minus-down return semivol asymmetry (on RET, fresh vs the CLOSE/VWAP resident)."},
    {"name": "ret_skew_neg_60", "family": "tail", "logic_score": 0.55,
     "expr": "-TsSkew(RET, 60)",
     "rationale": "Return skewness: negative-skew (crash-prone) names carry a premium."},
    {"name": "amp_skew_neg_60", "family": "tail", "logic_score": 0.5,
     "expr": "-TsSkew(AMP, 60)",
     "rationale": "Amplitude skewness (occasional violent-range days)."},

    # momentum / level (new to this set)
    {"name": "mom_intermediate", "family": "momentum", "logic_score": 0.5,
     "expr": "TsSum(RET, 120) - TsSum(RET, 20)",
     "rationale": "Intermediate (12-1 style) momentum: long-band return excl. recent month."},
    {"name": "vol_rank_60", "family": "level", "logic_score": 0.5,
     "expr": "TsRank(VOLUME, 60)",
     "rationale": "Where current volume sits in its 60d range (self-relative attention level)."},
    {"name": "crashday_freq_120", "family": "event_freq", "logic_score": 0.5,
     "expr": "-TsCount(RET < -2 * TsStd(RET, 60), 120)",
     "rationale": "Crash-day rarity (downside-only event count)."},
]

assert len(CANDIDATES) == 15, len(CANDIDATES)
