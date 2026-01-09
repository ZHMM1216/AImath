import streamlit as st
import json
import time
import re
from pathlib import Path

# ==========================================
# 页面配置
# ==========================================
st.set_page_config(
    page_title="AI-Math Reasoning Demo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 科技感 CSS 样式
# ==========================================
st.markdown("""
<style>
    /* 深色赛博朋克背景 with 粒子效果 */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        color: #e0e0e0;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        position: relative;
        overflow: hidden;
    }
    
    /* 粒子背景层 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(0, 245, 255, 0.3), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(0, 255, 136, 0.3), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(138, 43, 226, 0.3), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(0, 245, 255, 0.4), transparent),
            radial-gradient(2px 2px at 90% 60%, rgba(255, 107, 0, 0.3), transparent),
            radial-gradient(1px 1px at 33% 85%, rgba(0, 255, 136, 0.3), transparent),
            radial-gradient(1px 1px at 75% 40%, rgba(0, 245, 255, 0.3), transparent);
        background-size: 200% 200%, 180% 180%, 220% 220%, 190% 190%, 210% 210%, 195% 195%, 205% 205%;
        background-position: 0% 0%, 100% 0%, 50% 50%, 0% 100%, 100% 100%, 25% 25%, 75% 75%;
        animation: particleFloat 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    /* 流星效果 */
    .stApp::after {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background-image:
            linear-gradient(90deg, transparent 0%, rgba(0, 245, 255, 0.8) 50%, transparent 100%);
        background-size: 200px 2px;
        background-repeat: no-repeat;
        animation: meteor 15s linear infinite;
        pointer-events: none;
        z-index: 1;
        opacity: 0.3;
    }
    
    @keyframes particleFloat {
        0%, 100% {
            background-position: 0% 0%, 100% 0%, 50% 50%, 0% 100%, 100% 100%, 25% 25%, 75% 75%;
        }
        50% {
            background-position: 100% 100%, 0% 100%, 75% 75%, 100% 0%, 0% 0%, 75% 75%, 25% 25%;
        }
    }
    
    @keyframes meteor {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
            opacity: 0;
        }
        10% {
            opacity: 0.3;
        }
        50% {
            transform: translateX(50%) translateY(50%) rotate(45deg);
            opacity: 0.3;
        }
        90% {
            opacity: 0;
        }
        100% {
            transform: translateX(200%) translateY(200%) rotate(45deg);
            opacity: 0;
        }
    }
    
    /* 确保内容在粒子层之上 */
    .main .block-container {
        position: relative;
        z-index: 2;
    }
    
    /* 修复Streamlit容器高度问题 - 确保页面可见 */
    html, body, #root, .stApp {
        height: auto !important;
        min-height: 100vh !important;
    }
    
    .main {
        height: auto !important;
        min-height: 100vh !important;
    }
    
    /* 移除全局 * 选择器，因为它会破坏 KaTeX 公式的字体渲染 */
    
    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 标题样式 - 霓虹灯效果 */
    .main-title {
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00f5ff, #0099ff, #00f5ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
        margin-bottom: 10px;
        animation: glow 2s ease-in-out infinite alternate;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px #00f5ff); }
        to { filter: drop-shadow(0 0 20px #00f5ff); }
    }
    
    .subtitle {
        text-align: center;
        color: #00ff88;
        font-size: 18px;
        margin-bottom: 30px;
        letter-spacing: 2px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    /* 统计面板 */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
        gap: 20px;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.1), rgba(0, 153, 255, 0.1));
        border: 2px solid #00f5ff;
        border-radius: 15px;
        padding: 25px;
        flex: 1;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
        transition: all 0.3s ease;
        animation: pulse 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .stat-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 245, 255, 0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
        }
        50% {
            box-shadow: 0 0 50px rgba(0, 245, 255, 0.5), 0 0 70px rgba(0, 255, 136, 0.3);
        }
    }
    
    @keyframes rotate {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    .stat-box:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 5px 40px rgba(0, 245, 255, 0.5);
        animation-play-state: paused;
    }
    
    .stat-label {
        color: #888;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        position: relative;
        z-index: 1;
    }
    
    .stat-value {
        color: #00ff88;
        font-size: 36px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        position: relative;
        z-index: 1;
        animation: glow-value 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-value {
        from {
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
        to {
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.8), 0 0 30px rgba(0, 245, 255, 0.4);
        }
    }
    
    /* 问题容器 */
    .question-container {
        background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 0, 128, 0.1));
        border-left: 5px solid #ff6b00;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(255, 107, 0, 0.3);
    }
    
    .question-label {
        color: #ff6b00;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .question-text {
        color: #e0e0e0;
        font-size: 16px;
        line-height: 1.8;
        font-family: 'Georgia', serif;
    }
    
    /* AI 推理容器 */
    .reasoning-container {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 200, 255, 0.1));
        border-left: 5px solid #00ff88;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.3);
    }
    
    .reasoning-label {
        color: #00ff88;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .reasoning-text {
        color: #e0e0e0;
        font-size: 15px;
        line-height: 1.9;
        font-family: 'Consolas', monospace;
    }
    
    /* 光标闪烁效果 */
    .cursor {
        display: inline-block;
        width: 10px;
        height: 20px;
        background-color: #00ff88;
        margin-left: 3px;
        animation: blink 0.7s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    /* 答案框 */
    /* 答案框 */
    .answer-box {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.2), rgba(75, 0, 130, 0.2));
        border: 3px solid #8a2be2;
        border-bottom: none;
        border-radius: 15px 15px 0 0;
        padding: 20px 30px;
        margin: 25px 0 0 0;
        text-align: center;
        box-shadow: 0 -5px 20px rgba(138, 43, 226, 0.3);
    }
    
    .answer-body {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.15));
        border: 3px solid #8a2be2;
        border-top: none;
        border-radius: 0 0 15px 15px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 30px rgba(138, 43, 226, 0.3);
    }
    
    .answer-label {
        color: #da70d6;
        font-size: 16px;
        margin-bottom: 15px;
        letter-spacing: 2px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .answer-value {
        color: #ffffff;
        font-size: 42px;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(218, 112, 214, 0.8);
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    /* 进度条 */
    .progress-container {
        margin: 30px 0;
        padding: 20px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #00f5ff, #00ff88);
        border-radius: 10px;
        transition: width 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.6);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #00f5ff, #0099ff);
        color: #000;
        border: none;
        border-radius: 25px;
        padding: 15px 40px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 30px rgba(0, 245, 255, 0.6);
    }
    
    /* 标签 */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .badge-correct {
        background: linear-gradient(135deg, #00ff88, #00cc66);
        color: #000;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    
    .badge-incorrect {
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: #fff;
        box-shadow: 0 0 15px rgba(255, 68, 68, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 辅助函数
# ==========================================

def load_evaluation_data():
    """加载评估数据"""
    try:
        with open("evaluation_results.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def extract_pure_question(question_text):
    """从 question 字段中提取纯粹的数学问题（去除 Assistant 的回答）"""
    # 找到第一个 "Assistant:" 的位置
    assistant_pos = question_text.find("Assistant:")
    
    if assistant_pos != -1:
        # 只取 Assistant 之前的内容
        question_only = question_text[:assistant_pos].strip()
    else:
        question_only = question_text
    
    # 移除提示词部分（"请你一步一步地思考..." 之后的内容）
    prompt_phrases = [
        "请你一步一步地思考，并给出最终答案",
        "Please reason step by step"
    ]
    
    for phrase in prompt_phrases:
        if phrase in question_only:
            question_only = question_only.split(phrase)[0].strip()
            break
    
    return question_only

def extract_reasoning_and_answer(model_output):
    """从 model_output 中提取推理过程和答案（取第一次 Assistant 的推理过程）"""
    # 找到所有 "Assistant:" 的位置
    assistant_positions = [m.start() for m in re.finditer(r'Assistant:', model_output)]
    
    # 提取第一次 Assistant 的内容（标准答案的推理过程）
    if len(assistant_positions) >= 1:
        # 取第一个 Assistant 开始到第二个 Assistant 之前（如果有的话）
        if len(assistant_positions) >= 2:
            first_assistant_output = model_output[assistant_positions[0]:assistant_positions[1]]
        else:
            first_assistant_output = model_output[assistant_positions[0]:]
    else:
        first_assistant_output = model_output
    
    # 提取 <reasoning> 标签内容（完整推理过程）
    reasoning_match = re.search(r'<reasoning>(.*?)</reasoning>', first_assistant_output, re.DOTALL)
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    
    # 提取第一个 <answer> 标签内容
    answer_match = re.search(r'<answer>(.*?)</answer>', first_assistant_output, re.DOTALL)
    answer = answer_match.group(1).strip() if answer_match else ""
    
    # 提取 \boxed{} 内容
    if "\\boxed{" in answer:
        boxed_match = re.search(r'\\boxed\{([^}]+)\}', answer)
        if boxed_match:
            answer = boxed_match.group(1)
    
    return reasoning, answer

def render_latex(text):
    """将文本中的 LaTeX 公式转换为 Streamlit 可渲染的格式"""
    # 移除：text = re.sub(r'\$([^\$]+)\$', r'$\1$', text) 
    # 该正则可能导致不必要转义或破坏
    
    # === 处理双重转义的 LaTeX 定界符 (Main Fix) ===
    # JSON 数据中存在双重转义的定界符，例如 \\( ... \\) 和 \\[ ... \\]
    # 需要匹配两个反斜杠，Regex 中需要 5 个反斜杠 r'\\\\\(' 来匹配字符串中的 \\(
    
    # 1. 双重转义行内公式: \\( ... \\) -> $ ... $
    text = re.sub(r'\\\\\((.*?)\\\\\)', lambda m: f"${m.group(1)}$", text, flags=re.DOTALL)
    
    # 2. 双重转义块级公式: \\[ ... \\] -> $$ ... $$
    text = re.sub(r'\\\\\[(.*?)\\\\\]', lambda m: f"$${m.group(1)}$$", text, flags=re.DOTALL)

    # === 处理各种块级公式定界符 ===
    
    # 3. 标准 LaTeX: \[ ... \] -> $$ ... $$
    # 使用 lambda 避免替换字符串中的反斜杠被误处理
    text = re.sub(r'\\\[(.*?)\\\]', lambda m: f"$${m.group(1)}$$", text, flags=re.DOTALL)
    
    # === 处理行内公式定界符 ===
    
    # 3. 标准 LaTeX: \( ... \) -> $ ... $
    text = re.sub(r'\\\((.*?)\\\)', lambda m: f"${m.group(1)}$", text, flags=re.DOTALL)
    
    # 4. 将 \\boxed{} 转换为更好的显示格式
    text = re.sub(r'\\boxed\{([^}]+)\}', r'**[\1]**', text)
    
    # 5. 将 \qquad 转换为可见的下划线，方便阅读填空题
    text = text.replace(r'\qquad', ' ______ ')
    
    return text

def stream_text(text, placeholder, speed=0.01):
    """流式输出文本（打字机效果）- 支持 LaTeX 渲染"""
    displayed_text = ""
    # 预处理 LaTeX 格式，确保流式输出时也能正确渲染
    processed_text = render_latex(text)
    
    # 简单的按字符流式输出可能会破坏 LaTeX 语法（例如拆分了 \frac），
    # 但在这里我们简化处理，假设渲染速度足够快，或者用户最终会看到完整结果。
    # 为了更好的体验，可以按单词或小块输出，但按字符最简单。
    
    # 如果文本包含 LaTeX，流式输出可能会闪烁或显示源码，直到公式闭合。
    # 这是一个已知权衡。
    
    for char in text: # 注意：这里如果用 processed_text 流式输出，光标位置可能不准确，简单起见还是用原文本流式，但渲染时用 processed
        displayed_text += char
        # 实时渲染需要处理当前的 displayed_text
        current_render = render_latex(displayed_text)
        
        # 使用 Streamlit 的 markdown 渲染 LaTeX
        placeholder.markdown(
            current_render + ' ▊',  # 使用方块作为光标
            unsafe_allow_html=False
        )
        time.sleep(speed)
    
    # 最后一次显示完整文本（不带光标）
    # 使用处理过的 LaTeX 文本进行最终展示
    placeholder.markdown(render_latex(displayed_text), unsafe_allow_html=False)

# ==========================================
# 主应用
# ==========================================

def main():
    # Title
    st.markdown('<div class="main-title">⚡ AI-MATH REASONING Demonstration</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🚀 Powered by Llama-3.2-3B | Model Optimized via Two-Stage SFT + GRPO</div>', unsafe_allow_html=True)
    
    # 加载数据
    data = load_evaluation_data()
    
    if not data:
        st.error("❌ 无法加载 evaluation_results.json 文件")
        return
    
    # 初始化 session state
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'is_streaming' not in st.session_state:
        st.session_state.is_streaming = False
    
    # 使用完整的题目列表
    filtered_results = data["detailed_results"]
    
    # 简化的统计面板 - 只显示题目总数和当前题号
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="stat-box">
            <div class="stat-label">📚 Total Questions</div>
            <div class="stat-value">{data["total_questions"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-box">
            <div class="stat-label">📍 Current Question</div>
            <div class="stat-value">#{st.session_state.current_index + 1}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    
    # 进度条
    progress = (st.session_state.current_index + 1) / len(filtered_results) * 100 if filtered_results else 0
    st.markdown(f'''
    <div class="progress-container">
        <div style="color: #00f5ff; margin-bottom: 10px; text-align: center;">
            Progress: {st.session_state.current_index + 1} / {len(filtered_results)}
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden;">
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    
    # 获取当前题目
    current_item = filtered_results[st.session_state.current_index]
    
    # 提取纯粹的问题（不包含 Assistant 回答）
    pure_question = extract_pure_question(current_item["question"])
    
    # 显示问题（只显示纯粹的数学问题）
    st.markdown('''
    <div class="question-container">
        <div class="question-label">📐 Problem Statement (Q{0})</div>
    </div>
    '''.format(st.session_state.current_index + 1), unsafe_allow_html=True)
    
    # 在容器内使用 Streamlit markdown 渲染 LaTeX
    with st.container():
        st.markdown(f'<div style="padding: 0 25px 25px 25px; background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 0, 128, 0.1)); border-radius: 0 0 10px 10px; margin-top: -20px;">', unsafe_allow_html=True)
        st.markdown(render_latex(pure_question))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 控制按钮
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 1])
    
    with col_btn1:
        if st.button("⏮️ PREVIOUS", disabled=st.session_state.current_index == 0):
            st.session_state.current_index -= 1
            st.session_state.is_streaming = False
            st.rerun()
    
    with col_btn2:
        if st.button("▶️ START REASONING", disabled=st.session_state.is_streaming):
            st.session_state.is_streaming = True
            st.rerun()
    
    with col_btn3:
        if st.button("⏭️ NEXT", disabled=st.session_state.current_index >= len(filtered_results) - 1):
            st.session_state.current_index += 1
            st.session_state.is_streaming = False
            st.rerun()
    
    with col_btn4:
        if st.button("🔄 RESET"):
            st.session_state.current_index = 0
            st.session_state.is_streaming = False
            st.rerun()
    
    # AI 推理过程展示
    st.markdown(f'''
    <div class="reasoning-container">
        <div class="reasoning-label">⚡ Model Reasoning Process</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 创建推理内容容器
    reasoning_container = st.container()
    
    # 提取推理和答案（只取第二次 Assistant 之后的内容）
    reasoning, extracted_answer = extract_reasoning_and_answer(current_item["model_output"])
    
    if st.session_state.is_streaming:
        # 流式输出推理过程
        with reasoning_container:
            st.markdown('<div style="padding: 0 25px 25px 25px; background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 200, 255, 0.1)); border-radius: 0 0 10px 10px; margin-top: -20px;">', unsafe_allow_html=True)
            
            reasoning_placeholder = st.empty()
            
            if reasoning:
                # 流式输出推理过程（支持 LaTeX 渲染）
                stream_text(reasoning, reasoning_placeholder, speed=0.03)
            else:
                reasoning_placeholder.markdown("*No reasoning generated by the model.*")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 显示答案
        is_correct = current_item.get("is_correct", False)
        badge_class = "badge-correct" if is_correct else "badge-incorrect"
        badge_text = "✅ CORRECT" if is_correct else "❌ INCORRECT"
        
        time.sleep(0.5)
        
        st.markdown(f'''
        <div class="answer-box">
            <div class="answer-label">🎯 Final Answer (Evaluation) <span class="badge {badge_class}">{badge_text}</span></div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 格式化答案用于显示 (LaTeX wrapper)
        def fmt_ans(txt):
            if not txt: return "N/A"
            # 如果看起来像 Latex 或者包含特殊符号，用 $$ 包裹
            if any(c in txt for c in ['\\', '^', '_', '{', '}']):
                clean_txt = txt.replace('$', '')
                return f"${clean_txt}$"
            return txt

        model_disp = fmt_ans(extracted_answer)
        real_disp = fmt_ans(current_item["expected_answer"])

        st.markdown(f'''
        <div class="answer-body">
            <!-- 占位，内容通过 st.columns 动态填充 -->
        </div>
        ''', unsafe_allow_html=True)
        
        # 使用 columns 将内容“移入” answer-body 的视觉范围内
        # 注意：Streamlit 不支持直接将组件嵌入自定义 HTML div 中。
        # 我们使用负 margin 将 columns 向上移动覆盖到 answer-body 上。
        
        with st.container():
            st.markdown('<div style="margin-top: -120px; position: relative; z-index: 100;">', unsafe_allow_html=True)
            col_pred, col_truth = st.columns(2)
            
            with col_pred:
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 10px; margin: 0 10px;">
                        <div style="color: #da70d6; font-size: 14px; margin-bottom: 10px; text-transform: uppercase;">Prediction</div>
                        <div style="color: #fff; font-size: 24px; font-weight: bold;">{model_disp}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
            with col_truth:
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 10px; border: 1px solid rgba(0,255,136,0.3); margin: 0 10px;">
                        <div style="color: #00ff88; font-size: 14px; margin-bottom: 10px; text-transform: uppercase;">Ground Truth</div>
                        <div style="color: #fff; font-size: 24px; font-weight: bold;">{real_disp}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 自动标记为完成
        st.session_state.is_streaming = False
        
    else:
        # 未开始推理，显示等待状态
        with reasoning_container:
            st.markdown('<div style="padding: 0 25px 25px 25px; background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 200, 255, 0.1)); border-radius: 0 0 10px 10px; margin-top: -20px; color: #666; font-style: italic;">', unsafe_allow_html=True)
            st.markdown("⏸️  Waiting to start. Click **START REASONING** to view the chain of thought...")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()