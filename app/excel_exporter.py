import io
import json
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from app.survey_data import SURVEY_METADATA


def decode_json_list(val):
    if not val:
        return []
    try:
        data = json.loads(val)
        return data if isinstance(data, list) else [data]
    except Exception:
        return [str(val)]


def map_factors(items, lang="ko"):
    if not items:
        return ""
    meta = SURVEY_METADATA["four_satisfaction_factors"][lang]
    names = [meta.get(str(i), str(i)) for i in items]
    return ", ".join(names)


def map_scale(val, scale_type="satisfaction", lang="ko"):
    if val is None or pd.isna(val):
        return ""
    try:
        val = int(val)
    except Exception:
        return str(val)
    if scale_type == "satisfaction":
        return SURVEY_METADATA["scale_5pt_satisfaction"][lang].get(val, str(val))
    elif scale_type == "recommendation":
        return SURVEY_METADATA["scale_5pt_recommendation"][lang].get(val, str(val))
    else:
        return SURVEY_METADATA["scale_5pt_agreement"][lang].get(val, str(val))


def map_conf_topic(val, lang="ko"):
    if val is None or pd.isna(val):
        return ""
    try:
        return SURVEY_METADATA["conf_q3_options"][lang].get(int(val), str(val))
    except Exception:
        return str(val)


def map_reg_topic(val, lang="ko"):
    if val is None or pd.isna(val):
        return ""
    try:
        return SURVEY_METADATA["reg_q3_options"][lang].get(int(val), str(val))
    except Exception:
        return str(val)


