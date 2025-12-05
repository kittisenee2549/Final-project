import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkFont
import json
import os

# โครงสร้างข้อมูล
subjects_list = ["คณิตศาสตร์", "วิทยาศาสตร์", "ภาษาอังกฤษ", "ภาษาไทย", "สังคมศึกษา"]
students = {}
DATA_FILE = "students_data.json"

# โหลดข้อมูลจากไฟล์
def load_data():
    global students
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                students = json.load(f)
        except:
            students = {}

# บันทึกข้อมูลลงไฟล์
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

# ฟังก์ชันคำนวณเกรด
def calculate_grade(avg):
    if avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

# หน้าจอแรก - Main Menu
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ระบบจัดการคะแนนนักเรียน")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")
        
        # กำหนด font
        self.title_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = tkFont.Font(family="Helvetica", size=11)
        
        self.create_widgets()
        load_data()
        
    def create_widgets(self):
        # ส่วนหัว
        header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="ระบบจัดการคะแนนนักเรียน", 
                        font=self.title_font, bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        # ส่วนปุ่ม
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=30, fill=tk.BOTH, expand=True)
        
        buttons = [
            ("➕ เพิ่มข้อมูลนักเรียน", self.open_add_student, "#27ae60"),
            ("📋 แสดงรายชื่อนักเรียน", self.open_show_students, "#3498db"),
            ("🔍 ค้นหาคะแนนนักเรียน", self.open_search_student, "#9b59b6"),
            ("✏️ อัปเดตคะแนนนักเรียน", self.open_update_student, "#f39c12"),
            ("📊 แสดงผลการจัดเกรด", self.open_show_grades, "#e74c3c"),
            ("🗑️ ลบข้อมูลนักเรียน", self.open_delete_student, "#c0392b"),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                           font=self.button_font, bg=color, fg="white",
                           width=40, height=2, cursor="hand2",
                           relief=tk.FLAT, activebackground="#222")
            btn.pack(pady=8)
        
        # ปุ่มออก
        exit_btn = tk.Button(button_frame, text="🚪 ออกจากระบบ", command=self.quit_app,
                            font=self.button_font, bg="#34495e", fg="white",
                            width=40, height=2, cursor="hand2",
                            relief=tk.FLAT, activebackground="#222")
        exit_btn.pack(pady=8)
    
    def open_add_student(self):
        AddStudentWindow(self)
    
    def open_show_students(self):
        ShowStudentsWindow(self)
    
    def open_search_student(self):
        SearchStudentWindow(self)
    
    def open_update_student(self):
        UpdateStudentWindow(self)
    
    def open_show_grades(self):
        ShowGradesWindow(self)
    
    def open_delete_student(self):
        DeleteStudentWindow(self)
    
    def quit_app(self):
        if messagebox.askyesno("ออกจากระบบ", "คุณแน่ใจหรือว่าต้องการออกจากระบบ?"):
            save_data()
            self.destroy()

