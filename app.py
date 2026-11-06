import streamlit as st
import pandas as pd

# =========================================================================
# 1. CẤU HÌNH THÔNG TIN FILE GOOGLE SHEETS (Thay bằng thông tin của bạn)
# =========================================================================
SHEET_ID = "Thay_Đoạn_ID_File_Của_Bạn_Vào_Đây" 
SHEET_NAME = "Sheet1" # Tên tab chứa danh sách vụ việc

# Đường dẫn đọc dữ liệu nhanh dưới dạng CSV
URL_DOC = f"https://docs.google.com/spreadsheets/d/1V0LTx9OZuQml9NohWGECtTZWnQTiPTlLZ_fseQQukrk/edit?gid=1720202120#gid=1720202120={2025}"

st.set_page_config(page_title="Hệ Thống Quản Lý PC09", layout="centered", initial_sidebar_state="collapsed")
st.title("📱 Hệ Thống Nhập Liệu & Tra Cứu PC09")

# =========================================================================
# 2. CHỨC NĂNG TRA CỨU DỮ LIỆU (TỐI ƯU TRÊN ĐIỆN THOẠI)
# =========================================================================
st.markdown("---")
st.subheader("🔍 Tra Cứu Vụ Việc")

try:
    # Tải dữ liệu từ file có sẵn
    df = pd.read_csv(URL_DOC)
    
    # Ô tìm kiếm tổng hợp (Gõ từ khóa bất kỳ: Tên cán bộ, địa bàn, tên vụ...)
    tu_khoa = st.text_input("Nhập thông tin cần tìm (Tên cán bộ, Tên vụ, Địa bàn...):")
    
    if tu_khoa:
        # Lọc dữ liệu chứa từ khóa không phân biệt chữ hoa chữ thường
        ket_qua = df[df.astype(str).apply(lambda x: x.str.contains(tu_khoa, case=False)).any(axis=1)]
        st.write(f"📊 Tìm thấy **{len(ket_qua)}** vụ việc phù hợp:")
        st.dataframe(ket_qua)
    else:
        st.write("📋 5 vụ việc cập nhật gần nhất:")
        st.dataframe(df.tail(5)) # Hiển thị nhanh các vụ cuối cùng

except Exception as e:
    st.error("Chưa kết nối được dữ liệu. Vui lòng kiểm tra lại ID Sheet hoặc quyền chia sẻ.")

# =========================================================================
# 3. CHỨC NĂNG NHẬP LIỆU VỤ VIỆC MỚI (FORM DỌC DI ĐỘNG)
# =========================================================================
st.markdown("---")
st.subheader("➕ Cập Nhật Vụ Việc Mới")

with st.form("form_nhap_lieu", clear_on_submit=True):
    # Các ô nhập liệu thiết kế dựa trên các cột sẵn có của bạn
    dia_ban = st.selectbox("2. Địa bàn:", ["Nam Định", "Ninh Bình", "Hà Nam"])
    ngay_kn = st.text_input("3. Ngày khám nghiệm (DD/MM/YYYY):")
    noi_xay_ra = st.text_input("Nơi xảy ra (Xã/Phường, Huyện):")
    ten_vu = st.text_input("Tên vụ việc:")
    co_quan_yeu_cau = st.text_input("4. Cơ quan yêu cầu (Ví dụ: PC01, PC02...):")
    
    tinh_chat = st.selectbox("6. Tính chất vụ việc:", [
        "Tai nạn giao thông", "Giết người", "Tự tử", 
        "Trộm cắp tài sản", "Hiếp dâm, cưỡng dâm", 
        "Cố ý gây thương tích", "Tội phạm về môi trường", "Chết người do các nguyên nhân khác"
    ])
    
    tinh_trang_ht = st.selectbox("7. Tình trạng hiện trường:", ["Nguyên vẹn", "Xáo trộn"])
    noi_dung_tom_tat = st.text_area("8. Nội dung vụ việc (Tóm tắt):")
    can_bo_kn = st.text_input("Cán bộ khám nghiệm (Ghi rõ họ và tên, cách nhau dấu phẩy):")

    # Nút bấm Xác nhận gửi dữ liệu
    submit_btn = st.form_submit_button("🚀 LƯU VÀO FILE EXCEL")

    if submit_btn:
        if not ten_vu or not ngay_kn:
            st.error("❌ Vui lòng điền tối thiểu Tên vụ và Ngày khám nghiệm!")
        else:
            try:
                # Sử dụng thư viện kết nối API của Google để ghi dữ liệu trực tiếp
                import gspread
                from google.oauth2.service_account import Credentials
                
                scope = ["https://google.com", "https://googleapis.com"]
                creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
                client = gspread.authorize(creds)
                
                # Mở Sheet và chèn dòng mới vào cuối bảng tính
                sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
                
                # Sắp xếp mảng này đúng theo thứ tự các cột hiện tại trong file của bạn
                row_to_append = [
                    len(df) + 1, "", dia_ban, ngay_kn, noi_xay_ra, ten_vu, 
                    co_quan_yeu_cau, "", tinh_chat, tinh_trang_ht, 
                    noi_dung_tom_tat, "", "", "", can_bo_kn
                ]
                
                sheet.append_row(row_to_append)
                st.success("🎉 Đã lưu dữ liệu thành công vào file Excel!")
                st.rerun() # Tải lại ứng dụng để cập nhật bảng tra cứu bên trên
                
            except Exception as err:
                st.error(f"Lỗi phân quyền hệ thống: {err}. Hãy chắc chắn bạn đã cấu hình mục Secrets trên Streamlit Cloud.")
