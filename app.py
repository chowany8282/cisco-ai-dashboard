import datetime
from pathlib import Path

import streamlit as st

from services.llm import LLMError, get_gemini_response
from services.parsers import parse_log_analysis, sanitize_basic_html
from services.schemas import validate_log_analysis_json

# ========================================================
# 🎨 페이지 기본 설정
# ========================================================
st.set_page_config(page_title="Cisco AI Master System", page_icon="🛡️", layout="wide")

PROMPT_DIR = Path("prompts")
USAGE_KEYS = ["select_cnt", "log_cnt", "spec_cnt", "os_cnt"]


def load_prompt(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8")


@st.cache_data(show_spinner=False)
def get_prompt_template(name: str) -> str:
    return load_prompt(name)


def render_prompt(template: str, **values: str) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{key}}}", value)
    return rendered


@st.cache_resource
def get_shared_store() -> dict:
    return {
        "date": "",
        "stats": {key: 0 for key in USAGE_KEYS},
    }


def clear_log_input() -> None:
    st.session_state["raw_log_area"] = ""


def clear_analysis_input() -> None:
    st.session_state["log_analysis_area"] = ""


def clear_spec_input() -> None:
    st.session_state["input_spec"] = ""


def clear_os_input() -> None:
    st.session_state["os_model"] = ""
    st.session_state["os_ver"] = ""


def llm_with_count(prompt: str, api_key: str, model_id: str, count_key: str) -> str:
    response = get_gemini_response(prompt=prompt, api_key=api_key, model_id=model_id)
    shared_data["stats"][count_key] += 1
    return response


shared_data = get_shared_store()
kst_now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
today_str = kst_now.strftime("%Y-%m-%d")

if shared_data["date"] != today_str:
    shared_data["date"] = today_str
    for key in USAGE_KEYS:
        shared_data["stats"][key] = 0

try:
    API_KEY_LOG = st.secrets["API_KEY_LOG"]
    API_KEY_SPEC = st.secrets["API_KEY_SPEC"]
    API_KEY_OS = st.secrets["API_KEY_OS"]
except Exception:
    st.error("🚨 API 키를 찾을 수 없습니다.")
    st.info("로컬 실행 시: .streamlit/secrets.toml 파일을 생성하세요.")
    st.info("배포 시: Streamlit Cloud 설정의 'Secrets' 메뉴에 키를 입력하세요.")
    st.stop()

with st.sidebar:
    st.header("🤖 엔진 설정")
    selected_model_name = st.selectbox(
        "사용할 AI 모델을 선택하세요:",
        (
            "Gemini 3.0 Pro (최고 성능/정밀 분석용)",
            "Gemini 2.5 Flash (표준/균형)",
            "Gemini 2.5 Lite (초고속/가성비)",
        ),
    )

    if "3.0 Pro" in selected_model_name:
        MODEL_ID = "models/gemini-3-flash-preview"
    elif "2.5 Lite" in selected_model_name:
        MODEL_ID = "models/gemini-2.5-flash-lite"
    else:
        MODEL_ID = "models/gemini-2.5-flash"

    st.success(f"현재 엔진: {selected_model_name}")
    st.caption(f"System ID: {MODEL_ID}")

    st.markdown("---")
    st.markdown("### 📊 일일 누적 사용량")
    st.caption(f"📅 {today_str} 기준")
    st.text(f"⚡ 로그분석: {shared_data['stats']['select_cnt']}회")
    st.text(f"📊 정밀진단: {shared_data['stats']['log_cnt']}회")
    st.text(f"🔍 스펙조회: {shared_data['stats']['spec_cnt']}회")
    st.text(f"💿 OS 추천: {shared_data['stats']['os_cnt']}회")

    st.markdown("---")
    st.markdown("Created by Wan Hee Cho")

st.title("🛡️Cisco Technical")

tab0, tab1, tab2, tab3 = st.tabs(["📑 로그 분류", "📊 로그 진단", "🔍 하드웨어 스펙", "💿 OS 추천"])

