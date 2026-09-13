"""Khai báo MCP Tools và dữ liệu mô phỏng cho trợ lý tư vấn sức khoẻ Vinmec."""

import json
from typing import Any, Dict, List, Optional


# ============================================================================
# 1. TOOL SCHEMAS (JSON Schema)
# ============================================================================

TOOLS_SCHEMA = [
    {
        "name": "doctor_schedule_query",
        "description": (
            "Tra cứu lịch làm việc và các khung giờ còn trống của bác sĩ Vinmec "
            "theo chuyên khoa, cơ sở và ngày khám."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "specialty": {
                    "type": "string",
                    "description": "Chuyên khoa cần khám, ví dụ: 'Tim mạch', 'Da liễu'."
                },
                "facility": {
                    "type": "string",
                    "description": "Cơ sở Vinmec, ví dụ: 'Vinmec Times City'."
                },
                "date": {
                    "type": "string",
                    "description": "Ngày khám theo định dạng DD/MM/YYYY, ví dụ: '15/09/2026'."
                },
                "doctor_name": {
                    "type": "string",
                    "description": "Tên bác sĩ mong muốn. Bỏ trống nếu cần tìm tất cả bác sĩ phù hợp."
                }
            },
            "required": ["specialty", "facility", "date"]
        }
    },
    {
        "name": "book_medical_appointment",
        "description": (
            "Tạo lịch khám tại Vinmec sau khi đã xác định được bác sĩ hoặc khung giờ phù hợp."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {
                    "type": "string",
                    "description": "Họ và tên người bệnh."
                },
                "phone_number": {
                    "type": "string",
                    "description": "Số điện thoại liên hệ của người bệnh."
                },
                "specialty": {
                    "type": "string",
                    "description": "Chuyên khoa khám."
                },
                "facility": {
                    "type": "string",
                    "description": "Cơ sở Vinmec thực hiện khám."
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian khám theo định dạng 'HH:MM DD/MM/YYYY', ví dụ: '09:00 16/09/2026'."
                },
                "doctor_name": {
                    "type": "string",
                    "description": "Tên bác sĩ đã chọn. Có thể bỏ trống để hệ thống chọn bác sĩ phù hợp."
                }
            },
            "required": ["patient_name", "phone_number", "specialty", "facility", "datetime_str"]
        }
    }
]


# ============================================================================
# 2. MOCK DATA VÀ TOOL EXECUTION LAYER
# ============================================================================

DOCTOR_SCHEDULES: List[Dict[str, Any]] = [
    {
        "doctor_name": "Nguyễn Thị Lan",
        "specialty": "Tim mạch",
        "facility": "Vinmec Times City",
        "schedules": {
            "15/09/2026": ["08:00", "09:00", "10:00"],
            "16/09/2026": ["13:00", "14:00"]
        }
    },
    {
        "doctor_name": "Trần Minh Anh",
        "specialty": "Da liễu",
        "facility": "Vinmec Times City",
        "schedules": {
            "17/09/2026": ["08:00", "09:00", "10:00", "11:00"]
        }
    },
    {
        "doctor_name": "Phạm Quốc Bảo",
        "specialty": "Nội tổng quát",
        "facility": "Vinmec Central Park",
        "schedules": {
            "16/09/2026": ["09:00", "10:00", "14:00"]
        }
    }
]


def _normalize(value: str) -> str:
    """Chuẩn hoá chuỗi để so sánh không phân biệt hoa thường/khoảng trắng."""
    return " ".join(value.casefold().split())


