#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate the comprehensive Chinese research report -> 因子挖掘研究报告.pdf.

Covers the full arc: method -> 3 sets -> 2026 OOS -> neutralization -> cost-aware
-> IC monitor -> meta-composite -> 2026 per-factor screen -> robust_2026 curated
set + backtest -> new mining rounds -> value_20d sleeve -> conclusions.

Conventions (hard-won): STSong-Light CID font for CJK; ASCII double-quote is ONLY
a Python delimiter (in-text use 【】 or <b>); _san() maps U+2212/U+2013 to ASCII
hyphen because STSong-Light lacks the minus glyph.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "results" / "mining" / "figs"
OUT = ROOT / "因子挖掘研究报告.pdf"

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
FONT = "STSong-Light"


def _san(s: str) -> str:
    return s.replace("−", "-").replace("–", "-").replace("—", "-")


ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName=FONT, fontSize=15,
                    spaceBefore=14, spaceAfter=7, textColor=colors.HexColor("#1a2b4a"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName=FONT, fontSize=12,
                    spaceBefore=9, spaceAfter=4, textColor=colors.HexColor("#2e5b9e"))
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontName=FONT, fontSize=9.6,
                      leading=15, alignment=TA_LEFT, spaceAfter=5)
CAP = ParagraphStyle("CAP", parent=BODY, fontSize=8, textColor=colors.grey, spaceBefore=2)
TITLE = ParagraphStyle("TITLE", parent=ss["Title"], fontName=FONT, fontSize=22,
                       textColor=colors.HexColor("#1a2b4a"), spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=BODY, fontSize=11, textColor=colors.grey)

story = []


def P(t):
    story.append(Paragraph(_san(t), BODY))


def h1(t):
    story.append(Paragraph(_san(t), H1))


def h2(t):
    story.append(Paragraph(_san(t), H2))


def sp(h=0.2):
    story.append(Spacer(1, h * cm))


def fig(name, caption, width=15.5):
    p = FIGS / name
    if not p.exists():
        return
    img = Image(str(p))
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = width * cm
    img.drawHeight = width * ratio * cm
    story.append(img)
    story.append(Paragraph(_san(caption), CAP))
    sp(0.25)


def table(data, widths=None, header=True):
    t = Table([[_san(str(c)) for c in row] for row in data], colWidths=widths)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), FONT), ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d3e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2b4a")),
                  ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                  ("FONTSIZE", (0, 0), (-1, 0), 8)]
    t.setStyle(TableStyle(style))
    story.append(t)
    sp(0.25)


# ---------------------------------------------------------------- cover
story.append(Spacer(1, 3 * cm))
story.append(Paragraph("A股因子挖掘研究报告", TITLE))
story.append(Paragraph(_san("全市场 2017-2026 · 行为价量 + 价值基本面 · 中性化构造 · 2026样本外"), SUB))
sp(0.6)
story.append(Paragraph(_san("更新日期 2026-07-21 · 仓库 alphas-exploration"), SUB))
story.append(PageBreak())

# ---------------------------------------------------------------- 0 摘要
h1("摘要")
P("本项目在本地 tushare 全A面板（2017-2026）上，以【检索→生成→评估→蒸馏】的轮次循环挖掘选股因子。"
  "因子分属若干独立【集】，各自拥有登记簿、经验记忆、逐轮报告与评估产物。核心发现如下：")
P("<b>1. 2026样本外是显著衰减而非干净反转。</b> 复合信号2026日频rank IC仍弱正"
  "（行为全量+0.065、规范价量+0.057、复合+0.025），但远低于历史约0.10；组合回测因样本小（约10次调仓）+极端分位而反转亏损。")
P("<b>2. 规模+行业中性化是免费的最高价值改造。</b> 它在2026把多空损失近乎腰斩（行为全量多空 -20.8%→-10.0%），"
  "历史零成本，日频IC反而升高；证明2026失败大部分是风格暴露而非核心信号。")
P("<b>3. 成本约束在复合层面而非单因子层面生效。</b> 单因子中位数扣15bp换手成本后 -1.6%（70%不可交易），"
  "但复合组合净超额 +5.1%/年。因此换手/成本感知打分为【上报】而非硬门槛。")
P("<b>4. 2026逐因子筛选：隔夜跳空持续是最稳健且可交易的alpha。</b> 329个因子中111个仍有效、29个同时高效；"
  "冠军为隔夜跳空持续 TsMed(OPEN/Delay(CLOSE,1)-1)。此结论直接印证了 GTJA-191 复现中【A股价量优势本质是隔夜效应】的判断。")
