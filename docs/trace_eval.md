# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Đào Ngọc Bình Thiên 
> **Mã Sinh Viên / Mã Học viên:** 2A202602814  
> **Chủ đề Lựa chọn:** Trợ lý tư vấn sức khoẻ Vinmec: Tra cứu lịch làm việc bác sĩ chuyên khoa và đặt lịch khám bệnh

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5 / 5 | Yêu cầu đặt lịch thường gồm nhiều bước nối tiếp: xác định chuyên khoa/bác sĩ/cơ sở và thời gian mong muốn, tra cứu lịch làm việc, kiểm tra khung giờ trống, sau đó tạo lịch hẹn và trả về mã xác nhận. |
| **2. Tool Interaction** | 5 / 5 | Agent cần gọi MCP Tool để truy vấn dữ liệu bác sĩ, chuyên khoa và lịch trống từ cơ sở dữ liệu; khi người dùng xác nhận đủ thông tin, Agent tiếp tục gọi Tool đặt lịch khám. Không thể cung cấp lịch chính xác chỉ bằng tri thức tĩnh của LLM.  |
| **3. Dynamic Decision** | 5 / 5 | Hành động đặt lịch phụ thuộc trực tiếp vào quan sát từ bước tra cứu lịch. Nếu bác sĩ không làm việc hoặc khung giờ đã kín, Agent phải đề xuất bác sĩ, cơ sở hoặc thời gian thay thế trước khi tiếp tục. |
| **4. Long Horizon Goal** | 4 / 5 | Agent phải duy trì mục tiêu hoàn tất một lịch khám xuyên suốt nhiều lượt hội thoại, đồng thời ghi nhớ các thông tin đã thu thập như bệnh nhân, chuyên khoa, bác sĩ, cơ sở, thời gian và số điện thoại. Phạm vi phiên làm việc tương đối ngắn nên không cần trạng thái dài hạn phức tạp. |
| **TỔNG ĐIỂM AGENTIC FIT** | **19 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "gpa": 3.85
      }
    },
    "latency_ms": 120.5
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** ___ / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** ___ lượt.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