with tab0:
    st.header("📑 로그 핵심 요약 (Summary & Attention)")
    st.caption("로그 파일을 분석하여 **전체 요약**과 **주의가 필요한 로그**만 추출합니다.")

    uploaded_file = st.file_uploader("📂 로그 파일 업로드 (txt, log)", type=["txt", "log"])
    raw_log_input = st.text_area(
        "📝 또는 여기에 로그를 직접 붙여넣으세요:",
        height=200,
        key="raw_log_area",
    )

    col_btn1, col_btn2 = st.columns([1, 6])
    with col_btn1:
        run_btn = st.button("분석 실행", key="btn_classify")
    with col_btn2:
        st.button("🗑️ 입력창 지우기", on_click=clear_log_input, key="clr_class")

    if run_btn:
        final_log_content = ""
        if uploaded_file is not None:
            try:
                final_log_content = uploaded_file.getvalue().decode("utf-8")
                st.info(f"📂 업로드된 파일 '{uploaded_file.name}'을 분석합니다.")
            except Exception as e:
                st.error(f"파일 오류: {e}")
        elif raw_log_input:
            final_log_content = raw_log_input

        if not final_log_content:
            st.warning("분석할 로그를 입력해주세요!")
        else:
            with st.spinner(f"🤖 AI({MODEL_ID.split('/')[-1]})가 핵심 내용만 요약 중입니다..."):
                classify_prompt = f"""
당신은 Cisco 네트워크 엔지니어입니다.
아래 로그 파일을 분석하여 **딱 두 가지 항목**으로만 요약하세요.

[출력 형식 가이드]
1. **전체 요약 (Executive Summary):**
- 로그의 전반적인 상태(정상/장애/작업 등)를 3~5줄로 명확히 요약하세요.

2. **주요 주의 사항 (Attention Required):**
- Error, Warning, Fail, Traceback 등 엔지니어가 확인해야 할 로그만 추출하세요.
- **[중요]** 특정 로그 메시지를 인용할 때는 반드시 **코드 블록(```)**으로 감싸서 출력하세요.

[제외 대상]
- 타임라인, 운영 맥락, 결론 등은 모두 생략하세요.
- 의미 없는 반복 로그는 하나로 합치세요.

[입력 데이터]
{final_log_content}
"""
                try:
                    classified_result = llm_with_count(
                        prompt=classify_prompt,
                        api_key=API_KEY_LOG,
                        model_id=MODEL_ID,
                        count_key="select_cnt",
                    )
                    st.session_state["classified_result"] = classified_result
                except LLMError as e:
                    st.error("로그 분류에 실패했습니다. 잠시 후 다시 시도해주세요.")
                    with st.expander("오류 상세"):
                        st.code(str(e))

    if "classified_result" in st.session_state:
        st.markdown("---")
        col_copy_btn, _ = st.columns([2, 5])
        with col_copy_btn:
            if st.button("📝 분석 결과 전체 복사"):
                st.session_state["log_transfer"] = st.session_state["classified_result"]
                st.success("✅ 복사 완료! '로그 진단' 탭에서 사용할 수 있습니다.")

        st.subheader("🎯 핵심 분석 결과")
        st.markdown(st.session_state["classified_result"])

with tab1:
    st.header("📊 로그 정밀 진단 & 솔루션")
    default_log_value = st.session_state.get("log_transfer", "")
    log_input = st.text_area(
        "분석할 로그(또는 위에서 복사한 내용)를 입력하세요:",
        value=default_log_value,
        height=150,
        key="log_analysis_area",
    )

    c1, c2 = st.columns([1, 6])
    with c1:
        btn_run_log = st.button("정밀 진단 실행", key="btn_log")
    with c2:
        st.button("🗑️ 입력창 지우기", on_click=clear_analysis_input, key="clr_anal")

    if btn_run_log:
        if not log_input:
            st.warning("로그를 입력해주세요!")
        else:
            prompt = render_prompt(
                get_prompt_template("log_analysis.txt"),
                log_input=log_input,
            )
            with st.spinner("AI가 정밀 진단 중입니다..."):
                try:
                    result = llm_with_count(
                        prompt=prompt,
                        api_key=API_KEY_LOG,
                        model_id=MODEL_ID,
                        count_key="log_cnt",
                    )
                except LLMError as e:
                    st.error("로그 분석에 실패했습니다. 잠시 후 다시 시도해주세요.")
                    with st.expander("오류 상세"):
                        st.code(str(e))
                else:
                    parsed_json = validate_log_analysis_json(result)
                    if parsed_json:
                        st.subheader("🔴 발생 원인")
                        st.error(parsed_json.part1)
                        st.subheader("🟡 네트워크 영향")
                        st.warning(parsed_json.part2)
                        st.subheader("🟢 권장 조치")
                        st.success(parsed_json.part3)
                    else:
                        parsed_legacy = parse_log_analysis(result)
                        if parsed_legacy:
                            st.subheader("🔴 발생 원인")
                            st.error(parsed_legacy["part1"])
                            st.subheader("🟡 네트워크 영향")
                            st.warning(parsed_legacy["part2"])
                            st.subheader("🟢 권장 조치")
                            st.success(parsed_legacy["part3"])
                        else:
                            st.info("구조화 파싱에 실패하여 원문을 표시합니다.")
                            st.markdown(result)

