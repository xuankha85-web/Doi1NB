import streamlit as st
import pandas as pd

st.set_page_config(page_title="He Thong Quan Ly PC09", layout="centered", initial_sidebar_state="collapsed")
st.title("📱 Hệ Thống Nhập Liệu & Tra Cứu PC09")

# Đường link tĩnh xuất dữ liệu trực tiếp dạng thô CSV từ file Google Sheets của bạn
URL_DOC = "https://google.com"

DANH_SACH_CAN_BO = [
    "Bùi Văn Thiên", "Phạm Minh Cường", "Đỗ Duy Hoà", "Đoàn Văn Đạt", "Nguyễn Xuân Kha", 
    "Trần Đăng Dũng", "Nguyễn Văn Khang", "Trịnh Huy Hảo", "Bùi Xuân Mạnh", 
    "Trịnh Văn Đường", "Vũ Thanh Tùng", "Lê Ngọc Lâm", "Phạm Như Quý", "Nguyễn Văn Quy", 
    "Trần Văn Hưng", "Đoàn Văn Dự", "Nguyễn Xuân Hưng", "Nguyễn Xuân Tiến", "Phạm Hồng Nam", 
    "Hoàng Anh Cường", "Nguyễn Duy Hưng", "Đỗ Ngọc Linh", "Nguyễn Văn Cảnh", "Đoàn Văn Tuyên", 
    "Mai Tiến Dũng", "Đặng Văn Trường", "Nguyễn Văn Khoa", "Trung Dũng", "Đặng Đình Tùng", 
    "Vũ Văn Trường", "Lưu Văn Trường", "Ngụy Hữu Bình", "Nguyễn Văn Tiến", "Nguyễn Văn Đông",
    "Nguyễn Thiện Quang", "Tạ Thành Vinh", "Phạm Đức Thắng", "Phan Duy Hiệp", "Phạm Gia Đô"
]

# =========================================================================
# 2. CHỨC NĂNG TRA CỨU DỮ LIỆU
# =========================================================================
st.markdown("---")
st.subheader("🔍 Tra Cứu Vụ Việc")

try:
    df = pd.read_csv(URL_DOC)
    df = df.dropna(how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.fillna("")
    
    tu_khoa = st.text_input("Nhập thông tin cần tìm (Tên cán bộ, Địa bàn, Tên vụ...):")
    
    if tu_khoa:
        ket_qua = df[df.astype(str).apply(lambda x: x.str.contains(tu_khoa, case=False)).any(axis=1)]
        st.write(f"📊 Tìm thấy **{len(ket_qua)}** vụ việc phù hợp:")
        st.dataframe(ket_qua)
    else:
        st.write("📋 5 vụ việc cập nhật gần nhất:")
        st.dataframe(df.tail(5))

except Exception as e:
    st.error(f"Lỗi hệ thống: {e}")

# =========================================================================
# 3. BIỂU MẪU NHẬP LIỆU
# =========================================================================
st.markdown("---")
st.subheader("➕ Cập Nhật Vụ Việc Mới")

with st.form("form_nhap_lieu", clear_on_submit=True):
    dia_ban = st.selectbox("2. Địa bàn:", ["Nam Định", "Ninh Bình", "Hà Nam"])
    ngay_kn = st.text_input("3. Ngày khám nghiệm (DD/MM/YYYY):")
    noi_xay_ra = st.text_input("Nơi xảy ra (Xã/Phường, Huyện):")
    ten_vu = st.text_input("Tên vụ việc:")
    co_quan_yeu_cau = st.text_input("4. Cơ quan yêu cầu (Ví dụ: PC01, PC02...):")
    
    hoat_dong = st.selectbox("Hoạt động tiến hành:", ["Khám nghiệm hiện trường", "Khám nghiệm tử thi", "Dựng lại hiện trường", "Thực nghiệm điều tra"])
    
    tinh_chat = st.selectbox("6. Tính chất vụ việc:", [
        "Tai nạn giao thông", "Tai nạn lao động", "Giết người", "Tự tử", 
        "Trộm cắp tài sản", "Cố ý gây thương tích", "Chết người chưa rõ nguyên nhân", "Tội phạm về ma túy", "Chết người do các nguyên nhân khác"
    ])
    
    tinh_trang_ht = st.selectbox("7. Tình trạng hiện trường:", ["Nguyên vẹn", "Xáo trộn"])
    noi_dung_tom_tat = st.text_area("8. Nội dung vụ việc (Tóm tắt):")
    ket_qua_kn = st.text_area("9. Kết quả khám nghiệm:")
    dau_vet = st.text_input("10. Dấu vết, tài liệu thu được:")
    nhan_dinh = st.text_input("Nhận định đánh giá:")
    
    can_bo_chon = st.multiselect("Cán bộ khám nghiệm:", DANH_SACH_CAN_BO)

    submit_btn = st.form_submit_button("🚀 LƯU VÀO FILE EXCEL")

    if submit_btn:
        if not ten_vu or not ngay_kn:
            st.error("❌ Vui lòng điền tối thiểu Tên vụ và Ngày khám nghiệm!")
        else:
            try:
                import gspread
                from google.oauth2.service_account import Credentials
                
                scope = ["https://google.com", "https://googleapis.com"]
                creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
                client = gspread.authorize(creds)
                
               # Sửa lại chữ trong ngoặc thành "form_responses" viết thường
sheet = client.open_by_key("110klaLC9naS_C4cMJrVZTn2Gr777vcc3K1Rbk_fvdE0w").worksheet("form_responses")

                chuoi_can_bo = ", ".join(can_bo_chon)
                
                stt_moi = len(df) + 1
                row_to_append = [
                    stt_moi, "", dia_ban, ngay_kn, noi_xay_ra, ten_vu, 
                    co_quan_yeu_cau, hoat_dong, tinh_chat, tinh_trang_ht, 
                    noi_dung_tom_tat, ket_qua_kn, dau_vet, nhan_dinh, chuoi_can_bo
                ]
                
                sheet.append_row(row_to_append)
                st.success(f"🎉 Đã chèn thành công vụ việc '{ten_vu}' vào file Excel!")
                st.rerun()
                
            except Exception as err:
                st.error(f"Lỗi kết nối ghi file: {err}")
