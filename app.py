import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CO-STAR 提示词生成器", page_icon="✨")

st.title("✨ AI 提示词生成器 (CO-STAR版)")
st.markdown("输入你的简单需求，我会把它转化为 **CO-STAR 框架** 的专业提示词。")

with st.sidebar:
    st.header("配置")
    api_key = st.text_input("请输入 API Key", type="password")
    base_url = st.text_input(
        "Base URL (可选)",
        value="https://api.moonshot.cn/v1",
        help="如果是Kimi，填这个；如果是OpenAI，留空或填官方地址"
    )
    st.markdown("---")
    st.markdown("**CO-STAR 框架说明：**\n\n- **C**: Context 背景\n- **O**: Objective 目标\n- **S**: Style 风格\n- **T**: Tone 语气\n- **A**: Audience 受众\n- **R**: Response 格式")

user_input = st.text_area(
    "你的需求是什么？",
    height=150,
    placeholder="例如：帮我写一封给老板的周报，重点是项目进度延期了，但我有解决方案。"
)

system_prompt = """
你是一位精通 "Prompt Engineering" 的专家。
你的任务是将用户的简单指令，重写为符合 **CO-STAR** 框架的高质量提示词。

请严格按照以下结构输出（使用 Markdown 格式）：

# CO-STAR PROMPT

### (C) Context - 背景
[根据用户输入补充详细背景]

### (O) Objective - 目标
[清晰定义任务目标]

### (S) Style - 风格
[定义写作风格，如：商业、学术、创意等]

### (T) Tone - 语气
[定义情感基调，如：专业、幽默、共情等]

### (A) Audience - 受众
[定义谁会看这个内容]

### (R) Response - 格式
[定义输出格式，如：表格、代码块、Markdown文章]

---
**[优化后的完整提示词内容]**
(在此处根据上述框架，为用户生成一段完整的、可直接复制使用的 Prompt)
"""

if st.button("🚀 立即生成", type="primary"):
    if not api_key:
        st.error("请先在左侧填写 API Key！")
    elif not user_input:
        st.warning("请输入你的需求！")
    else:
        try:
            with st.spinner("AI 正在思考 CO-STAR 策略..."):
                client = OpenAI(api_key=api_key, base_url=base_url)
                response = client.chat.completions.create(
                    model="moonshot-v1-8k",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7
                )
                result = response.choices[0].message.content
            st.success("生成成功！")
            st.markdown("### 👇 复制下面的内容：")
            st.code(result, language="markdown")
        except Exception as e:
            st.error(f"发生错误: {e}")
