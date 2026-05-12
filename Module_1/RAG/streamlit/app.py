# # # """
# # # app.py  —  Advanced Streamlit UI for the multi-document RAG chatbot
# # # Run with:  streamlit run app.py
# # # """

# # # import os
# # # import time
# # # import streamlit as st

# # # from rag_backend import (
# # #     save_uploaded_files,
# # #     process_documents,
# # #     llm_model,
# # #     build_qa_chain,
# # #     ask_question,
# # # )

# # # # ─────────────────────────────────────────────
# # # # PAGE CONFIG & GLOBAL STYLE
# # # # ─────────────────────────────────────────────

# # # st.set_page_config(
# # #     page_title="DocMind — RAG Chatbot",
# # #     page_icon="🧠",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded",
# # # )

# # # st.markdown(
# # #     """
# # #     <style>
# # #     /* ── Fonts ── */
# # #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:wght@300;400;500&display=swap');

# # #     /* ── Root palette ── */
# # #     :root {
# # #         --bg:        #0d0f14;
# # #         --surface:   #161922;
# # #         --border:    #252b38;
# # #         --accent:    #6ee7b7;       /* mint green */
# # #         --accent2:   #818cf8;       /* soft indigo */
# # #         --warn:      #fbbf24;
# # #         --text:      #e2e8f0;
# # #         --muted:     #64748b;
# # #         --user-bg:   #1e293b;
# # #         --bot-bg:    #162032;
# # #         --radius:    14px;
# # #     }

# # #     /* ── Global reset ── */
# # #     html, body, [class*="css"] {
# # #         font-family: 'DM Mono', monospace;
# # #         background-color: var(--bg) !important;
# # #         color: var(--text) !important;
# # #     }

# # #     /* ── Sidebar ── */
# # #     [data-testid="stSidebar"] {
# # #         background: var(--surface) !important;
# # #         border-right: 1px solid var(--border);
# # #     }

# # #     /* ── Main content area ── */
# # #     .block-container { padding: 2rem 2.5rem !important; }

# # #     /* ── Logo / header ── */
# # #     .logo-header {
# # #         display: flex;
# # #         align-items: center;
# # #         gap: 12px;
# # #         margin-bottom: 0.3rem;
# # #     }
# # #     .logo-icon {
# # #         font-size: 2.4rem;
# # #         line-height: 1;
# # #     }
# # #     .logo-title {
# # #         font-family: 'Syne', sans-serif;
# # #         font-weight: 800;
# # #         font-size: 2rem;
# # #         background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
# # #         -webkit-background-clip: text;
# # #         -webkit-text-fill-color: transparent;
# # #     }
# # #     .logo-sub {
# # #         font-size: 0.75rem;
# # #         color: var(--muted);
# # #         letter-spacing: 0.15em;
# # #         text-transform: uppercase;
# # #         margin-top: -4px;
# # #     }

# # #     /* ── Divider ── */
# # #     .fancy-divider {
# # #         height: 1px;
# # #         background: linear-gradient(90deg, transparent, var(--accent), transparent);
# # #         margin: 1.2rem 0;
# # #         opacity: 0.4;
# # #     }

# # #     /* ── Status pill ── */
# # #     .status-pill {
# # #         display: inline-flex;
# # #         align-items: center;
# # #         gap: 6px;
# # #         padding: 5px 14px;
# # #         border-radius: 999px;
# # #         font-size: 0.75rem;
# # #         font-weight: 500;
# # #         letter-spacing: 0.05em;
# # #     }
# # #     .status-ready   { background: rgba(110,231,183,.15); color: var(--accent);  border: 1px solid rgba(110,231,183,.3); }
# # #     .status-waiting { background: rgba(251,191,36,.12);  color: var(--warn);    border: 1px solid rgba(251,191,36,.3); }
# # #     .status-error   { background: rgba(248,113,113,.12); color: #f87171;        border: 1px solid rgba(248,113,113,.3); }

# # #     /* ── Stat cards ── */
# # #     .stat-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 0.8rem 0; }
# # #     .stat-card {
# # #         flex: 1;
# # #         min-width: 90px;
# # #         background: var(--bg);
# # #         border: 1px solid var(--border);
# # #         border-radius: var(--radius);
# # #         padding: 10px 14px;
# # #         text-align: center;
# # #     }
# # #     .stat-num {
# # #         font-family: 'Syne', sans-serif;
# # #         font-size: 1.5rem;
# # #         font-weight: 800;
# # #         color: var(--accent);
# # #     }
# # #     .stat-label {
# # #         font-size: 0.65rem;
# # #         color: var(--muted);
# # #         text-transform: uppercase;
# # #         letter-spacing: 0.1em;
# # #     }

# # #     /* ── Chat messages ── */
# # #     .chat-wrap { display: flex; flex-direction: column; gap: 14px; margin-bottom: 1.5rem; }

# # #     .msg-row { display: flex; gap: 10px; align-items: flex-start; }
# # #     .msg-row.user  { flex-direction: row-reverse; }
# # #     .msg-row.bot   { flex-direction: row; }

# # #     .avatar {
# # #         width: 34px;
# # #         height: 34px;
# # #         border-radius: 50%;
# # #         display: flex;
# # #         align-items: center;
# # #         justify-content: center;
# # #         font-size: 1rem;
# # #         flex-shrink: 0;
# # #     }
# # #     .avatar.user { background: linear-gradient(135deg, var(--accent2), #6366f1); }
# # #     .avatar.bot  { background: linear-gradient(135deg, var(--accent), #059669); }

# # #     .bubble {
# # #         max-width: 78%;
# # #         padding: 13px 17px;
# # #         border-radius: var(--radius);
# # #         font-size: 0.88rem;
# # #         line-height: 1.65;
# # #         position: relative;
# # #     }
# # #     .bubble.user {
# # #         background: var(--user-bg);
# # #         border: 1px solid rgba(129,140,248,.25);
# # #         color: var(--text);
# # #     }
# # #     .bubble.bot {
# # #         background: var(--bot-bg);
# # #         border: 1px solid rgba(110,231,183,.18);
# # #         color: var(--text);
# # #     }

# # #     /* ── Source chips ── */
# # #     .sources-wrap { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px; }
# # #     .src-chip {
# # #         display: inline-flex;
# # #         align-items: center;
# # #         gap: 5px;
# # #         padding: 3px 10px;
# # #         background: rgba(110,231,183,.08);
# # #         border: 1px solid rgba(110,231,183,.22);
# # #         border-radius: 999px;
# # #         font-size: 0.68rem;
# # #         color: var(--accent);
# # #         cursor: default;
# # #     }

# # #     /* ── Input bar ── */
# # #     .stTextInput > div > div > input {
# # #         background: var(--surface) !important;
# # #         border: 1px solid var(--border) !important;
# # #         border-radius: var(--radius) !important;
# # #         color: var(--text) !important;
# # #         font-family: 'DM Mono', monospace !important;
# # #         font-size: 0.9rem !important;
# # #         padding: 12px 16px !important;
# # #     }
# # #     .stTextInput > div > div > input:focus {
# # #         border-color: var(--accent) !important;
# # #         box-shadow: 0 0 0 3px rgba(110,231,183,.15) !important;
# # #     }

# # #     /* ── Buttons ── */
# # #     .stButton > button {
# # #         background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
# # #         color: #0d0f14 !important;
# # #         border: none !important;
# # #         border-radius: var(--radius) !important;
# # #         font-family: 'Syne', sans-serif !important;
# # #         font-weight: 700 !important;
# # #         font-size: 0.85rem !important;
# # #         padding: 10px 22px !important;
# # #         transition: opacity .2s, transform .15s !important;
# # #     }
# # #     .stButton > button:hover {
# # #         opacity: .88 !important;
# # #         transform: translateY(-1px) !important;
# # #     }

# # #     /* ── File uploader ── */
# # #     [data-testid="stFileUploader"] {
# # #         background: var(--surface) !important;
# # #         border: 1px dashed var(--border) !important;
# # #         border-radius: var(--radius) !important;
# # #         padding: 0.5rem !important;
# # #     }

# # #     /* ── Expander (sources) ── */
# # #     .streamlit-expanderHeader {
# # #         background: var(--surface) !important;
# # #         border: 1px solid var(--border) !important;
# # #         border-radius: 10px !important;
# # #         color: var(--muted) !important;
# # #         font-size: 0.78rem !important;
# # #     }

# # #     /* ── Scrollbar ── */
# # #     ::-webkit-scrollbar { width: 6px; }
# # #     ::-webkit-scrollbar-track { background: var(--bg); }
# # #     ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
# # #     ::-webkit-scrollbar-thumb:hover { background: var(--muted); }

# # #     /* ── Typing indicator ── */
# # #     .typing-dot {
# # #         display: inline-block;
# # #         width: 7px;
# # #         height: 7px;
# # #         background: var(--accent);
# # #         border-radius: 50%;
# # #         margin: 0 2px;
# # #         animation: bounce 1.2s infinite;
# # #     }
# # #     .typing-dot:nth-child(2) { animation-delay: 0.2s; }
# # #     .typing-dot:nth-child(3) { animation-delay: 0.4s; }
# # #     @keyframes bounce {
# # #         0%,80%,100% { transform: translateY(0); }
# # #         40%          { transform: translateY(-7px); }
# # #     }

# # #     /* Hide Streamlit branding */
# # #     #MainMenu, footer, header { visibility: hidden; }
# # #     </style>
# # #     """,
# # #     unsafe_allow_html=True,
# # # )


# # # # ─────────────────────────────────────────────
# # # # SESSION STATE DEFAULTS
# # # # ─────────────────────────────────────────────

# # # def init_state():
# # #     defaults = {
# # #         "messages":        [],   # [{role, content, sources}]
# # #         "qa_chain":        None,
# # #         "docs_processed":  False,
# # #         "doc_names":       [],
# # #         "chunk_count":     0,
# # #         "doc_count":       0,
# # #         "processing":      False,
# # #     }
# # #     for k, v in defaults.items():
# # #         if k not in st.session_state:
# # #             st.session_state[k] = v

# # # init_state()


# # # # ─────────────────────────────────────────────
# # # # SIDEBAR
# # # # ─────────────────────────────────────────────

# # # with st.sidebar:
# # #     # Logo
# # #     st.markdown(
# # #         """
# # #         <div class="logo-header">
# # #             <div class="logo-icon">🧠</div>
# # #             <div>
# # #                 <div class="logo-title">DocMind</div>
# # #                 <div class="logo-sub">RAG Document Intelligence</div>
# # #             </div>
# # #         </div>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )
# # #     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# # #     # ── API Key ──────────────────────────────
# # #     st.markdown("**🔑 Groq API Key**")
# # #     api_key = st.text_input(
# # #         "Groq API Key",
# # #         type="password",
# # #         placeholder="gsk_...",
# # #         label_visibility="collapsed",
# # #     )

# # #     # ── Model selector ───────────────────────
# # #     st.markdown("**🤖 Model**")
# # #     model_choice = st.selectbox(
# # #         "Model",
# # #         [
# # #             "llama-3.3-70b-versatile",
# # #             "llama3-8b-8192",
# # #             "mixtral-8x7b-32768",
# # #             "gemma2-9b-it",
# # #         ],
# # #         label_visibility="collapsed",
# # #     )

# # #     # ── Advanced settings ────────────────────
# # #     with st.expander("⚙️  Advanced Settings"):
# # #         temperature   = st.slider("Temperature",      0.0, 1.0, 0.3, 0.05)
# # #         chunk_size    = st.slider("Chunk Size",        300, 2000, 1000, 100)
# # #         chunk_overlap = st.slider("Chunk Overlap",      50,  500,  200,  50)
# # #         top_k         = st.slider("Retrieval Top-K",    2,   10,    4,    1)

# # #     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# # #     # ── File uploader ────────────────────────
# # #     st.markdown("**📄 Upload Documents**")
# # #     uploaded_files = st.file_uploader(
# # #         "Upload PDFs",
# # #         type=["pdf"],
# # #         accept_multiple_files=True,
# # #         label_visibility="collapsed",
# # #         help="Upload one or more PDF files to chat with.",
# # #     )

# # #     process_btn = st.button("⚡  Process Documents", use_container_width=True)

# # #     # ── Status indicator ─────────────────────
# # #     st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
# # #     if st.session_state.docs_processed:
# # #         st.markdown(
# # #             '<span class="status-pill status-ready">● Ready</span>',
# # #             unsafe_allow_html=True,
# # #         )
# # #     elif uploaded_files:
# # #         st.markdown(
# # #             '<span class="status-pill status-waiting">◌ Files loaded — click Process</span>',
# # #             unsafe_allow_html=True,
# # #         )
# # #     else:
# # #         st.markdown(
# # #             '<span class="status-pill status-waiting">◌ Awaiting documents</span>',
# # #             unsafe_allow_html=True,
# # #         )

