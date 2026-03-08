# Credit Score Prediction API (Backend)

Đây là **backend service** của Mini Project dự đoán điểm tín dụng cho hồ
sơ vay vốn.

Backend được xây dựng bằng **FastAPI** và sử dụng **machine learning
model** để dự đoán credit score của người dùng khi nộp hồ sơ vay.

------------------------------------------------------------------------

# Công nghệ sử dụng

-   Python
-   FastAPI
-   Uvicorn
-   XGBoost (Machine Learning Model)
-   Pydantic
-   SQLite (lưu lịch sử hồ sơ)

------------------------------------------------------------------------

# Cấu trúc project
```
    credit-score-backend
    │
    ├── app
    │   ├── database.py
    │   ├── main.py
    │   ├── model_loader.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── utils.py
    │
    ├── model
    ├── notebooks
    │
    ├── requirements.txt
    ├── .gitignore
    └── backend_README.md
```
------------------------------------------------------------------------

# Chức năng chính

-   Nhận dữ liệu hồ sơ vay
-   Dự đoán **credit score**
-   Xác định trạng thái **approve / reject**
-   Lưu lịch sử hồ sơ vay
-   Trả dữ liệu cho frontend thông qua REST API

------------------------------------------------------------------------

# API Endpoints

## 1. Kiểm tra trạng thái hệ thống

GET /health

Kiểm tra trạng thái hoạt động của API, model và database.

Response ví dụ:

{
  "status": "ok",
  "model_loaded": true,
  "database_connected": true
}

## 2. Dự đoán khả năng duyệt khoản vay

POST /predict

Nhận dữ liệu hồ sơ vay từ người dùng và trả về kết quả dự đoán từ mô hình Machine Learning.

Ví dụ request:

``` json
{
  "income": "60000",
  
  "age": "35",
  
  "employment_years": "10",
  
  "loan_amount": 15000,
  
  "loan_term": 36,
  
  "credit_history_length": 8,
  
  "num_credit_lines": 4,
  
  "num_delinquencies": 0,
  
  "debt_to_income_ratio": 0.3,
  
  "savings_balance": 20000
}
```

Ví dụ response:

``` json
{
  "approval_score": 0.9984201192855835,
  
  "approved": true,
  
  "risk_level": "Low",
  
  "recommendation": "Loan likely safe to approve."
}
```

Ngoài ra, kết quả dự đoán sẽ được lưu vào Supabase database để theo dõi lịch sử.

------------------------------------------------------------------------

## 3. Lấy lịch sử hồ sơ vay

GET /applications

Trả về danh sách các hồ sơ đã được dự đoán trước đó.

API hỗ trợ phân trang (pagination).

Query Parameters

| Parameter | Mô tả               |
| --------- | ------------------- |
| page      | Trang hiện tại      |
| limit     | Số record mỗi trang |

Ví dụ

GET /applications?page=1&limit=10

## 4. Xem chi tiết một hồ sơ vay

GET /applications/{id}

Lấy thông tin chi tiết của một hồ sơ vay theo ID.

Ví dụ

GET /applications/123

## 5. Thông tin mô hình

GET /model-info

Trả về thông tin về mô hình Machine Learning đang được sử dụng.

Response ví dụ

{

  "model_name": "credit_risk_model",

  "version": "1.0",

  "algorithm": "RandomForestClassifier"

}

## 6. CORS Support

Backend đã cấu hình CORS middleware để cho phép frontend gọi API.

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

## 7. Graceful Degradation

Nếu Supabase database không kết nối được:

- API vẫn predict bình thường

- Response vẫn trả kết quả cho client

- Chỉ bỏ qua bước lưu vào database

Điều này đảm bảo hệ thống không bị crash khi DB lỗi.

------------------------------------------------------------------------

# Hướng dẫn cài đặt và chạy local

## 1. Clone project

``` bash
git clone <repository-url>
cd credit-score-backend
```

## 2. Tạo virtual environment

``` bash
python -m venv venv
```

Windows:

``` bash
venv\Scripts\activate
```

Mac/Linux:

``` bash
source venv/bin/activate
```

## 3. Cài đặt thư viện

``` bash
pip install -r requirements.txt
```

## 4. Chạy server

``` bash
uvicorn app.main:app --reload
```

Server:

http://127.0.0.1:8000

------------------------------------------------------------------------

# API Documentation

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# Machine Learning Model

Model được lưu trong thư mục:

    model/

Được load thông qua:

    app/model_loader.py

------------------------------------------------------------------------

# Hướng phát triển

-   Deploy backend lên cloud
-   Sử dụng PostgreSQL
-   Tăng độ chính xác model
-   Docker hóa hệ thống