def _find_schedules(
    specialty: str, facility: str, doctor_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Lấy các lịch bác sĩ khớp điều kiện tra cứu."""
    return [
        doctor for doctor in DOCTOR_SCHEDULES
        if _normalize(doctor["specialty"]) == _normalize(specialty)
        and _normalize(doctor["facility"]) == _normalize(facility)
        and (not doctor_name or _normalize(doctor["doctor_name"]) == _normalize(doctor_name))
    ]


def execute_doctor_schedule_query(
    specialty: str, facility: str, date: str, doctor_name: Optional[str] = None
) -> str:
    """Tra cứu bác sĩ và các khung giờ trống theo yêu cầu."""
    doctors = _find_schedules(specialty, facility, doctor_name)
    available = [
        {
            "doctor_name": doctor["doctor_name"],
            "specialty": doctor["specialty"],
            "facility": doctor["facility"],
            "date": date,
            "available_slots": doctor["schedules"].get(date, [])
        }
        for doctor in doctors
        if doctor["schedules"].get(date)
    ]

    if available:
        return json.dumps({"status": "SUCCESS", "data": available}, ensure_ascii=False)

    target = f"bác sĩ {doctor_name}" if doctor_name else f"chuyên khoa {specialty}"
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy lịch trống của {target} tại {facility} vào ngày {date}."
    }, ensure_ascii=False)


def execute_book_medical_appointment(
    patient_name: str,
    phone_number: str,
    specialty: str,
    facility: str,
    datetime_str: str,
    doctor_name: Optional[str] = None
) -> str:
    """Kiểm tra khung giờ và tạo lịch khám mô phỏng."""
    try:
        time_str, date = datetime_str.strip().split(maxsplit=1)
    except ValueError:
        return json.dumps({
            "status": "INVALID_INPUT",
            "message": "Thời gian khám phải có định dạng 'HH:MM DD/MM/YYYY'."
        }, ensure_ascii=False)

    doctors = _find_schedules(specialty, facility, doctor_name)
    selected_doctor = next(
        (doctor for doctor in doctors if time_str in doctor["schedules"].get(date, [])),
        None
    )
    if not selected_doctor:
        return json.dumps({
            "status": "SLOT_UNAVAILABLE",
            "message": "Khung giờ yêu cầu không còn trống. Vui lòng tra cứu lịch và chọn thời gian khác."
        }, ensure_ascii=False)

    booking_id = f"VM-{date.replace('/', '')}-{phone_number[-4:]}"
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": booking_id,
        "patient_name": patient_name,
        "phone_number": phone_number,
        "doctor_name": selected_doctor["doctor_name"],
        "specialty": selected_doctor["specialty"],
        "facility": selected_doctor["facility"],
        "datetime": datetime_str,
        "message": (
            f"Đặt lịch khám thành công cho {patient_name} với bác sĩ "
            f"{selected_doctor['doctor_name']} vào lúc {datetime_str} tại {facility}."
        )
    }, ensure_ascii=False)


TOOL_ROUTER = {
    "doctor_schedule_query": execute_doctor_schedule_query,
    "book_medical_appointment": execute_book_medical_appointment
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Điều phối Tool Call và luôn trả về kết quả JSON."""
    if tool_name not in TOOL_ROUTER:
        return json.dumps({
            "status": "UNKNOWN_TOOL",
            "error": f"Tool '{tool_name}' không tồn tại."
        }, ensure_ascii=False)
    try:
        return TOOL_ROUTER[tool_name](**arguments)
    except TypeError as error:
        return json.dumps({"status": "INVALID_INPUT", "error": str(error)}, ensure_ascii=False)
    except Exception as error:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(error)}, ensure_ascii=False)


# if __name__ == "__main__":
#     print(f"✅ [TOOLS CHECK]: Đã đăng ký thành công {len(TOOLS_SCHEMA)} Native Tools trong TOOLS_SCHEMA!")

#     result = json.loads(dispatch_tool_call(
#         "doctor_schedule_query",
#         {
#             "specialty": "Tim mạch",
#             "facility": "Vinmec Times City",
#             "date": "15/09/2026"
#         }
#     ))
#     doctor_name = result["data"][0]["doctor_name"] if result["status"] == "SUCCESS" else "Không có dữ liệu"
#     print(f"🧪 Kết quả gọi thử doctor_schedule_query: Status {result['status']} ({doctor_name})")