with tab2:
    st.header("🔍 장비 하드웨어 스펙 조회")
    model_input = st.text_input("장비 모델명 (예: C9300-48P)", key="input_spec")

    c1, c2 = st.columns([1, 6])
    with c1:
        btn_run_spec = st.button("스펙 조회 실행", key="btn_spec")
    with c2:
        st.button("🗑️ 입력창 지우기", on_click=clear_spec_input, key="clr_spec")

    if btn_run_spec:
        if not model_input:
            st.warning("모델명을 입력해주세요!")
        else:
            prompt = render_prompt(
                get_prompt_template("spec_lookup.txt"),
                model_input=model_input,
            )
            with st.spinner("데이터시트 검색 중..."):
                try:
                    result = llm_with_count(
                        prompt=prompt,
                        api_key=API_KEY_SPEC,
                        model_id=MODEL_ID,
                        count_key="spec_cnt",
                    )
                except LLMError as e:
                    st.error("스펙 조회에 실패했습니다. 모델명/네트워크 상태를 확인해주세요.")
                    with st.expander("오류 상세"):
                        st.code(str(e))
                else:
                    st.markdown(result)

with tab3:
    st.header("💿 OS 추천 및 안정성 진단")

    device_family = st.radio(
        "장비 계열 선택 (Device Family)",
        ("Catalyst (IOS-XE)", "Nexus (NX-OS)"),
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        os_model = st.text_input("장비 모델명", placeholder="예: C9300-48P", key="os_model")
    with col2:
        os_ver = st.text_input("현재 버전 (선택)", placeholder="예: 17.09.04a", key="os_ver")

    c1, c2 = st.columns([1, 6])
    with c1:
        btn_run_os = st.button("OS 분석 실행", key="btn_os")
    with c2:
        st.button("🗑️ 입력창 지우기", on_click=clear_os_input, key="clr_os")

    if btn_run_os:
        if not os_model:
            st.warning("장비 모델명은 필수입니다!")
        else:
            if "Nexus" in device_family:
                family_prompt = (
                    "당신은 Cisco Nexus(NX-OS) 전문가입니다. 반드시 **NX-OS 버전**만 추천하세요."
                )
            else:
                family_prompt = (
                    "당신은 Cisco Catalyst(IOS-XE) 전문가입니다. "
                    "반드시 **IOS-XE 버전**만 추천하세요."
                )

            prompt = f"""
{family_prompt}
다음 장비의 **OS 소프트웨어**를 분석하여 **HTML Table** 코드로 출력하세요.

[필수 지침]
1. 오직 HTML 코드만 출력하세요.
2. 테이블 스타일: <table border='1' style='width:100%; border-collapse:collapse; text-align:left;'>

[분석 내용]
- MD 및 Gold Star 버전 최우선 추천.
- 안정성 등급 별점(⭐⭐⭐⭐⭐) 표시.

[대상 장비]: {os_model} ({device_family})
[현재 OS 버전]: {os_ver if os_ver else '정보 없음'}

<h3>1. 현재 버전 상태</h3>
<table>...</table>
<br>
<h3>2. 추천 OS (Recommended Releases)</h3>
<table>...</table>
"""
            with st.spinner("추천 버전을 검색 중..."):
                try:
                    response_html = llm_with_count(
                        prompt=prompt,
                        api_key=API_KEY_OS,
                        model_id=MODEL_ID,
                        count_key="os_cnt",
                    )
                except LLMError as e:
                    st.error("OS 분석에 실패했습니다. 잠시 후 다시 시도해주세요.")
                    with st.expander("오류 상세"):
                        st.code(str(e))
                else:
                    response_html = response_html.replace("```html", "").replace("```", "")
                    safe_html = sanitize_basic_html(response_html)
                    st.markdown(safe_html, unsafe_allow_html=True)
