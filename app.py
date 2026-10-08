import streamlit as st
from datetime import datetime
import pandas as pd
import io

# ============================================================
# CẤU HÌNH APP
# ============================================================

st.set_page_config(
    page_title="Milk Tea POS",
    page_icon="🧋",
    layout="wide"
)

# ============================================================
# CSS - GIAO DIỆN
# ============================================================

st.markdown("""
<style>
    .main {
        background-color: #fff8fb;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #d63384;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .bill-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .total {
        font-size: 28px;
        font-weight: bold;
        color: #d63384;
    }

    .success-box {
        background-color: #f0fff4;
        border: 1px solid #b7ebc6;
        padding: 15px;
        border-radius: 10px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DỮ LIỆU MENU
# ============================================================

DRINKS = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa caramel": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Matcha đá xay": 40000,
    "Socola đá xay": 40000
}

SIZES = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding": 7000,
    "Kem cheese": 10000,
    "Trân châu hoàng kim": 7000,
    "Thạch phô mai": 7000
}

SUGAR_LEVELS = [
    "100% đường",
    "70% đường",
    "50% đường",
    "30% đường",
    "0% đường"
]

ICE_LEVELS = [
    "100% đá",
    "70% đá",
    "50% đá",
    "30% đá",
    "Không đá"
]


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def format_money(amount):
    return f"{amount:,.0f} VNĐ"


# ============================================================
# HÀM THÊM MÓN
# ============================================================

def add_item():
    drink = st.session_state.drink
    size = st.session_state.size
    topping = st.session_state.topping
    sugar = st.session_state.sugar
    ice = st.session_state.ice
    quantity = st.session_state.quantity

    base_price = DRINKS[drink]
    size_price = SIZES[size]
    topping_price = TOPPINGS[topping]

    unit_price = base_price + size_price + topping_price
    total_price = unit_price * quantity

    item = {
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price
    }

    st.session_state.cart.append(item)


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="title">🧋 MILK TEA POS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">HỆ THỐNG TÍNH TIỀN HÓA ĐƠN QUÁN TRÀ SỮA</div>',
    unsafe_allow_html=True
)


# ============================================================
# THÔNG TIN KHÁCH HÀNG
# ============================================================

st.markdown("## 👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng...",
    key="customer_name"
)

# ============================================================
# CHỌN MÓN
# ============================================================

st.markdown("## 🧋 Thêm món")

col1, col2, col3 = st.columns(3)

with col1:
    st.selectbox(
        "Loại trà sữa",
        list(DRINKS.keys()),
        key="drink"
    )

with col2:
    st.selectbox(
        "Size",
        list(SIZES.keys()),
        key="size"
    )

with col3:
    st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
        key="quantity"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.selectbox(
        "Loại topping",
        list(TOPPINGS.keys()),
        key="topping"
    )

with col5:
    st.selectbox(
        "Mức độ đường",
        SUGAR_LEVELS,
        key="sugar"
    )

with col6:
    st.selectbox(
        "Mức độ đá",
        ICE_LEVELS,
        key="ice"
    )


# ============================================================
# GIÁ MÓN ĐANG CHỌN
# ============================================================

current_price = (
    DRINKS[st.session_state.drink]
    + SIZES[st.session_state.size]
    + TOPPINGS[st.session_state.topping]
)

st.info(
    f"💰 Đơn giá: **{format_money(current_price)}**"
)


# ============================================================
# NÚT THÊM MÓN
# ============================================================

st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    use_container_width=True,
    on_click=add_item
)


# ============================================================
# HIỂN THỊ GIỎ HÀNG
# ============================================================

st.markdown("## 🛒 Hóa đơn hiện tại")

if len(st.session_state.cart) == 0:

    st.warning(
        "Chưa có món nào trong hóa đơn. "
        "Hãy chọn món và bấm 'Thêm món vào hóa đơn'."
    )

else:

    for index, item in enumerate(st.session_state.cart):

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [3, 2, 2, 1]
            )

            with col1:
                st.markdown(
                    f"### 🧋 {item['drink']}"
                )

                st.write(
                    f"Size: **{item['size']}** | "
                    f"Topping: **{item['topping']}**"
                )

                st.write(
                    f"Đường: **{item['sugar']}** | "
                    f"Đá: **{item['ice']}**"
                )

            with col2:
                st.write(
                    f"Số lượng: **{item['quantity']}**"
                )

                st.write(
                    f"Đơn giá: **{format_money(item['unit_price'])}**"
                )

            with col3:
                st.write("Thành tiền")
                st.markdown(
                    f"### {format_money(item['total_price'])}"
                )

            with col4:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{index}"
                ):
                    st.session_state.cart.pop(index)
                    st.rerun()


# ============================================================
# TỔNG TIỀN
# ============================================================

if len(st.session_state.cart) > 0:

    subtotal = sum(
        item["total_price"]
        for item in st.session_state.cart
    )

    total_quantity = sum(
        item["quantity"]
        for item in st.session_state.cart
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tổng số món",
            total_quantity
        )

    with col2:
        st.metric(
            "Tạm tính",
            format_money(subtotal)
        )


# ============================================================
# THANH TOÁN
# ============================================================

st.divider()

st.markdown("## 💳 Thanh toán")

if len(st.session_state.cart) == 0:

    st.button(
        "💳 THANH TOÁN",
        disabled=True,
        use_container_width=True
    )

else:

    if st.button(
        "💳 THANH TOÁN",
        use_container_width=True
    ):

        if customer_name.strip() == "":
            customer_name = "Khách lẻ"

        st.session_state.paid = True
        st.session_state.payment_time = datetime.now()

        st.success(
            "✅ Thanh toán thành công!"
        )


# ============================================================
# HÓA ĐƠN SAU KHI THANH TOÁN
# ============================================================

if st.session_state.paid and len(st.session_state.cart) > 0:

    st.divider()

    st.markdown("## 🧾 HÓA ĐƠN")

    subtotal = sum(
        item["total_price"]
        for item in st.session_state.cart
    )

    payment_time = st.session_state.get(
        "payment_time",
        datetime.now()
    )

    bill_number = payment_time.strftime(
        "HD%m%d%H%M%S"
    )

    # --------------------------------------------------------
    # TẠO NỘI DUNG HÓA ĐƠN
    # --------------------------------------------------------

    bill_text = ""

    bill_text += "=" * 50 + "\n"
    bill_text += "              MILK TEA SHOP\n"
    bill_text += "              HÓA ĐƠN THANH TOÁN\n"
    bill_text += "=" * 50 + "\n\n"

    bill_text += f"Mã hóa đơn: {bill_number}\n"
    bill_text += (
        f"Thời gian: "
        f"{payment_time.strftime('%d/%m/%Y %H:%M:%S')}\n"
    )

    bill_text += (
        f"Khách hàng: "
        f"{customer_name if customer_name else 'Khách lẻ'}\n"
    )

    bill_text += "\n"
    bill_text += "-" * 50 + "\n"

    for i, item in enumerate(st.session_state.cart, 1):

        bill_text += (
            f"{i}. {item['drink']} "
            f"(Size {item['size']})\n"
        )

        bill_text += (
            f"   Topping: {item['topping']}\n"
        )

        bill_text += (
            f"   Đường: {item['sugar']} | "
            f"Đá: {item['ice']}\n"
        )

        bill_text += (
            f"   SL: {item['quantity']} x "
            f"{format_money(item['unit_price'])}\n"
        )

        bill_text += (
            f"   Thành tiền: "
            f"{format_money(item['total_price'])}\n\n"
        )

    bill_text += "-" * 50 + "\n"

    bill_text += (
        f"TẠM TÍNH: {format_money(subtotal)}\n"
    )

    bill_text += (
        f"TỔNG CỘNG: {format_money(subtotal)}\n"
    )

    bill_text += "=" * 50 + "\n"
    bill_text += "       CẢM ƠN QUÝ KHÁCH ❤️\n"
    bill_text += "=" * 50 + "\n"


    # --------------------------------------------------------
    # HIỂN THỊ HÓA ĐƠN
    # --------------------------------------------------------

    st.markdown(
        '<div class="bill-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h2 style="text-align:center;">
            🧋 MILK TEA SHOP
        </h2>

        <p style="text-align:center;">
            HÓA ĐƠN THANH TOÁN
        </p>

        <hr>

        <b>Mã hóa đơn:</b> {bill_number}<br>
        <b>Khách hàng:</b> {customer_name if customer_name else "Khách lẻ"}<br>
        <b>Thời gian:</b> {payment_time.strftime("%d/%m/%Y %H:%M:%S")}
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Bảng hóa đơn
    bill_data = []

    for item in st.session_state.cart:

        bill_data.append({
            "Món": item["drink"],
            "Size": item["size"],
            "Topping": item["topping"],
            "Đường": item["sugar"],
            "Đá": item["ice"],
            "SL": item["quantity"],
            "Đơn giá": format_money(item["unit_price"]),
            "Thành tiền": format_money(item["total_price"])
        })

    bill_df = pd.DataFrame(bill_data)

    st.dataframe(
        bill_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.markdown(
        f"""
        <div style="text-align:right;">
            <p>Tạm tính: <b>{format_money(subtotal)}</b></p>
            <p class="total">
                TỔNG CỘNG: {format_money(subtotal)}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align:center;">
             Cảm ơn quý khách và hẹn gặp lại!
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # XUẤT HÓA ĐƠN
    # ========================================================

    st.markdown("### 📥 Xuất hóa đơn")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📄 TẢI HÓA ĐƠN TXT",
            data=bill_text,
            file_name=f"{bill_number}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        csv_data = bill_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="📊 TẢI CHI TIẾT CSV",
            data=csv_data,
            file_name=f"{bill_number}.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# NÚT TẠO HÓA ĐƠN MỚI
# ============================================================

if st.session_state.paid:

    st.divider()

    if st.button(
        "🔄 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.customer_name = ""

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧋 Milk Tea POS • Hệ thống quản lý hóa đơn trà sữa"
)