P("<b>5. 精选集 robust_2026 与 20日价值套件 value_20d。</b> 前者为跨期稳健且可交易的非隔夜因子精选（历史超额+10.2%/年 IR1.74）；"
  "后者验证价值在20日远强于10日，是与行为组合正交的真实分散来源，但2026处于价值不利区间。")

# ---------------------------------------------------------------- 1 方法
h1("一、方法与评估框架")
P("入口 code/mining/round.py。候选文件定义 CANDIDATES=[{name, expr, family, rationale, logic_score}] 与可选 SET_NAME/FIELD_WHITELIST，"
  "经 data.py（宽表面板）、operators.py（算子沙箱）、pipeline.py（四阶段门）、alphaseval.py（指标）、registry.py、memory.py 流转。")
P("标签 fwd_ret_10d（t+1 vwap入场，停牌安全）；全A tradable_entry掩码；日频Spearman rank IC。"
  "窗口：样本内 2017-2021；样本外门 2022-2023；持有 2024-2025（已耗尽）；2026 为全新样本外。")
table([
    ["评估门", "阈值"],
    ["S1 快速IC", "|IS IC|>=0.03, |ICIR|>=0.30, 覆盖>=0.60"],
    ["S2 集合相关", "|corr|<0.70 vs 现有集；1.3倍IC替换豁免"],
    ["S3 轮内去重", "|corr|>=0.70 保留最优"],
    ["S4 稳健性（6子测）", "OOS同号；3子域2/3；年度同号率>=0.60；滚动120/20>=0.70；分块自助p<=0.05；分位单调>=0.60"],
    ["构造（2026-07新增）", "GATE_ON_NEUTRALIZED：S1/S4对规模+行业中性化后的残差打分"],
], widths=[3.2 * cm, 11.5 * cm])
P("2026-07的三项改造沉淀于 code/mining/construct.py（中性化/复合/可投掩码的单一真源）："
  "① 中性化默认构造 ② S4分位单调门 ③ 状态型可投过滤（弃用微盘规模剔除）。")

# ---------------------------------------------------------------- 2 三集
h1("二、三个因子集")
table([
    ["集", "因子数", "词表", "说明"],
    ["behavioral_full", "112", "全词表", "OHLCV+换手+振幅+涨跌停+资金流+北向+两融+估值+行业"],
    ["canonical", "105", "仅OHLCV/VWAP/AMOUNT/RET", "AST强制；与behavioral_full高度重叠"],
    ["canonical_composite", "119", "规范因子的秩积复合", "cxalpha_；2026成本脆弱"],
], widths=[3.6 * cm, 1.6 * cm, 4.5 * cm, 5 * cm])
P("behavioral_full 与 canonical 截面秩相关高达0.96（见元复合），基本冗余。behavioral_full 为主部署集。")

# ---------------------------------------------------------------- 3 2026 OOS
h1("三、2026样本外检验：显著衰减，而非干净反转")
P("抓取全新2026数据（8个日频端点，约128天），扩展面板并在真正未见的2026窗口回测各集EW复合。"
  "更正后的诚实结论：复合<b>日频rank IC在2026保持弱正</b>（+0.065/+0.057/+0.025 vs 历史约0.10），即约腰斩式衰减；"
  "分位/组合回测（仅约10次非重叠调仓）反转亏损是小样本+极端分位假象。此前所称【反转】言过其实。")
fig("fig_ic_trajectory.png", "图1 复合信号历史vs各窗口IC（若存在）。", 14)

# ---------------------------------------------------------------- 4 中性化
h1("四、规模+行业中性化")
P("对复合信号逐日在【行业哑变量 + log流通市值】上取残差（Barra-lite）。四变体（原始/筛选/中性化/筛选+中性化）在历史与2026对比：")
table([
    ["集 (中性化)", "历史超额", "历史IC", "2026超额", "2026多空", "2026 IC"],
    ["behavioral_full", "+8.0%", "0.105", "-2.7%", "-10.0%", "0.073"],
    ["canonical", "+6.1%", "0.102", "-7.5%", "-23.3%", "0.067"],
    ["canonical_composite", "+5.6%", "0.076", "-15.6%", "-41.4%", "0.033"],
], widths=[3.8 * cm, 2.3 * cm, 2.1 * cm, 2.2 * cm, 2.2 * cm, 2 * cm])
P("中性化把2026多空损失近乎腰斩，历史零成本，日频IC反升（例 +0.065→+0.073）：<b>2026失败大部分是风格暴露</b>。"
  "而生硬微盘剔除反而有害（edge部分存在于小盘）。详见 results/mining/NEUTRALIZE_REPORT.md。")
fig("fig_neutralize.png", "图2 中性化 vs 微盘筛选：2026多空与历史超额对比。", 15)

