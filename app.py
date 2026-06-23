import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# ==================== 配置页面 ====================
st.set_page_config(
    page_title="💰 我的财务健康看板",
    page_icon="💰",
    layout="wide"
)

# ==================== 自定义样式 ====================
def get_custom_css():
    """自定义CSS样式，实现毛玻璃效果和渐变背景"""
    return """
    <style>
    /* 全局渐变背景 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        min-height: 100vh;
    }
    
    /* 毛玻璃卡片效果 */
    .glass-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* 数字样式 */
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value.negative {
        color: #ff6b6b;
    }
    
    /* 按钮悬停效果 */
    .stButton>button {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-radius: 12px;
    }
    
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* 输入框样式 */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stDateInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #ffffff;
    }
    
    /* 表格样式 */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* 标签样式 */
    .css-15tx938 {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* 标题样式 */
    h1, h2, h3, h4 {
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """

# ==================== 数据处理函数 ====================

def generate_sample_data():
    """
    生成60条模拟流水数据（2026年6月1日至6月30日）
    覆盖餐饮、交通、购物、房租/水电、娱乐、医疗等类别
    """
    data = []
    start_date = datetime(2026, 6, 1)
    
    # 收入数据
    data.append({"日期": start_date + timedelta(days=29), "类别": "工资", "收支类型": "收入", "金额": 8000, "备注": "月薪"})
    data.append({"日期": start_date + timedelta(days=15), "类别": "兼职", "收支类型": "收入", "金额": 1500, "备注": "项目奖金"})
    
    # 房租（月初支付）
    data.append({"日期": start_date, "类别": "房租/水电", "收支类型": "支出", "金额": 1500, "备注": "房租"})
    data.append({"日期": start_date + timedelta(days=10), "类别": "房租/水电", "收支类型": "支出", "金额": 150, "备注": "水电费"})
    
    # 餐饮支出（模拟一个月的三餐）
    for day in range(30):
        date = start_date + timedelta(days=day)
        # 早餐 10-15元
        data.append({"日期": date, "类别": "餐饮", "收支类型": "支出", "金额": np.random.randint(10, 16), "备注": "早餐"})
        # 午餐 15-30元
        data.append({"日期": date, "类别": "餐饮", "收支类型": "支出", "金额": np.random.randint(15, 31), "备注": "午餐"})
        # 晚餐 15-35元
        data.append({"日期": date, "类别": "餐饮", "收支类型": "支出", "金额": np.random.randint(15, 36), "备注": "晚餐"})
    
    # 周末大餐
    weekend_days = [4, 5, 11, 12, 18, 19, 25, 26]
    for day in weekend_days:
        date = start_date + timedelta(days=day)
        data.append({"日期": date, "类别": "餐饮", "收支类型": "支出", "金额": np.random.randint(150, 301), "备注": "周末聚餐"})
    
    # 交通支出
    for day in range(30):
        date = start_date + timedelta(days=day)
        # 工作日通勤
        if day % 7 not in [5, 6]:  # 工作日
            data.append({"日期": date, "类别": "交通", "收支类型": "支出", "金额": 10, "备注": "地铁通勤"})
    
    # 购物支出
    shopping_dates = [2, 8, 14, 20, 28]
    for day in shopping_dates:
        date = start_date + timedelta(days=day)
        data.append({"日期": date, "类别": "购物", "收支类型": "支出", "金额": np.random.randint(50, 301), "备注": "日常购物"})
    
    # 娱乐支出
    entertainment_dates = [3, 9, 16, 22, 29]
    for day in entertainment_dates:
        date = start_date + timedelta(days=day)
        data.append({"日期": date, "类别": "娱乐", "收支类型": "支出", "金额": np.random.randint(30, 151), "备注": "娱乐消费"})
    
    # 医疗支出
    data.append({"日期": start_date + timedelta(days=7), "类别": "医疗", "收支类型": "支出", "金额": 88, "备注": "买药"})
    
    # 转换为DataFrame并筛选前60条
    df = pd.DataFrame(data)
    df['日期'] = pd.to_datetime(df['日期']).dt.date  # 转换为日期类型
    df = df.sample(n=60, random_state=42).sort_values('日期').reset_index(drop=True)
    
    return df