# # #     # ── Stats ────────────────────────────────
# # #     if st.session_state.docs_processed:
# # #         st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
# # #         st.markdown(
# # #             f"""
# # #             <div class="stat-row">
# # #               <div class="stat-card">
# # #                 <div class="stat-num">{st.session_state.doc_count}</div>
# # #                 <div class="stat-label">Docs</div>
# # #               </div>
# # #               <div class="stat-card">
# # #                 <div class="stat-num">{st.session_state.chunk_count}</div>
# # #                 <div class="stat-label">Chunks</div>
# # #               </div>
# # #               <div class="stat-card">
# # #                 <div class="stat-num">{len(st.session_state.messages)//2}</div>
# # #                 <div class="stat-label">Q&amp;A</div>
# # #               </div>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# # #     # ── Document list ────────────────────────
# # #     if st.session_state.doc_names:
# # #         st.markdown("**📚 Loaded Documents**")
# # #         for name in st.session_state.doc_names:
# # #             st.markdown(
# # #                 f'<div style="font-size:0.75rem;color:var(--muted);padding:3px 0;">'
# # #                 f'📃 {name}</div>',
# # #                 unsafe_allow_html=True,
# # #             )

# # #     # ── Clear chat ───────────────────────────
# # #     st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
# # #     if st.button("🗑️  Clear Chat", use_container_width=True):
# # #         st.session_state.messages = []
# # #         st.rerun()


# # # # ─────────────────────────────────────────────
# # # # PROCESS DOCUMENTS LOGIC
# # # # ─────────────────────────────────────────────

# # # if process_btn:
# # #     if not api_key:
# # #         st.error("⚠️  Please enter your Groq API key in the sidebar.")
# # #     elif not uploaded_files:
# # #         st.warning("📄  Please upload at least one PDF file.")
# # #     else:
# # #         with st.spinner("🔄  Loading & embedding documents — this takes a moment…"):
# # #             try:
# # #                 paths = save_uploaded_files(uploaded_files)
# # #                 db, embeddings, n_chunks = process_documents(
# # #                     paths,
# # #                     chunk_size=chunk_size,
# # #                     chunk_overlap=chunk_overlap,
# # #                 )
# # #                 llm = llm_model(
# # #                     api_key=api_key,
# # #                     model_name=model_choice,
# # #                     temperature=temperature,
# # #                 )
# # #                 chain = build_qa_chain(db, llm, k=top_k)

# # #                 st.session_state.qa_chain       = chain
# # #                 st.session_state.docs_processed = True
# # #                 st.session_state.doc_names      = [f.name for f in uploaded_files]
# # #                 st.session_state.doc_count      = len(uploaded_files)
# # #                 st.session_state.chunk_count    = n_chunks
# # #                 st.session_state.messages       = []   # fresh chat for new docs

# # #                 st.success(
# # #                     f"✅  {len(uploaded_files)} document(s) processed into {n_chunks} chunks. Start chatting!"
# # #                 )
# # #                 time.sleep(1)
# # #                 st.rerun()
# # #             except Exception as e:
# # #                 st.error(f"❌  Processing failed: {e}")


# # # # ─────────────────────────────────────────────
# # # # MAIN CHAT AREA
# # # # ─────────────────────────────────────────────

# # # # ── Header ──────────────────────────────────
# # # st.markdown(
# # #     """
# # #     <div class="logo-header" style="margin-bottom:4px;">
# # #         <div class="logo-icon" style="font-size:1.8rem;">🧠</div>
# # #         <div>
# # #             <div class="logo-title" style="font-size:1.6rem;">DocMind</div>
# # #             <div class="logo-sub">Ask anything about your documents</div>
# # #         </div>
# # #     </div>
# # #     <div class="fancy-divider"></div>
# # #     """,
# # #     unsafe_allow_html=True,
# # # )

# # # # ── Welcome / placeholder ────────────────────
# # # if not st.session_state.docs_processed:
# # #     st.markdown(
# # #         """
# # #         <div style="
# # #             text-align:center;
# # #             padding: 60px 20px;
# # #             color: var(--muted);
# # #         ">
# # #             <div style="font-size:4rem;margin-bottom:16px;">📂</div>
# # #             <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
# # #                         color:var(--text);margin-bottom:8px;">
# # #                 Upload & Process Documents First
# # #             </div>
# # #             <div style="font-size:0.85rem;max-width:380px;margin:0 auto;line-height:1.7;">
# # #                 Add your PDF files in the sidebar, enter your Groq API key,
# # #                 then hit <strong>⚡ Process Documents</strong> to begin.
# # #             </div>
# # #         </div>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )

# # # else:
# # #     # ── Chat history ─────────────────────────
# # #     chat_html = '<div class="chat-wrap">'

# # #     for msg in st.session_state.messages:
# # #         role    = msg["role"]
# # #         content = msg["content"]
# # #         sources = msg.get("sources", [])
# # #         avatar  = "👤" if role == "user" else "🧠"
# # #         cls     = "user" if role == "user" else "bot"

# # #         # Source chips HTML
# # #         chips = ""
# # #         if sources:
# # #             chips = '<div class="sources-wrap">'
# # #             for s in sources:
# # #                 chips += (
# # #                     f'<span class="src-chip" title="…{s["snippet"]}…">'
# # #                     f'📄 {s["file"]} · p{s["page"]}'
# # #                     f'</span>'
# # #                 )
# # #             chips += "</div>"

# # #         chat_html += f"""
# # #         <div class="msg-row {cls}">
# # #             <div class="avatar {cls}">{avatar}</div>
# # #             <div class="bubble {cls}">
# # #                 {content}
# # #                 {chips}
# # #             </div>
# # #         </div>
# # #         """

# # #     chat_html += "</div>"
# # #     st.markdown(chat_html, unsafe_allow_html=True)

# # #     # ── Empty chat prompt ─────────────────────
# # #     if not st.session_state.messages:
# # #         st.markdown(
# # #             """
# # #             <div style="text-align:center;padding:40px 0;color:var(--muted);">
# # #                 <div style="font-size:2rem;margin-bottom:10px;">💬</div>
# # #                 <div style="font-size:0.85rem;">Documents ready — ask your first question below</div>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #     # ── Example questions ────────────────────
# # #     with st.expander("💡  Suggested Questions", expanded=False):
# # #         examples = [
# # #             "Summarise the main topics covered in the documents.",
# # #             "What are the key findings or conclusions?",
# # #             "List the most important facts mentioned.",
# # #             "Are there any dates or numbers I should know?",
# # #             "Compare the different sections or documents.",
# # #         ]
# # #         cols = st.columns(2)
# # #         for i, q in enumerate(examples):
# # #             if cols[i % 2].button(q, key=f"ex_{i}"):
# # #                 st.session_state["prefill"] = q
# # #                 st.rerun()

# # #     st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# # #     # ── Input ────────────────────────────────
# # #     prefill = st.session_state.pop("prefill", "")
# # #     col_input, col_send = st.columns([9, 1])

# # #     with col_input:
# # #         user_input = st.text_input(
# # #             "Ask a question",
# # #             value=prefill,
# # #             placeholder="Ask anything about your documents…",
# # #             label_visibility="collapsed",
# # #             key="chat_input",
# # #         )
# # #     with col_send:
# # #         send = st.button("Send", use_container_width=True)

# # #     # ── Handle send ──────────────────────────
# # #     if (send or user_input) and user_input.strip():
# # #         question = user_input.strip()

# # #         # Append user message immediately
# # #         st.session_state.messages.append(
# # #             {"role": "user", "content": question, "sources": []}
# # #         )

# # #         # Typing indicator
# # #         with st.spinner("🧠  Thinking…"):
# # #             try:
# # #                 result = ask_question(st.session_state.qa_chain, question)
# # #                 answer  = result["answer"]
# # #                 sources = result["sources"]
# # #             except Exception as e:
# # #                 answer  = f"⚠️  Something went wrong: {e}"
# # #                 sources = []

# # #         st.session_state.messages.append(
# # #             {"role": "bot", "content": answer, "sources": sources}
# # #         )
# # #         st.rerun()

# # #     # ── Source details expander ──────────────
# # #     if st.session_state.messages:
# # #         last_bot = next(
# # #             (m for m in reversed(st.session_state.messages) if m["role"] == "bot"),
# # #             None,
# # #         )
# # #         if last_bot and last_bot.get("sources"):
# # #             with st.expander("🔍  Source Excerpts (last answer)"):
# # #                 for i, s in enumerate(last_bot["sources"], 1):
# # #                     st.markdown(
# # #                         f"**{i}. {s['file']}** — Page {s['page']}\n\n"
# # #                         f"> {s['snippet']}…"
# # #                     )



# # """
# # app.py  —  Advanced Streamlit UI for the multi-document RAG chatbot
# # 3-column layout: Left Sidebar | Chat | Right Panel (Chunks & Sources)
# # Run with:  streamlit run app.py
# # """

# # import os
# # import time
# # from collections import Counter
# # import streamlit as st

# # from rag_backend import (
# #     save_uploaded_files,
# #     process_documents,
# #     llm_model,
# #     build_qa_chain,
# #     ask_question,
# # )

# # # ─────────────────────────────────────────────
# # # PAGE CONFIG
# # # ─────────────────────────────────────────────

# # st.set_page_config(
# #     page_title="DocMind — RAG Chatbot",
# #     page_icon="🧠",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )

# # # ─────────────────────────────────────────────
# # # GLOBAL CSS
# # # ─────────────────────────────────────────────

# # st.markdown(
# #     """
# #     <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:wght@300;400;500&display=swap');

# #     :root {
# #         --bg:        #0d0f14;
# #         --surface:   #161922;
# #         --surface2:  #1c2130;
# #         --border:    #252b38;
# #         --accent:    #6ee7b7;
# #         --accent2:   #818cf8;
# #         --accent3:   #f472b6;
# #         --warn:      #fbbf24;
# #         --text:      #e2e8f0;
# #         --muted:     #64748b;
# #         --user-bg:   #1e293b;
# #         --bot-bg:    #162032;
# #         --radius:    14px;
# #         --radius-sm: 8px;
# #     }

# #     html, body, [class*="css"] {
# #         font-family: 'DM Mono', monospace;
# #         background-color: var(--bg) !important;
# #         color: var(--text) !important;
# #     }

# #     /* ── Left sidebar ── */
# #     [data-testid="stSidebar"] {
# #         background: var(--surface) !important;
# #         border-right: 1px solid var(--border);
# #     }

# #     .block-container { padding: 1.5rem 1.8rem !important; }

# #     /* ── Logo ── */
# #     .logo-header { display:flex; align-items:center; gap:10px; margin-bottom:2px; }
# #     .logo-title {
# #         font-family: 'Syne', sans-serif;
# #         font-weight: 800;
# #         font-size: 1.8rem;
# #         background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #     }
# #     .logo-sub {
# #         font-size: 0.7rem;
# #         color: var(--muted);
# #         letter-spacing: 0.15em;
# #         text-transform: uppercase;
# #         margin-top: -2px;
# #     }

# #     /* ── Divider ── */
# #     .fancy-divider {
# #         height: 1px;
# #         background: linear-gradient(90deg, transparent, var(--accent), transparent);
# #         margin: 1rem 0;
# #         opacity: 0.35;
# #     }
# #     .divider-pink   { background: linear-gradient(90deg, transparent, var(--accent3), transparent); }
# #     .divider-indigo { background: linear-gradient(90deg, transparent, var(--accent2), transparent); }

# #     /* ── Status pills ── */
# #     .status-pill {
# #         display:inline-flex; align-items:center; gap:6px;
# #         padding:4px 12px; border-radius:999px;
# #         font-size:0.72rem; font-weight:500; letter-spacing:0.05em;
# #     }
# #     .status-ready   { background:rgba(110,231,183,.15); color:var(--accent);  border:1px solid rgba(110,231,183,.3); }
# #     .status-waiting { background:rgba(251,191,36,.12);  color:var(--warn);    border:1px solid rgba(251,191,36,.3); }

# #     /* ── Stat cards ── */
# #     .stat-row { display:flex; gap:8px; flex-wrap:wrap; margin:0.7rem 0; }
# #     .stat-card {
# #         flex:1; min-width:70px;
# #         background:var(--bg); border:1px solid var(--border);
# #         border-radius:var(--radius); padding:8px 10px; text-align:center;
# #     }
# #     .stat-num {
# #         font-family:'Syne',sans-serif; font-size:1.3rem;
# #         font-weight:800; color:var(--accent);
# #     }
# #     .stat-label { font-size:0.6rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.1em; }

# #     /* ── Chat messages ── */
# #     .chat-wrap { display:flex; flex-direction:column; gap:12px; margin-bottom:1rem; }
# #     .msg-row { display:flex; gap:8px; align-items:flex-start; }
# #     .msg-row.user { flex-direction:row-reverse; }

# #     .avatar {
# #         width:30px; height:30px; border-radius:50%;
# #         display:flex; align-items:center; justify-content:center;
# #         font-size:0.9rem; flex-shrink:0;
# #     }
# #     .avatar.user { background:linear-gradient(135deg,var(--accent2),#6366f1); }
# #     .avatar.bot  { background:linear-gradient(135deg,var(--accent),#059669); }