def generate_survey_excel(rows) -> io.BytesIO:
    """
    DB 응답 레코드 목록을 받아 전문적인 서식이 적용된 다중 시트 엑셀(.xlsx) 바이트 스트림 생성
    - 시트 1: 설문 응답 상세 (국문/영문 텍스트 라벨 매핑)
    - 시트 2: 통계 요약 (평균 점수, 응답자 분포 등)
    - 시트 3: 원천 데이터 (수치형 코드값 - SPSS, R, 통계분석용)
    """
    raw_list = [dict(r) for r in rows]
    df_raw = pd.DataFrame(raw_list)

    if df_raw.empty:
        df_display = pd.DataFrame(columns=["ID", "제출일시", "언어", "소재국가", "Invest KOREA 2026 총괄 만족도"])
        df_code = df_display.copy()
        df_stats = pd.DataFrame([{"항목": "응답 데이터 없음", "값": 0}])
    else:
        # 1. 텍스트 라벨이 적용된 Display용 DataFrame 구성
        display_records = []
        for r in raw_list:
            lang = r.get("lang") or "en"
            conf_factors = decode_json_list(r.get("conf_q2"))
            semi_factors = decode_json_list(r.get("semi_q2"))
            max_factors = decode_json_list(r.get("max_q2"))
            vc_factors = decode_json_list(r.get("vc_q2"))
            fin_factors = decode_json_list(r.get("fin_q2"))

            rec = {
                "ID": r.get("id"),
                "제출일시": r.get("submitted_at"),
                "언어": "English(EN)" if lang == "en" else "국문(KR)",
                "소재국가": r.get("country"),
                
                # 총괄 (문1)
                "Invest KOREA 2026 총괄 만족도": f"{r.get('q1_overall')}점 ({map_scale(r.get('q1_overall'), 'satisfaction', lang)})" if r.get('q1_overall') else "",
                
                # 세션 1: IKS 컨퍼런스 (문2-1, 2-2, 2-3, 2-4)
                "IKS 컨퍼런스 만족도": f"{r.get('conf_q1')}점 ({map_scale(r.get('conf_q1'), 'satisfaction', lang)})" if r.get('conf_q1') else "",
                "IKS 컨퍼런스 만족요인": map_factors(conf_factors, lang),
                "IKS 컨퍼런스 희망주제(1순위)": map_conf_topic(r.get("conf_q3_rank1"), lang),
                "IKS 컨퍼런스 희망주제(2순위)": map_conf_topic(r.get("conf_q3_rank2"), lang),
                "IKS 컨퍼런스 희망주제(3순위)": map_conf_topic(r.get("conf_q3_rank3"), lang),
                "IKS 컨퍼런스 희망주제(기타)": r.get("conf_q3_other") or "",
                "외투기업 애로사항": r.get("conf_q4") or "",
                
                # 세션 2: 지자체 IR
                "지자체IR 만족도": f"{r.get('reg_q1')}점 ({map_scale(r.get('reg_q1'), 'satisfaction', lang)})" if r.get('reg_q1') else "",
                "지자체IR 투자이해 도움": f"{r.get('reg_q2')}점 ({map_scale(r.get('reg_q2'), 'agreement', lang)})" if r.get('reg_q2') else "",
                "지자체IR 개선사항(1순위)": map_reg_topic(r.get("reg_q3_rank1"), lang),
                "지자체IR 개선사항(2순위)": map_reg_topic(r.get("reg_q3_rank2"), lang),
                "지자체IR 개선사항(기타)": r.get("reg_q3_other") or "",
                
                # 세션 3: 외투 환경 세미나
                "외투세미나 만족도": f"{r.get('semi_q1')}점 ({map_scale(r.get('semi_q1'), 'satisfaction', lang)})" if r.get('semi_q1') else "",
                "외투세미나 만족요인": map_factors(semi_factors, lang),
                "외투세미나 개선/제안": r.get("semi_q3") or "",
                
                # 세션 4: M.AX 에너지 전략 포럼
                "M.AX포럼 만족도": f"{r.get('max_q1')}점 ({map_scale(r.get('max_q1'), 'satisfaction', lang)})" if r.get('max_q1') else "",
                "M.AX포럼 만족요인": map_factors(max_factors, lang),
                "M.AX포럼 개선/제안": r.get("max_q3") or "",
                
                # 세션 5: 글로벌 VC 스타트업 포럼
                "글로벌VC포럼 만족도": f"{r.get('vc_q1')}점 ({map_scale(r.get('vc_q1'), 'satisfaction', lang)})" if r.get('vc_q1') else "",
                "글로벌VC포럼 만족요인": map_factors(vc_factors, lang),
                "글로벌VC포럼 개선/제안": r.get("vc_q3") or "",

                # [신규] 세션 6: 재무적 투자포럼
                "재무적투자포럼 만족도": f"{r.get('fin_q1')}점 ({map_scale(r.get('fin_q1'), 'satisfaction', lang)})" if r.get('fin_q1') else "",
                "재무적투자포럼 만족요인": map_factors(fin_factors, lang),
                "재무적투자포럼 개선/제안": r.get("fin_q3") or "",

                # 효과 및 성과
                "글로벌현안 파악기여도(6-1)": f"{r.get('eff_q1')}점 ({map_scale(r.get('eff_q1'), 'recommendation', lang)})" if r.get('eff_q1') else "",
                "향후사업 네트워크기여도(6-2)": f"{r.get('eff_q2')}점 ({map_scale(r.get('eff_q2'), 'recommendation', lang)})" if r.get('eff_q2') else "",
            }
            display_records.append(rec)
        df_display = pd.DataFrame(display_records)

        # 2. 통계 요약 DataFrame 생성
        total_count = len(df_raw)
        en_count = int((df_raw["lang"] == "en").sum())
        ko_count = int((df_raw["lang"] == "ko").sum())

        score_cols = {
            "Invest KOREA 2026 전반적 만족도": "q1_overall",
            "IKS 컨퍼런스 만족도 (세션1)": "conf_q1",
            "지자체 투자환경 IR 만족도 (세션2)": "reg_q1",
            "지자체 IR 투자이해 기여도": "reg_q2",
            "외투 환경 세미나 만족도 (세션3)": "semi_q1",
            "M.AX 에너지 전략 포럼 만족도 (세션4)": "max_q1",
            "글로벌 VC 스타트업 포럼 만족도 (세션5)": "vc_q1",
            "재무적 투자포럼 만족도 (세션6)": "fin_q1",
            "글로벌 현안 파악 기여도 (6-1)": "eff_q1",
            "향후 사업 및 네트워크 기여도 (6-2)": "eff_q2"
        }

        stats_rows = [
            {"지표 / 세션명": "총 응답자 수", "응답 건수": total_count, "평균 점수(5점 만점)": f"{total_count}명", "비고": "100%"},
            {"지표 / 세션명": "영문(EN) 응답자", "응답 건수": en_count, "평균 점수(5점 만점)": f"{(en_count/total_count*100):.1f}%", "비고": "-"},
            {"지표 / 세션명": "국문(KR) 응답자", "응답 건수": ko_count, "평균 점수(5점 만점)": f"{(ko_count/total_count*100):.1f}%", "비고": "-"},
        ]

        for label, col in score_cols.items():
            if col in df_raw.columns:
                series = pd.to_numeric(df_raw[col], errors='coerce').dropna()
                cnt = int(series.count())
                avg = f"{series.mean():.2f}" if cnt > 0 else "-"
                stats_rows.append({
                    "지표 / 세션명": label,
                    "응답 건수": cnt,
                    "평균 점수(5점 만점)": avg,
                    "비고": "5점 척도 리커트"
                })

        df_stats = pd.DataFrame(stats_rows)
        df_code = df_raw.copy()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_display.to_excel(writer, sheet_name="설문응답_상세", index=False)
        df_stats.to_excel(writer, sheet_name="만족도통계_요약", index=False)
        df_code.to_excel(writer, sheet_name="원천수치데이터_SPSS용", index=False)

        workbook = writer.book

        header_font = Font(name="맑은 고딕", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        cell_font = Font(name="맑은 고딕", size=10)
        thin_border = Border(
            left=Side(style='thin', color='D1D5DB'),
            right=Side(style='thin', color='D1D5DB'),
            top=Side(style='thin', color='D1D5DB'),
            bottom=Side(style='thin', color='D1D5DB')
        )

        for sheet in workbook.worksheets:
            sheet.views.sheetView[0].showGridLines = True
            for cell in sheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

            sheet.row_dimensions[1].height = 28

            for col in sheet.columns:
                max_len = 0
                col_letter = get_column_letter(col[0].column)
                for cell in col:
                    cell.border = thin_border
                    if cell.row > 1:
                        cell.font = cell_font
                        cell.alignment = Alignment(vertical="center")
                    val_str = str(cell.value or "")
                    line_len = max([len(line.encode('cp949', errors='ignore')) for line in val_str.split('\n')] or [0])
                    if line_len > max_len:
                        max_len = line_len

                sheet.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 45)

    output.seek(0)
    return output