def parse_date(date_str):
    """
    日期解析函数，支持多种日期格式
    """
    formats = ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y', '%d-%m-%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def get_category_mapping():
    """
    获取类别映射字典
    """
    return {
        '餐饮': ['餐饮', '吃饭', '外卖', '早餐', '午餐', '晚餐'],
        '交通': ['交通', '地铁', '公交', '打车', '加油'],
        '购物': ['购物', '超市', '网购', '衣服', '日用品'],
        '房租/水电': ['房租', '水电', '房租/水电', '物业费'],
        '娱乐': ['娱乐', '电影', '游戏', 'KTV', '旅游'],
        '医疗': ['医疗', '药品', '医院', '体检'],
        '工资': ['工资', '收入', '奖金', '兼职'],
        '其他': ['其他']
    }

def categorize_transaction(description):
    """
    根据描述自动分类
    """
    category_mapping = get_category_mapping()
    description = str(description).lower()
    
    for category, keywords in category_mapping.items():
        for keyword in keywords:
            if keyword.lower() in description:
                return category
    return '其他'

# ==================== 页面功能函数 ====================

def page_data_entry():
    """数据录入与上传页"""
    st.title("📝 数据录入与上传")
    
    # 手动添加记录
    with st.container():
        st.subheader("添加一笔收支")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            entry_date = st.date_input("日期", value=datetime.now().date())
        
        with col2:
            entry_type = st.selectbox("收支类型", ["支出", "收入"])
        
        with col3:
            categories = ["餐饮", "交通", "购物", "房租/水电", "娱乐", "医疗", "工资", "其他"]
            entry_category = st.selectbox("类别", categories)
        
        with col4:
            entry_amount = st.number_input("金额（元）", min_value=0.01, step=0.01)
        
        entry_note = st.text_input("备注（可选）")
        
        if st.button("➕ 添加记录"):
            new_record = {
                "日期": entry_date,
                "类别": entry_category,
                "收支类型": entry_type,
                "金额": entry_amount,
                "备注": entry_note if entry_note else "-"
            }
            st.session_state['data'] = pd.concat([
                st.session_state['data'],
                pd.DataFrame([new_record])
            ], ignore_index=True)
            st.toast(f"✅ 已添加：{entry_type} ¥{entry_amount:.2f}", icon="💰")
    
    st.markdown("---")
    
    # 上传CSV文件
    with st.container():
        st.subheader("📁 上传CSV文件")
        uploaded_file = st.file_uploader("选择CSV文件", type="csv")
        
        if uploaded_file is not None:
            try:
                # 尝试多种编码读取
                encodings = ['utf-8', 'gb2312', 'gbk', 'utf-8-sig']
                df_upload = None
                
                for encoding in encodings:
                    try:
                        uploaded_file.seek(0)
                        df_upload = pd.read_csv(uploaded_file, encoding=encoding)
                        break
                    except:
                        continue
                
                if df_upload is None:
                    st.error("无法读取文件，请检查文件编码")
                else:
                    # 列名映射
                    expected_cols = ['日期', '类别', '收支类型', '金额', '备注']
                    df_upload.columns = df_upload.columns.str.strip()
                    
                    # 处理日期列
                    if '日期' in df_upload.columns:
                        df_upload['日期'] = pd.to_datetime(df_upload['日期'], errors='coerce').dt.date
                    
                    # 确保必要列存在
                    for col in expected_cols[:4]:
                        if col not in df_upload.columns:
                            st.warning(f"缺少必要列：{col}")
                            return
                    
                    # 添加备注列（如果不存在）
                    if '备注' not in df_upload.columns:
                        df_upload['备注'] = '-'
                    
                    # 显示预览
                    st.write("上传数据预览：")
                    st.dataframe(df_upload.head(5))
                    
                    # 选择覆盖或追加
                    mode = st.radio("选择导入模式", ["覆盖现有数据", "追加到现有数据"])
                    
                    if st.button("确认导入"):
                        if mode == "覆盖现有数据":
                            st.session_state['data'] = df_upload
                            st.toast("✅ 数据已覆盖", icon="📊")
                        else:
                            st.session_state['data'] = pd.concat([
                                st.session_state['data'],
                                df_upload
                            ], ignore_index=True)
                            st.toast(f"✅ 已追加 {len(df_upload)} 条记录", icon="📊")
            
            except Exception as e:
                st.error(f"读取文件失败：{str(e)}")
    
    # 当前数据预览
    st.markdown("---")
    st.subheader("📋 当前数据预览")
    st.dataframe(st.session_state['data'].tail(10))
    st.write(f"总计记录数：{len(st.session_state['data'])}")