# #     .bubble {
# #         max-width:84%; padding:11px 15px; border-radius:var(--radius);
# #         font-size:0.85rem; line-height:1.65;
# #     }
# #     .bubble.user { background:var(--user-bg); border:1px solid rgba(129,140,248,.2); }
# #     .bubble.bot  { background:var(--bot-bg);  border:1px solid rgba(110,231,183,.15); }

# #     /* ── Source chips inside bubble ── */
# #     .sources-wrap { margin-top:8px; display:flex; flex-wrap:wrap; gap:5px; }
# #     .src-chip {
# #         display:inline-flex; align-items:center; gap:4px;
# #         padding:2px 9px;
# #         background:rgba(110,231,183,.07); border:1px solid rgba(110,231,183,.2);
# #         border-radius:999px; font-size:0.65rem; color:var(--accent); cursor:default;
# #     }

# #     /* ── Right panel ── */
# #     .rp-header {
# #         font-family:'Syne',sans-serif; font-weight:800; font-size:1rem;
# #         color:var(--text); margin-bottom:4px;
# #         display:flex; align-items:center; gap:7px;
# #     }
# #     .rp-sub { font-size:0.68rem; color:var(--muted); margin-bottom:8px; }

# #     .chunk-card {
# #         background: var(--surface2);
# #         border: 1px solid var(--border);
# #         border-radius: var(--radius);
# #         padding: 12px 14px;
# #         margin-bottom: 10px;
# #         transition: border-color .2s;
# #     }
# #     .chunk-card:hover { border-color: rgba(110,231,183,.4); }

# #     .chunk-badge {
# #         display:inline-flex; align-items:center; gap:5px;
# #         background:rgba(110,231,183,.1); border:1px solid rgba(110,231,183,.25);
# #         border-radius:999px; padding:2px 9px;
# #         font-size:0.62rem; color:var(--accent); margin-bottom:6px;
# #     }
# #     .chunk-rank {
# #         width:20px; height:20px; border-radius:50%;
# #         background:linear-gradient(135deg,var(--accent),var(--accent2));
# #         color:#0d0f14; font-size:0.65rem; font-weight:800;
# #         display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;
# #     }
# #     .chunk-text {
# #         font-size:0.75rem; color:var(--text); line-height:1.6;
# #         border-left:2px solid rgba(110,231,183,.3);
# #         padding-left:9px; margin-top:6px;
# #         word-break: break-word;
# #     }
# #     .chunk-meta { display:flex; gap:7px; flex-wrap:wrap; margin-top:8px; }
# #     .meta-tag {
# #         font-size:0.6rem; color:var(--muted);
# #         background:var(--bg); border:1px solid var(--border);
# #         border-radius:999px; padding:2px 8px;
# #     }
# #     .meta-tag.file  { color:var(--accent2); border-color:rgba(129,140,248,.25); background:rgba(129,140,248,.07); }
# #     .meta-tag.page  { color:var(--accent3); border-color:rgba(244,114,182,.25); background:rgba(244,114,182,.07); }
# #     .meta-tag.score { color:var(--accent);  border-color:rgba(110,231,183,.25); background:rgba(110,231,183,.07); }

# #     /* ── Source info cards ── */
# #     .src-card {
# #         background:var(--surface2); border:1px solid var(--border);
# #         border-radius:var(--radius); padding:11px 13px; margin-bottom:8px;
# #     }
# #     .src-card-title {
# #         font-family:'Syne',sans-serif; font-weight:700; font-size:0.8rem;
# #         color:var(--accent2); margin-bottom:5px;
# #         display:flex; align-items:center; gap:6px;
# #     }
# #     .src-card-row { display:flex; justify-content:space-between; margin:3px 0; }
# #     .src-card-key { font-size:0.63rem; color:var(--muted); }
# #     .src-card-val { font-size:0.63rem; color:var(--text); text-align:right; max-width:60%; word-break:break-all; }

# #     /* ── Empty right panel ── */
# #     .rp-empty {
# #         display:flex; flex-direction:column; align-items:center;
# #         padding:50px 10px; color:var(--muted); text-align:center; gap:10px;
# #     }
# #     .rp-empty-icon { font-size:2.5rem; }
# #     .rp-empty-text { font-size:0.75rem; line-height:1.6; }

# #     /* ── Right panel wrapper ── */
# #     .right-panel-wrap {
# #         background: var(--surface);
# #         border: 1px solid var(--border);
# #         border-radius: var(--radius);
# #         padding: 16px 14px;
# #         min-height: 400px;
# #     }

# #     /* ── Input ── */
# #     .stTextInput > div > div > input {
# #         background:var(--surface) !important; border:1px solid var(--border) !important;
# #         border-radius:var(--radius) !important; color:var(--text) !important;
# #         font-family:'DM Mono',monospace !important; font-size:0.88rem !important;
# #         padding:11px 15px !important;
# #     }
# #     .stTextInput > div > div > input:focus {
# #         border-color:var(--accent) !important;
# #         box-shadow:0 0 0 3px rgba(110,231,183,.12) !important;
# #     }

# #     /* ── Buttons ── */
# #     .stButton > button {
# #         background:linear-gradient(135deg,var(--accent),var(--accent2)) !important;
# #         color:#0d0f14 !important; border:none !important;
# #         border-radius:var(--radius) !important;
# #         font-family:'Syne',sans-serif !important; font-weight:700 !important;
# #         font-size:0.82rem !important; padding:9px 18px !important;
# #         transition:opacity .2s,transform .15s !important;
# #     }
# #     .stButton > button:hover { opacity:.87 !important; transform:translateY(-1px) !important; }

# #     /* ── File uploader ── */
# #     [data-testid="stFileUploader"] {
# #         background:var(--surface) !important; border:1px dashed var(--border) !important;
# #         border-radius:var(--radius) !important; padding:0.4rem !important;
# #     }

# #     /* ── Expander ── */
# #     .streamlit-expanderHeader {
# #         background:var(--surface) !important; border:1px solid var(--border) !important;
# #         border-radius:10px !important; color:var(--muted) !important; font-size:0.76rem !important;
# #     }

# #     /* ── Scrollbar ── */
# #     ::-webkit-scrollbar { width:5px; }
# #     ::-webkit-scrollbar-track { background:var(--bg); }
# #     ::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }

# #     #MainMenu, footer, header { visibility:hidden; }
# #     </style>
# #     """,
# #     unsafe_allow_html=True,
# # )


# # # ─────────────────────────────────────────────
# # # SESSION STATE
# # # ─────────────────────────────────────────────

# # def init_state():
# #     defaults = {
# #         "messages":       [],
# #         "qa_chain":       None,
# #         "docs_processed": False,
# #         "doc_names":      [],
# #         "chunk_count":    0,
# #         "doc_count":      0,
# #         "last_sources":   [],   # [{file, page, snippet}, …]
# #     }
# #     for k, v in defaults.items():
# #         if k not in st.session_state:
# #             st.session_state[k] = v

# # init_state()


# # # ─────────────────────────────────────────────
# # # LEFT SIDEBAR
# # # ─────────────────────────────────────────────

# # with st.sidebar:
# #     st.markdown(
# #         """
# #         <div class="logo-header">
# #             <div style="font-size:2rem;">🧠</div>
# #             <div>
# #                 <div class="logo-title">DocMind</div>
# #                 <div class="logo-sub">RAG · Document Intelligence</div>
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )
# #     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# #     st.markdown("**🔑 Groq API Key**")
# #     api_key = st.text_input(
# #         "Groq API Key", type="password",
# #         placeholder="gsk_...", label_visibility="collapsed",
# #     )

# #     st.markdown("**🤖 Model**")
# #     model_choice = st.selectbox("Model", [
# #         "llama-3.3-70b-versatile",
# #         "llama3-8b-8192",
# #         "mixtral-8x7b-32768",
# #         "gemma2-9b-it",
# #     ], label_visibility="collapsed")

# #     with st.expander("⚙️  Advanced Settings"):
# #         temperature   = st.slider("Temperature",    0.0, 1.0, 0.3, 0.05)
# #         chunk_size    = st.slider("Chunk Size",      300, 2000, 1000, 100)
# #         chunk_overlap = st.slider("Chunk Overlap",    50,  500,  200,  50)
# #         top_k         = st.slider("Retrieval Top-K",   2,   10,    4,   1)

# #     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# #     st.markdown("**📄 Upload Documents**")
# #     uploaded_files = st.file_uploader(
# #         "Upload PDFs", type=["pdf"], accept_multiple_files=True,
# #         label_visibility="collapsed",
# #     )
# #     process_btn = st.button("⚡  Process Documents", use_container_width=True)

# #     st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
# #     if st.session_state.docs_processed:
# #         st.markdown('<span class="status-pill status-ready">● Ready</span>', unsafe_allow_html=True)
# #     elif uploaded_files:
# #         st.markdown('<span class="status-pill status-waiting">◌ Click Process</span>', unsafe_allow_html=True)
# #     else:
# #         st.markdown('<span class="status-pill status-waiting">◌ Awaiting files</span>', unsafe_allow_html=True)

# #     if st.session_state.docs_processed:
# #         st.markdown(
# #             f"""
# #             <div class="stat-row">
# #               <div class="stat-card">
# #                 <div class="stat-num">{st.session_state.doc_count}</div>
# #                 <div class="stat-label">Docs</div>
# #               </div>
# #               <div class="stat-card">
# #                 <div class="stat-num">{st.session_state.chunk_count}</div>
# #                 <div class="stat-label">Chunks</div>
# #               </div>
# #               <div class="stat-card">
# #                 <div class="stat-num">{len(st.session_state.messages)//2}</div>
# #                 <div class="stat-label">Q&amp;A</div>
# #               </div>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# #     if st.session_state.doc_names:
# #         st.markdown("**📚 Loaded Files**")
# #         for name in st.session_state.doc_names:
# #             st.markdown(
# #                 f'<div style="font-size:0.73rem;color:var(--muted);padding:2px 0;">📃 {name}</div>',
# #                 unsafe_allow_html=True,
# #             )

# #     st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
# #     if st.button("🗑️  Clear Chat", use_container_width=True):
# #         st.session_state.messages     = []
# #         st.session_state.last_sources = []
# #         st.rerun()


# # # ─────────────────────────────────────────────
# # # PROCESS DOCUMENTS
# # # ─────────────────────────────────────────────

# # if process_btn:
# #     if not api_key:
# #         st.error("⚠️  Please enter your Groq API key.")
# #     elif not uploaded_files:
# #         st.warning("📄  Upload at least one PDF first.")
# #     else:
# #         with st.spinner("🔄  Embedding documents…"):
# #             try:
# #                 paths = save_uploaded_files(uploaded_files)
# #                 db, embeddings, n_chunks = process_documents(
# #                     paths, chunk_size=chunk_size, chunk_overlap=chunk_overlap,
# #                 )
# #                 llm   = llm_model(api_key=api_key, model_name=model_choice, temperature=temperature)
# #                 chain = build_qa_chain(db, llm, k=top_k)

# #                 st.session_state.qa_chain       = chain
# #                 st.session_state.docs_processed = True
# #                 st.session_state.doc_names      = [f.name for f in uploaded_files]
# #                 st.session_state.doc_count      = len(uploaded_files)
# #                 st.session_state.chunk_count    = n_chunks
# #                 st.session_state.messages       = []
# #                 st.session_state.last_sources   = []

# #                 st.success(f"✅  {len(uploaded_files)} doc(s) → {n_chunks} chunks. Start chatting!")
# #                 time.sleep(0.8)
# #                 st.rerun()
# #             except Exception as e:
# #                 st.error(f"❌  {e}")


# # # ─────────────────────────────────────────────
# # # MAIN 2-COLUMN LAYOUT (Chat | Right Panel)
# # # ─────────────────────────────────────────────

# # col_chat, col_right = st.columns([6, 4], gap="medium")


# # # ══════════════════════════════════════════════
# # # CHAT COLUMN
# # # ══════════════════════════════════════════════

# # with col_chat:
# #     st.markdown(
# #         """
# #         <div class="logo-header" style="margin-bottom:2px;">
# #             <div style="font-size:1.5rem;">🧠</div>
# #             <div>
# #                 <div class="logo-title" style="font-size:1.4rem;">DocMind</div>
# #                 <div class="logo-sub">Ask anything about your documents</div>
# #             </div>
# #         </div>
# #         <div class="fancy-divider"></div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     if not st.session_state.docs_processed:
# #         st.markdown(
# #             """
# #             <div style="text-align:center;padding:70px 10px;color:var(--muted);">
# #                 <div style="font-size:3.5rem;margin-bottom:14px;">📂</div>
# #                 <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
# #                             color:var(--text);margin-bottom:8px;">
# #                     Upload & Process Documents First
# #                 </div>
# #                 <div style="font-size:0.82rem;max-width:340px;margin:0 auto;line-height:1.75;">
# #                     Add PDFs in the sidebar → enter Groq API key →
# #                     click <strong>⚡ Process Documents</strong>.
# #                 </div>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )
# #     else:
# #         # ── Chat history ─────────────────────
# #         chat_html = '<div class="chat-wrap">'
# #         for msg in st.session_state.messages:
# #             role    = msg["role"]
# #             content = msg["content"]
# #             sources = msg.get("sources", [])
# #             avatar  = "👤" if role == "user" else "🧠"
# #             cls     = "user" if role == "user" else "bot"