# ---------------------------------------------------------------- 5 成本
h1("五、换手/成本感知打分")
P("每个因子登记其分位换手与扣15/30bp成本后的多头超额。关键：<b>成本约束在复合层面生效，而非单因子。</b>")
table([
    ["层级", "毛超额", "净@15bp", "分位换手"],
    ["单因子（behavioral_full中位）", "+3.7%", "-1.6%", "0.65"],
    ["复合（behavioral_full）", "+9.0%", "+5.1%", "0.48"],
], widths=[6.5 * cm, 2.6 * cm, 2.6 * cm, 3 * cm])
P("单因子net>0门会误杀70%语料；复合通过分散既升毛超额又降换手，净由负转强正。故 GATE_ON_NET_COST 默认关闭，"
  "cost_aware_score 用于【偏好】低换手候选。详见 results/mining/COST_ANALYSIS.md。")

# ---------------------------------------------------------------- 6 IC monitor
h1("六、滚动IC衰减监测")
P("对中性化生产信号跟踪120日移动rank IC，相对样本内基线分级 健康(>=0.60x)/观察(0.30-0.60x)/受损/破裂。")
table([
    ["集", "基线IC", "2025末移动IC", "状态", "2026 IC", "2026状态"],
    ["behavioral_full", "0.105", "0.087 (0.83x)", "健康", "0.073 (0.70x)", "健康"],
    ["canonical", "0.100", "0.075 (0.75x)", "健康", "0.067 (0.67x)", "健康"],
    ["canonical_composite", "0.069", "0.066 (0.97x)", "健康", "0.033 (0.47x)", "观察"],
], widths=[3.6 * cm, 2 * cm, 3 * cm, 1.8 * cm, 2.6 * cm, 1.8 * cm])
P("中性化信号2017-2025<b>无长期衰减</b>（行为全量年度IC 0.089-0.115）；2026为首个低于基线之年但未破裂。"
  "信号历史上曾进入观察区（2020疫情、2022-23熊市）并复原，故属【降低信心】而非退出。")
fig("fig_ic_monitor.png", "图3 滚动IC健康监测：三集中性化复合的120日移动IC vs 基线。", 15)

# ---------------------------------------------------------------- 7 meta
h1("七、跨集元复合（负面结果）")
P("三集基于不同词表，本应部分正交。实测：behavioral_full~canonical 截面秩相关<b>0.962</b>、IC序列相关0.98；"
  "等权/IR加权元复合（历史超额+7.5%、2026 -10.5%）<b>劣于单独 behavioral_full</b>（+8.0%、-2.7%）。")
P("教训：混合同一底层行为的价量词表毫无增益——真正的分散必须来自<b>不同数据族</b>（价值/基本面），见第十一节。")

# ---------------------------------------------------------------- 8 2026 screen
h1("八、2026逐因子筛选：哪些alpha有效且高效")
P("对全部329因子按表达式在2017-2026重算，在2026窗口打分：<b>有效</b>=方向化IC同号且>=0.03；"
  "<b>高效</b>=扣自身15bp换手成本后多头超额>0。")
table([
    ["", "数量"],
    ["有效（2026仍预测）", "111 (34%)"],
    ["高效（净成本后可交易）", "34 (10%)"],
    ["有效且高效", "29 → 24个独立信号"],
], widths=[7 * cm, 4 * cm])
P("<b>冠军是隔夜跳空持续</b>：TsMed(OPEN/Delay(CLOSE,1)-1,20) 净+46.6%/年，前十有四个是同一隔夜信号——"
  "直接印证 GTJA-191 复现【A股价量优势本质是隔夜效应】。其余稳健低换手脉络：事件稀有（【安静】股跑赢）与大单资金流背离。"
  "有效性常见，<b>高效性才是约束</b>：高换手的非对称/彩票族多被成本吞噬。")
fig("fig_valid_2026.png", "图4 2026逐因子筛选：有效性(方向化IC) × 效率(扣成本净超额)。绿=两者兼备29个。", 15)

# ---------------------------------------------------------------- 9 robust_2026
h1("九、精选集 robust_2026 及回测")
P("按用户选择构建的非隔夜、跨期稳健且可交易精选集（25个 ralpha_）：5个新挖(R13-14) + 19个过往有效高效(排除隔夜) + 1个(R1-2)。"
  "中性化EW复合回测：")