def page_trend_analysis():
    """趋势分析页"""
    st.title("📈 趋势分析")
    
    # 获取数据
    df = st.session_state['data'].copy()
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 月份选择器
    months = df['日期'].dt.to_period('M').unique()
    month_options = [str(m) for m in months]
    selected_month = st.selectbox("选择月份", month_options, index=len(month_options)-1)
    
    # 筛选当月数据
    df_month = df[df['日期'].dt.to_period('M') == selected_month]
    
    # 计算每日收支
    daily_data = df_month.groupby(df_month['日期'].dt.date).agg(
        支出=('金额', lambda x: x[df_month.loc[x.index, '收支类型'] == '支出'].sum()),
        收入=('金额', lambda x: x[df_month.loc[x.index, '收支类型'] == '收入'].sum())
    ).fillna(0).reset_index()
    
    # 计算累计余额
    daily_data['累计余额'] = (daily_data['收入'] - daily_data['支出']).cumsum()
    
    # 每日收支变化组合图
    with st.container():
        st.subheader("📊 每日收支变化")
        fig = go.Figure()
        
        # 柱状图：每日支出
        fig.add_trace(go.Bar(
            x=daily_data['日期'],
            y=daily_data['支出'],
            name='支出',
            marker_color='rgba(255, 107, 107, 0.8)',
            yaxis='y',
            hovertemplate='支出: ¥%{y:.2f}'
        ))
        
        # 柱状图：每日收入
        fig.add_trace(go.Bar(
            x=daily_data['日期'],
            y=daily_data['收入'],
            name='收入',
            marker_color='rgba(78, 205, 196, 0.8)',
            yaxis='y',
            hovertemplate='收入: ¥%{y:.2f}'
        ))
        
        # 折线图：累计余额
        fig.add_trace(go.Scatter(
            x=daily_data['日期'],
            y=daily_data['累计余额'],
            name='累计余额',
            mode='lines+markers',
            line=dict(color='#fff', width=3),
            marker=dict(color='#fff', size=8),
            yaxis='y',
            hovertemplate='累计余额: ¥%{y:.2f}'
        ))
        
        fig.update_layout(
            title='每日收支与累计余额变化',
            xaxis_title='日期',
            yaxis_title='金额（元）',
            barmode='group',
            plot_bgcolor='rgba(255, 255, 255, 0.1)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        fig.update_xaxes(
            tickformat='%m-%d',
            gridcolor='rgba(255, 255, 255, 0.1)'
        )
        
        fig.update_yaxes(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickprefix='¥'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 分类支出占比环形图
    with st.container():
        st.subheader("🥧 分类支出占比")
        
        # 筛选支出数据
        expense_data = df_month[df_month['收支类型'] == '支出']
        category_expense = expense_data.groupby('类别')['金额'].sum().reset_index()
        
        fig = px.pie(
            category_expense,
            values='金额',
            names='类别',
            hole=0.4,
            title='支出类别分布',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(255, 255, 255, 0.1)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        fig.update_traces(
            hovertemplate='%{label}: ¥%{value:.2f} (%{percent})',
            textinfo='label+percent'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def page_financial_diagnosis():
    """财务诊断与预警页"""
    st.title("⚕️ 财务诊断与预警")
    
    # 获取当前月份数据
    df = st.session_state['data'].copy()
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 获取当前月份
    current_month = df['日期'].dt.to_period('M').max()
    df_month = df[df['日期'].dt.to_period('M') == current_month]
    
    # 计算核心指标
    total_income = df_month[df_month['收支类型'] == '收入']['金额'].sum()
    total_expense = df_month[df_month['收支类型'] == '支出']['金额'].sum()
    balance = total_income - total_expense
    
    # 核心指标卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📥 本月总收入",
            value=f"¥{total_income:.2f}",
            delta=f"+{total_income:.2f}",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="📤 本月总支出",
            value=f"¥{total_expense:.2f}",
            delta=f"-{total_expense:.2f}",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="💰 本月结余",
            value=f"¥{balance:.2f}",
            delta=f"{balance:.2f}",
            delta_color="normal" if balance >= 0 else "inverse"
        )
    
    # 恩格尔系数
    st.markdown("---")
    with st.container():
        st.subheader("📊 恩格尔系数分析")
        
        food_expense = df_month[(df_month['收支类型'] == '支出') & (df_month['类别'] == '餐饮')]['金额'].sum()
        
        if total_expense > 0:
            engel_coefficient = food_expense / total_expense * 100
            
            # 恩格尔系数解读
            if engel_coefficient > 59:
                engel_status = "贫困"
                engel_advice = "恩格尔系数 > 59%，生活水平较低，建议优化支出结构"
            elif engel_coefficient > 50:
                engel_status = "温饱"
                engel_advice = "恩格尔系数 50%-59%，基本解决温饱问题"
            elif engel_coefficient > 40:
                engel_status = "小康"
                engel_advice = "恩格尔系数 40%-50%，达到小康水平"
            elif engel_coefficient > 30:
                engel_status = "富裕"
                engel_advice = "恩格尔系数 30%-40%，生活较为富裕"
            else:
                engel_status = "最富裕"
                engel_advice = "恩格尔系数 < 30%，生活非常富裕"
            
            st.write(f"🍚 餐饮支出：¥{food_expense:.2f}")
            st.write(f"📈 恩格尔系数：{engel_coefficient:.1f}%")
            st.write(f"🏆 生活水平：{engel_status}")
            st.info(engel_advice)
        else:
            st.warning("本月暂无支出数据，无法计算恩格尔系数")
    
    # 支出占比预警
    st.markdown("---")
    with st.container():
        st.subheader("⚠️ 支出占比预警")
        
        expense_by_category = df_month[df_month['收支类型'] == '支出'].groupby('类别')['金额'].sum()
        
        for category, amount in expense_by_category.items():
            percentage = (amount / total_expense * 100) if total_expense > 0 else 0
            
            if percentage > 35:
                st.warning(f"🚨 本月{category}占比过高（{percentage:.1f}%），建议减少相关支出！")
    
    # 超支日历
    st.markdown("---")
    with st.container():
        st.subheader("📅 超支日历")
        
        # 计算每日支出
        daily_expense = df_month[df_month['收支类型'] == '支出'].groupby(df_month['日期'].dt.date)['金额'].sum().reset_index()
        daily_expense.columns = ['日期', '支出']
        
        if not daily_expense.empty:
            avg_daily = daily_expense['支出'].mean()
            threshold = avg_daily * 1.5
            
            # 创建日历表格
            first_day = daily_expense['日期'].min()
            last_day = daily_expense['日期'].max()
            
            # 获取当月第一天是周几
            first_weekday = first_day.weekday()  # 0=周一, 6=周日
            
            # 创建日历数据
            calendar_data = []
            current_date = first_day - timedelta(days=first_weekday)
            
            while current_date <= last_day:
                week_data = []
                for _ in range(7):
                    if current_date >= first_day and current_date <= last_day:
                        expense = daily_expense[daily_expense['日期'] == current_date]['支出'].values
                        expense = expense[0] if len(expense) > 0 else 0
                        is_overbudget = expense > threshold
                        week_data.append({
                            '日期': current_date.day,
                            '支出': expense,
                            '超支': is_overbudget
                        })
                    else:
                        week_data.append(None)
                    current_date += timedelta(days=1)
                calendar_data.append(week_data)
            
            # 显示日历
            week_days = ['一', '二', '三', '四', '五', '六', '日']
            
            # 表头
            st.write(f"日均支出：¥{avg_daily:.2f} | 超支阈值：¥{threshold:.2f}")
            
            # 日历表格
            for week in calendar_data:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day:
                            bg_color = 'background-color: rgba(255, 107, 107, 0.3);' if day['超支'] else ''
                            st.markdown(f"<div style='{bg_color} padding: 8px; text-align: center; border-radius: 8px;'>"
                                       f"<strong>{day['日期']}</strong><br>"
                                       f"<span style='font-size: 12px;'>¥{day['支出']:.0f}</span>"
                                       f"{(' 🔥' if day['超支'] else '')}</div>",
                                       unsafe_allow_html=True)
                        else:
                            st.write("")
        else:
            st.info("本月暂无支出数据")

def page_data_export():
    """数据导出页"""
    st.title("📥 数据导出")
    
    # 数据预览
    st.subheader("当前数据概览")
    st.dataframe(st.session_state['data'])
    st.write(f"总记录数：{len(st.session_state['data'])}")
    
    # 导出CSV
    csv_data = st.session_state['data'].to_csv(index=False, encoding='utf-8-sig')
    csv_buffer = io.BytesIO(csv_data.encode('utf-8-sig'))
    
    st.download_button(
        label="📥 导出为CSV文件",
        data=csv_buffer,
        file_name=f"财务数据_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
        help="点击下载当前所有财务数据"
    )
    
    # 数据统计
    st.markdown("---")
    st.subheader("📊 数据统计")
    
    df = st.session_state['data'].copy()
    df['日期'] = pd.to_datetime(df['日期'])
    
    total_records = len(df)
    total_income = df[df['收支类型'] == '收入']['金额'].sum()
    total_expense = df[df['收支类型'] == '支出']['金额'].sum()
    date_range = f"{df['日期'].min().date()} 至 {df['日期'].max().date()}"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总记录数", total_records)
    
    with col2:
        st.metric("日期范围", date_range)
    
    with col3:
        st.metric("总收入", f"¥{total_income:.2f}")
    
    with col4:
        st.metric("总支出", f"¥{total_expense:.2f}")

# ==================== 主函数 ====================

def main():
    # 应用样式
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # 初始化数据
    if 'data' not in st.session_state:
        st.session_state['data'] = generate_sample_data()
        st.toast("🎉 欢迎！已加载示例数据", icon="💰")
    
    # 侧边栏导航
    st.sidebar.title("💰 财务健康看板")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "选择功能",
        ["📝 数据录入", "📈 趋势分析", "⚕️ 财务诊断", "📥 数据导出"]
    )
    
    # 页面路由
    if page == "📝 数据录入":
        page_data_entry()
    elif page == "📈 趋势分析":
        page_trend_analysis()
    elif page == "⚕️ 财务诊断":
        page_financial_diagnosis()
    elif page == "📥 数据导出":
        page_data_export()

if __name__ == "__main__":
    main()