# #             chips = ""
# #             if sources:
# #                 chips = '<div class="sources-wrap">'
# #                 for s in sources:
# #                     chips += (
# #                         f'<span class="src-chip" title="{s.get("snippet","")[:80]}">'
# #                         f'📄 {s["file"]} · p{s["page"]}</span>'
# #                     )
# #                 chips += "</div>"

# #             chat_html += f"""
# #             <div class="msg-row {cls}">
# #                 <div class="avatar {cls}">{avatar}</div>
# #                 <div class="bubble {cls}">{content}{chips}</div>
# #             </div>
# #             """
# #         chat_html += "</div>"
# #         st.markdown(chat_html, unsafe_allow_html=True)

# #         if not st.session_state.messages:
# #             st.markdown(
# #                 """
# #                 <div style="text-align:center;padding:35px 0;color:var(--muted);">
# #                     <div style="font-size:1.8rem;margin-bottom:8px;">💬</div>
# #                     <div style="font-size:0.8rem;">Ready — ask your first question below</div>
# #                 </div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )

# #         # ── Suggested questions ───────────────
# #         with st.expander("💡  Suggested Questions", expanded=False):
# #             examples = [
# #                 "Summarise the main topics in the documents.",
# #                 "What are the key findings or conclusions?",
# #                 "List the most important facts mentioned.",
# #                 "Are there any important dates or numbers?",
# #                 "Compare the different sections or documents.",
# #             ]
# #             c1, c2 = st.columns(2)
# #             for i, q in enumerate(examples):
# #                 if (c1 if i % 2 == 0 else c2).button(q, key=f"ex_{i}"):
# #                     st.session_state["prefill"] = q
# #                     st.rerun()

# #         st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

# #         # ── Input row ────────────────────────
# #         prefill = st.session_state.pop("prefill", "")
# #         ci, cs  = st.columns([9, 1])
# #         with ci:
# #             user_input = st.text_input(
# #                 "Ask", value=prefill,
# #                 placeholder="Ask anything about your documents…",
# #                 label_visibility="collapsed", key="chat_input",
# #             )
# #         with cs:
# #             send = st.button("Send", use_container_width=True)

# #         # ── Handle send ───────────────────────
# #         if (send or user_input) and user_input.strip():
# #             question = user_input.strip()
# #             st.session_state.messages.append({"role": "user", "content": question, "sources": []})

# #             with st.spinner("🧠  Thinking…"):
# #                 try:
# #                     result  = ask_question(st.session_state.qa_chain, question)
# #                     answer  = result["answer"]
# #                     sources = result["sources"]
# #                 except Exception as e:
# #                     answer  = f"⚠️  Error: {e}"
# #                     sources = []

# #             st.session_state.messages.append({"role": "bot", "content": answer, "sources": sources})
# #             st.session_state.last_sources = sources
# #             st.rerun()


# # # ══════════════════════════════════════════════
# # # RIGHT PANEL: RETRIEVAL INSPECTOR
# # # ══════════════════════════════════════════════

# # with col_right:
# #     st.markdown('<div class="right-panel-wrap">', unsafe_allow_html=True)

# #     # ── Panel header ─────────────────────────
# #     st.markdown(
# #         """
# #         <div class="rp-header">🔍 Retrieval Inspector</div>
# #         <div class="rp-sub">Top retrieved chunks &amp; source metadata · updates after each answer</div>
# #         <div class="fancy-divider divider-indigo"></div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     sources = st.session_state.last_sources

# #     # ── Tabs ─────────────────────────────────
# #     tab_chunks, tab_sources = st.tabs(["📦  Top Chunks", "📑  Source Info"])

# #     # ────────────────────────────────
# #     # TAB 1 : TOP CHUNKS
# #     # ────────────────────────────────
# #     with tab_chunks:
# #         if not sources:
# #             st.markdown(
# #                 """
# #                 <div class="rp-empty">
# #                     <div class="rp-empty-icon">📭</div>
# #                     <div class="rp-empty-text">
# #                         No chunks yet.<br>
# #                         Ask a question and the top retrieved
# #                         chunks will appear here with relevance scores.
# #                     </div>
# #                 </div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )
# #         else:
# #             st.markdown(
# #                 f'<div style="font-size:0.7rem;color:var(--muted);margin-bottom:10px;">'
# #                 f'Showing <strong style="color:var(--accent)">{len(sources)}</strong> '
# #                 f'retrieved chunk(s) — ranked by relevance</div>',
# #                 unsafe_allow_html=True,
# #             )

# #             for i, chunk in enumerate(sources, 1):
# #                 file_name = chunk.get("file", "unknown")
# #                 page      = chunk.get("page", "?")
# #                 snippet   = chunk.get("snippet", "").replace("<", "&lt;").replace(">", "&gt;")
# #                 # Visual relevance bar: top chunk gets ~100%, decreasing
# #                 bar_pct   = max(25, 100 - (i - 1) * 20)

# #                 st.markdown(
# #                     f"""
# #                     <div class="chunk-card">

# #                         <!-- Header row: rank + file badge -->
# #                         <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
# #                             <div class="chunk-rank">#{i}</div>
# #                             <div class="chunk-badge">📄 {file_name}</div>
# #                         </div>

# #                         <!-- Relevance bar -->
# #                         <div style="margin-bottom:8px;">
# #                             <div style="display:flex;justify-content:space-between;
# #                                 font-size:0.6rem;color:var(--muted);margin-bottom:3px;">
# #                                 <span>Relevance</span>
# #                                 <span style="color:var(--accent);">{bar_pct}%</span>
# #                             </div>
# #                             <div style="height:5px;background:var(--border);
# #                                 border-radius:3px;overflow:hidden;">
# #                                 <div style="height:100%;width:{bar_pct}%;
# #                                     background:linear-gradient(90deg,var(--accent),var(--accent2));
# #                                     border-radius:3px;transition:width .4s ease;">
# #                                 </div>
# #                             </div>
# #                         </div>

# #                         <!-- Snippet text -->
# #                         <div class="chunk-text">{snippet}…</div>

# #                         <!-- Meta tags -->
# #                         <div class="chunk-meta">
# #                             <span class="meta-tag file">📁 {file_name}</span>
# #                             <span class="meta-tag page">📖 p.{page}</span>
# #                             <span class="meta-tag score">⭐ #{i}</span>
# #                             <span class="meta-tag" style="color:var(--warn);
# #                                 border-color:rgba(251,191,36,.3);background:rgba(251,191,36,.07);">
# #                                 🔤 {len(chunk.get("snippet",""))} chars
# #                             </span>
# #                         </div>

# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )

# #     # ────────────────────────────────
# #     # TAB 2 : SOURCE INFO
# #     # ────────────────────────────────
# #     with tab_sources:
# #         if not sources:
# #             st.markdown(
# #                 """
# #                 <div class="rp-empty">
# #                     <div class="rp-empty-icon">📋</div>
# #                     <div class="rp-empty-text">
# #                         No source data yet.<br>
# #                         After you ask a question, detailed source
# #                         metadata will appear here.
# #                     </div>
# #                 </div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )
# #         else:
# #             # ── Summary stats row ─────────────
# #             unique_files = list({s["file"] for s in sources})
# #             unique_pages = list({str(s["page"]) for s in sources})

# #             st.markdown(
# #                 f"""
# #                 <div class="stat-row" style="margin-bottom:12px;">
# #                     <div class="stat-card">
# #                         <div class="stat-num" style="font-size:1.1rem;color:var(--accent);">
# #                             {len(sources)}
# #                         </div>
# #                         <div class="stat-label">Sources</div>
# #                     </div>
# #                     <div class="stat-card">
# #                         <div class="stat-num" style="font-size:1.1rem;color:var(--accent2);">
# #                             {len(unique_files)}
# #                         </div>
# #                         <div class="stat-label">Files</div>
# #                     </div>
# #                     <div class="stat-card">
# #                         <div class="stat-num" style="font-size:1.1rem;color:var(--accent3);">
# #                             {len(unique_pages)}
# #                         </div>
# #                         <div class="stat-label">Pages</div>
# #                     </div>
# #                 </div>
# #                 <div class="fancy-divider divider-pink"></div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )

# #             # ── Per-source detail cards ───────
# #             for i, src in enumerate(sources, 1):
# #                 safe_snippet = (
# #                     src.get("snippet", "")[:160]
# #                     .replace("<", "&lt;")
# #                     .replace(">", "&gt;")
# #                 )
# #                 char_count = len(src.get("snippet", ""))

# #                 st.markdown(
# #                     f"""
# #                     <div class="src-card">
# #                         <div class="src-card-title">
# #                             <span style="background:rgba(129,140,248,.15);
# #                                 border:1px solid rgba(129,140,248,.3);
# #                                 border-radius:999px;padding:1px 7px;font-size:0.6rem;">
# #                                 #{i}
# #                             </span>
# #                             {src.get("file","unknown")}
# #                         </div>

# #                         <div class="src-card-row">
# #                             <span class="src-card-key">📖 Page</span>
# #                             <span class="src-card-val">{src.get("page","?")}</span>
# #                         </div>
# #                         <div class="src-card-row">
# #                             <span class="src-card-key">📁 Source File</span>
# #                             <span class="src-card-val">{src.get("file","unknown")}</span>
# #                         </div>
# #                         <div class="src-card-row">
# #                             <span class="src-card-key">🔤 Snippet Length</span>
# #                             <span class="src-card-val">{char_count} chars</span>
# #                         </div>
# #                         <div class="src-card-row">
# #                             <span class="src-card-key">⭐ Retrieval Rank</span>
# #                             <span class="src-card-val" style="color:var(--accent);">#{i}</span>
# #                         </div>

# #                         <!-- Excerpt block -->
# #                         <div style="margin-top:9px;">
# #                             <div style="font-size:0.6rem;color:var(--muted);margin-bottom:4px;">
# #                                 📝 Excerpt Preview
# #                             </div>
# #                             <div style="font-size:0.7rem;color:var(--text);
# #                                 background:var(--bg);border:1px solid var(--border);
# #                                 border-radius:8px;padding:8px 10px;line-height:1.6;
# #                                 border-left:3px solid rgba(244,114,182,.5);">
# #                                 {safe_snippet}…
# #                             </div>
# #                         </div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )

# #             # ── File coverage breakdown ───────
# #             st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
# #             st.markdown(
# #                 '<div style="font-size:0.7rem;color:var(--muted);margin-bottom:8px;">'
# #                 '📊 File Coverage Breakdown</div>',
# #                 unsafe_allow_html=True,
# #             )
# #             file_counts = Counter(s["file"] for s in sources)
# #             for fname, count in file_counts.items():
# #                 pct = int(count / len(sources) * 100)
# #                 st.markdown(
# #                     f"""
# #                     <div style="margin-bottom:9px;">
# #                         <div style="display:flex;justify-content:space-between;
# #                             font-size:0.65rem;margin-bottom:3px;">
# #                             <span style="color:var(--text);">📃 {fname}</span>
# #                             <span style="color:var(--accent);">{count} chunk(s) · {pct}%</span>
# #                         </div>
# #                         <div style="height:5px;background:var(--border);
# #                             border-radius:3px;overflow:hidden;">
# #                             <div style="height:100%;width:{pct}%;
# #                                 background:linear-gradient(90deg,var(--accent2),var(--accent3));
# #                                 border-radius:3px;">
# #                             </div>
# #                         </div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )

# #     st.markdown("</div>", unsafe_allow_html=True)   # close .right-panel-wrap

# """
# app.py  —  Advanced Streamlit UI for the multi-document RAG chatbot
# 3-column layout: Left Sidebar | Chat | Right Panel (Chunks & Sources)
# Run with:  streamlit run app.py
# """

# import os
# import time
# from collections import Counter
# import streamlit as st

# from rag_backend import (
#     save_uploaded_files,
#     process_documents,
#     llm_model,
#     build_qa_chain,
#     ask_question,
# )

# # ─────────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────────

# st.set_page_config(
#     page_title="DocMind — RAG Chatbot",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─────────────────────────────────────────────
# # GLOBAL CSS
# # ─────────────────────────────────────────────

# st.markdown(
#     """
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:wght@300;400;500&display=swap');

#     :root {
#         --bg:        #0d0f14;
#         --surface:   #161922;
#         --surface2:  #1c2130;
#         --border:    #252b38;
#         --accent:    #6ee7b7;
#         --accent2:   #818cf8;
#         --accent3:   #f472b6;
#         --warn:      #fbbf24;
#         --text:      #e2e8f0;
#         --muted:     #64748b;
#         --user-bg:   #1e293b;
#         --bot-bg:    #162032;
#         --radius:    14px;
#         --radius-sm: 8px;
#     }