table([
    ["窗口", "超额/IR", "多头净@15bp(IR)", "多空毛Sharpe"],
    ["全期 2017-25", "+10.2% / 1.74", "+14.2% / 0.62", "2.58"],
    ["样本内", "+11.7% / 2.12", "+11.4% / 0.56", "3.45"],
    ["OOS 2022-23", "+11.3% / 1.67", "+4.4% / 0.17", "1.79"],
    ["2026 中性化", "+23.4%", "多空 +69.2% / IC 0.111", "-"],
], widths=[3.4 * cm, 3.6 * cm, 4.4 * cm, 3 * cm])
P("<b>诚实警示（选择偏差）：</b>2026的+23.4%被高估——24因子中19个是<b>用2026数据挑选</b>的（2026 IC 0.111 反超历史0.081即是铁证）。"
  "唯一干净的样本外是5个新挖因子（仅用2017-25定门）。前瞻预期应参考历史约+10%超额并对衰减打折，而非选择膨胀的+23%。")
fig("fig_robust_2026_backtest.png", "图5 robust_2026：分位单调(历史vs2026) 及 2026多头超额 vs 源因子集。", 15)

# ---------------------------------------------------------------- 10 new mining
h1("十、新挖掘轮次（避开隔夜脉络）")
P("R13-14（behavioral_full）：从事件稀有、稳健中位、耦合等非隔夜脉络挖掘。R13 8/27录用，R14 4/19录用。"
  "在2026再筛选，2个跨期稳健且高效：")
table([
    ["因子", "脉络", "IS IC", "2026 IC", "2026净@15bp"],
    ["alpha_0144 -TsCount(TURN_F>2均,120)", "换手尖峰稀有(安静注意)", "+0.047", "+0.071", "+15.4%"],
    ["alpha_0146 TsMed(AMOUNT,60)/TsMean", "成交额中位/均值比", "+0.042", "+0.057", "+8.3%"],
], widths=[6.6 * cm, 3.4 * cm, 1.7 * cm, 1.7 * cm, 1.9 * cm])
P("教训：中位/均值<b>比值</b>（有界、低换手）可交易，而均值-中位<b>差</b>虽有效却被换手吞噬——【有效≠可交易】。"
  "robust_2026 自挖R1-2共33候选仅留1个（ralpha_0026 峰值相对成交量）：精选集因构造已近最优，其低换手脉络立即S2锁死。")

# ---------------------------------------------------------------- 11 value_20d
h1("十一、20日价值套件 value_20d")
P("专设20日价值/基本面套件（valpha_；全仓库唯一以 fwd_ret_20d 设门）。机制：候选文件在加载时置 cfg.HORIZON=20（round.py先runpy候选文件再读HORIZON，各轮独立进程），不污染10日各集。")
table([
    ["因子", "IS IC", "OOS IC", "2026 IC", "角度"],
    ["valpha_0001 CsRank(EP)*CsRank(CFP)", "+0.052", "+0.024", "+0.023", "价值一致(盈利+现金流)"],
    ["valpha_0002 CsRank(SP)+CsRank(Delta(SP,120))", "+0.044", "+0.069", "-0.013", "便宜+销售成长"],
    ["valpha_0003 CsRank(EP)-CsRank(Log(CMV))", "+0.029", "+0.067", "-0.007", "便宜+小盘"],
    ["valpha_0004 CsRank(EP)-CsRank(TsSum(RET,20))", "+0.078", "+0.057", "+0.006", "逆向价值"],
], widths=[7.4 * cm, 1.7 * cm, 1.7 * cm, 1.7 * cm, 3 * cm])
P("<b>价值在20日远强于10日</b>（IS/OOS 0.024-0.078 vs 约0.03），且与行为组合正交（S2相关约0）=真实分散来源。"
  "但四者在2026H1均弱转负（价值不利区间；2026@20d仅约4次调仓/85天=短窗，非否决，价值有周期性）。价值×行为交互在20日同样失败。")

# ---------------------------------------------------------------- 12 结论
h1("十二、结论与后续")
P("<b>结论：</b>①中性化是最高价值免费改造，应作默认构造；②成本约束在复合层生效；③隔夜跳空持续是最稳健可交易的价量alpha；"
  "④价值在20日是真实正交分散源但当前区间不利；⑤精选集近最优，再挖同一价量域收益递减。")
P("<b>后续（未请求）：</b>value_20d 在20日的EW复合回测；行为(10d)+价值(20d)混合套件的全历史风险调整检验；"
  "复合层换手削减（缓冲带）；围绕隔夜脉络的专门轮次（若放开避开约束）。")
P("所有构造/评估产物见 results/mining/：NEUTRALIZE_REPORT、COST_ANALYSIS、IC_MONITOR、META_COMPOSITE、VALID_2026、"
  "各集 BACKTEST 与逐轮 round_NN.md；图见 results/mining/figs/。")

doc = SimpleDocTemplate(str(OUT), pagesize=A4, topMargin=1.6 * cm,
                        bottomMargin=1.6 * cm, leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                        title="A股因子挖掘研究报告")
doc.build(story)
print("wrote", OUT, "pages via story of", len(story), "flowables")
