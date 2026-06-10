import logging


logging.basicConfig(
    filename="arena_tickets.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ticket_db = [
    {
        "ticket_id": "T01",
        "buyer_name": "Nguyen Van A",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 1)
    },
    {
        "ticket_id": "T02",
        "buyer_name": "Tran Thi B",
        "price": 300.0,
        "status": "Cancelled",
        "seat": ("B", 5)
    },
    {
        "ticket_id": "T03",
        "buyer_name": "Le Van C",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 2)
    }
]


def display_tickets(tickets):
    logging.info("User viewed ticket list.")

    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print("--- DANH SÁCH VÉ ---")
    print(f"{'Mã Vé':<8} | {'Tên Khách Hàng':<20} | {'Giá Vé':<10} | {'Chỗ Ngồi':<10} | {'Trạng Thái'}")
    print("-" * 70)

    for ticket in tickets:
        try:
            seat = f"{ticket['seat'][0]}-{ticket['seat'][1]}"

            status = ticket["status"]

            if status == "Cancelled":
                status += " [ĐÃ HỦY]"

            print(f"{ticket['ticket_id']:<8} | {ticket['buyer_name']:<20} | {ticket['price']:<10} | {seat:<10} | {status}")

        except KeyError as error:
            print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
            logging.error(f"Missing key while displaying ticket: {error}")

    print("-" * 70)


def find_ticket_by_id(tickets, ticket_id):
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket

    return None


def book_ticket(tickets):
    print("--- ĐẶT VÉ MỚI ---")

    ticket_id = input("Nhập mã vé: ").strip()

    if find_ticket_by_id(tickets, ticket_id):
        print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
        logging.warning(f"Duplicate ticket ID entered: {ticket_id}")
        return

    buyer_name = input("Nhập tên khách hàng: ").strip()

    while True:
        try:
            price = float(input("Nhập giá vé: "))

            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break

        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")

            logging.warning("Invalid price input while booking ticket")

    seat_row = input("Nhập khu vực ghế: ").upper()

    while True:
        try:
            seat_number = int(
                input("Nhập số ghế: "))

            if seat_number <= 0:
                print("Số ghế phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break

        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    new_ticket = {
        "ticket_id": ticket_id,
        "buyer_name": buyer_name,
        "price": price,
        "status": "Booked",
        "seat": (
            seat_row,
            seat_number
        )
    }

    tickets.append(new_ticket)

    print(f"Thành công: Đã đặt vé {ticket_id} cho khách hàng {buyer_name}.")

    logging.info(f"Booked new ticket {ticket_id} for {buyer_name}")


def change_seat(tickets):
    print("--- ĐỔI CHỖ NGỒI ---")

    ticket_id = input("Nhập mã vé cần đổi chỗ: ").strip()

    ticket = find_ticket_by_id(tickets,ticket_id)

    if ticket is None:
        print(f"Không tìm thấy vé mang mã {ticket_id}.")

        logging.warning(f"Change seat failed - Ticket {ticket_id} not found")
        return

    new_row = input("Nhập khu vực ghế mới: ").upper()

    while True:
        try:
            new_number = int(input("Nhập số ghế mới: "))

            if new_number <= 0:
                print("Số ghế phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    ticket["seat"] = (new_row,new_number)

    print(f"\nThành công: Đã đổi chỗ vé {ticket_id} sang {new_row}-{new_number}.")

    logging.info(f"Seat changed for ticket {ticket_id} to {new_row}-{new_number}")

def cancel_ticket(tickets):
    print("--- HỦY VÉ ---")

    ticket_id = input("Nhập mã vé cần hủy: ").strip()

    ticket = find_ticket_by_id(tickets,ticket_id)

    if ticket is None:
        print(f"Không tìm thấy vé mang mã {ticket_id}.")

        logging.warning(f"Cancel ticket failed - Ticket {ticket_id} not found")
        return

    if ticket["status"] == "Cancelled":
        print(f"Vé {ticket_id} đã ở trạng thái Cancelled trước đó.")
        return

    ticket["status"] = "Cancelled"

    print(f"Thành công: Vé {ticket_id} đã được hủy.")
    logging.warning(f"Ticket {ticket_id} has been cancelled.")


def calculate_total_revenue(ticket_list):
    revenue = 0.0
    for ticket in ticket_list:
        try:
            if ticket["status"] == "Booked":
                revenue += ticket["price"]
        except KeyError:
            raise
    return revenue


def calculate_revenue(tickets):
    print("--- BÁO CÁO DOANH THU ---")

    try:
        booked_count = 0
        cancelled_count = 0

        for ticket in tickets:

            if ticket["status"] == "Booked":
                booked_count += 1

            elif ticket["status"] == "Cancelled":
                cancelled_count += 1
        revenue = calculate_total_revenue(tickets)

        print(f"Tổng số vé đã đặt: {booked_count}")
        print(f"Tổng số vé đã hủy: {cancelled_count}")
        print(f"Tổng doanh thu hợp lệ: {revenue}")

        logging.info(f"Revenue report generated. Total: {revenue}")

    except KeyError as error:
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")

        logging.error(f"Missing key while calculating revenue: {error}")

if __name__ == "__main__":

    while True:
        choice = input("""
=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===
1. Xem danh sách vé đã bán
2. Đặt vé mới
3. Đổi chỗ ngồi
4. Hủy vé
5. Báo cáo doanh thu
6. Thoát chương trình
========================================
Chọn chức năng (1-6): 
""")
        match choice:
            case "1":
                display_tickets(ticket_db)
            case "2":
                book_ticket(ticket_db)
            case "3":
                change_seat(ticket_db)
            case "4":
                cancel_ticket(ticket_db)
            case "5":
                calculate_revenue(ticket_db)
            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
                logging.info("Ticket management system closed.")
                break
            case _:
                print("Lựa chọn không hợp lệ.")
                logging.warning("Invalid menu choice selected")