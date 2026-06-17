import asyncio
import os
import sys
import streamlit as st
import chromadb
import pandas as pd
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

CHROMA_DIR = "./chroma_db"
WO_COLLECTION = "work_orders"
TOP_K = 15

AZURE_KEY        = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_ENDPOINT   = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_DEPLOY     = os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT", "embed-model")
AZURE_LLM_DEPLOY = os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT", "gpt-4o")

RECENCY_KEYWORDS = {
    "recent", "latest", "last", "newest", "most recent",
    "this week", "this month", "today", "yesterday", "just", "ago",
}

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="GMES Agent",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — Claude-inspired warm theme
# ---------------------------------------------------------------------------

st.markdown("""
<style>
/* ── Fonts & base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui,
                 "Helvetica Neue", Arial, sans-serif;
}

/* ── Hide Streamlit chrome ────────────────────────────────────────── */
#MainMenu                            { visibility: hidden; }
footer                               { visibility: hidden; }
[data-testid="stToolbar"]            { display: none !important; }
[data-testid="stDecoration"]         { display: none !important; }
[data-testid="stStatusWidget"]       { display: none !important; }

/* ── Page background ──────────────────────────────────────────────── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #F5F4EF;
}

/* ── Main content width & spacing ────────────────────────────────── */
.main .block-container {
    max-width: 820px;
    padding-top: 1.25rem;
    padding-bottom: 6rem;
    margin: 0 auto;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #EEECE3 !important;
    border-right: 1px solid #D8D4C8;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.75rem;
}
[data-testid="stSidebar"] hr {
    border-color: #D8D4C8;
    margin: 0.75rem 0;
}

/* ── Chat messages ────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E8E4DA;
    margin-bottom: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    padding: 4px 6px;
}

/* User messages — warm tint */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #EDE9DF;
    border-color: #DDD9CE;
}

/* ── Chat input ───────────────────────────────────────────────────── */
[data-testid="stChatInputContainer"] {
    background: #F5F4EF;
    border-top: 1px solid #E0DDD5;
    padding-top: 10px;
}
[data-testid="stChatInputContainer"] textarea {
    border-radius: 20px !important;
    border: 1.5px solid #D0CCC0 !important;
    background: #FFFFFF !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
    padding: 10px 16px !important;
    resize: none !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
[data-testid="stChatInputContainer"] textarea:focus {
    border-color: #CC785C !important;
    box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.12) !important;
    outline: none !important;
}

/* ── Tabs ─────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1.5px solid #E0DDD5;
    gap: 2px;
    margin-bottom: 1rem;
}
[data-testid="stTabs"] button[role="tab"] {
    font-size: 14px;
    font-weight: 500;
    color: #7A7568;
    border: none;
    background: transparent;
    border-radius: 8px 8px 0 0;
    padding: 8px 18px;
    margin-bottom: -1.5px;
    transition: color 0.15s ease, background 0.15s ease;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #1A1A1A;
    background: #E8E4DA;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #CC785C;
    border-bottom: 2px solid #CC785C;
    background: transparent;
    font-weight: 600;
}

/* ── Expanders ────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #E5E1D6 !important;
    border-radius: 10px !important;
    background: #FAFAF6 !important;
}
[data-testid="stExpander"] summary {
    font-size: 13.5px;
    color: #5A574F;
    font-weight: 500;
}

/* ── Sidebar widgets ──────────────────────────────────────────────── */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSelectbox > label {
    font-size: 13.5px;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid #C8C4B8;
    color: #3A3830;
    border-radius: 8px;
    font-size: 13.5px;
    transition: background 0.15s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #E0DDD5;
    border-color: #B8B4A8;
}

/* ── Analytics: metric cards ──────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E1D6;
    border-radius: 10px;
    padding: 14px 18px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: #1A1A1A !important;
}
[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    color: #7A7568 !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Widgets (analytics tab) ──────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    border-radius: 8px;
    border-color: #D0CCC0;
    background: #FAFAF6;
    font-size: 14px;
}
[data-testid="stTextInput"] input {
    border-radius: 8px;
    border-color: #D0CCC0;
    background: #FAFAF6;
    font-size: 14px;
}
[data-testid="stTextInput"] input:focus {
    border-color: #CC785C;
    box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.12);
}
[data-testid="stDateInput"] input {
    border-radius: 8px;
    border-color: #D0CCC0;
    background: #FAFAF6;
    font-size: 14px;
}

/* ── Charts ───────────────────────────────────────────────────────── */
[data-testid="stArrowVegaLiteChart"],
[data-testid="stVegaLiteChart"] {
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E5E1D6;
    padding: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

/* ── Alerts & info boxes ──────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px;
    font-size: 14px;
}

/* ── Code blocks ──────────────────────────────────────────────────── */
code {
    background: #EDE9DF;
    border-radius: 5px;
    padding: 2px 6px;
    font-size: 12.5px;
    color: #8B4513;
}

/* ── Dividers ─────────────────────────────────────────────────────── */
hr { border-color: #E0DDD5; }

/* ── Dataframe ────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #E5E1D6;
    overflow: hidden;
}

/* ── Success / warning callouts ───────────────────────────────────── */
.stSuccess { border-radius: 8px; }
.stWarning { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Azure client — hard fail if missing
# ---------------------------------------------------------------------------

if not (AZURE_KEY and AZURE_ENDPOINT):
    st.error(
        "**Azure OpenAI credentials missing.**  \n"
        "Set `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in your `.env` file."
    )
    st.stop()

_azure_client = AzureOpenAI(
    api_key=AZURE_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version="2024-12-01-preview",
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading knowledge base…")
def load_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(WO_COLLECTION)


@st.cache_data(show_spinner="Loading analytics data…", ttl=300)
def load_metadata_df(_collection) -> pd.DataFrame:
    total = _collection.count()
    all_meta = []
    for offset in range(0, total, 1000):
        res = _collection.get(limit=1000, offset=offset, include=["metadatas"])
        all_meta.extend(res["metadatas"])
    df = pd.DataFrame(all_meta)
    if "date_ts" in df.columns:
        df["date_parsed"] = pd.to_datetime(df["date_ts"], unit="s", errors="coerce")
    return df

# ---------------------------------------------------------------------------
# Chat helpers
# ---------------------------------------------------------------------------

def is_recency_query(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in RECENCY_KEYWORDS)


def rewrite_query(user_input: str, history: list) -> str:
    if len(history) < 2:
        return user_input
    context = ""
    for msg in history[-4:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content'][:400]}\n"
    prompt = (
        "You are a search query rewriter for a maintenance work order database.\n"
        "Rewrite the latest message into a fully self-contained search query, resolving "
        "any references like 'same machine', 'that equipment', 'last issue'.\n"
        "Return ONLY the rewritten query.\n\n"
        f"History:\n{context}\nLatest: {user_input}\nRewritten:"
    )
    resp = _azure_client.chat.completions.create(
        model=AZURE_LLM_DEPLOY,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=100,
    )
    return resp.choices[0].message.content.strip()


def embed_query(query: str) -> list:
    resp = _azure_client.embeddings.create(model=AZURE_DEPLOY, input=[query])
    return resp.data[0].embedding


def retrieve_context(query: str, collection, top_k: int = TOP_K) -> list:
    embedding = embed_query(query)
    fetch_k = top_k * 3 if is_recency_query(query) else top_k
    results = collection.query(
        query_embeddings=[embedding],
        n_results=fetch_k,
        include=["documents", "metadatas"],
    )
    items = [
        {
            "text":       doc,
            "ref":        f"WO #{m.get('wo_no','?')} | {m.get('equipment','?')} | {m.get('date','?')}",
            "date_ts":    m.get("date_ts", 0),
            "date":       m.get("date", "?"),
            "wo_no":      m.get("wo_no", "?"),
            "equipment":  m.get("equipment", "?"),
            "maint_type": m.get("maint_type", "?"),
            "line":       m.get("line", "?"),
            "group":      m.get("group", "?"),
        }
        for doc, m in zip(results["documents"][0], results["metadatas"][0])
    ]
    if is_recency_query(query):
        items = sorted(items, key=lambda x: x["date_ts"], reverse=True)[:top_k]
    return items


SYSTEM_BASE = (
    "You are an expert maintenance technician assistant for LG Electronics TN Production Engineering. "
    "You have access to historical work order records from GMES. "
    "When answering: identify similar past failures and resolutions, reference specific WO numbers and "
    "equipment IDs, suggest likely causes based on historical patterns, give step-by-step guidance based "
    "on what has worked before. If no relevant history exists, clearly say so."
)


def build_messages(query: str, items: list, history: list) -> list:
    context = "\n".join(f"\n--- {i['ref']} ---\n{i['text']}" for i in items)
    messages = [{"role": "system", "content": f"{SYSTEM_BASE}\n\nRELEVANT WORK ORDERS:\n{context}"}]
    for msg in history:
        if msg["role"] in ("user", "assistant"):
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})
    return messages


def call_llm(messages: list, model_name: str = None) -> str:
    resp = _azure_client.chat.completions.create(
        model=model_name or AZURE_LLM_DEPLOY,
        messages=messages,
        temperature=0.2,
        max_tokens=1500,
    )
    return resp.choices[0].message.content


def render_wo_cards(items: list):
    for i, item in enumerate(items):
        cols = st.columns([1, 3])
        with cols[0]:
            st.markdown(f"**WO #{item['wo_no']}**")
            st.caption(item["date"])
            st.markdown(f"*{item['maint_type']}*")
        with cols[1]:
            st.markdown(f"🔧 **{item['equipment']}**")
            st.markdown(f"Line: {item['line']} · Group: {item['group']}")
            st.markdown(item["text"][:400] + ("…" if len(item["text"]) > 400 else ""))
        if i < len(items) - 1:
            st.divider()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    # Branding
    st.markdown("""
    <div style="padding: 0.25rem 0 1.25rem 0;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:36px; height:36px; background:#CC785C; border-radius:9px;
                        display:flex; align-items:center; justify-content:center;
                        font-size:20px; flex-shrink:0;">🔧</div>
            <div>
                <div style="font-weight:700; font-size:15px; color:#1A1A1A;
                            letter-spacing:-0.01em;">GMES Agent</div>
                <div style="font-size:11px; color:#7A7568; margin-top:1px;">
                    LGE TN · Production Engineering</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**Model**")
    model_choice = st.selectbox(
        "LLM",
        ["gpt-4o", "gpt-4o-mini"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("**Context size**")
    top_k = st.slider("Top K", min_value=3, max_value=30, value=15, label_visibility="collapsed")

    st.divider()

    st.markdown("**Knowledge base**")
    st.caption("Ingest a new GMES export:")
    st.code("python ingest_excel.py", language="bash")

    st.divider()

    if st.button("🗑️  Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Load collection
# ---------------------------------------------------------------------------

try:
    collection = load_collection()
    wo_count = collection.count()
    st.sidebar.markdown(
        f"<div style='font-size:12px; color:#7A7568; margin-top:0.5rem;'>"
        f"✅ {wo_count:,} work orders indexed</div>",
        unsafe_allow_html=True,
    )
    db_ready = True
except Exception as e:
    db_ready = False
    collection = None
    st.error(
        "**No work orders indexed yet.**  \n"
        "Drop your Excel file here and run `python ingest_excel.py`\n\n"
        f"`{e}`"
    )

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_chat, tab_analytics = st.tabs(["💬  Chat", "📊  Analytics"])

# ============================================================
# TAB 1 — Chat
# ============================================================

with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome state
    if not st.session_state.messages and db_ready:
        st.markdown(
            """
            <div style="text-align:center; padding: 3rem 1rem 2rem;">
                <div style="font-size:40px; margin-bottom:12px;">🔧</div>
                <div style="font-size:22px; font-weight:600; color:#1A1A1A;
                            letter-spacing:-0.02em; margin-bottom:8px;">
                    What can I help you with?
                </div>
                <div style="font-size:14px; color:#7A7568; max-width:420px; margin:0 auto;">
                    Ask about equipment failures, past repairs, recurring issues,
                    or maintenance patterns across any line or shop.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Suggestion chips
        suggestions = [
            "What failures has the EPS vacuum pump had?",
            "Most common failures in the last 90 days",
            "Who last worked on the diverter in Line 3?",
            "What causes motor overheating in Body shop?",
        ]
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(s, use_container_width=True, key=f"sug_{i}"):
                    st.session_state._pending_input = s
                    st.rerun()

    # Flush a suggestion click into the chat
    pending = st.session_state.pop("_pending_input", None)

    # Render history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("items"):
                with st.expander(f"📋 {len(msg['items'])} work orders referenced"):
                    render_wo_cards(msg["items"])

    # Input
    if db_ready:
        user_input = st.chat_input("Ask a maintenance question…") or pending
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Searching work order history…"):
                    history_so_far = st.session_state.messages[:-1]
                    search_query = rewrite_query(user_input, history_so_far)
                    items = retrieve_context(search_query, collection, top_k=top_k)
                    messages = build_messages(user_input, items, history_so_far)

                try:
                    with st.spinner("Generating answer…"):
                        full_response = call_llm(messages, model_name=model_choice)
                    st.markdown(full_response)
                except Exception as e:
                    full_response = f"**Azure OpenAI error:** `{e}`"
                    st.error(full_response)

                with st.expander(f"📋 {len(items)} work orders referenced"):
                    render_wo_cards(items)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response, "items": items}
            )

# ============================================================
# TAB 2 — Analytics
# ============================================================

with tab_analytics:
    if not db_ready:
        st.warning("No work orders indexed yet. Run `python ingest_excel.py` first.")
        st.stop()

    df_full = load_metadata_df(collection)

    GROUP_LABELS = {
        "line":       "Line",
        "group":      "Shop / Group",
        "equipment":  "Equipment",
        "maint_type": "Maintenance Type",
    }

    # ── Controls ──────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns([2, 1, 2, 2, 2])
    with c1:
        group_field = st.selectbox(
            "Group by",
            options=list(GROUP_LABELS.keys()),
            format_func=lambda k: GROUP_LABELS[k],
        )
    with c2:
        top_n = st.slider("Top N", 3, 25, 10, label_visibility="visible")

    date_min = df_full["date_parsed"].min().date() if "date_parsed" in df_full.columns else None
    date_max = df_full["date_parsed"].max().date() if "date_parsed" in df_full.columns else None
    with c3:
        date_from = st.date_input("From", value=date_min, min_value=date_min, max_value=date_max)
    with c4:
        date_to = st.date_input("To", value=date_max, min_value=date_min, max_value=date_max)
    with c5:
        keyword = st.text_input("Keyword filter", placeholder="e.g. diverter, vacuum…")

    # ── Apply filters ──────────────────────────────────────────────────
    df = df_full.copy()
    if "date_parsed" in df.columns and date_from and date_to:
        df = df[df["date_parsed"].dt.date.between(date_from, date_to)]
    if keyword.strip():
        kw = keyword.strip().lower()
        mask_cols = [c for c in ["equipment", "maint_type", "line", "group"] if c in df.columns]
        mask = df[mask_cols].apply(lambda col: col.str.lower().str.contains(kw, na=False)).any(axis=1)
        df = df[mask]

    st.divider()

    if df.empty:
        st.info("No work orders match the current filters.")
        st.stop()

    if group_field not in df.columns:
        st.error(f"Field `{group_field}` not found in indexed metadata.")
        st.stop()

    # ── Metric cards ───────────────────────────────────────────────────
    counts = (
        df[group_field]
        .fillna("Unknown")
        .value_counts()
        .rename_axis(GROUP_LABELS[group_field])
        .rename("Work Orders")
    )

    top_value = counts.index[0] if not counts.empty else "—"
    top_count = int(counts.iloc[0]) if not counts.empty else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Work Orders", f"{len(df):,}")
    m2.metric("Date range", f"{date_from} → {date_to}" if date_from else "All time")
    m3.metric(f"Top {GROUP_LABELS[group_field]}", top_value)
    m4.metric("WOs (top)", f"{top_count:,}")

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    # ── Bar chart ──────────────────────────────────────────────────────
    kw_suffix = f"  ·  <span style='color:#CC785C;'>{keyword}</span>" if keyword.strip() else ""
    st.markdown(
        f"<div style='font-size:15px; font-weight:600; color:#1A1A1A; margin-bottom:4px;'>"
        f"Top {top_n} by {GROUP_LABELS[group_field]}{kw_suffix}</div>",
        unsafe_allow_html=True,
    )
    st.bar_chart(counts.head(top_n))

    # ── Full table ─────────────────────────────────────────────────────
    with st.expander("📋 Full table", expanded=False):
        st.dataframe(
            counts.reset_index(),
            use_container_width=True,
            hide_index=True,
            column_config={
                GROUP_LABELS[group_field]: st.column_config.TextColumn(GROUP_LABELS[group_field]),
                "Work Orders": st.column_config.NumberColumn("Work Orders", format="%d"),
            },
        )

    # ── Monthly trend ──────────────────────────────────────────────────
    if "date_parsed" in df.columns:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:15px; font-weight:600; color:#1A1A1A; margin-bottom:4px;'>"
            f"Monthly trend — top 5 {GROUP_LABELS[group_field]}</div>",
            unsafe_allow_html=True,
        )
        top5 = counts.head(5).index.tolist()
        trend_df = df[df[group_field].isin(top5)].copy()
        trend_df["month"] = trend_df["date_parsed"].dt.to_period("M").dt.to_timestamp()
        pivot = (
            trend_df.groupby(["month", group_field])
            .size()
            .unstack(fill_value=0)
            .sort_index()
        )
        st.line_chart(pivot)
