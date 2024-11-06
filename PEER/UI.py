import tkinter as tk
from tkinter import messagebox, filedialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng File Manager")
        self.geometry("400x300")
        
        self.files = ["file1.txt", "file2.txt", "file3.txt"]  # Danh sách các tệp giả lập

        # Hiển thị màn hình đầu tiên
        self.show_screen1()

    def show_screen1(self):
        # Xóa các widget hiện có
        for widget in self.winfo_children():
            widget.destroy()
        
        # Màn hình 1: Nút Start
        start_button = tk.Button(self, text="Start", command=self.show_screen2)
        start_button.pack(expand=True)

    def show_screen2(self):
        # Xóa các widget hiện có
        for widget in self.winfo_children():
            widget.destroy()
        
        # Màn hình 2: Nút Fetch All File và Upload
        fetch_button = tk.Button(self, text="Fetch All File", command=self.show_screen3)
        fetch_button.pack(pady=20)

        upload_button = tk.Button(self, text="Upload", command=self.upload_file)
        upload_button.pack(pady=20)

        # Nút Quay Về về màn hình 1
        back_button = tk.Button(self, text="Quay Về", command=self.show_screen1)
        back_button.pack(pady=20)

    def show_screen3(self):
        # Xóa các widget hiện có
        for widget in self.winfo_children():
            widget.destroy()
        
        # Màn hình 3: Hiển thị tất cả tệp với nút Download cho mỗi tệp
        for file_name in self.files:
            file_frame = tk.Frame(self)
            file_frame.pack(pady=5, padx=20, fill="x")

            file_label = tk.Label(file_frame, text=file_name)
            file_label.pack(side="left")

            download_button = tk.Button(file_frame, text="Download", command=lambda f=file_name: self.download_file(f))
            download_button.pack(side="right")

        # Nút Quay Về về màn hình 2
        back_button = tk.Button(self, text="Quay Về", command=self.show_screen2)
        back_button.pack(pady=20)

    def upload_file(self):
        # Mở cửa sổ chọn tệp
        file_path = filedialog.askopenfilename(
            title="Chọn tệp để upload",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Tệp được chọn", f"Tệp đã chọn: {file_path}")
            # Thực hiện thao tác upload ở đây nếu cần
        else:
            messagebox.showwarning("Chưa chọn tệp", "Vui lòng chọn một tệp để upload!")

    def download_file(self, file_name):
        # Hàm xử lý khi nhấn nút Download của từng tệp
        messagebox.showinfo("Download", f"Thực hiện chức năng download cho file: {file_name}")

# Chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()
