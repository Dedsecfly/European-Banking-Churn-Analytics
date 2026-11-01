import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='European Banking | Financial Intelligence', page_icon='🏦', layout='wide', initial_sidebar_state='expanded')

BG='#0B1120'; CARD='#111C2E'; TEXT='#E2E8F0'; MUTED='#94A3B8'; BLUE='#60A5FA'; RED='#FB7185'; GREEN='#34D399'
PLOT_TEMPLATE='plotly_dark'

st.markdown('''<style>
.stApp {background-color:#0B1120;color:#E2E8F0}
[data-testid="stSidebar"] {background-color:#111827;border-right:1px solid #243247}
h1,h2,h3 {color:#F8FAFC!important}
[data-testid="stMetric"] {background:#111C2E;padding:16px;border:1px solid #243247;border-radius:12px}
[data-testid="stMetricLabel"] {color:#94A3B8}
[data-testid="stMetricValue"] {color:#F8FAFC}
.block-container {padding-top:2rem}
</style>''',unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path=Path(__file__).resolve().parent.parent/'data'/'master_analytics.csv'
    if not file_path.exists():
        st.error(f'Dataset not found: {file_path}. Run analysis/15_master_analytics_dataset.py first.')
        st.stop()
    data=pd.read_csv(file_path)
    required=['CustomerId','Geography','AgeGroup','CreditScoreGroup','TenureGroup','BalanceGroup','ActivityStatus','NumOfProducts','Gender','HighValueStatus','Exited','Balance','ChurnAssociatedBalance','Age','CreditScore','IsActiveMember']
    missing=[c for c in required if c not in data.columns]
    if missing:
        st.error(f'Missing required columns: {missing}')
        st.stop()
    return data

df=load_data()

FILTERS={
    'countries':('Countries','Geography',sorted(df['Geography'].dropna().unique().tolist())),
    'ages':('Age groups','AgeGroup',['Under 30','30-45','46-60','Above 60']),
    'credits':('Credit score groups','CreditScoreGroup',['Low','Medium','High']),
    'tenures':('Tenure groups','TenureGroup',['New','Mid-term','Long-term']),
    'balances':('Balance groups','BalanceGroup',['Zero Balance','Low Balance','High Balance']),
    'activities':('Activity','ActivityStatus',['Active','Inactive']),
    'products':('Number of products','NumOfProducts',sorted(df['NumOfProducts'].dropna().unique().tolist())),
    'genders':('Gender','Gender',sorted(df['Gender'].dropna().unique().tolist())),
    'values':('Customer value','HighValueStatus',['High Value','Standard']),
}

def reset_filters():
    for key,(_,_,options) in FILTERS.items():
        st.session_state[key]=list(options)

with st.sidebar:
    st.title('EUROPEAN BANKING')
    st.caption('FINANCIAL INTELLIGENCE PLATFORM')
    st.divider()
    page=st.radio('NAVIGATION',['Executive Overview','Customer Segmentation','Geographic Intelligence','Financial Exposure','Management Insights'],label_visibility='visible')
    st.divider()
    st.markdown('### FILTERS')
    st.button('Reset all filters',use_container_width=True,on_click=reset_filters)
    selections={}
    for key,(label,col,options) in FILTERS.items():
        available=[x for x in options if x in df[col].dropna().unique()]
        selections[key]=st.multiselect(label,options=available,default=available,key=key)
    st.divider()
    st.caption('Dataset year: 2025 | Currency not verified')

filtered=df.copy()
for key,(_,col,_) in FILTERS.items():
    filtered=filtered[filtered[col].isin(selections[key])]

st.title('European Banking Intelligence')
st.caption('Customer Segmentation & Churn Pattern Analytics | Descriptive analysis of the supplied 2025 customer dataset')
st.caption(f'Current selection: {len(filtered):,} of {len(df):,} customers ({len(filtered)/len(df)*100:.1f}%)')

if filtered.empty:
    st.warning('No customers match the current filters. Change selections or click Reset all filters.')
    st.stop()

n=len(filtered); exited=int(filtered['Exited'].sum()); retained=n-exited
rate=exited/n*100; retained_rate=100-rate
churn_bal=float(filtered['ChurnAssociatedBalance'].sum()); total_bal=float(filtered['Balance'].sum())


def chart_style(fig,height=380):
    fig.update_layout(template=PLOT_TEMPLATE,paper_bgcolor=BG,plot_bgcolor=BG,font_color=TEXT,height=height,margin=dict(l=15,r=15,t=45,b=20),legend_title_text='')
    return fig

def segment_table(column):
    t=filtered.groupby(column,dropna=False,observed=True).agg(Customers=('CustomerId','count'),Churned=('Exited','sum'),Balance=('Balance','sum'),ChurnAssociatedBalance=('ChurnAssociatedBalance','sum')).reset_index()
    t['ChurnRate']=np.where(t['Customers']>0,t['Churned']/t['Customers']*100,0)
    return t

def rate_bar(column,title,order=None):
    t=segment_table(column)
    if order:
        t[column]=pd.Categorical(t[column],categories=order,ordered=True)
        t=t.sort_values(column)
    fig=px.bar(t,x=column,y='ChurnRate',text='ChurnRate',color='ChurnRate',color_continuous_scale='Reds',title=title,hover_data=['Customers','Churned'])
    fig.update_traces(texttemplate='%{text:.1f}%',textposition='outside',cliponaxis=False)
    fig.update_layout(coloraxis_showscale=False,yaxis_title='Churn rate (%)')
    return chart_style(fig)

def exposure_bar(column,title):
    t=segment_table(column).sort_values('ChurnAssociatedBalance',ascending=False)
    fig=px.bar(t,x=column,y='ChurnAssociatedBalance',color_discrete_sequence=[RED],title=title,hover_data=['Customers','Churned','ChurnRate'])
    fig.update_layout(yaxis_title='Churn-associated balance (dataset units)')
    return chart_style(fig)

def metric_row():
    a,b,c=st.columns(3)
    a.metric('Total customers',f'{n:,}')
    b.metric('Churned customers',f'{exited:,}')
    c.metric('Retained customers',f'{retained:,}')
    a,b,c=st.columns(3)
    a.metric('Churn rate',f'{rate:.2f}%')
    b.metric('Retention rate',f'{retained_rate:.2f}%')
    c.metric('Churn-associated balance',f'{churn_bal/1_000_000:,.2f}M')

if page=='Executive Overview':
    st.header('Executive Overview')
    metric_row()
    a,b=st.columns(2)
    with a:
        pie=px.pie(names=['Retained','Churned'],values=[retained,exited],hole=.62,color_discrete_sequence=[GREEN,RED],title='Customer retention mix')
        st.plotly_chart(chart_style(pie),use_container_width=True)
    with b:
        st.plotly_chart(rate_bar('Geography','Churn rate by country'),use_container_width=True)
    a,b=st.columns(2)
    with a: st.plotly_chart(rate_bar('AgeGroup','Churn rate by age',['Under 30','30-45','46-60','Above 60']),use_container_width=True)
    with b: st.plotly_chart(rate_bar('ActivityStatus','Churn rate by activity'),use_container_width=True)
    st.info('Churn-associated balances are recorded balances of customers flagged as exited—not verified deposit withdrawals, revenue loss, or realized financial loss. Currency is unspecified.')

elif page=='Customer Segmentation':
    st.header('Customer Segmentation')
    st.caption('Each chart uses the currently filtered customer population. Small segments can produce unstable rates.')
    pairs=[('CreditScoreGroup','Credit score'),('TenureGroup','Tenure'),('BalanceGroup','Account balance'),('NumOfProducts','Product ownership'),('Gender','Gender'),('ActivityStatus','Activity')]
    for i in range(0,len(pairs),2):
        a,b=st.columns(2)
        with a: st.plotly_chart(rate_bar(pairs[i][0],f'Churn rate by {pairs[i][1].lower()}'),use_container_width=True)
        with b: st.plotly_chart(rate_bar(pairs[i+1][0],f'Churn rate by {pairs[i+1][1].lower()}'),use_container_width=True)
    group=st.selectbox('Detailed segment table',options=[v[1] for v in FILTERS.values()],format_func=lambda x:x)
    st.dataframe(segment_table(group).round(2),use_container_width=True,hide_index=True)

elif page=='Geographic Intelligence':
    st.header('Geographic Intelligence')
    geo=segment_table('Geography').sort_values('ChurnRate',ascending=False)
    st.dataframe(geo.round(2),use_container_width=True,hide_index=True)
    a,b=st.columns(2)
    with a: st.plotly_chart(rate_bar('Geography','Country churn rates'),use_container_width=True)
    with b: st.plotly_chart(exposure_bar('Geography','Country churn-associated balances'),use_container_width=True)
    heat=filtered.groupby(['Geography','AgeGroup'],observed=True).agg(Customers=('CustomerId','size'),Churned=('Exited','sum')).reset_index()
    heat['ChurnRate']=heat['Churned']/heat['Customers']*100
    matrix=heat.pivot(index='Geography',columns='AgeGroup',values='ChurnRate').reindex(columns=['Under 30','30-45','46-60','Above 60'])
    fig=px.imshow(matrix,text_auto='.1f',color_continuous_scale='Reds',aspect='auto',title='Country × age churn rate (%)',labels={'color':'Churn %'})
    st.plotly_chart(chart_style(fig,360),use_container_width=True)
    st.caption('Blank heatmap cells mean no matching customers, not zero churn.')

elif page=='Financial Exposure':
    st.header('Financial Exposure')
    a,b,c=st.columns(3)
    a.metric('Total recorded balance',f'{total_bal/1_000_000:,.2f}M')
    b.metric('Churn-associated balance',f'{churn_bal/1_000_000:,.2f}M')
    c.metric('Share of selected balances associated with churn',f'{churn_bal/total_bal*100:.2f}%' if total_bal else 'N/A')
    a,b=st.columns(2)
    with a: st.plotly_chart(exposure_bar('Geography','Exposure by country'),use_container_width=True)
    with b: st.plotly_chart(exposure_bar('AgeGroup','Exposure by age'),use_container_width=True)
    a,b=st.columns(2)
    with a: st.plotly_chart(exposure_bar('BalanceGroup','Exposure by balance segment'),use_container_width=True)
    with b: st.plotly_chart(exposure_bar('HighValueStatus','Exposure by high-value status'),use_container_width=True)
    hv=filtered[filtered['HighValueStatus']=='High Value']
    st.subheader('High-value customers (fixed full-dataset top 20% threshold)')
    a,b,c=st.columns(3)
    a.metric('High-value customers',f'{len(hv):,}')
    b.metric('High-value churn rate',f'{hv["Exited"].mean()*100:.2f}%' if len(hv) else 'N/A')
    c.metric('High-value churn-associated balance',f'{hv["ChurnAssociatedBalance"].sum()/1_000_000:,.2f}M')
    st.info('Balance amounts use unspecified dataset currency units. A balance associated with a churned customer is not proof of withdrawn funds or lost revenue.')

elif page=='Management Insights':
    st.header('Management Insights')
    st.caption('Automatically calculated descriptive findings; recommendations are hypotheses to test, not causal conclusions.')
    st.metric('Current selection churn rate',f'{rate:.2f}%')
    for column,label in [('Geography','Country'),('AgeGroup','Age group'),('ActivityStatus','Activity status'),('NumOfProducts','Product count'),('BalanceGroup','Balance group')]:
        t=segment_table(column)
        t=t[t['Customers']>=30]
        if not t.empty:
            top=t.sort_values('ChurnRate',ascending=False).iloc[0]
            st.markdown(f'**{label}: {top[column]}** — {top["ChurnRate"]:.2f}% churn across {int(top["Customers"]):,} selected customers ({int(top["Churned"]):,} exits).')
    st.subheader('Suggested management actions')
    st.markdown('''- **Investigate elevated-churn segments:** review complaints, service quality, product suitability, and customer feedback before designing interventions.
- **Test engagement initiatives:** compare targeted outreach against a control group; activity is associated with churn but is not proven to cause it.
- **Prioritize exposure carefully:** examine churn-associated balances alongside customer profitability, costs, and actual deposit flows when available.
- **Validate unusual product patterns:** very high churn in small three- and four-product groups may reflect selection effects or data artifacts.
- **Monitor fairness and privacy:** avoid treating demographic differences as justification for discriminatory treatment.''')
    st.warning('No causal inference, forecasting, or predictive model has been performed. Small samples and overlapping characteristics may distort segment comparisons.')

st.divider()
st.subheader('Export current selection')
a,b=st.columns(2)
with a:
    st.download_button('Download filtered customer data (CSV)',data=filtered.to_csv(index=False).encode('utf-8'),file_name='european_banking_filtered.csv',mime='text/csv',use_container_width=True)
with b:
    summary=pd.DataFrame([{'Customers':n,'Churned':exited,'Retained':retained,'ChurnRatePercent':rate,'ChurnAssociatedBalance':churn_bal,'TotalBalance':total_bal}])
    st.download_button('Download filtered KPI summary (CSV)',data=summary.to_csv(index=False).encode('utf-8'),file_name='european_banking_kpis.csv',mime='text/csv',use_container_width=True)
st.caption('Source: supplied European banking customer dataset (2025). All calculations are based on the active filters. No currency is assumed.')
