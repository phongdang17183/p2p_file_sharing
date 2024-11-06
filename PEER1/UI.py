import tkinter as tk
from tkinter import messagebox, filedialog
import os
import platform
import socket
from apiclient import ClientSite
from peer import Peer
from utils import get_host_default

host = get_host_default()
port = 2000

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.client = ClientSite(Peer(host, port))
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
        self.title("P2P DOWNLOADFILE APPLICATION")
        self.geometry("350x400")
        # Danh sách các tệp giả lập
        self.files = []

        # Đường dẫn thư mục Download
        self.download_path = os.path.join(os.path.dirname(__file__), "Download")
        os.makedirs(self.download_path, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        # Hiển thị màn hình đầu tiên
        self.show_screen1()

    def show_screen1(self):
        # Xóa các widget hiện có
        for widget in self.winfo_children():
            widget.destroy()
        
        # Màn hình 1: Nút Start
        start_button = tk.Button(self, text="Start", width=10, height=2, command=self.start)
        start_button.pack(expand=True)
        
    def start(self):
        self.client.start()
        self.show_screen2()
        
    def show_screen2(self):
        # Xóa các widget hiện có
        for widget in self.winfo_children():
            widget.destroy()
        
        # Màn hình 2: Nút Fetch All File, Upload và Show All Downloaded Files
        fetch_button = tk.Button(self, text="Fetch All File", command=self.show_screen3)
        fetch_button.pack(pady=40)

        upload_button = tk.Button(self, text="Upload", command=self.upload_file)
        upload_button.pack(pady=40)

        show_downloaded_button = tk.Button(self, text="Show All Downloaded Files", command=self.open_download_folder)
        show_downloaded_button.pack(pady=40)

        # Nút Quay Về về màn hình 1
        back_button = tk.Button(self, text="Quay Về", command=self.show_screen1)
        back_button.pack(pady=20)

    def show_screen3(self):
    # Xóa các widget hiện có
        for widget in self.winfo_children():
            widget.destroy()
            
        self.files = self.client.get_all_file()
        
        # Tạo Frame chính cho screen 3
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Tạo Canvas và Scrollbar trong một Frame để chứa danh sách tệp
        file_list_frame = tk.Frame(main_frame)
        file_list_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(file_list_frame)
        scrollbar = tk.Scrollbar(file_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Cấu hình thanh cuộn
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Hiển thị danh sách tệp trong frame cuộn
        for file_name, hashcode in self.files:
            file_frame = tk.Frame(scrollable_frame)
            file_frame.pack(pady=5, padx=20, fill="x")

            # Hiển thị tên tệp và mã hash
            file_label = tk.Label(file_frame, text=f"{file_name} - {hashcode}")
            file_label.pack(side="top", fill="x")  # Đặt ở trên cùng

            # Nút tải xuống nằm dưới tên tệp và mã hash
            download_button = tk.Button(file_frame, text="Download", command=lambda f=file_name: self.download_file(f))
            download_button.pack(side="top", pady=5)  # Đặt ở dưới cùng, cách một khoảng nhỏ

        # Đặt Canvas và Scrollbar trong file_list_frame
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Nút Quay Về về màn hình 2 (đặt bên dưới frame cuộn)
        back_button = tk.Button(main_frame, text="Quay Về", command=self.show_screen2)
        back_button.pack(pady=10)



    def upload_file(self):
        # Mở cửa sổ chọn tệp
        file_path = filedialog.askopenfilename(
            title="Chọn tệp để upload",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Tệp được chọn", f"Tệp đã chọn: {file_path}")
        else:
            messagebox.showwarning("Chưa chọn tệp", "Vui lòng chọn một tệp để upload!")

    def download_file(self, file_name):
        # Hàm xử lý khi nhấn nút Download của từng tệp
        download_path = os.path.join(self.download_path, file_name)
        # Mã để tải về file (giả lập)
        with open(download_path, 'w') as f:
            f.write("Đây là nội dung của file " + file_name)
        messagebox.showinfo("Download", f"Tệp {file_name} đã được tải về {self.download_path}")

    def open_download_folder(self):
        # Hàm mở thư mục Download trong hệ thống
        try:
            if platform.system() == "Windows":
                os.startfile(self.download_path)
            elif platform.system() == "Darwin":  # macOS
                os.system(f"open {self.download_path}")
            else:  # Linux
                os.system(f"xdg-open {self.download_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")

    def on_closing(self):
        self.client.exit(host, port)
        self.destroy()
# Chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()