#     html, body, [class*="css"] {
#         font-family: 'DM Mono', monospace;
#         background-color: var(--bg) !important;
#         color: var(--text) !important;
#     }

#     /* ── Left sidebar ── */
#     [data-testid="stSidebar"] {
#         background: var(--surface) !important;
#         border-right: 1px solid var(--border);
#     }

#     .block-container { padding: 1.5rem 1.8rem !important; }

#     /* ── Logo ── */
#     .logo-header { display:flex; align-items:center; gap:10px; margin-bottom:2px; }
#     .logo-title {
#         font-family: 'Syne', sans-serif;
#         font-weight: 800;
#         font-size: 1.8rem;
#         background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
#     .logo-sub {
#         font-size: 0.7rem;
#         color: var(--muted);
#         letter-spacing: 0.15em;
#         text-transform: uppercase;
#         margin-top: -2px;
#     }

#     /* ── Divider ── */
#     .fancy-divider {
#         height: 1px;
#         background: linear-gradient(90deg, transparent, var(--accent), transparent);
#         margin: 1rem 0;
#         opacity: 0.35;
#     }
#     .divider-pink   { background: linear-gradient(90deg, transparent, var(--accent3), transparent); }
#     .divider-indigo { background: linear-gradient(90deg, transparent, var(--accent2), transparent); }

#     /* ── Status pills ── */
#     .status-pill {
#         display:inline-flex; align-items:center; gap:6px;
#         padding:4px 12px; border-radius:999px;
#         font-size:0.72rem; font-weight:500; letter-spacing:0.05em;
#     }
#     .status-ready   { background:rgba(110,231,183,.15); color:var(--accent);  border:1px solid rgba(110,231,183,.3); }
#     .status-waiting { background:rgba(251,191,36,.12);  color:var(--warn);    border:1px solid rgba(251,191,36,.3); }

#     /* ── Stat cards ── */
#     .stat-row { display:flex; gap:8px; flex-wrap:wrap; margin:0.7rem 0; }
#     .stat-card {
#         flex:1; min-width:70px;
#         background:var(--bg); border:1px solid var(--border);
#         border-radius:var(--radius); padding:8px 10px; text-align:center;
#     }
#     .stat-num {
#         font-family:'Syne',sans-serif; font-size:1.3rem;
#         font-weight:800; color:var(--accent);
#     }
#     .stat-label { font-size:0.6rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.1em; }

#     /* ── Chat messages ── */
#     .chat-wrap { display:flex; flex-direction:column; gap:12px; margin-bottom:1rem; }
#     .msg-row { display:flex; gap:8px; align-items:flex-start; }
#     .msg-row.user { flex-direction:row-reverse; }

#     .avatar {
#         width:30px; height:30px; border-radius:50%;
#         display:flex; align-items:center; justify-content:center;
#         font-size:0.9rem; flex-shrink:0;
#     }
#     .avatar.user { background:linear-gradient(135deg,var(--accent2),#6366f1); }
#     .avatar.bot  { background:linear-gradient(135deg,var(--accent),#059669); }

#     .bubble {
#         max-width:84%; padding:11px 15px; border-radius:var(--radius);
#         font-size:0.85rem; line-height:1.65;
#     }
#     .bubble.user { background:var(--user-bg); border:1px solid rgba(129,140,248,.2); }
#     .bubble.bot  { background:var(--bot-bg);  border:1px solid rgba(110,231,183,.15); }

#     /* ── Source chips inside bubble ── */
#     .sources-wrap { margin-top:8px; display:flex; flex-wrap:wrap; gap:5px; }
#     .src-chip {
#         display:inline-flex; align-items:center; gap:4px;
#         padding:2px 9px;
#         background:rgba(110,231,183,.07); border:1px solid rgba(110,231,183,.2);
#         border-radius:999px; font-size:0.65rem; color:var(--accent); cursor:default;
#     }

#     /* ── Right panel ── */
#     .rp-header {
#         font-family:'Syne',sans-serif; font-weight:800; font-size:1rem;
#         color:var(--text); margin-bottom:4px;
#         display:flex; align-items:center; gap:7px;
#     }
#     .rp-sub { font-size:0.68rem; color:var(--muted); margin-bottom:8px; }

#     .chunk-card {
#         background: var(--surface2);
#         border: 1px solid var(--border);
#         border-radius: var(--radius);
#         padding: 12px 14px;
#         margin-bottom: 10px;
#         transition: border-color .2s;
#     }
#     .chunk-card:hover { border-color: rgba(110,231,183,.4); }

#     .chunk-badge {
#         display:inline-flex; align-items:center; gap:5px;
#         background:rgba(110,231,183,.1); border:1px solid rgba(110,231,183,.25);
#         border-radius:999px; padding:2px 9px;
#         font-size:0.62rem; color:var(--accent); margin-bottom:6px;
#     }
#     .chunk-rank {
#         width:20px; height:20px; border-radius:50%;
#         background:linear-gradient(135deg,var(--accent),var(--accent2));
#         color:#0d0f14; font-size:0.65rem; font-weight:800;
#         display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;
#     }
#     .chunk-text {
#         font-size:0.75rem; color:var(--text); line-height:1.6;
#         border-left:2px solid rgba(110,231,183,.3);
#         padding-left:9px; margin-top:6px;
#         word-break: break-word;
#     }
#     .chunk-meta { display:flex; gap:7px; flex-wrap:wrap; margin-top:8px; }
#     .meta-tag {
#         font-size:0.6rem; color:var(--muted);
#         background:var(--bg); border:1px solid var(--border);
#         border-radius:999px; padding:2px 8px;
#     }
#     .meta-tag.file  { color:var(--accent2); border-color:rgba(129,140,248,.25); background:rgba(129,140,248,.07); }
#     .meta-tag.page  { color:var(--accent3); border-color:rgba(244,114,182,.25); background:rgba(244,114,182,.07); }
#     .meta-tag.score { color:var(--accent);  border-color:rgba(110,231,183,.25); background:rgba(110,231,183,.07); }

#     /* ── Source info cards ── */
#     .src-card {
#         background:var(--surface2); border:1px solid var(--border);
#         border-radius:var(--radius); padding:11px 13px; margin-bottom:8px;
#     }
#     .src-card-title {
#         font-family:'Syne',sans-serif; font-weight:700; font-size:0.8rem;
#         color:var(--accent2); margin-bottom:5px;
#         display:flex; align-items:center; gap:6px;
#     }
#     .src-card-row { display:flex; justify-content:space-between; margin:3px 0; }
#     .src-card-key { font-size:0.63rem; color:var(--muted); }
#     .src-card-val { font-size:0.63rem; color:var(--text); text-align:right; max-width:60%; word-break:break-all; }

#     /* ── Empty right panel ── */
#     .rp-empty {
#         display:flex; flex-direction:column; align-items:center;
#         padding:50px 10px; color:var(--muted); text-align:center; gap:10px;
#     }
#     .rp-empty-icon { font-size:2.5rem; }
#     .rp-empty-text { font-size:0.75rem; line-height:1.6; }

#     /* ── Right panel wrapper ── */
#     .right-panel-wrap {
#         background: var(--surface);
#         border: 1px solid var(--border);
#         border-radius: var(--radius);
#         padding: 16px 14px;
#         min-height: 400px;
#     }

#     /* ── Input ── */
#     .stTextInput > div > div > input {
#         background:var(--surface) !important; border:1px solid var(--border) !important;
#         border-radius:var(--radius) !important; color:var(--text) !important;
#         font-family:'DM Mono',monospace !important; font-size:0.88rem !important;
#         padding:11px 15px !important;
#     }
#     .stTextInput > div > div > input:focus {
#         border-color:var(--accent) !important;
#         box-shadow:0 0 0 3px rgba(110,231,183,.12) !important;
#     }

#     /* ── Buttons ── */
#     .stButton > button {
#         background:linear-gradient(135deg,var(--accent),var(--accent2)) !important;
#         color:#0d0f14 !important; border:none !important;
#         border-radius:var(--radius) !important;
#         font-family:'Syne',sans-serif !important; font-weight:700 !important;
#         font-size:0.82rem !important; padding:9px 18px !important;
#         transition:opacity .2s,transform .15s !important;
#     }
#     .stButton > button:hover { opacity:.87 !important; transform:translateY(-1px) !important; }

#     /* ── File uploader ── */
#     [data-testid="stFileUploader"] {
#         background:var(--surface) !important; border:1px dashed var(--border) !important;
#         border-radius:var(--radius) !important; padding:0.4rem !important;
#     }

#     /* ── Expander ── */
#     .streamlit-expanderHeader {
#         background:var(--surface) !important; border:1px solid var(--border) !important;
#         border-radius:10px !important; color:var(--muted) !important; font-size:0.76rem !important;
#     }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width:5px; }
#     ::-webkit-scrollbar-track { background:var(--bg); }
#     ::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }

#     #MainMenu, footer, header { visibility:hidden; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ─────────────────────────────────────────────
# # SESSION STATE
# # ─────────────────────────────────────────────

# def init_state():
#     defaults = {
#         "messages":       [],
#         "qa_chain":       None,
#         "docs_processed": False,
#         "doc_names":      [],
#         "chunk_count":    0,
#         "doc_count":      0,
#         "last_sources":   [],   # [{file, page, snippet}, …]
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_state()


# # ─────────────────────────────────────────────
# # LEFT SIDEBAR
# # ─────────────────────────────────────────────

# with st.sidebar:
#     st.markdown(
#         """
#         <div class="logo-header">
#             <div style="font-size:2rem;">🧠</div>
#             <div>
#                 <div class="logo-title">DocMind</div>
#                 <div class="logo-sub">RAG · Document Intelligence</div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

#     st.markdown("**🔑 Groq API Key**")
#     api_key = st.text_input(
#         "Groq API Key", type="password",
#         placeholder="gsk_...", label_visibility="collapsed",
#     )

#     st.markdown("**🤖 Model**")
#     model_choice = st.selectbox("Model", [
#         "llama-3.3-70b-versatile",
#         "llama3-8b-8192",
#         "mixtral-8x7b-32768",
#         "gemma2-9b-it",
#     ], label_visibility="collapsed")

#     with st.expander("⚙️  Advanced Settings"):
#         temperature   = st.slider("Temperature",    0.0, 1.0, 0.3, 0.05)
#         chunk_size    = st.slider("Chunk Size",      300, 2000, 1000, 100)
#         chunk_overlap = st.slider("Chunk Overlap",    50,  500,  200,  50)
#         top_k         = st.slider("Retrieval Top-K",   2,   10,    4,   1)

#     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

#     st.markdown("**📄 Upload Documents**")
#     uploaded_files = st.file_uploader(
#         "Upload PDFs", type=["pdf"], accept_multiple_files=True,
#         label_visibility="collapsed",
#     )
#     process_btn = st.button("⚡  Process Documents", use_container_width=True)

#     st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
#     if st.session_state.docs_processed:
#         st.markdown('<span class="status-pill status-ready">● Ready</span>', unsafe_allow_html=True)
#     elif uploaded_files:
#         st.markdown('<span class="status-pill status-waiting">◌ Click Process</span>', unsafe_allow_html=True)
#     else:
#         st.markdown('<span class="status-pill status-waiting">◌ Awaiting files</span>', unsafe_allow_html=True)

#     if st.session_state.docs_processed:
#         st.markdown(
#             f"""
#             <div class="stat-row">
#               <div class="stat-card">
#                 <div class="stat-num">{st.session_state.doc_count}</div>
#                 <div class="stat-label">Docs</div>
#               </div>
#               <div class="stat-card">
#                 <div class="stat-num">{st.session_state.chunk_count}</div>
#                 <div class="stat-label">Chunks</div>
#               </div>
#               <div class="stat-card">
#                 <div class="stat-num">{len(st.session_state.messages)//2}</div>
#                 <div class="stat-label">Q&amp;A</div>
#               </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

#     if st.session_state.doc_names:
#         st.markdown("**📚 Loaded Files**")
#         for name in st.session_state.doc_names:
#             st.markdown(
#                 f'<div style="font-size:0.73rem;color:var(--muted);padding:2px 0;">📃 {name}</div>',
#                 unsafe_allow_html=True,
#             )

#     st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
#     if st.button("🗑️  Clear Chat", use_container_width=True):
#         st.session_state.messages     = []
#         st.session_state.last_sources = []
#         st.rerun()


# # ─────────────────────────────────────────────
# # PROCESS DOCUMENTS
# # ─────────────────────────────────────────────

# if process_btn:
#     if not api_key:
#         st.error("⚠️  Please enter your Groq API key.")
#     elif not uploaded_files:
#         st.warning("📄  Upload at least one PDF first.")
#     else:
#         with st.spinner("🔄  Embedding documents…"):
#             try:
#                 paths = save_uploaded_files(uploaded_files)
#                 db, embeddings, n_chunks = process_documents(
#                     paths, chunk_size=chunk_size, chunk_overlap=chunk_overlap,
#                 )
#                 llm   = llm_model(api_key=api_key, model_name=model_choice, temperature=temperature)
#                 chain = build_qa_chain(db, llm, k=top_k)

