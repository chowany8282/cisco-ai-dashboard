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
            "Gemini 2.5 Flash Lite (추천/가성비)",
            "Gemini 2.5 Flash (표준)",
            "Gemini 3 Flash Preview (최신)",
        ),
    )
    if "Lite" in selected_model_name:
        MODEL_ID = "models/gemini-2.5-flash-lite"
    elif "Gemini 3" in selected_model_name:
        MODEL_ID = "models/gemini-3-flash-preview"
    else:
        MODEL_ID = "models/gemini-2.5-flash"

    st.success(f"현재 엔진: {MODEL_ID}")
    st.markdown("---")
    st.markdown("Created by Wan Hee Cho")

st.title("🛡️ Cisco Technical AI Dashboard")
st.markdown("네트워크 엔지니어를 위한 **로그 분석, 스펙 조회, OS 추천** 올인원 솔루션입니다.")

tab1, tab2, tab3 = st.tabs(["📊 로그 정밀 분석", "🔍 하드웨어 스펙 조회", "💿 OS 추천"])

with tab1:
    st.header("로그 분석 및 장애 진단")
    log_input = st.text_area("분석할 로그를 입력하세요:", height=150)
    if st.button("로그 분석 실행", key="btn_log"):
        if not log_input:
            st.warning("로그를 입력해주세요!")
        else:
            prompt = render_prompt(
                get_prompt_template("log_analysis.txt"),
                log_input=log_input,
            )
            with st.spinner(f"AI가 로그를 분석 중입니다... ({selected_model_name})"):
                try:
                    result = get_gemini_response(
                        prompt=prompt,
                        api_key=API_KEY_LOG,
                        model_id=MODEL_ID,
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
                        # backward compatibility for older prompt format
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
    st.header("장비 하드웨어 스펙 조회")
    model_input = st.text_input("장비 모델명 (예: C9300-48P)", key="input_spec")
    if st.button("스펙 조회 실행", key="btn_spec"):
        if not model_input:
            st.warning("모델명을 입력해주세요!")
        else:
            prompt = render_prompt(
                get_prompt_template("spec_lookup.txt"),
                model_input=model_input,
            )
            with st.spinner("데이터시트 검색 중..."):
                try:
                    result = get_gemini_response(
                        prompt=prompt,
                        api_key=API_KEY_SPEC,
                        model_id=MODEL_ID,
                    )
                except LLMError as e:
                    st.error("스펙 조회에 실패했습니다. 모델명/네트워크 상태를 확인해주세요.")
                    with st.expander("오류 상세"):
                        st.code(str(e))
                else:
                    st.markdown(result)

with tab3:
    st.header("OS 추천 및 안정성 진단")
    st.caption("💡 추천 OS와 안정성 등급을 확인하고, 우측 링크를 클릭하여 EOL 날짜를 검증하세요.")

    col1, col2 = st.columns(2)
    with col1:
        os_model = st.text_input("장비 모델명", placeholder="예: Nexus 93180YC-FX", key="os_model")
    with col2:
        os_ver = st.text_input("현재 버전 (선택)", placeholder="예: 17.06.01", key="os_ver")

    if st.button("OS 분석 실행", key="btn_os"):
        if not os_model:
            st.warning("장비 모델명은 필수입니다!")
        else:
            current_ver_query = (
                f"Cisco {os_model} {os_ver if os_ver else ''} Last Date of Support"
            )
            current_ver_url = (
                f"https://www.google.com/search?q={current_ver_query.replace(' ', '+')}"
            )
            prompt = render_prompt(
                get_prompt_template("os_recommendation.txt"),
                os_model=os_model,
                os_ver=(os_ver if os_ver else "정보 없음"),
                current_ver_url=current_ver_url,
            )

            with st.spinner("안정성(Stability) 데이터 분석 및 HTML 리포트 생성 중..."):
                try:
                    response_html = get_gemini_response(
                        prompt=prompt,
                        api_key=API_KEY_OS,
                        model_id=MODEL_ID,
                    )
                except LLMError as e:
                    st.error("OS 분석에 실패했습니다. 잠시 후 다시 시도해주세요.")
                    with st.expander("오류 상세"):
                        st.code(str(e))
                else:
                    safe_html = sanitize_basic_html(response_html)
                    st.markdown(safe_html, unsafe_allow_html=True)
