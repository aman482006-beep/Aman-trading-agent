import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# ---------------- CONFIG ----------------
config = DEFAULT_CONFIG.copy()

config.update({
    "llm_provider": "ollama",
    "deep_think_llm": "mistral",
    "quick_think_llm": "mistral",
    "deep_thinking_llm": "mistral",
    "quick_thinking_llm": "mistral",
    "backend_url": "http://localhost:11434/v1",
    "max_recur_limit": 2,
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
})

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Trading Analyst", 
    page_icon="🚀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ---------------- MODERN CSS ----------------
st.markdown("""
<style>
    /* Global Theme & Background */
    body {
        background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 60%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Title Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(148, 163, 184, 0.2);
    }

    /* Signal Badges */
    .signal-badge {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 12px;
        font-size: 28px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .badge-buy { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .badge-sell { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-hold { background: rgba(234, 179, 8, 0.1); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.3); }

    /* Button Override */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
        height: 42px;
        margin-top: 28px; /* Align with inputs */
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">AI Trading Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Agent AI • Local LLM • Built with Ollama</div>', unsafe_allow_html=True)

# ---------------- INPUT LAYOUT ----------------
# Using a container to group the input section neatly
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

    with col1:
        ticker = st.text_input("Stock Ticker", "NVDA", help="Enter a valid Yahoo Finance ticker.")

    with col2:
        date = st.text_input("Analysis Date", "2024-05-10", help="Format: YYYY-MM-DD")

    with col3:
        run = st.button("🚀 Analyze")
    
    with col4:
        # Empty column for spacing/alignment
        pass
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RUN ANALYSIS ----------------
if run:
    start_time = time.time()
    
    # Modern status indicator with estimated time
    with st.status("🤖 Initiating AI Trading Agents...", expanded=True) as status:
        st.write("⏳ **Estimated time:** 1-3 minutes depending on your local hardware.")
        st.write(f"📊 Fetching market data for **{ticker}**...")
        st.write("🧠 Agents are debating and analyzing risk...")
        
        # Execute the LLM logic
        try:
            ta = TradingAgentsGraph(debug=False, config=config)
            result = ta.propagate(ticker, date)
            result_str = str(result)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Update status upon completion
            status.update(
                label=f"✅ Analysis Complete in {elapsed_time:.1f} seconds!", 
                state="complete", 
                expanded=False
            )
        except Exception as e:
            status.update(label="❌ Error during analysis", state="error", expanded=True)
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.divider()

    # ---------------- CHART & METRICS ----------------
    col_chart, col_metric = st.columns([3, 1])
    
    with col_chart:
        st.markdown("### 📈 Historical Price Trend")
        try:
            data = yf.download(ticker, start="2023-01-01")
            fig = go.Figure()
            
            # Add a beautiful gradient fill to the chart
            fig.add_trace(go.Scatter(
                x=data.index, 
                y=data["Close"], 
                name="Price",
                line=dict(color='#38bdf8', width=2),
                fill='tozeroy',
                fillcolor='rgba(56, 189, 248, 0.1)'
            ))
            
            fig.update_layout(
                template="plotly_dark", 
                height=350,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning("Could not load chart data. Verify the ticker symbol.")

    with col_metric:
        st.markdown("### ⏱️ Execution Data")
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 30px 10px;">
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 5px;">Analysis Time</p>
            <h2 style="margin: 0; color: #f8fafc;">{elapsed_time:.1f}s</h2>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 15px; margin-bottom: 5px;">Model</p>
            <h4 style="margin: 0; color: #38bdf8;">Mistral</h4>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TABS ----------------
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🎯 Overview", "⚡ Key Insights", "📄 Full Report"])

    # --- TAB 1: OVERVIEW ---
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        col_dec, col_conf = st.columns(2)
        
        with col_dec:
            st.markdown("#### The Verdict")
            if "BUY" in result_str.upper():
                st.markdown('<div class="signal-badge badge-buy">🟢 STRONG BUY</div>', unsafe_allow_html=True)
                confidence = 80
            elif "SELL" in result_str.upper():
                st.markdown('<div class="signal-badge badge-sell">🔴 SELL</div>', unsafe_allow_html=True)
                confidence = 70
            else:
                st.markdown('<div class="signal-badge badge-hold">🟡 HOLD</div>', unsafe_allow_html=True)
                confidence = 60
                
        with col_conf:
            st.markdown("#### AI Confidence Level")
            st.markdown(f"<h1 style='margin-bottom: 5px;'>{confidence}%</h1>", unsafe_allow_html=True)
            st.progress(confidence / 100.0)

    # --- TAB 2: INSIGHTS ---
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        points = result_str.split(".")[:6]
        
        for idx, p in enumerate(points):
            if len(p.strip()) > 25:
                st.markdown(f"""
                <div class="glass-card" style="padding: 16px 20px; display: flex; align-items: start; gap: 15px;">
                    <span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; flex-shrink: 0;">{idx+1}</span>
                    <span style="font-size: 1.05rem; line-height: 1.5; color: #e2e8f0;">{p.strip()}.</span>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 3: FULL REPORT ---
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write(result_str)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button styled nicely
        st.download_button(
            label="📥 Download Detailed Report",
            data=result_str,
            file_name=f"{ticker}_AI_analysis_{date}.txt",
            mime="text/plain"
        )