#                 st.session_state.qa_chain       = chain
#                 st.session_state.docs_processed = True
#                 st.session_state.doc_names      = [f.name for f in uploaded_files]
#                 st.session_state.doc_count      = len(uploaded_files)
#                 st.session_state.chunk_count    = n_chunks
#                 st.session_state.messages       = []
#                 st.session_state.last_sources   = []

#                 st.success(f"✅  {len(uploaded_files)} doc(s) → {n_chunks} chunks. Start chatting!")
#                 time.sleep(0.8)
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"❌  {e}")


# # ─────────────────────────────────────────────
# # MAIN 2-COLUMN LAYOUT (Chat | Right Panel)
# # ─────────────────────────────────────────────

# col_chat, col_right = st.columns([6, 4], gap="medium")


# # ══════════════════════════════════════════════
# # CHAT COLUMN
# # ══════════════════════════════════════════════

# with col_chat:
#     st.markdown(
#         """
#         <div class="logo-header" style="margin-bottom:2px;">
#             <div style="font-size:1.5rem;">🧠</div>
#             <div>
#                 <div class="logo-title" style="font-size:1.4rem;">DocMind</div>
#                 <div class="logo-sub">Ask anything about your documents</div>
#             </div>
#         </div>
#         <div class="fancy-divider"></div>
#         """,
#         unsafe_allow_html=True,
#     )

#     if not st.session_state.docs_processed:
#         st.markdown(
#             """
#             <div style="text-align:center;padding:70px 10px;color:var(--muted);">
#                 <div style="font-size:3.5rem;margin-bottom:14px;">📂</div>
#                 <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
#                             color:var(--text);margin-bottom:8px;">
#                     Upload & Process Documents First
#                 </div>
#                 <div style="font-size:0.82rem;max-width:340px;margin:0 auto;line-height:1.75;">
#                     Add PDFs in the sidebar → enter Groq API key →
#                     click <strong>⚡ Process Documents</strong>.
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#     else:
#         # ── Chat history ─────────────────────
#         chat_html = '<div class="chat-wrap">'
#         for msg in st.session_state.messages:
#             role    = msg["role"]
#             content = msg["content"]
#             sources = msg.get("sources", [])
#             avatar  = "👤" if role == "user" else "🧠"
#             cls     = "user" if role == "user" else "bot"

#             chips = ""
#             if sources:
#                 chips = '<div class="sources-wrap">'
#                 for s in sources:
#                     chips += (
#                         f'<span class="src-chip" title="{s.get("snippet","")[:80]}">'
#                         f'📄 {s["file"]} · p{s["page"]}</span>'
#                     )
#                 chips += "</div>"

#             chat_html += f"""
#             <div class="msg-row {cls}">
#                 <div class="avatar {cls}">{avatar}</div>
#                 <div class="bubble {cls}">{content}{chips}</div>
#             </div>
#             """
#         chat_html += "</div>"
#         st.markdown(chat_html, unsafe_allow_html=True)

#         if not st.session_state.messages:
#             st.markdown(
#                 """
#                 <div style="text-align:center;padding:35px 0;color:var(--muted);">
#                     <div style="font-size:1.8rem;margin-bottom:8px;">💬</div>
#                     <div style="font-size:0.8rem;">Ready — ask your first question below</div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#         # ── Suggested questions ───────────────
#         with st.expander("💡  Suggested Questions", expanded=False):
#             examples = [
#                 "Summarise the main topics in the documents.",
#                 "What are the key findings or conclusions?",
#                 "List the most important facts mentioned.",
#                 "Are there any important dates or numbers?",
#                 "Compare the different sections or documents.",
#             ]
#             c1, c2 = st.columns(2)
#             for i, q in enumerate(examples):
#                 if (c1 if i % 2 == 0 else c2).button(q, key=f"ex_{i}"):
#                     # Store as pending question — processed after form below
#                     st.session_state["pending_question"] = q
#                     st.rerun()

#         st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

#         # ── Handle pending question from suggested-question buttons ───
#         pending = st.session_state.pop("pending_question", None)
#         if pending:
#             last_user = next(
#                 (m for m in reversed(st.session_state.messages) if m["role"] == "user"),
#                 None,
#             )
#             if not (last_user and last_user["content"] == pending):
#                 st.session_state.messages.append({"role": "user", "content": pending, "sources": []})
#                 with st.spinner("🧠  Thinking…"):
#                     try:
#                         result  = ask_question(st.session_state.qa_chain, pending)
#                         answer  = result["answer"]
#                         sources = result["sources"]
#                     except Exception as e:
#                         answer  = f"⚠️  Error: {e}"
#                         sources = []
#                 st.session_state.messages.append({"role": "bot", "content": answer, "sources": sources})
#                 st.session_state.last_sources = sources
#                 st.rerun()

#         # ── Input form (prevents infinite re-run loop) ────────────────
#         # st.form only submits on Enter key OR button click — never on re-render
#         with st.form(key="chat_form", clear_on_submit=True):
#             ci, cs = st.columns([9, 1])
#             with ci:
#                 user_input = st.text_input(
#                     "Ask",
#                     placeholder="Ask anything about your documents…",
#                     label_visibility="collapsed",
#                 )
#             with cs:
#                 send = st.form_submit_button("Send", use_container_width=True)

#         # ── Handle send — only fires once per actual submission ────────
#         if send and user_input and user_input.strip():
#             question = user_input.strip()

#             # Guard: skip if this exact question was already the last user message
#             last_user = next(
#                 (m for m in reversed(st.session_state.messages) if m["role"] == "user"),
#                 None,
#             )
#             if last_user and last_user["content"] == question:
#                 st.stop()   # duplicate submission guard

#             st.session_state.messages.append({"role": "user", "content": question, "sources": []})

#             with st.spinner("🧠  Thinking…"):
#                 try:
#                     result  = ask_question(st.session_state.qa_chain, question)
#                     answer  = result["answer"]
#                     sources = result["sources"]
#                 except Exception as e:
#                     answer  = f"⚠️  Error: {e}"
#                     sources = []

#             st.session_state.messages.append({"role": "bot", "content": answer, "sources": sources})
#             st.session_state.last_sources = sources
#             st.rerun()


# # ══════════════════════════════════════════════
# # RIGHT PANEL: RETRIEVAL INSPECTOR
# # ══════════════════════════════════════════════

# with col_right:
#     st.markdown('<div class="right-panel-wrap">', unsafe_allow_html=True)

#     # ── Panel header ─────────────────────────
#     st.markdown(
#         """
#         <div class="rp-header">🔍 Retrieval Inspector</div>
#         <div class="rp-sub">Top retrieved chunks &amp; source metadata · updates after each answer</div>
#         <div class="fancy-divider divider-indigo"></div>
#         """,
#         unsafe_allow_html=True,
#     )

#     sources = st.session_state.last_sources

#     # ── Tabs ─────────────────────────────────
#     tab_chunks, tab_sources = st.tabs(["📦  Top Chunks", "📑  Source Info"])

#     # ────────────────────────────────
#     # TAB 1 : TOP CHUNKS
#     # ────────────────────────────────
#     with tab_chunks:
#         if not sources:
#             st.markdown(
#                 """
#                 <div class="rp-empty">
#                     <div class="rp-empty-icon">📭</div>
#                     <div class="rp-empty-text">
#                         No chunks yet.<br>
#                         Ask a question and the top retrieved
#                         chunks will appear here with relevance scores.
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#         else:
#             st.markdown(
#                 f'<div style="font-size:0.7rem;color:var(--muted);margin-bottom:10px;">'
#                 f'Showing <strong style="color:var(--accent)">{len(sources)}</strong> '
#                 f'retrieved chunk(s) — ranked by relevance</div>',
#                 unsafe_allow_html=True,
#             )

#             for i, chunk in enumerate(sources, 1):
#                 file_name = chunk.get("file", "unknown")
#                 page      = chunk.get("page", "?")
#                 snippet   = chunk.get("snippet", "").replace("<", "&lt;").replace(">", "&gt;")
#                 # Visual relevance bar: top chunk gets ~100%, decreasing
#                 bar_pct   = max(25, 100 - (i - 1) * 20)

#                 st.markdown(
#                     f"""
#                     <div class="chunk-card">

#                         <!-- Header row: rank + file badge -->
#                         <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
#                             <div class="chunk-rank">#{i}</div>
#                             <div class="chunk-badge">📄 {file_name}</div>
#                         </div>

#                         <!-- Relevance bar -->
#                         <div style="margin-bottom:8px;">
#                             <div style="display:flex;justify-content:space-between;
#                                 font-size:0.6rem;color:var(--muted);margin-bottom:3px;">
#                                 <span>Relevance</span>
#                                 <span style="color:var(--accent);">{bar_pct}%</span>
#                             </div>
#                             <div style="height:5px;background:var(--border);
#                                 border-radius:3px;overflow:hidden;">
#                                 <div style="height:100%;width:{bar_pct}%;
#                                     background:linear-gradient(90deg,var(--accent),var(--accent2));
#                                     border-radius:3px;transition:width .4s ease;">
#                                 </div>
#                             </div>
#                         </div>

#                         <!-- Snippet text -->
#                         <div class="chunk-text">{snippet}…</div>

#                         <!-- Meta tags -->
#                         <div class="chunk-meta">
#                             <span class="meta-tag file">📁 {file_name}</span>
#                             <span class="meta-tag page">📖 p.{page}</span>
#                             <span class="meta-tag score">⭐ #{i}</span>
#                             <span class="meta-tag" style="color:var(--warn);
#                                 border-color:rgba(251,191,36,.3);background:rgba(251,191,36,.07);">
#                                 🔤 {len(chunk.get("snippet",""))} chars
#                             </span>
#                         </div>

#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#     # ────────────────────────────────
#     # TAB 2 : SOURCE INFO
#     # ────────────────────────────────
#     with tab_sources:
#         if not sources:
#             st.markdown(
#                 """
#                 <div class="rp-empty">
#                     <div class="rp-empty-icon">📋</div>
#                     <div class="rp-empty-text">
#                         No source data yet.<br>
#                         After you ask a question, detailed source
#                         metadata will appear here.
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#         else:
#             # ── Summary stats row ─────────────
#             unique_files = list({s["file"] for s in sources})
#             unique_pages = list({str(s["page"]) for s in sources})

#             st.markdown(
#                 f"""
#                 <div class="stat-row" style="margin-bottom:12px;">
#                     <div class="stat-card">
#                         <div class="stat-num" style="font-size:1.1rem;color:var(--accent);">
#                             {len(sources)}
#                         </div>
#                         <div class="stat-label">Sources</div>
#                     </div>
#                     <div class="stat-card">
#                         <div class="stat-num" style="font-size:1.1rem;color:var(--accent2);">
#                             {len(unique_files)}
#                         </div>
#                         <div class="stat-label">Files</div>
#                     </div>
#                     <div class="stat-card">
#                         <div class="stat-num" style="font-size:1.1rem;color:var(--accent3);">
#                             {len(unique_pages)}
#                         </div>
#                         <div class="stat-label">Pages</div>
#                     </div>
#                 </div>
#                 <div class="fancy-divider divider-pink"></div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             # ── Per-source detail cards ───────
#             for i, src in enumerate(sources, 1):
#                 safe_snippet = (
#                     src.get("snippet", "")[:160]
#                     .replace("<", "&lt;")
#                     .replace(">", "&gt;")
#                 )
#                 char_count = len(src.get("snippet", ""))

#                 st.markdown(
#                     f"""
#                     <div class="src-card">
#                         <div class="src-card-title">
#                             <span style="background:rgba(129,140,248,.15);
#                                 border:1px solid rgba(129,140,248,.3);
#                                 border-radius:999px;padding:1px 7px;font-size:0.6rem;">
#                                 #{i}
#                             </span>
#                             {src.get("file","unknown")}
#                         </div>

#                         <div class="src-card-row">
#                             <span class="src-card-key">📖 Page</span>
#                             <span class="src-card-val">{src.get("page","?")}</span>
#                         </div>
#                         <div class="src-card-row">
#                             <span class="src-card-key">📁 Source File</span>
#                             <span class="src-card-val">{src.get("file","unknown")}</span>
#                         </div>
#                         <div class="src-card-row">
#                             <span class="src-card-key">🔤 Snippet Length</span>
#                             <span class="src-card-val">{char_count} chars</span>
#                         </div>
#                         <div class="src-card-row">
#                             <span class="src-card-key">⭐ Retrieval Rank</span>
#                             <span class="src-card-val" style="color:var(--accent);">#{i}</span>
#                         </div>

