import json
import os
import re
from pathlib import Path
from urllib.parse import quote

import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.json"

st.set_page_config(
    page_title="رِواء | RIWAA",
    page_icon="ر",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "burgundy": "#641F2B",
    "burgundy_dark": "#46151E",
    "burgundy_soft": "#8D4B55",
    "brown": "#704C3D",
    "cream": "#F6F0E7",
    "paper": "#FFFDF9",
    "paper2": "#F1E7DC",
    "gold": "#B18B59",
    "ink": "#302522",
    "muted": "#776963",
    "line": "#E3D5C7",
    "danger": "#8B3E3E",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@400;700&family=Amiri:wght@400;700&display=swap');

html, body, [class*="css"] {{
    font-family: "Amiri", serif;
}}
.stApp {{
    background: {COLORS["cream"]};
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLORS["burgundy_dark"]} 0%, {COLORS["burgundy"]} 62%, #7A3943 100%);
    border: 0;
}}
section[data-testid="stSidebar"] * {{
    color: #FFF9F1 !important;
}}
.block-container {{
    padding-top: 0.7rem;
    padding-bottom: 4rem;
    max-width: 1240px;
}}
.brand {{
    padding: 30px 16px 18px;
    text-align: center;
}}
.brand-name {{
    font-family: "Aref Ruqaa", serif;
    font-size: 50px;
    line-height: 1;
}}
.brand-sub {{
    margin-top: 8px;
    font-size: 15px;
    opacity: .9;
}}
.nav-label {{
    margin: 24px 12px 10px;
    font-size: 13px;
    opacity: .68;
}}
div.stButton > button {{
    width: 100%;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,.16);
    background: rgba(255,255,255,.07);
    color: #FFF9F1;
    font-family: "Amiri", serif;
    font-size: 17px;
    padding: 10px 12px;
}}
div.stButton > button:hover {{
    background: rgba(255,255,255,.16);
    border-color: rgba(255,255,255,.28);
}}
.hero {{
    background: linear-gradient(135deg, #5A2029 0%, #78434A 100%);
    color: #FFF9F1;
    border-radius: 28px;
    padding: 44px 48px;
    margin: 16px 0 28px;
    box-shadow: 0 18px 50px rgba(57,31,27,.12);
}}
.hero-kicker {{
    font-family: Arial, sans-serif;
    letter-spacing: 2px;
    font-size: 11px;
    color: #E9D2AA;
}}
.hero-title {{
    font-family: "Aref Ruqaa", serif;
    font-size: 62px;
    line-height: 1;
    margin: 12px 0 12px;
}}
.hero-text {{
    font-size: 20px;
    line-height: 1.9;
    max-width: 760px;
}}
.page-kicker {{
    color: {COLORS["gold"]};
    font-family: Arial, sans-serif;
    letter-spacing: 2px;
    font-size: 11px;
    margin-top: 12px;
}}
.page-title {{
    font-family: "Aref Ruqaa", serif;
    color: {COLORS["burgundy"]};
    font-size: 48px;
    line-height: 1.15;
    margin: 4px 0;
}}
.page-sub {{
    color: {COLORS["muted"]};
    font-size: 18px;
    margin-bottom: 22px;
}}
.card {{
    background: {COLORS["paper"]};
    border: 1px solid {COLORS["line"]};
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(64,39,29,.06);
}}
.feature-title {{
    color: {COLORS["burgundy"]};
    font-family: "Aref Ruqaa", serif;
    font-size: 28px;
}}
.feature-text {{
    color: {COLORS["muted"]};
    font-size: 17px;
    line-height: 1.9;
}}
.chat-wrap {{
    background: rgba(255,255,255,.48);
    border: 1px solid {COLORS["line"]};
    border-radius: 26px;
    padding: 22px;
    min-height: 420px;
}}
.user-row {{
    display: flex;
    justify-content: flex-start;
    margin: 14px 0;
}}
.riwaa-row {{
    display: flex;
    justify-content: flex-end;
    margin: 14px 0;
}}
.user-bubble {{
    max-width: 74%;
    background: {COLORS["burgundy"]};
    color: #FFF9F1;
    padding: 13px 18px;
    border-radius: 20px 20px 5px 20px;
    font-size: 18px;
    line-height: 1.9;
}}
.riwaa-bubble {{
    max-width: 78%;
    background: {COLORS["paper"]};
    color: {COLORS["ink"]};
    border: 1px solid {COLORS["line"]};
    padding: 15px 20px;
    border-radius: 20px 20px 20px 5px;
    font-size: 18px;
    line-height: 1.95;
    box-shadow: 0 6px 20px rgba(64,39,29,.05);
}}
.bubble-label {{
    font-family: Arial, sans-serif;
    font-size: 11px;
    letter-spacing: 1px;
    margin-bottom: 4px;
    opacity: .7;
}}
.source-box {{
    background: {COLORS["paper2"]};
    border: 1px solid #DECBBB;
    border-radius: 15px;
    padding: 12px 15px;
    margin: 6px 0 16px;
    color: #493A34;
    font-size: 15px;
    line-height: 1.8;
}}
.source-head {{
    color: {COLORS["burgundy"]};
    font-weight: 700;
    margin-bottom: 3px;
}}
.abstain {{
    background: #F4E6E0;
    border: 1px solid #D7B7AA;
    border-radius: 16px;
    padding: 14px 16px;
    color: #5C312A;
    line-height: 1.9;
}}
.notice {{
    background: #F4ECE2;
    border: 1px solid {COLORS["line"]};
    border-radius: 16px;
    padding: 14px 16px;
    color: #55463F;
    line-height: 1.9;
}}
.small {{
    color: {COLORS["muted"]};
    font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)


def load_knowledge():
    if not KB_PATH.exists():
        return []
    try:
        data = json.loads(KB_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("entries", "items", "knowledge"):
            if isinstance(data.get(key), list):
                return data[key]
    return []


KB = load_knowledge()


def normalize(text):
    text = str(text or "").lower()
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    replacements = {
        "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
        "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    return text


def words(text):
    return set(re.findall(r"[\u0600-\u06FFa-zA-Z]{2,}", normalize(text)))


def entry_blob(entry):
    fields = []
    if isinstance(entry, dict):
        for key in ("title", "question", "answer", "content", "summary", "keywords", "domain"):
            value = entry.get(key, "")
            if isinstance(value, list):
                fields.extend(str(x) for x in value)
            else:
                fields.append(str(value))
    else:
        fields.append(str(entry))
    return " ".join(fields)


def retrieve(question, limit=4):
    q = normalize(question)
    q_words = words(question)
    scored = []
    for entry in KB:
        blob = normalize(entry_blob(entry))
        score = 0
        for word in q_words:
            if word in blob:
                score += 1
        if q and q in blob:
            score += 8
        if score:
            scored.append((score, entry))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [entry for score, entry in scored[:limit] if score > 0]


def get_answer(entry):
    if isinstance(entry, dict):
        for key in ("answer", "content", "summary", "text"):
            value = entry.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return str(entry).strip()


def get_source(entry):
    if not isinstance(entry, dict):
        return {"name": "قاعدة المعرفة في رِواء", "url": ""}
    return {
        "name": str(entry.get("source_name") or entry.get("source") or entry.get("reference") or "مصدر موثق"),
        "url": str(entry.get("source_url") or entry.get("url") or ""),
        "location": str(entry.get("source_location") or entry.get("location") or ""),
    }


def is_personal_or_fatwa(question):
    q = normalize(question)
    patterns = [
        "هل يجوز لي", "هل يجوز لي ان", "ماذا افعل انا", "حكمي", "حكم حالتي",
        "زوجي", "زوجتي", "طلاق", "ميراثي", "ميراث", "فتوى", "اكفر", "كافر",
        "هل انا", "هل اكون", "علي كفاره", "علي كفارة",
    ]
    return any(p in q for p in patterns)


def local_answer(question):
    if is_personal_or_fatwa(question):
        return {
            "answer": "هذا السؤال قد يتعلق بحالة شخصية أو فتوى، ولذلك لا تصدر رِواء حكمًا فرديًا. يمكنها تقديم معلومات عامة موثقة، أما الحكم على الحالة نفسها فيحتاج إلى مختص مؤهل.",
            "sources": [],
            "abstain": True,
            "reason": "personal_case",
        }

    matches = retrieve(question)
    if not matches:
        return {
            "answer": "لم أجد في قاعدة المعرفة الحالية مادة موثقة تكفي للإجابة عن هذا السؤال. لن أنشئ إجابة من خارج المصادر المعتمدة.",
            "sources": [],
            "abstain": True,
            "reason": "insufficient_evidence",
        }

    best = matches[0]
    answer = get_answer(best)
    if not answer:
        return {
            "answer": "وجدت مادة مرتبطة بالسؤال، لكن بياناتها لا تحتوي على إجابة كافية. لذلك أتوقف بدل إنشاء معلومة غير موثقة.",
            "sources": [],
            "abstain": True,
            "reason": "empty_entry",
        }

    sources = []
    for entry in matches:
        source = get_source(entry)
        if source["name"] not in [x["name"] for x in sources]:
            sources.append(source)

    return {"answer": answer, "sources": sources, "abstain": False, "reason": "retrieved"}


def openai_answer(question):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or OpenAI is None:
        return None

    matches = retrieve(question, limit=5)
    if not matches:
        return None

    context_parts = []
    source_list = []
    for i, entry in enumerate(matches, 1):
        source = get_source(entry)
        context_parts.append(
            f"[مادة {i}]\nالعنوان: {entry.get('title','') if isinstance(entry,dict) else ''}\n"
            f"المحتوى: {get_answer(entry)}\nالمصدر: {source['name']}\n"
        )
        source_list.append(source)

    client = OpenAI(api_key=api_key)
    system = """أنت رِواء، مساعد تعليمي عربي قائم على الاسترجاع من مصادر محددة.
قواعدك:
1) أجب فقط اعتمادًا على المواد المسترجعة في السياق.
2) لا تضف معلومة شرعية من معرفتك العامة.
3) لا تخترع نصًا أو حديثًا أو نسبة إلى مصدر.
4) إذا كان الدليل غير كافٍ، قل بوضوح إن المعلومات المتاحة لا تكفي.
5) لا تصدر فتوى شخصية أو حكمًا فرديًا؛ أحل الحالة إلى مختص.
6) فرّق بين النص المنقول والشرح التعليمي.
7) لا تقل إنك مفتي أو عالم.
اكتب جوابًا عربيًا واضحًا ومختصرًا ومناسبًا للتعلم."""
    user = f"السؤال:\n{question}\n\nالمواد المسترجعة:\n" + "\n".join(context_parts)

    try:
        response = client.responses.create(
            model="gpt-5.6-mini",
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        text = response.output_text.strip()
        if not text:
            return None
        return {"answer": text, "sources": source_list, "abstain": False, "reason": "rag_ai"}
    except Exception:
        return None


def answer_question(question):
    ai = openai_answer(question)
    if ai:
        return ai
    return local_answer(question)


def render_sources(sources):
    if not sources:
        return ""
    rows = []
    for source in sources:
        name = source["name"]
        url = source.get("url", "")
        location = source.get("location", "")
        if url:
            rows.append(f'• <a href="{url}" target="_blank">{name}</a>')
        else:
            rows.append(f"• {name}")
        if location:
            rows.append(f'<span class="small">الموضع: {location}</span>')
    return '<div class="source-box"><div class="source-head">المصادر</div>' + "<br>".join(rows) + "</div>"


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="brand">
            <div class="brand-name">رِواء</div>
            <div class="brand-sub">رفيقك إلى المعرفة الإسلامية الموثوقة</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-label">التجربة</div>', unsafe_allow_html=True)
        pages = [
            ("الرئيسية", "home"),
            ("اسأل رِواء", "ask"),
            ("استكشف القرآن", "quran"),
            ("المصادر", "sources"),
            ("سجل الأسئلة", "history"),
            ("عن رِواء", "about"),
        ]
        for label, key in pages:
            if st.button(label, key=f"nav_{key}"):
                st.session_state.page = key
                st.rerun()

        st.markdown('<div class="nav-label">الحساب</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:0 14px;font-size:16px;">زائر · لا يلزم تسجيل الدخول</div>', unsafe_allow_html=True)


def home_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">RIWAA · SOURCE-GROUNDED ISLAMIC LEARNING</div>
        <div class="hero-title">رِواء</div>
        <div class="hero-text">تجربة تفاعلية للمعرفة الإسلامية تبدأ من السؤال، وتعود إلى المصدر، وتمتنع عندما لا يكفي الدليل.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><div class="feature-title">اسأل رِواء</div><div class="feature-text">محادثة تعليمية مع استرجاع من قاعدة معرفة محددة المصادر.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="feature-title">استكشف القرآن</div><div class="feature-text">مساحة للقراءة والبحث مع ربط تجربة القرآن بمصدر معتمد.</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><div class="feature-title">تحقّق من المصدر</div><div class="feature-text">كل إجابة مدعومة بمادة مصدرية، وعند نقص الدليل يحدث الامتناع.</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="notice"><b>مبدأ رِواء:</b> المصدر قبل النموذج. رِواء ليست مفتيًا ولا تصدر أحكامًا شخصية في الحالات الفردية.</div>', unsafe_allow_html=True)


def ask_page():
    st.markdown('<div class="page-kicker">ASK RIWAA</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">اسأل رِواء</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">اكتب سؤالك بطريقة طبيعية. ستظهر المحادثة هنا مثل تطبيقات الدردشة، مع المصدر تحت الإجابة.</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:70px 20px;color:#776963;">
            <div style="font-family:'Aref Ruqaa';font-size:38px;color:#641F2B;">مرحبًا بك في رِواء</div>
            <div style="font-size:18px;margin-top:8px;">ابدأ بسؤالك، وستبقى المحادثة أمامك مع مصادرها.</div>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-row"><div class="user-bubble"><div class="bubble-label" style="color:#F0D8B4;">أنت</div>{message["text"]}</div></div>',
                unsafe_allow_html=True
            )
        else:
            source_html = render_sources(message.get("sources", []))
            if message.get("abstain"):
                body = f'<div class="abstain">{message["text"]}</div>'
            else:
                body = message["text"]
            st.markdown(
                f'<div class="riwaa-row"><div style="max-width:80%;"><div class="riwaa-bubble"><div class="bubble-label" style="color:#704C3D;">رِواء</div>{body}</div>{source_html}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.chat_input("اكتب سؤالك هنا…")
    if prompt:
        st.session_state.messages.append({"role": "user", "text": prompt})
        result = answer_question(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "text": result["answer"],
            "sources": result["sources"],
            "abstain": result["abstain"],
        })
        st.session_state.history.append({
            "question": prompt,
            "answer": result["answer"],
            "sources": result["sources"],
        })
        st.rerun()

    if st.session_state.messages:
        if st.button("بدء محادثة جديدة"):
            st.session_state.messages = []
            st.rerun()


def quran_page():
    st.markdown('<div class="page-kicker">QURAN EXPERIENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">استكشف القرآن</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">تجربة مرتبطة بالموسوعة القرآنية، مع فصل واضح بين النص القرآني والشرح.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="feature-title">قراءة وبحث</div>
        <div class="feature-text">
        يمكن للمستخدم الانتقال إلى المصحف والبحث في السور والآيات من المصدر القرآني المعتمد.
        رِواء لا تنسخ نصًا قرآنيًا من مصدر غير موثق إلى الواجهة.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    q = st.text_input("ابحث عن سورة أو موضوع قرآني", placeholder="مثال: سورة الفاتحة")
    if q:
        url = "https://quranpedia.net/search?q=" + quote(q)
        st.markdown(
            f'<div class="notice">نتيجة البحث من المصدر: <a href="{url}" target="_blank">فتح البحث في الموسوعة القرآنية</a></div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="card" style="margin-top:18px;">
        <div class="feature-title">المصدر القرآني</div>
        <div class="feature-text">الموسوعة القرآنية — quranpedia.net</div>
    </div>
    """, unsafe_allow_html=True)


def sources_page():
    st.markdown('<div class="page-kicker">SOURCE FRAMEWORK</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">المصادر</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">مصادر الإطار العلمي المستخدمة في تصميم رِواء، مع توضيح أن قاعدة المعرفة الحالية هي التي تحدد ما يمكن الإجابة عنه.</div>', unsafe_allow_html=True)

    official_sources = [
        ("الموسوعة القرآنية", "Quranpedia", "https://quranpedia.net/"),
        ("الموسوعة الحديثية", "الدرر السنية", "https://dorar.net/hadith-category"),
        ("الموسوعة العقدية", "الدرر السنية", "https://dorar.net/aqeeda"),
        ("مجمع الملك فهد لطباعة المصحف الشريف", "King Fahd Quran Complex", "https://qurancomplex.gov.sa/"),
    ]

    for title, name, url in official_sources:
        st.markdown(
            f'<div class="card" style="margin:12px 0;"><div class="feature-title">{title}</div><div class="feature-text">{name}<br><a href="{url}" target="_blank">فتح المصدر</a></div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="notice" style="margin-top:18px;"><b>حدود الإجابة:</b> وجود رابط للمصدر لا يعني أن رِواء تستخدم كل محتواه تلقائيًا. الإجابة يجب أن تمر عبر قاعدة المعرفة المرتبطة بالمشروع.</div>', unsafe_allow_html=True)


def history_page():
    st.markdown('<div class="page-kicker">QUESTION HISTORY</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">سجل الأسئلة</div>', unsafe_allow_html=True)
    history = st.session_state.get("history", [])

    if not history:
        st.markdown('<div class="card"><div class="feature-title">لا توجد أسئلة بعد</div><div class="feature-text">ابدأ محادثة مع رِواء وستظهر الأسئلة هنا.</div></div>', unsafe_allow_html=True)
        return

    for item in reversed(history):
        st.markdown(
            f'<div class="card" style="margin:12px 0;"><div class="feature-title" style="font-size:24px;">{item["question"]}</div><div class="feature-text">{item["answer"]}</div></div>',
            unsafe_allow_html=True
        )


def about_page():
    st.markdown('<div class="page-kicker">ABOUT RIWAA</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">عن رِواء</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="feature-title">فكرة رِواء</div>
        <div class="feature-text">
        رِواء تجربة تعليمية تفاعلية تهدف إلى تسهيل الوصول إلى المعرفة الإسلامية الموثوقة.
        تعتمد على الاسترجاع من مواد محددة المصادر، وتعرض المصدر، وتمتنع عندما لا يكفي الدليل.
        </div>
        <br>
        <div class="notice">رِواء أداة تعليمية مدعومة بالذكاء الاصطناعي وليست بديلًا عن المختص في الفتاوى أو الحالات الشخصية.</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    render_sidebar()

    pages = {
        "home": home_page,
        "ask": ask_page,
        "quran": quran_page,
        "sources": sources_page,
        "history": history_page,
        "about": about_page,
    }
    pages.get(st.session_state.page, home_page)()


if __name__ == "__main__":
    main()
