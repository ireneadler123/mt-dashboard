import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os
import warnings
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'Dashboard', layout = 'wide', page_icon = ':trophy:')
st.sidebar.image('images/logo-vinasoy.png')
st.sidebar.title('MY DASHBOARD')

st.markdown('''
                <style>
                    body{
                        font-family: calibri;
                        background-color: yellow;
                    }
                </style>
            ''', unsafe_allow_html = True)

upload = st.file_uploader(' ', ['xlsx'])
pages = st.sidebar.selectbox('Chọn trang: ', ['Tổng quan', 'Tăng trưởng', 'Tăng trưởng lũy kế'])
if pages ==  'Tổng quan':


    if upload:
        df = pd.read_exel(upload)
        os.makedirs('dataset', exist_ok=True) 
        df.to_csv('dataset/' + upload.name, index = False, encoding = 'utf-8')
        new_df = pd.read_csv('dataset/' + upload.name)
        # st.write(new_df)

        col1, col2 = st.columns((2))

        df['Ngày lấy đơn'] = pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)

        startDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).min()
        endDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).max()

        # Process
        df['Tháng'] = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).dt.month
        df['Năm']  = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).dt.year

        df['Tháng - năm'] = df['Năm'].astype('str')  + ' - ' + df['Tháng'].astype('str')
        df['Tháng - năm'] = df['Tháng - năm'].map({'2022 - 8': '2022 - 08',
                                        '2023 - 8': '2023 - 08',
                                        '2022 - 9': '2022 - 09',
                                        '2023 - 9': '2023 - 09',
                                        '2022 - 7': '2022 - 07',
                                        '2023 - 7': '2023 - 07',
                                        '2022 - 6': '2022 - 06',
                                        '2023 - 6': '2023 - 06',
                                        '2022 - 5': '2022 - 05',
                                        '2023 - 5': '2023 - 05',
                                        '2022 - 4': '2022 - 04',
                                        '2023 - 4': '2023 - 04',
                                        '2022 - 3': '2022 - 03',
                                        '2023 - 3': '2023 - 03',
                                        '2022 - 2': '2022 - 02',
                                        '2023 - 2': '2023 - 02',
                                        '2022 - 1': '2022 - 01',
                                        '2023 - 1': '2023 - 01',
                                        '2022 - 10': '2022 - 10',
                                        '2023 - 10': '2023 - 10',
                                        '2022 - 11': '2022 - 11',
                                        '2023 - 11': '2023 - 11',
                                        '2022 - 12': '2022 - 12',
                                        '2023 - 12': '2023 - 12',})
        
        SBM = df.groupby(by = 'Tháng - năm').agg({'Thành tiền': 'sum'}).reset_index()
        months = st.subheader('Hoàn thành tiến độ tháng')
        # process['Hoàn thành'] = process['Thành tiền'] / process['Target'].astype('float64') * 100

        # months = st.selectbox('Chọn tháng: ', process['Month'])
        # st.table(process[process['Month'] == months])

        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input('Từ ngày: ', startDate), dayfirst = True)

        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input('Đến ngày: ', endDate), dayfirst = True)

        df = df[(df['Ngày lấy đơn'] >= date1) & (df['Ngày lấy đơn'] <= date2)].copy()

        # Line chart   
        lineChart = px.line(SBM, x = SBM['Tháng - năm'], y = SBM['Thành tiền'])
        st.plotly_chart(lineChart, use_container_width = True, height = 200)


        col3, col4 = st.columns((2))

        with col3:
                
            # Bar chart by Suppliers

            sup = df.groupby(by = 'Tên NPP').agg({'Thành tiền': 'sum'}).reset_index()

            barChartSuppliers = px.bar(sup, sup['Tên NPP'], sup['Thành tiền'], title = 'DOANH SỐ BÁN RA THEO NHÀ PHÂN PHỐI')
            st.plotly_chart(barChartSuppliers, use_container_width = True, height = 200)

        with col4:
            # Pie chart

            sys = df['Tên KH'].str.split(' ')
            system = sys.agg(lambda x: x[0])
            df['Hệ thống'] = system
            systems = df.groupby(by = 'Hệ thống').agg({'Thành tiền': 'sum'}).reset_index()
            systems['Hệ thống'] = systems['Hệ thống'].map({
                'BHX': 'Bách Hóa Xanh',
                'VMP': 'Vincommerce',
                'Lotte': 'Lotte Mart',
                'MM': 'Mega Market',
                'VM': 'Vincommerce',
                'BigC': 'BigC và Go!',
                'Coopfood': 'Sài Gòn Coop',
                'Coopmart': 'Sài Gòn Coop'
            })
            pieChart = px.pie(systems, values = systems['Thành tiền'], names = systems['Hệ thống'], title = 'TỶ LỆ ĐÓNG GÓP CỦA CÁC HỆ THỐNG SIÊU THỊ')
            st.plotly_chart(pieChart, use_container_width = True, height = 200)


        # Sorting by SKUs

        skus = df.groupby(by = 'Tên sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
        skus = skus.sort_values('Hàng bán (Thùng)', ascending = True)

        barChartSkus = px.bar(skus, y = skus['Tên sản phẩm'], x = skus['Hàng bán (Thùng)'], title = 'Sản lượng bán ra theo SKUs', orientation = 'h')
        st.plotly_chart(barChartSkus, use_container_width = True, height = 1000)
    else:
        st.warning('Tải file có tên Vinasoy.csv vào đây để tiếp tục nhé')
###################################################################################################################################################################        
###################################################################################################################################################################        
###################################################################################################################################################################         
elif pages == 'Tăng trưởng':

    df = pd.read_csv('dataset/Vinasoy.csv')

    df['Mã NV'] = df['Mã NV'].astype('str')
    df['Mã NPP'] = df['Mã NPP'].astype('str')

    df['Tháng'] = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).dt.month
    df['Năm']  = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).dt.year

    df['Tháng - năm'] = df['Năm'].astype('str')  + ' - ' + df['Tháng'].astype('str')
    df['Tháng - năm'] = df['Tháng - năm'].map({'2022 - 8': '2022 - 08',
                                    '2023 - 8': '2023 - 08',
                                    '2022 - 9': '2022 - 09',
                                    '2023 - 9': '2023 - 09',
                                    '2022 - 7': '2022 - 07',
                                    '2023 - 7': '2023 - 07',
                                    '2022 - 6': '2022 - 06',
                                    '2023 - 6': '2023 - 06',
                                    '2022 - 5': '2022 - 05',
                                    '2023 - 5': '2023 - 05',
                                    '2022 - 4': '2022 - 04',
                                    '2023 - 4': '2023 - 04',
                                    '2022 - 3': '2022 - 03',
                                    '2023 - 3': '2023 - 03',
                                    '2022 - 2': '2022 - 02',
                                    '2023 - 2': '2023 - 02',
                                    '2022 - 1': '2022 - 01',
                                    '2023 - 1': '2023 - 01',
                                    '2022 - 10': '2022 - 10',
                                    '2023 - 10': '2023 - 10',
                                    '2022 - 11': '2022 - 11',
                                    '2023 - 11': '2023 - 11',
                                    '2022 - 12': '2022 - 12',
                                    '2023 - 12': '2023 - 12',})

    df['Mã hệ thống'] = df['Tên KH'].str.split(' ').agg(lambda x: x[0])
    df['Hệ thống'] = df['Mã hệ thống'].map({'VMP': 'Vincommerce',
                                            'VM': 'Vincommerce',
                                            'Coopfood': 'Sài Gòn Coop',
                                            'MM': 'Mega Market',
                                            'BigC': 'BigC và Go!',
                                            'Lotte': 'Lotte Mart',
                                            'Coopmart': 'Sài Gòn Coop',
                                            'BHX': 'Bách Hóa Xanh'})

    df['Ngày lấy đơn'] = df['Ngày lấy đơn'].str.split(' ').agg(lambda x: x[0])

    col1, col2 = st.sidebar.columns(2)

    with col1:
        months = st.selectbox('Chọn tháng: ', df['Tháng - năm'].sort_values(ascending = True).unique())

    with col2:
        growth_month = st.selectbox('Chọn tháng so sánh: ', df['Tháng - năm'].sort_values(ascending = True).unique())

    systems = st.sidebar.selectbox('Chọn hệ thống: ', df['Hệ thống'].sort_values(ascending = True).unique())
    # names = st.sidebar.selectbox('Chọn hệ thống: ', df['Tên KH'].sort_values(ascending = True).unique())
    df_system = df[df['Tháng - năm'] == months]
    df_system = df_system[df_system['Hệ thống'] == systems]

    df_new = df[df['Tháng - năm'] == growth_month]
    df_new = df_new[df_new['Hệ thống'] == systems]

    growth = format(round((df_system['Thành tiền'].sum() - df_new['Thành tiền'].sum()) / df_new['Thành tiền'].sum(), 2), '.2%')

    sys = df_system.groupby(by = 'Ngày lấy đơn').agg({'Thành tiền': 'sum'}).reset_index()

    df_total = df[df['Tháng - năm'] == months]
    df_total_new = df[df['Tháng - năm'] == growth_month]
    total_growth = (df_total['Thành tiền'].sum() - df_total_new['Thành tiền'].sum()) / df_total_new['Thành tiền'].sum()

    col6, col7, col8 = st.columns(3)

    with col7:
        st.metric(label = 'Tổng doanh số toàn khu vực ' + months + ' (VNĐ)', value = format(df_total['Thành tiền'].sum(), ','), delta = format(round(total_growth, 2), '.2%'))


    df_total['Nhóm sản phẩm'] = df_total['Tên sản phẩm'].map({
        'Fa.36h': 'Hộp nguyên chất',
        'Fl.36h': 'Hộp nguyên chất',
        'Fa.10h': 'Hộp 1 lít',
        'Ca.10h': 'Hộp 1 lít',
        'Fa.40b': 'Bịch nguyên chất',
        'Fl.40b': 'Bịch nguyên chất',
        'Ft.36h': 'Nguyên chất vị mới',
        'Fc.36h': 'Nguyên chất vị mới',
        'Fc.40b': 'Nguyên chất vị mới',
        'Fs.36h': 'Nguyên chất vị mới',
        'Fs.40b': 'Nguyên chất vị mới',
        'Fg.36h': 'Nguyên chất vị mới',
        'Ca.36h': 'Hộp canxi',
        'Ca.40b': 'Bịch canxi',
        'Cl.36h': 'Hộp canxi',
        'Cl.40b': 'Bịch canxi',
        'Cf.36h': 'Canxi vị mới',
        'Ch.36h': 'Canxi vị mới',
        'Cs.36h': 'Canxi vị mới',
        'Cp.36h': 'Canxi vị mới',
        'Cp.40b': 'Canxi vị mới',
        'Ct.36h': 'Canxi vị mới',
        'Ct.40b': 'Canxi vị mới',
        'Fd.36h': 'Fami go',
        'Fd.40b': 'Fami go',
        'Fm.36h': 'Fami go',
        'Fm.40b': 'Fami go',
        'Vo.30h': 'Sữa chua uống',
        'Vs.30h': 'Sữa chua uống',
        'Vp.30h': 'Sữa chua uống',
    })

    df_total_new['Nhóm sản phẩm'] = df_total_new['Tên sản phẩm'].map({
        'Fa.36h': 'Hộp nguyên chất',
        'Fl.36h': 'Hộp nguyên chất',
        'Fa.10h': 'Hộp 1 lít',
        'Ca.10h': 'Hộp 1 lít',
        'Fa.40b': 'Bịch nguyên chất',
        'Fl.40b': 'Bịch nguyên chất',
        'Ft.36h': 'Nguyên chất vị mới',
        'Fc.36h': 'Nguyên chất vị mới',
        'Fc.40b': 'Nguyên chất vị mới',
        'Fs.36h': 'Nguyên chất vị mới',
        'Fs.40b': 'Nguyên chất vị mới',
        'Fg.36h': 'Nguyên chất vị mới',
        'Ca.36h': 'Hộp canxi',
        'Ca.40b': 'Bịch canxi',
        'Cl.36h': 'Hộp canxi',
        'Cl.40b': 'Bịch canxi',
        'Cf.36h': 'Canxi vị mới',
        'Ch.36h': 'Canxi vị mới',
        'Cs.36h': 'Canxi vị mới',
        'Cp.36h': 'Canxi vị mới',
        'Cp.40b': 'Canxi vị mới',
        'Ct.36h': 'Canxi vị mới',
        'Ct.40b': 'Canxi vị mới',
        'Fd.36h': 'Fami go',
        'Fd.40b': 'Fami go',
        'Fm.36h': 'Fami go',
        'Fm.40b': 'Fami go',
        'Vo.30h': 'Sữa chua uống',
        'Vs.30h': 'Sữa chua uống',
        'Vp.30h': 'Sữa chua uống',
    })

    total_flavor = df_total.groupby(by = 'Nhóm sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    total_flavor_new = df_total_new.groupby(by = 'Nhóm sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    total_flavor_new = total_flavor_new.rename(columns = {'Hàng bán (Thùng)': 'Hàng bán'})

    final_flavor = total_flavor.set_index('Nhóm sản phẩm').join(total_flavor_new.set_index('Nhóm sản phẩm')).reset_index()
    final_flavor['Tăng trưởng (%)'] = (final_flavor['Hàng bán (Thùng)'] - final_flavor['Hàng bán']) / final_flavor['Hàng bán']

    st.subheader('Tăng trưởng theo nhóm sản phẩm')
    barChart_growth_flavor = px.bar(final_flavor, x = final_flavor['Nhóm sản phẩm'], y = final_flavor['Tăng trưởng (%)'])
    st.plotly_chart(barChart_growth_flavor, use_container_width = True, height = 200)
    st.markdown('---')

    center,centerr,centerrr = st.columns(3)
    with centerr:
        st.header(systems)

    col3, col4, col5 = st.columns(3)
    with col3:
        # Metrics
        st.metric(label = 'Tổng doanh số ' + months + ' (VNĐ)', value  = (format(df_system['Thành tiền'].sum(), ',')) , delta = growth,)
    with col4:
        quality = df_system.groupby(by = 'Ngày lấy đơn').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
        quantity = quality['Ngày lấy đơn'].nunique()
        quality_order = round(quality['Hàng bán (Thùng)'].sum() / quantity, 2)

        quality2 = df_new.groupby(by = 'Ngày lấy đơn').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
        quantity2 = quality2['Ngày lấy đơn'].nunique()
        quality_order2 = round(quality2['Hàng bán (Thùng)'].sum() / quantity2, 2)

        quality_order_growth = (quality_order - quality_order2) / quality_order2

        st.metric(label = 'Chất lượng đơn hàng ' + months + ' (Thùng/đơn)', value = quality_order , delta = format(round(quality_order_growth, 2), '.2%'))

    with col5:
        quan_final = (quantity - quantity2) / quantity2
        st.metric(label = 'Đơn hàng thành công '+ months + ' (Đơn)', value = quantity, delta = format(round(quan_final, 2), '.2%'))
        

    # Line chart
    st.subheader('Doanh số theo ngày')
    lineChart = px.line(sys, x = sys['Ngày lấy đơn'], y = sys['Thành tiền'])
    st.plotly_chart(lineChart, use_container_width = True, height = 200)

    # Group of SKUs

    df_system['Hương vị'] = df_system['Tên sản phẩm'].map({
        'Fa.36h': 'Hộp nguyên chất',
        'Fl.36h': 'Hộp nguyên chất',
        'Fa.10h': 'Hộp 1 lít',
        'Ca.10h': 'Hộp 1 lít',
        'Fa.40b': 'Bịch nguyên chất',
        'Fl.40b': 'Bịch nguyên chất',
        'Ft.36h': 'Nguyên chất vị mới',
        'Fc.36h': 'Nguyên chất vị mới',
        'Fc.40b': 'Nguyên chất vị mới',
        'Fs.36h': 'Nguyên chất vị mới',
        'Fs.40b': 'Nguyên chất vị mới',
        'Fg.36h': 'Nguyên chất vị mới',
        'Ca.36h': 'Hộp canxi',
        'Ca.40b': 'Bịch canxi',
        'Cl.36h': 'Hộp canxi',
        'Cl.40b': 'Bịch canxi',
        'Cf.36h': 'Canxi vị mới',
        'Ch.36h': 'Canxi vị mới',
        'Cs.36h': 'Canxi vị mới',
        'Cp.36h': 'Canxi vị mới',
        'Cp.40b': 'Canxi vị mới',
        'Ct.36h': 'Canxi vị mới',
        'Ct.40b': 'Canxi vị mới',
        'Fd.36h': 'Fami go',
        'Fd.40b': 'Fami go',
        'Fm.36h': 'Fami go',
        'Fm.40b': 'Fami go',
        'Vo.30h': 'Sữa chua uống',
        'Vs.30h': 'Sữa chua uống',
        'Vp.30h': 'Sữa chua uống',
    })

    st.subheader('Sản lượng theo nhóm sản phẩm')

    flavors = df_system.groupby(by = 'Hương vị').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    flavors = flavors.sort_values('Hàng bán (Thùng)', ascending = False)
    barChart = px.bar(flavors, x = flavors['Hương vị'], y = flavors['Hàng bán (Thùng)'])
    st.plotly_chart(barChart, use_container_width = True, height = 200)

    df_new['Hương vị'] = df_new['Tên sản phẩm'].map({
        'Fa.36h': 'Hộp nguyên chất',
        'Fl.36h': 'Hộp nguyên chất',
        'Fa.10h': 'Hộp 1 lít',
        'Ca.10h': 'Hộp 1 lít',
        'Fa.40b': 'Bịch nguyên chất',
        'Fl.40b': 'Bịch nguyên chất',
        'Ft.36h': 'Nguyên chất vị mới',
        'Fc.36h': 'Nguyên chất vị mới',
        'Fc.40b': 'Nguyên chất vị mới',
        'Fs.36h': 'Nguyên chất vị mới',
        'Fs.40b': 'Nguyên chất vị mới',
        'Fg.36h': 'Nguyên chất vị mới',
        'Ca.36h': 'Hộp canxi',
        'Ca.40b': 'Bịch canxi',
        'Cl.36h': 'Hộp canxi',
        'Cl.40b': 'Bịch canxi',
        'Cf.36h': 'Canxi vị mới',
        'Ch.36h': 'Canxi vị mới',
        'Cs.36h': 'Canxi vị mới',
        'Cp.36h': 'Canxi vị mới',
        'Cp.40b': 'Canxi vị mới',
        'Ct.36h': 'Canxi vị mới',
        'Ct.40b': 'Canxi vị mới',
        'Fd.36h': 'Fami go',
        'Fd.40b': 'Fami go',
        'Fm.36h': 'Fami go',
        'Fm.40b': 'Fami go',
        'Vo.30h': 'Sữa chua uống',
        'Vs.30h': 'Sữa chua uống',
        'Vp.30h': 'Sữa chua uống',
    })

    flavors_new = df_new.groupby(by = 'Hương vị').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    flavors_new = flavors_new.sort_values('Hàng bán (Thùng)', ascending = False)
    flavors_new = flavors_new.rename(columns = {'Hàng bán (Thùng)': 'Hàng bán'})

    flavors_growth = flavors.set_index('Hương vị').join(flavors_new.set_index('Hương vị')).reset_index()

    flavors_growth['Tăng trưởng (%)'] = (flavors_growth['Hàng bán (Thùng)'] - flavors_growth['Hàng bán']) / flavors_growth['Hàng bán']
    st.subheader('Tăng trưởng theo nhóm sản phẩm')
    barChart_growth = px.bar(flavors_growth, x = flavors_growth['Hương vị'], y = flavors_growth['Tăng trưởng (%)'])
    st.plotly_chart(barChart_growth, use_container_width = True, height = 200)
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
elif pages == 'Tăng trưởng lũy kế':

    df = pd.read_csv('dataset/Vinasoy.csv')

    col1, col2, col3 = st.columns((3))

    df['Ngày lấy đơn'] = pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)

    startDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).min()
    endDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).max()

    with col1:
        date1 = pd.to_datetime(st.date_input('Từ ngày: ', startDate), dayfirst = True)

    with col2:
        kinds = ['QTD - YOY %','YTD - YOY %']
        kind = st.selectbox('Chọn kiểu so sánh: ', kinds)

    with col3:
        date2 = pd.to_datetime(st.date_input('Đến ngày: ', endDate), dayfirst = True)
    df1 = df[(df['Ngày lấy đơn'] >= date1) & (df['Ngày lấy đơn'] <= date2)].copy()

    df1['Mã NV'] = df1['Mã NV'].astype('str')
    df1['Mã NPP'] = df1['Mã NPP'].astype('str')
    df1['Hệ thống'] = df1['Tên KH'].str.split(' ')
    df1['Hệ thống'] = df1['Hệ thống'].agg({lambda x: x[0]})
    df1['Hệ thống'] = df1['Hệ thống'].map({
        'VMP': 'Vincommerce',
        'VM': 'Vincommerce',
        'BHX': 'Bách Hóa Xanh',
        'Lotte': 'Lotte mart',
        'MM': 'Mega Market',
        'Coopmart': 'Sài Gòn Coop',
        'Coopfood': 'Sài Gòn Coop',
        'BigC': 'BigC và Go!',
        'CK': 'Circle K',
        'FM': 'Family Mart',
        'MN': 'Ministop',
        'GS25': 'GS25',
    })
    
    supermarket = st.sidebar.selectbox('Các hệ thống siêu thị: ', df1['Hệ thống'].unique())
    
    df1 = df1[df1['Hệ thống'] == supermarket]
    df1['Ngày lấy đơn'] = df1['Ngày lấy đơn'].astype('str').str.split(' ')
    df1['Ngày lấy đơn'] = df1['Ngày lấy đơn'].agg({lambda x: x[0]})
    df1 = df1[df1['Loại đơn'] == 'Đơn bán']
    middle, middlee, middleee = st.columns(3)
    with middle:
        if kind == 'QTD - YOY %':
            df_past = df1[df1['Hệ thống'] == supermarket]
            df_past = df[(df['Ngày lấy đơn'].astype('datetime64[ns]') >= (date1 - timedelta(days = 365))) & (pd.to_datetime(df['Ngày lấy đơn'].astype('datetime64[ns]')) <= (date2 - timedelta(days = 365)))]
            df_past['Ngày lấy đơn'] = df_past['Ngày lấy đơn'].astype('str').str.split(' ')
            df_past['Ngày lấy đơn'] = df_past['Ngày lấy đơn'].agg({lambda x: x[0]})
            quality = df1[(pd.to_datetime(df1['Ngày lấy đơn'], dayfirst = True) >= date1) & (pd.to_datetime(df1['Ngày lấy đơn'], dayfirst = True) <= date2)].copy()
            quality = df1.groupby(by = 'Mã đơn hàng').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
            quantity = quality['Mã đơn hàng'].count()
            quality_order = round(quality['Hàng bán (Thùng)'].sum() / quantity, 2)

            quality2 = df_past.groupby(by = 'Mã đơn hàng').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
            quantity2 = quality2['Mã đơn hàng'].count()
            quality_order2 = round(quality2['Hàng bán (Thùng)'].sum() / quantity2, 2)

            quality_order_growth = (quality_order - quality_order2) / quality_order2

            st.metric(label = 'Chất lượng đơn hàng ' + ' (Thùng/đơn)', value = quality_order , delta = format(round(quality_order_growth, 2), '.2%'))

    with middlee:
        if kind == 'QTD - YOY %':
            df_past = df1[df1['Hệ thống'] == supermarket]
            df_past = df[(df['Ngày lấy đơn'].astype('datetime64[ns]') >= (date1 - timedelta(days = 365))) & (pd.to_datetime(df['Ngày lấy đơn'].astype('datetime64[ns]')) <= (date2 - timedelta(days = 365)))]
            df_past = df_past[df_past['Loại đơn'] == 'Đơn bán']
            df_past = df_past[df_past['Loại đơn'] == 'Đơn bán']
            delta = (df1['Thành tiền'].sum() - df_past['Thành tiền'].sum()) / df_past['Thành tiền'].sum() 
            st.metric(label = 'Tổng doanh số', value = format(round(df1['Thành tiền'].sum(), 2), ','), delta = format(delta, '.2%'))
    col5, col6 = st.columns(2)
    groupby = [df1.columns[1], df1.columns[2], df1.columns[3], df1.columns[5], df1.columns[7], df1.columns[3], df1.columns[17],  df1.columns[18], df1.columns[30]]
    group = st.sidebar.selectbox('Chọn một mục để so sánh: ', groupby)

    with middleee:
        quan_final = (quantity - quantity2) / quantity2
        st.metric(label = 'Đơn hàng thành công ' + ' (Đơn)', value = quantity, delta = format(round(quan_final, 2), '.2%'))

    with col5:
        if kind == 'QTD - YOY %':
            df_past = df[(df['Ngày lấy đơn'].astype('datetime64[ns]') >= (date1 - timedelta(days = 365))) & (pd.to_datetime(df['Ngày lấy đơn'].astype('datetime64[ns]')) <= (date2 - timedelta(days = 365)))]
            df_past = df_past[df_past['Loại đơn'] == 'Đơn bán']
            df_past['Hệ thống'] = df_past['Tên KH'].str.split(' ')
            df_past['Hệ thống'] = df_past['Hệ thống'].agg({lambda x: x[0]})
            df_past['Hệ thống'] = df_past['Hệ thống'].map({
                'VMP': 'Vincommerce',
                'VM': 'Vincommerce',
                'BHX': 'Bách Hóa Xanh',
                'Lotte': 'Lotte mart',
                'MM': 'Mega Market',
                'Coopmart': 'Sài Gòn Coop',
                'Coopfood': 'Sài Gòn Coop',
                'BigC': 'BigC và Go!',
                'CK': 'Circle K',
                'FM': 'Family Mart',
                'MN': 'Ministop',
                'GS25': 'GS25',
            })
            df_past = df_past[df_past['Hệ thống'] == supermarket]
            df_past['Ngày lấy đơn'] = df_past['Ngày lấy đơn'].astype('str').str.split(' ')
            df_past['Ngày lấy đơn'] = df_past['Ngày lấy đơn'].agg({lambda x: x[0]})
            if group == 'Ngày lấy đơn':
                compared = df_past.groupby(by = 'Ngày lấy đơn').agg({'Thành tiền': 'sum'}).reset_index()
                lineChart_now = px.line(compared,y = compared['Thành tiền'], x = compared['Ngày lấy đơn'], title = 'Quá khứ')
                st.plotly_chart(lineChart_now, use_container_width = True)
            elif group == 'Tên sản phẩm':
                compared = df_past.groupby(by = 'Tên sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
                compared = compared.sort_values('Hàng bán (Thùng)', ascending = False)
                barChart_now = px.bar(compared,y = compared['Hàng bán (Thùng)'], x = compared['Tên sản phẩm'], title = 'Quá khứ')
                st.plotly_chart(barChart_now, use_container_width = True)
            else:
                compared = df_past.groupby(by = group).agg({'Thành tiền': 'sum'}).reset_index()
                pieChart_past = px.pie(compared,values = compared['Thành tiền'], names = compared[group], title = 'Quá khứ')
                st.plotly_chart(pieChart_past, use_container_width = True)

    with col6:
        if kind == 'QTD - YOY %':
            if group == 'Ngày lấy đơn':
                compared = df1.groupby(by = 'Ngày lấy đơn').agg({'Thành tiền': 'sum'}).reset_index()
                barChart_now = px.line(compared,y = compared['Thành tiền'], x = compared['Ngày lấy đơn'], title = 'Hiện tại')
                st.plotly_chart(barChart_now, use_container_width = True)
            elif group == 'Tên sản phẩm':
                compared = df1.groupby(by = 'Tên sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
                compared = compared.sort_values('Hàng bán (Thùng)', ascending = False)
                barChart_now = px.bar(compared,y = compared['Hàng bán (Thùng)'], x = compared['Tên sản phẩm'], title = 'Hiện tại')
                st.plotly_chart(barChart_now, use_container_width = True)
            else:    
                df1['Ngày lấy đơn'] = df1['Ngày lấy đơn'].astype('str').str.split(' ')
                df1['Ngày lấy đơn'] = df1['Ngày lấy đơn'].agg({lambda x: x[0]})
                compared = df1.groupby(by = group).agg({'Thành tiền': 'sum'}).reset_index()
                pieChart_now = px.pie(compared,values = compared['Thành tiền'], names = compared[group], title = 'Hiện tại')
                st.plotly_chart(pieChart_now, use_container_width = True)


    if kind == 'QTD - YOY %':
        df_past['Hương vị'] = df_past['Tên sản phẩm'].map({
            'Fa.36h': 'Nguyên chất',
            'Fl.36h': 'Nguyên chất',
            'Fa.10h': 'Nguyên chất',
            'Ca.10h': 'Canxi',
            'Fa.40b': 'Nguyên chất',
            'Fl.40b': 'Nguyên chất',
            'Ft.36h': 'Nguyên chất',
            'Fc.36h': 'Nguyên chất',
            'Fc.40b': 'Nguyên chất',
            'Fs.36h': 'Nguyên chất',
            'Fs.40b': 'Nguyên chất',
            'Fg.36h': 'Nguyên chất',
            'Ca.36h': 'Canxi',
            'Ca.40b': 'Canxi',
            'Cl.36h': 'Canxi',
            'Cl.40b': 'Canxi',
            'Cf.36h': 'Canxi',
            'Ch.36h': 'Canxi',
            'Cs.36h': 'Canxi',
            'Cp.36h': 'Canxi',
            'Cp.40b': 'Canxi',
            'Ct.36h': 'Canxi',
            'Ct.40b': 'Canxi',
            'Fd.36h': 'Khác',
            'Fd.40b': 'Khác',
            'Fm.36h': 'Khác',
            'Fm.40b': 'Khác',
            'Vo.30h': 'Sữa chua uống',
            'Vs.30h': 'Sữa chua uống',
            'Vp.30h': 'Sữa chua uống',
        })
        df1['Hương vị'] = df1['Tên sản phẩm'].map({
            'Fa.36h': 'Nguyên chất',
            'Fl.36h': 'Nguyên chất',
            'Fa.10h': 'Nguyên chất',
            'Ca.10h': 'Canxi',
            'Fa.40b': 'Nguyên chất',
            'Fl.40b': 'Nguyên chất',
            'Ft.36h': 'Nguyên chất',
            'Fc.36h': 'Nguyên chất',
            'Fc.40b': 'Nguyên chất',
            'Fs.36h': 'Nguyên chất',
            'Fs.40b': 'Nguyên chất',
            'Fg.36h': 'Nguyên chất',
            'Ca.36h': 'Canxi',
            'Ca.40b': 'Canxi',
            'Cl.36h': 'Canxi',
            'Cl.40b': 'Canxi',
            'Cf.36h': 'Canxi',
            'Ch.36h': 'Canxi',
            'Cs.36h': 'Canxi',
            'Cp.36h': 'Canxi',
            'Cp.40b': 'Canxi',
            'Ct.36h': 'Canxi',
            'Ct.40b': 'Canxi',
            'Fd.36h': 'Khác',
            'Fd.40b': 'Khác',
            'Fm.36h': 'Khác',
            'Fm.40b': 'Khác',
            'Vo.30h': 'Sữa chua uống',
            'Vs.30h': 'Sữa chua uống',
            'Vp.30h': 'Sữa chua uống',
        })
        flavor1 = df1.groupby(by = 'Hương vị').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
        df_past = df_past[df_past['Hệ thống'] == supermarket]
        flavor2 = df_past.groupby(by = 'Hương vị').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
        flavor2 = flavor2.rename(columns = {'Hàng bán (Thùng)': 'Hàng bán'})
        flavor3 = flavor1.set_index('Hương vị').join(flavor2.set_index('Hương vị')).reset_index()
        flavor3['Tăng trưởng (%)'] = (flavor3['Hàng bán (Thùng)'] - flavor3['Hàng bán']) / flavor3['Hàng bán']
        lineFlavor = px.bar(flavor3, x = flavor3['Hương vị'], y = flavor3['Tăng trưởng (%)'], title = 'Tăng trưởng theo hương vị (%)')
        st.plotly_chart(lineFlavor, use_container_width = True, height = 300)
