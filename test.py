
import streamlit as st
import pandas as pd

# 1. ĐƯỜNG LINK FILE TEST1 CỦA BẠN ĐÃ ĐƯỢC CHUẨN HÓA CẤU TRÚC ĐỌC FILE
URL_DATA = "https://google.com"

st.set_page_config(page_title="App Thu Nghiem", layout="centered")
st.title("📱 Ứng Dụng Thử Nghiệm Đơn Giản")

# CHỨC NĂNG 1: TRA CỨU DỮ LIỆU MẪU
st.markdown("---")
st.header("🔍 Tra Cứu Thông Tin")
try:
    # Đọc dữ liệu trực tiếp từ file Google Sheets của bạn
    df = pd.read_csv(URL_DATA)
    
    tu_khoa = st.text_input("Nhập tên cần tìm (Ví dụ: Nguyễn Văn A):")
    if tu_khoa:
        ket_qua = df[df.astype(str).apply(lambda x: x.str.contains(tu_khoa, case=False)).any(axis=1)]
        st.write(f"📊 Tìm thấy **{len(ket_qua)}** kết quả:")
        st.dataframe(ket_qua)
    else:
        st.write("📋 Danh sách dữ liệu hiện tại trong file:")
        st.dataframe(df)
except Exception as e:
    st.error("Chưa kết nối được với file Google Sheets. Bạn hãy kiểm tra lại xem đã bật quyền chia sẻ 'Bất kỳ ai có đường liên kết - Người chỉnh sửa' chưa nhé.")

# CHỨC NĂNG 2: GIAO DIỆN NHẬP LIỆU MẪU
st.markdown("---")
st.header("➕ Nhập Thêm Người Mới")
with st.form("form_test", clear_on_submit=True):
    ten = st.text_input("Họ và tên:")
    sdt = st.text_input("Số điện thoại:")
    note = st.text_area("Ghi chú:")
    
    submit = st.form_submit_button("🚀 Lưu Lại")
    if submit:
        if ten == "":
            st.error("❌ Vui lòng điền Họ tên trước khi bấm lưu!")
        else:
            st.success(f"🎉 Đã xác nhận thông tin của: {ten}. Giao diện form nhập liệu hoạt động hoàn hảo!")