#                         <!-- Excerpt block -->
#                         <div style="margin-top:9px;">
#                             <div style="font-size:0.6rem;color:var(--muted);margin-bottom:4px;">
#                                 📝 Excerpt Preview
#                             </div>
#                             <div style="font-size:0.7rem;color:var(--text);
#                                 background:var(--bg);border:1px solid var(--border);
#                                 border-radius:8px;padding:8px 10px;line-height:1.6;
#                                 border-left:3px solid rgba(244,114,182,.5);">
#                                 {safe_snippet}…
#                             </div>
#                         </div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#             # ── File coverage breakdown ───────
#             st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
#             st.markdown(
#                 '<div style="font-size:0.7rem;color:var(--muted);margin-bottom:8px;">'
#                 '📊 File Coverage Breakdown</div>',
#                 unsafe_allow_html=True,
#             )
#             file_counts = Counter(s["file"] for s in sources)
#             for fname, count in file_counts.items():
#                 pct = int(count / len(sources) * 100)
#                 st.markdown(
#                     f"""
#                     <div style="margin-bottom:9px;">
#                         <div style="display:flex;justify-content:space-between;
#                             font-size:0.65rem;margin-bottom:3px;">
#                             <span style="color:var(--text);">📃 {fname}</span>
#                             <span style="color:var(--accent);">{count} chunk(s) · {pct}%</span>
#                         </div>
#                         <div style="height:5px;background:var(--border);
#                             border-radius:3px;overflow:hidden;">
#                             <div style="height:100%;width:{pct}%;
#                                 background:linear-gradient(90deg,var(--accent2),var(--accent3));
#                                 border-radius:3px;">
#                             </div>
#                         </div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#     st.markdown("</div>", unsafe_allow_html=True)   # close .right-panel-wrap

"""
app.py  —  DocMind RAG Chatbot  (clean rewrite)
Run:  streamlit run app.py
"""

import os, time, warnings
from collections import Counter
import streamlit as st

from rag_backend import (
    save_uploaded_files,
    process_documents,
    llm_model,
    build_qa_chain,
    ask_question,
)

# ──────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind · RAG Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# THEME & GLOBAL CSS
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

/* ── palette ── */
:root {
    --bg:       #f0f4f8;
    --surface:  #ffffff;
    --sidebar:  #1e2433;
    --border:   #e2e8f0;
    --accent:   #6366f1;
    --accent-light: #eef2ff;
    --accent2:  #10b981;
    --accent2-light: #ecfdf5;
    --danger:   #ef4444;
    --warn:     #f59e0b;
    --text:     #1e293b;
    --muted:    #64748b;
    --user-bg:  #6366f1;
    --bot-bg:   #ffffff;
    --radius:   12px;
    --shadow:   0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06);
    --shadow-md:0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.06);
}

/* ── reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: var(--sidebar) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] strong { color: #f1f5f9 !important; }

/* ── sidebar inputs ── */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select,
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #2d3548 !important;
    border: 1px solid #3d4a63 !important;
    color: #f1f5f9 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stSlider { filter: brightness(1.3); }

/* ── main area ── */
.block-container { padding: 1.5rem 2rem 1rem !important; max-width: 100% !important; }