# หน้าจอเพิ่มนักเรียน
class AddStudentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("เพิ่มข้อมูลนักเรียน")
        self.geometry("500x600")
        self.configure(bg="#ecf0f1")
        
        # ตัวแปรเก็บข้อมูล
        self.scores = {subject: 0 for subject in subjects_list}
        
        self.create_widgets()
    
    def create_widgets(self):
        # ส่วนข้อมูลพื้นฐาน
        form_frame = ttk.LabelFrame(self, text="ข้อมูลนักเรียน", padding=15)
        form_frame.pack(fill=tk.BOTH, padx=15, pady=15)
        
        ttk.Label(form_frame, text="เลขที่:").grid(row=0, column=0, sticky="w", pady=8)
        self.no_entry = ttk.Entry(form_frame, width=20)
        self.no_entry.grid(row=0, column=1, sticky="w", pady=8)
        
        ttk.Label(form_frame, text="ชื่อ:").grid(row=1, column=0, sticky="w", pady=8)
        self.name_entry = ttk.Entry(form_frame, width=20)
        self.name_entry.grid(row=1, column=1, sticky="w", pady=8)
        
        ttk.Label(form_frame, text="ชั้น (ป.1-ป.6):").grid(row=2, column=0, sticky="w", pady=8)
        self.grade_entry = ttk.Entry(form_frame, width=20)
        self.grade_entry.grid(row=2, column=1, sticky="w", pady=8)
        
        ttk.Label(form_frame, text="ห้อง (1-10):").grid(row=3, column=0, sticky="w", pady=8)
        self.classroom_entry = ttk.Entry(form_frame, width=20)
        self.classroom_entry.grid(row=3, column=1, sticky="w", pady=8)
        
        # ส่วนคะแนน
        score_frame = ttk.LabelFrame(self, text="กรอกคะแนนแต่ละวิชา", padding=15)
        score_frame.pack(fill=tk.BOTH, padx=15, pady=15, expand=True)
        
        self.score_entries = {}
        for i, subject in enumerate(subjects_list):
            ttk.Label(score_frame, text=f"{subject}:").grid(row=i, column=0, sticky="w", pady=8)
            entry = ttk.Entry(score_frame, width=15)
            entry.grid(row=i, column=1, sticky="w", pady=8)
            self.score_entries[subject] = entry
        
        # ปุ่ม
        button_frame = tk.Frame(self, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        save_btn = tk.Button(button_frame, text="💾 บันทึก", command=self.save_student,
                            bg="#27ae60", fg="white", width=15, cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="❌ ยกเลิก", command=self.destroy,
                             bg="#e74c3c", fg="white", width=15, cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def save_student(self):
        try:
            no = self.no_entry.get().strip()
            name = self.name_entry.get().strip()
            grade = self.grade_entry.get().strip()
            classroom = self.classroom_entry.get().strip()
            
            if not all([no, name, grade, classroom]):
                messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน")
                return
            
            scores = {}
            for subject, entry in self.score_entries.items():
                try:
                    score = float(entry.get()) if entry.get() else 0
                    if score < 0 or score > 100:
                        raise ValueError
                    scores[subject] = score
                except:
                    messagebox.showerror("ข้อผิดพลาด", f"คะแนน {subject} ไม่ถูกต้อง (0-100)")
                    return
            
            if no in students:
                messagebox.showerror("ข้อผิดพลาด", f"เลขที่ {no} มีอยู่แล้ว")
                return
            
            students[no] = {"ชื่อ": name, "ชั้น": grade, "ห้อง": classroom, "คะแนน": scores}
            save_data()
            messagebox.showinfo("สำเร็จ", f"เพิ่มข้อมูลนักเรียน {name} เรียบร้อยแล้ว!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", str(e))

# หน้าจอแสดงรายชื่อ
class ShowStudentsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("แสดงรายชื่อนักเรียน")
        self.geometry("700x500")
        self.configure(bg="#ecf0f1")
        
        self.create_widgets()
    
    def create_widgets(self):
        # ส่วนกรอกข้อมูล
        filter_frame = ttk.LabelFrame(self, text="ค้นหาตามชั้นและห้อง", padding=15)
        filter_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(filter_frame, text="ชั้น:").pack(side=tk.LEFT, padx=5)
        self.grade_var = ttk.Entry(filter_frame, width=10)
        self.grade_var.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="ห้อง:").pack(side=tk.LEFT, padx=5)
        self.classroom_var = ttk.Entry(filter_frame, width=10)
        self.classroom_var.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="🔍 แสดง", command=self.show_list).pack(side=tk.LEFT, padx=5)
        
        # ส่วนแสดงรายชื่อ
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("เลขที่", "ชื่อ"), height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("#0", text="เลขที่")
        self.tree.heading("เลขที่", text="ชื่อ")
        self.tree.column("#0", width=80)
        self.tree.column("เลขที่", width=200)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def show_list(self):
        grade = self.grade_var.get().strip()
        classroom = self.classroom_var.get().strip()
        
        if not grade or not classroom:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชั้นและห้อง")
            return
        
        # ล้าง tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # เพิ่มข้อมูล
        found = False
        for no in sorted(students.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            info = students[no]
            if info["ชั้น"] == grade and info["ห้อง"] == classroom:
                found = True
                self.tree.insert("", "end", text=no, values=(info["ชื่อ"],))
        
        if not found:
            messagebox.showinfo("ผลลัพธ์", "ไม่พบข้อมูลนักเรียนในชั้นและห้องนี้")

# หน้าจอค้นหาคะแนน
class SearchStudentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ค้นหาคะแนนนักเรียน")
        self.geometry("600x500")
        self.configure(bg="#ecf0f1")
        
        self.create_widgets()
    
    def create_widgets(self):
        # ส่วนค้นหา
        search_frame = ttk.LabelFrame(self, text="ค้นหา", padding=15)
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(search_frame, text="ชื่อนักเรียน:").pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(search_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="🔍 ค้นหา", command=self.search).pack(side=tk.LEFT, padx=5)
        
        # ส่วนผลลัพธ์
        result_frame = ttk.LabelFrame(self, text="ผลการค้นหา", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.result_text = tk.Text(result_frame, height=20, width=70, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def search(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อนักเรียน")
            return
        
        self.result_text.delete("1.0", tk.END)
        
        found = False
        for no, info in students.items():
            if info["ชื่อ"] == name:
                found = True
                result = f"""เลขที่: {no}
ชื่อ: {info['ชื่อ']}
ชั้น: {info['ชั้น']}
ห้อง: {info['ห้อง']}

คะแนน:
"""
                for subject in subjects_list:
                    result += f"  {subject}: {info['คะแนน'][subject]}\n"
                
                self.result_text.insert(tk.END, result)
                break
        
        if not found:
            self.result_text.insert(tk.END, "ไม่พบชื่อนักเรียนในระบบ")

# หน้าจออัปเดตคะแนน
class UpdateStudentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("อัปเดตคะแนนนักเรียน")
        self.geometry("500x400")
        self.configure(bg="#ecf0f1")
        
        self.current_student = None
        self.create_widgets()
    
    def create_widgets(self):
        # ส่วนค้นหา
        search_frame = ttk.LabelFrame(self, text="ค้นหานักเรียน", padding=15)
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(search_frame, text="ชื่อนักเรียน:").pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(search_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="🔍 ค้นหา", command=self.find_student).pack(side=tk.LEFT, padx=5)
        
        # ส่วนอัปเดต
        update_frame = ttk.LabelFrame(self, text="อัปเดตคะแนน", padding=15)
        update_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        ttk.Label(update_frame, text="เลือกวิชา:").pack(anchor="w", pady=5)
        self.subject_var = ttk.Combobox(update_frame, values=subjects_list, state="readonly", width=30)
        self.subject_var.pack(anchor="w", pady=5)
        
        ttk.Label(update_frame, text="คะแนนใหม่:").pack(anchor="w", pady=5)
        self.score_entry = ttk.Entry(update_frame, width=20)
        self.score_entry.pack(anchor="w", pady=5)
        
        # ข้อความสถานะ
        self.status_label = ttk.Label(update_frame, text="กรุณาค้นหานักเรียนก่อน", foreground="red")
        self.status_label.pack(anchor="w", pady=10)
        
        # ปุ่ม
        button_frame = tk.Frame(update_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        save_btn = tk.Button(button_frame, text="💾 บันทึก", command=self.update_score,
                            bg="#27ae60", fg="white", cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=5)
    
    def find_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อนักเรียน")
            return
        
        for no, info in students.items():
            if info["ชื่อ"] == name:
                self.current_student = (no, info)
                self.status_label.config(text=f"✓ พบนักเรียน: {name}", foreground="green")
                return
        
        messagebox.showerror("ข้อผิดพลาด", "ไม่พบชื่อนักเรียนในระบบ")
        self.current_student = None
        self.status_label.config(text="ไม่พบนักเรียน", foreground="red")
    
    def update_score(self):
        if not self.current_student:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาค้นหานักเรียนก่อน")
            return
        
        subject = self.subject_var.get()
        if not subject:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกวิชา")
            return
        
        try:
            score = float(self.score_entry.get())
            if score < 0 or score > 100:
                raise ValueError
        except:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกคะแนน (0-100)")
            return
        
        no, info = self.current_student
        info["คะแนน"][subject] = score
        save_data()
        messagebox.showinfo("สำเร็จ", f"อัปเดตคะแนน {subject} เป็น {score} เรียบร้อยแล้ว!")
        self.score_entry.delete(0, tk.END)

# หน้าจอแสดงเกรด
class ShowGradesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("แสดงผลการจัดเกรด")
        self.geometry("700x500")
        self.configure(bg="#ecf0f1")
        
        self.create_widgets()
    
    def create_widgets(self):
        # ส่วนตัวเลือก
        filter_frame = ttk.LabelFrame(self, text="ค้นหาตามชั้นและห้อง", padding=15)
        filter_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(filter_frame, text="ชั้น:").pack(side=tk.LEFT, padx=5)
        self.grade_var = ttk.Entry(filter_frame, width=10)
        self.grade_var.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="ห้อง:").pack(side=tk.LEFT, padx=5)
        self.classroom_var = ttk.Entry(filter_frame, width=10)
        self.classroom_var.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="🔍 แสดง", command=self.show_grades).pack(side=tk.LEFT, padx=5)
        
        # ส่วนผลลัพธ์
        result_frame = ttk.LabelFrame(self, text="ผลการจัดเกรด", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(result_frame, height=20, width=80, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def show_grades(self):
        grade = self.grade_var.get().strip()
        classroom = self.classroom_var.get().strip()
        
        if not grade or not classroom:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชั้นและห้อง")
            return
        
        self.result_text.delete("1.0", tk.END)
        
        found = False
        result = f"ผลการจัดเกรด ชั้น {grade} ห้อง {classroom}\n"
        result += "=" * 60 + "\n\n"
        
        for no in sorted(students.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            info = students[no]
            if info["ชั้น"] == grade and info["ห้อง"] == classroom:
                found = True
                total_score = sum(info["คะแนน"].values())
                avg_score = total_score / len(subjects_list)
                gpa = calculate_grade(avg_score)
                
                result += f"เลขที่ {no}: {info['ชื่อ']}\n"
                result += f"  คะแนนเฉลี่ย: {avg_score:.2f} → เกรด: {gpa}\n\n"
        
        if not found:
            result = "ไม่พบข้อมูลนักเรียนในชั้นและห้องนี้"
        
        self.result_text.insert(tk.END, result)

# หน้าจอลบนักเรียน
class DeleteStudentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ลบข้อมูลนักเรียน")
        self.geometry("500x300")
        self.configure(bg="#ecf0f1")
        
        self.current_student = None
        self.create_widgets()
    
    def create_widgets(self):
        # ส่วนค้นหา
        search_frame = ttk.LabelFrame(self, text="ค้นหานักเรียน", padding=15)
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(search_frame, text="ชื่อนักเรียน:").pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(search_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="🔍 ค้นหา", command=self.find_student).pack(side=tk.LEFT, padx=5)
        
        # ส่วนข้อมูล
        info_frame = ttk.LabelFrame(self, text="ข้อมูลนักเรียน", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.info_text = tk.Text(info_frame, height=8, width=60, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # ปุ่ม
        button_frame = tk.Frame(self, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        delete_btn = tk.Button(button_frame, text="🗑️ ลบ", command=self.delete_student,
                             bg="#e74c3c", fg="white", width=15, cursor="hand2")
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="❌ ยกเลิก", command=self.destroy,
                             bg="#95a5a6", fg="white", width=15, cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def find_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อนักเรียน")
            return
        
        self.info_text.delete("1.0", tk.END)
        
        for no, info in students.items():
            if info["ชื่อ"] == name:
                self.current_student = (no, info)
                text = f"""เลขที่: {no}
ชื่อ: {info['ชื่อ']}
ชั้น: {info['ชั้น']}
ห้อง: {info['ห้อง']}"""
                self.info_text.insert(tk.END, text)
                return
        
        messagebox.showerror("ข้อผิดพลาด", "ไม่พบชื่อนักเรียนในระบบ")
        self.current_student = None
    
    def delete_student(self):
        if not self.current_student:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาค้นหานักเรียนก่อน")
            return
        
        if messagebox.askyesno("ยืนยันการลบ", f"คุณแน่ใจหรือว่าต้องการลบข้อมูล {self.current_student[1]['ชื่อ']}?"):
            no = self.current_student[0]
            del students[no]
            save_data()
            messagebox.showinfo("สำเร็จ", "ลบข้อมูลนักเรียนเรียบร้อยแล้ว!")
            self.destroy()

# เรียกใช้แอปพลิเคชัน
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
