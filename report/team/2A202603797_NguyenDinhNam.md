# Báo cáo cá nhân — 2A202603797_NguyenDinhNam

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đình Nam
- MSSV: 2A202603797
- Email: dinhnam269@gmail.com

## 2. Phần việc phụ trách

- Phụ trách **Checkpoint 5 (CP5)**: xây dựng dashboard HTML để trình bày kết quả evaluation.
- Phối hợp thảo luận và hoàn thiện phần giới thiệu, câu hỏi mẫu và hướng dẫn sử dụng dashboard trong báo cáo nhóm.

## 3. Đóng góp cụ thể

- Tạo `starter_v0/demo_cp5.html`, dashboard chạy phía trình duyệt, cho phép tải run JSON từ máy người dùng và xem các chỉ số tổng quan như case accuracy, tool routing, argument accuracy, multi-turn và provider errors.
- Bổ sung tìm kiếm/lọc test case và bảng chi tiết để đối chiếu câu hỏi, expected tool calls, actual tool calls, trạng thái và lỗi của từng case.
- Giữ dashboard độc lập, không gọi model và không gửi run JSON lên mạng; hướng dẫn chạy bằng `python -m http.server 8000` và mở `http://localhost:8000/demo_cp5.html`.
- Tham gia hoàn thiện A1/A3 và hướng dẫn cách dùng dashboard trong `report/team/group_report.md`.
- Dashboard hiện là công cụ xem kết quả eval, **không phải giao diện chat live**. Phần deploy public và transcript chat live chưa hoàn tất.

## 4. Bằng chứng

- **File/commit:**
  - Dashboard: `starter_v0/demo_cp5.html`
  - Báo cáo nhóm: `report/team/group_report.md` (A1, A3 và hướng dẫn chạy UI)
  - Commit: `64181a2` — `Add CP5 evaluation demo`
- **Cách tự kiểm tra:**
  1. Chạy `python -m http.server 8000` từ `starter_v0/` và mở `http://localhost:8000/demo_cp5.html`.
  2. Tải một file `runs/*.json` vào trang; kiểm tra metric, tìm kiếm/lọc case và mở từng case để đối chiếu expected với actual.
  3. Có thể thử file JSON không hợp lệ để xác nhận dashboard báo lỗi định dạng thay vì hiển thị kết quả sai.
- **AI/công cụ đã dùng:** Copilot hỗ trợ thảo luận và rà soát nội dung; dashboard đọc run JSON cục bộ trên trình duyệt.

## 5. Tự đánh giá

- Hoàn thành dashboard trực quan để nhóm trình bày và rà soát kết quả eval đã chạy.
- Đã đóng góp nội dung giới thiệu và hướng dẫn dùng dashboard trong báo cáo nhóm.
- CP5 chưa hoàn tất toàn bộ: dashboard hiện không thay thế yêu cầu UI chat; cần bổ sung giao diện gọi agent, chạy tối thiểu 3 lượt live có transcript và triển khai link public nếu tiếp tục hoàn thiện checkpoint.