/* ── page header ── */
.page-header {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 16px;
}
.page-title {
    font-size: 1.5rem; font-weight: 700;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.page-sub { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }

/* ── divider ── */
.divider { height: 1px; background: var(--border); margin: 12px 0; }

/* ── pills ── */
.pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 999px; font-size: 0.72rem; font-weight: 500;
}
.pill-green  { background: var(--accent2-light); color: var(--accent2);  border: 1px solid #6ee7b7; }
.pill-yellow { background: #fffbeb; color: var(--warn); border: 1px solid #fde68a; }
.pill-indigo { background: var(--accent-light);  color: var(--accent);   border: 1px solid #c7d2fe; }

/* ── stat cards in sidebar ── */
.stat-row { display: flex; gap: 8px; margin: 10px 0; }
.stat-card {
    flex: 1; background: #2d3548; border: 1px solid #3d4a63;
    border-radius: 10px; padding: 8px; text-align: center;
}
.stat-num  { font-size: 1.3rem; font-weight: 700; color: #6ee7b7; }
.stat-lbl  { font-size: 0.6rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .08em; }

/* ── sidebar file list ── */
.file-item {
    display: flex; align-items: center; gap: 7px;
    background: #2d3548; border: 1px solid #3d4a63;
    border-radius: 8px; padding: 6px 10px; margin: 4px 0;
    font-size: 0.72rem; color: #cbd5e1;
}

/* ── sidebar button ── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--accent), #818cf8) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.82rem !important; padding: 10px !important;
    width: 100% !important; transition: opacity .2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover { opacity: .88 !important; }

/* clear chat button override */
.clear-btn > button {
    background: #2d3548 !important;
    border: 1px solid #3d4a63 !important;
    color: #94a3b8 !important;
}

/* ── chat container ── */
.chat-scroll {
    display: flex; flex-direction: column; gap: 16px;
    padding: 8px 4px 20px; min-height: 200px;
}

/* ── message rows ── */
.msg-user {
    display: flex; justify-content: flex-end; gap: 10px; align-items: flex-end;
}
.msg-bot {
    display: flex; justify-content: flex-start; gap: 10px; align-items: flex-end;
}
.avatar-circle {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem; flex-shrink: 0;
}
.avatar-user { background: var(--accent); }
.avatar-bot  { background: linear-gradient(135deg, var(--accent2), #059669); }

.bubble-user {
    background: var(--accent); color: #fff;
    padding: 10px 14px; border-radius: 18px 18px 4px 18px;
    max-width: 75%; font-size: 0.875rem; line-height: 1.6;
    box-shadow: var(--shadow);
}
.bubble-bot {
    background: var(--surface); color: var(--text);
    padding: 12px 16px; border-radius: 18px 18px 18px 4px;
    max-width: 80%; font-size: 0.875rem; line-height: 1.7;
    box-shadow: var(--shadow); border: 1px solid var(--border);
}

/* ── source chips under bot bubble ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
.chip {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 8px; border-radius: 999px; font-size: 0.65rem;
    background: var(--accent-light); color: var(--accent);
    border: 1px solid #c7d2fe;
}

/* ── form input ── */
.stForm { background: transparent !important; border: none !important; padding: 0 !important; }
.stTextInput input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 12px 16px !important;
    box-shadow: var(--shadow) !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}
.stTextInput input::placeholder { color: #94a3b8 !important; }

/* send button */
.stFormSubmitButton > button {
    background: var(--accent) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important;
    font-size: 0.85rem !important; height: 46px !important;
    padding: 0 20px !important; white-space: nowrap !important;
}
.stFormSubmitButton > button:hover { background: #4f46e5 !important; }

/* ── expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stExpander"] summary {
    color: var(--muted) !important; font-size: 0.8rem !important;
}

/* ── suggested Q buttons ── */
div[data-testid="stExpander"] .stButton > button {
    background: var(--accent-light) !important;
    color: var(--accent) !important;
    border: 1px solid #c7d2fe !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    white-space: normal !important;
    height: auto !important;
}

/* ── RIGHT PANEL ── */
.rp-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 16px;
    height: 100%;
}
.rp-title {
    font-size: 0.9rem; font-weight: 700; color: var(--text);
    display: flex; align-items: center; gap: 6px; margin-bottom: 2px;
}
.rp-sub { font-size: 0.7rem; color: var(--muted); margin-bottom: 12px; }

/* chunk card */
.chunk-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    transition: border-color .15s, box-shadow .15s;
}
.chunk-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(99,102,241,.08);
}
.chunk-header {
    display: flex; align-items: center; gap: 8px; margin-bottom: 8px;
}
.rank-badge {
    width: 22px; height: 22px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: #fff; font-size: 0.65rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.file-badge {
    background: var(--accent-light); color: var(--accent);
    border: 1px solid #c7d2fe; border-radius: 999px;
    font-size: 0.65rem; padding: 2px 8px; font-weight: 500;
}
.rel-bar-wrap { margin-bottom: 8px; }
.rel-bar-label {
    display: flex; justify-content: space-between;
    font-size: 0.62rem; color: var(--muted); margin-bottom: 3px;
}
.rel-bar-track {
    height: 5px; background: var(--border); border-radius: 3px; overflow: hidden;
}
.rel-bar-fill {
    height: 100%; border-radius: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width .4s ease;
}
.chunk-snippet {
    font-size: 0.775rem; color: var(--text); line-height: 1.6;
    border-left: 3px solid var(--accent); padding-left: 10px;
    background: var(--surface); border-radius: 0 6px 6px 0;
    padding: 6px 10px; margin-bottom: 8px;
}
.meta-row { display: flex; gap: 6px; flex-wrap: wrap; }
.meta-tag {
    font-size: 0.62rem; border-radius: 999px; padding: 2px 8px; font-weight: 500;
}
.mt-file  { background: var(--accent-light);  color: var(--accent);  border: 1px solid #c7d2fe; }
.mt-page  { background: var(--accent2-light); color: var(--accent2); border: 1px solid #6ee7b7; }
.mt-rank  { background: #fff7ed; color: #f97316; border: 1px solid #fed7aa; }
.mt-chars { background: #fefce8; color: #ca8a04; border: 1px solid #fde68a; }

/* source info card */
.src-card {
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 14px; margin-bottom: 10px;
}
.src-card-head {
    font-weight: 600; font-size: 0.78rem; color: var(--text);
    display: flex; align-items: center; gap: 6px; margin-bottom: 8px;
}
.src-row {
    display: flex; justify-content: space-between;
    font-size: 0.7rem; padding: 4px 0;
    border-bottom: 1px solid var(--border);
}
.src-row:last-child { border-bottom: none; }
.src-key { color: var(--muted); }
.src-val { color: var(--text); font-weight: 500; text-align: right; max-width: 60%; word-break: break-all; }
.excerpt-box {
    margin-top: 8px; padding: 8px 10px;
    background: var(--surface); border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 0 8px 8px 0;
    font-size: 0.72rem; color: var(--muted); line-height: 1.6;
}

/* coverage bar */
.cov-item { margin-bottom: 10px; }
.cov-label {
    display: flex; justify-content: space-between;
    font-size: 0.68rem; margin-bottom: 4px;
}
.cov-track { height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.cov-fill  {
    height: 100%; border-radius: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}

/* empty state */
.empty-state {
    display: flex; flex-direction: column; align-items: center;
    padding: 40px 10px; color: var(--muted); text-align: center; gap: 8px;
}
.empty-icon { font-size: 2.2rem; }
.empty-text { font-size: 0.78rem; line-height: 1.6; }

/* welcome card */
.welcome-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); box-shadow: var(--shadow);
    padding: 50px 30px; text-align: center;
}
.welcome-icon  { font-size: 3rem; margin-bottom: 12px; }
.welcome-title { font-size: 1.2rem; font-weight: 700; color: var(--text); margin-bottom: 6px; }
.welcome-sub   { font-size: 0.83rem; color: var(--muted); line-height: 1.7; max-width: 340px; margin: 0 auto; }

.step-row { display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap; }
.step {
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 10px 14px;
    font-size: 0.75rem; color: var(--text); text-align: center; width: 130px;
}
.step-num {
    width: 24px; height: 24px; border-radius: 50%;
    background: var(--accent); color: #fff;
    font-size: 0.7rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 6px;
}

/* file uploader */
[data-testid="stFileUploader"] {
    background: #2d3548 !important;
    border: 1px dashed #4d5a78 !important;
    border-radius: 10px !important;
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg) !important;
    border-radius: 8px !important; padding: 3px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    font-size: 0.78rem !important; font-weight: 500 !important;
    color: var(--muted) !important;
    padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--accent) !important;
    box-shadow: var(--shadow) !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────
def _init():
    defaults = dict(
        messages=[], qa_chain=None, docs_processed=False,
        doc_names=[], chunk_count=0, doc_count=0, last_sources=[],
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ──────────────────────────────────────────────────────────
# LEFT SIDEBAR
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="padding:10px 0 6px;">
            <div style="font-size:1.6rem;font-weight:800;
                background:linear-gradient(135deg,#6ee7b7,#818cf8);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                🧠 DocMind
            </div>
            <div style="font-size:0.68rem;color:#64748b;letter-spacing:.12em;
                text-transform:uppercase;margin-top:2px;">
                RAG · Document Intelligence
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider" style="background:#2d3548;"></div>', unsafe_allow_html=True)

    # API Key
    st.markdown('<p style="font-size:0.75rem;font-weight:600;color:#94a3b8;margin-bottom:4px;">🔑 GROQ API KEY</p>', unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="gsk_...", label_visibility="collapsed")

    # Model
    st.markdown('<p style="font-size:0.75rem;font-weight:600;color:#94a3b8;margin:10px 0 4px;">🤖 MODEL</p>', unsafe_allow_html=True)
    model_choice = st.selectbox("Model", [
        "llama-3.3-70b-versatile", "llama3-8b-8192",
        "mixtral-8x7b-32768", "gemma2-9b-it",
    ], label_visibility="collapsed")

    with st.expander("⚙️ Advanced Settings"):
        temperature   = st.slider("Temperature",   0.0, 1.0, 0.3, 0.05)
        chunk_size    = st.slider("Chunk Size",     300, 2000, 1000, 100)
        chunk_overlap = st.slider("Chunk Overlap",   50,  500,  200,  50)
        top_k         = st.slider("Retrieval Top-K",  2,   10,    4,   1)

    st.markdown('<div class="divider" style="background:#2d3548;margin:14px 0;"></div>', unsafe_allow_html=True)

    # Upload
    st.markdown('<p style="font-size:0.75rem;font-weight:600;color:#94a3b8;margin-bottom:6px;">📄 UPLOAD DOCUMENTS</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed",
    )
    process_btn = st.button("⚡  Process Documents", use_container_width=True)

    # Status
    st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
    if st.session_state.docs_processed:
        st.markdown('<span class="pill pill-green">● Ready to chat</span>', unsafe_allow_html=True)
    elif uploaded_files:
        st.markdown('<span class="pill pill-yellow">◌ Click Process</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill pill-yellow">◌ Upload files first</span>', unsafe_allow_html=True)

    # Stats
    if st.session_state.docs_processed:
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-num">{st.session_state.doc_count}</div>
                <div class="stat-lbl">Docs</div>
            </div>
            <div class="stat-card">
                <div class="stat-num">{st.session_state.chunk_count}</div>
                <div class="stat-lbl">Chunks</div>
            </div>
            <div class="stat-card">
                <div class="stat-num">{len(st.session_state.messages)//2}</div>
                <div class="stat-lbl">Q&amp;A</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # File list
    if st.session_state.doc_names:
        st.markdown('<div class="divider" style="background:#2d3548;margin:12px 0;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.72rem;font-weight:600;color:#94a3b8;margin-bottom:6px;">📚 LOADED FILES</p>', unsafe_allow_html=True)
        for name in st.session_state.doc_names:
            st.markdown(f'<div class="file-item">📃 {name}</div>', unsafe_allow_html=True)

    # Clear
    st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑️  Clear Chat", use_container_width=True):
            st.session_state.messages     = []
            st.session_state.last_sources = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# PROCESS DOCUMENTS
# ──────────────────────────────────────────────────────────
if process_btn:
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
    elif not uploaded_files:
        st.warning("📄 Please upload at least one PDF file.")
    else:
        with st.spinner("🔄 Processing documents — embedding & indexing…"):
            try:
                paths = save_uploaded_files(uploaded_files)
                db, embeddings, n_chunks = process_documents(
                    paths, chunk_size=chunk_size, chunk_overlap=chunk_overlap,
                )
                llm   = llm_model(api_key=api_key, model_name=model_choice, temperature=temperature)
                chain = build_qa_chain(db, llm, k=top_k)

                st.session_state.update(dict(
                    qa_chain=chain, docs_processed=True,
                    doc_names=[f.name for f in uploaded_files],
                    doc_count=len(uploaded_files), chunk_count=n_chunks,
                    messages=[], last_sources=[],
                ))
                st.success(f"✅ {len(uploaded_files)} doc(s) → {n_chunks} chunks. Start chatting!")
                time.sleep(0.8)
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")


# ──────────────────────────────────────────────────────────
# MAIN LAYOUT: Chat (left 60%) | Inspector (right 40%)
# ──────────────────────────────────────────────────────────
col_chat, col_right = st.columns([6, 4], gap="large")


# ══════════════════════════════════════════════
# CHAT COLUMN
# ══════════════════════════════════════════════
with col_chat:

    # Page header
    st.markdown("""
    <div class="page-header">
        <span style="font-size:1.5rem;">🧠</span>
        <div>
            <div class="page-title">DocMind</div>
            <div class="page-sub">Ask anything about your uploaded documents</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Welcome screen ──────────────────────────────
    if not st.session_state.docs_processed:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">📂</div>
            <div class="welcome-title">Welcome to DocMind</div>
            <div class="welcome-sub">
                Upload your PDF documents, process them, and start
                having intelligent conversations with your content.
            </div>
            <div class="step-row">
                <div class="step">
                    <div class="step-num">1</div>
                    Enter Groq API key
                </div>
                <div class="step">
                    <div class="step-num">2</div>
                    Upload PDF files
                </div>
                <div class="step">
                    <div class="step-num">3</div>
                    Click Process Documents
                </div>
                <div class="step">
                    <div class="step-num">4</div>
                    Ask questions!
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # ── Chat messages ───────────────────────────
        # Render each message with st.chat_message for proper markdown support
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center;padding:40px 0;color:var(--muted);">
                <div style="font-size:2rem;margin-bottom:8px;">💬</div>
                <div style="font-size:0.82rem;">
                    Documents are ready! Ask your first question below.
                </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.messages:
            role    = msg["role"]
            content = msg["content"]
            sources = msg.get("sources", [])

            if role == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant", avatar="🧠"):
                    st.markdown(content)
                    # Source chips
                    if sources:
                        chips_html = '<div class="chip-row">'
                        for s in sources:
                            chips_html += (
                                f'<span class="chip" title="{s.get("snippet","")[:100]}">'
                                f'📄 {s["file"]} · p{s["page"]}</span>'
                            )
                        chips_html += "</div>"
                        st.markdown(chips_html, unsafe_allow_html=True)

        # ── Suggested questions ────────────────────
        with st.expander("💡 Suggested Questions", expanded=False):
            examples = [
                "Summarise the main topics in the documents.",
                "What are the key findings or conclusions?",
                "List the most important facts mentioned.",
                "Are there any important dates or numbers?",
                "Compare the different sections or documents.",
            ]
            c1, c2 = st.columns(2)
            for i, q in enumerate(examples):
                col = c1 if i % 2 == 0 else c2
                if col.button(q, key=f"ex_{i}", use_container_width=True):
                    st.session_state["pending_q"] = q
                    st.rerun()

        st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

        # ── Handle pending suggested question ──────
        pending = st.session_state.pop("pending_q", None)
        if pending:
            last_user = next(
                (m for m in reversed(st.session_state.messages) if m["role"] == "user"), None
            )
            if not (last_user and last_user["content"] == pending):
                st.session_state.messages.append({"role": "user", "content": pending, "sources": []})
                with st.spinner("🧠 Thinking…"):
                    try:
                        res     = ask_question(st.session_state.qa_chain, pending)
                        answer  = res["answer"]
                        sources = res["sources"]
                    except Exception as e:
                        answer  = f"⚠️ Error: {e}"
                        sources = []
                st.session_state.messages.append({"role": "bot", "content": answer, "sources": sources})
                st.session_state.last_sources = sources
                st.rerun()

        # ── Input form ─────────────────────────────
        with st.form("chat_form", clear_on_submit=True):
            ci, cs = st.columns([9, 1])
            with ci:
                user_input = st.text_input(
                    "Question", placeholder="Ask anything about your documents…",
                    label_visibility="collapsed",
                )
            with cs:
                submitted = st.form_submit_button("Send", use_container_width=True)

        if submitted and user_input and user_input.strip():
            question  = user_input.strip()
            last_user = next(
                (m for m in reversed(st.session_state.messages) if m["role"] == "user"), None
            )
            if last_user and last_user["content"] == question:
                st.stop()

            st.session_state.messages.append({"role": "user", "content": question, "sources": []})
            with st.spinner("🧠 Thinking…"):
                try:
                    res     = ask_question(st.session_state.qa_chain, question)
                    answer  = res["answer"]
                    sources = res["sources"]
                except Exception as e:
                    answer  = f"⚠️ Error: {e}"
                    sources = []
            st.session_state.messages.append({"role": "bot", "content": answer, "sources": sources})
            st.session_state.last_sources = sources
            st.rerun()


# ══════════════════════════════════════════════
# RIGHT PANEL — RETRIEVAL INSPECTOR
# ══════════════════════════════════════════════
with col_right:
    st.markdown('<div class="rp-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div class="rp-title">🔍 Retrieval Inspector</div>
    <div class="rp-sub">Top retrieved chunks &amp; source metadata — updates after each answer</div>
    """, unsafe_allow_html=True)

    sources = st.session_state.last_sources
    tab_chunks, tab_sources = st.tabs(["📦 Top Chunks", "📑 Source Info"])

    # ────────────────────────────────
    # TAB 1: TOP CHUNKS
    # ────────────────────────────────
    with tab_chunks:
        if not sources:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-text">
                    No chunks yet.<br>
                    Ask a question to see the top retrieved
                    chunks with relevance scores here.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                f'<p style="font-size:0.72rem;color:var(--muted);margin-bottom:12px;">'
                f'Showing <strong style="color:var(--accent);">{len(sources)}</strong> '
                f'chunk(s) ranked by relevance</p>',
                unsafe_allow_html=True,
            )
            for i, chunk in enumerate(sources, 1):
                fname   = chunk.get("file", "unknown")
                page    = chunk.get("page", "?")
                snippet = chunk.get("snippet", "")
                # Sanitize snippet for safe HTML display
                safe_snippet = snippet[:300].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                bar_pct = max(20, 100 - (i - 1) * 22)
                char_count = len(snippet)

                st.markdown(f"""
                <div class="chunk-card">
                    <div class="chunk-header">
                        <div class="rank-badge">#{i}</div>
                        <div class="file-badge">📄 {fname}</div>
                    </div>
                    <div class="rel-bar-wrap">
                        <div class="rel-bar-label">
                            <span>Relevance</span>
                            <span style="color:var(--accent);font-weight:600;">{bar_pct}%</span>
                        </div>
                        <div class="rel-bar-track">
                            <div class="rel-bar-fill" style="width:{bar_pct}%;"></div>
                        </div>
                    </div>
                    <div class="chunk-snippet">{safe_snippet}…</div>
                    <div class="meta-row">
                        <span class="meta-tag mt-file">📁 {fname}</span>
                        <span class="meta-tag mt-page">📖 p.{page}</span>
                        <span class="meta-tag mt-rank">⭐ #{i}</span>
                        <span class="meta-tag mt-chars">🔤 {char_count} chars</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ────────────────────────────────
    # TAB 2: SOURCE INFO
    # ────────────────────────────────
    with tab_sources:
        if not sources:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <div class="empty-text">
                    No source data yet.<br>
                    Ask a question to see detailed
                    source metadata here.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            unique_files = list({s["file"] for s in sources})
            unique_pages = list({str(s["page"]) for s in sources})

            # Summary stat row
            st.markdown(f"""
            <div class="stat-row" style="margin-bottom:12px;">
                <div class="stat-card" style="background:var(--accent-light);border-color:#c7d2fe;">
                    <div class="stat-num" style="color:var(--accent);">{len(sources)}</div>
                    <div class="stat-lbl" style="color:var(--accent);">Sources</div>
                </div>
                <div class="stat-card" style="background:var(--accent2-light);border-color:#6ee7b7;">
                    <div class="stat-num" style="color:var(--accent2);">{len(unique_files)}</div>
                    <div class="stat-lbl" style="color:var(--accent2);">Files</div>
                </div>
                <div class="stat-card" style="background:#fff7ed;border-color:#fed7aa;">
                    <div class="stat-num" style="color:#f97316;">{len(unique_pages)}</div>
                    <div class="stat-lbl" style="color:#f97316;">Pages</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Per-source detail cards
            for i, src in enumerate(sources, 1):
                safe_excerpt = (
                    src.get("snippet", "")[:180]
                    .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                )
                char_count = len(src.get("snippet", ""))

                st.markdown(f"""
                <div class="src-card">
                    <div class="src-card-head">
                        <span class="pill pill-indigo" style="padding:1px 7px;font-size:0.6rem;">#{i}</span>
                        {src.get("file","unknown")}
                    </div>
                    <div class="src-row">
                        <span class="src-key">📖 Page</span>
                        <span class="src-val">{src.get("page","?")}</span>
                    </div>
                    <div class="src-row">
                        <span class="src-key">📁 File</span>
                        <span class="src-val">{src.get("file","unknown")}</span>
                    </div>
                    <div class="src-row">
                        <span class="src-key">🔤 Characters</span>
                        <span class="src-val">{char_count}</span>
                    </div>
                    <div class="src-row">
                        <span class="src-key">⭐ Rank</span>
                        <span class="src-val" style="color:var(--accent);">#{i} of {len(sources)}</span>
                    </div>
                    <div class="excerpt-box">{safe_excerpt}…</div>
                </div>
                """, unsafe_allow_html=True)

            # File coverage
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:0.72rem;font-weight:600;color:var(--muted);margin-bottom:10px;">📊 File Coverage</p>', unsafe_allow_html=True)

            file_counts = Counter(s["file"] for s in sources)
            for fname, count in file_counts.items():
                pct = int(count / len(sources) * 100)
                st.markdown(f"""
                <div class="cov-item">
                    <div class="cov-label">
                        <span style="color:var(--text);font-size:0.7rem;">📃 {fname}</span>
                        <span style="color:var(--accent);font-weight:600;font-size:0.7rem;">
                            {count} chunk(s) · {pct}%
                        </span>
                    </div>
                    <div class="cov-track">
                        <div class="cov-fill" style="width:{pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)   # close rp-wrap