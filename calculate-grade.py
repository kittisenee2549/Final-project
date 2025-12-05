# รายวิชาที่ใช้ในระบบ
subjects_list = ["คณิตศาสตร์", "วิทยาศาสตร์", "ภาษาอังกฤษ", "ภาษาไทย", "สังคมศึกษา"]

# โครงสร้างข้อมูลนักเรียน
students = {}

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

# เมนู 1: เพิ่มคะแนนนักเรียน
def add_student():
    no = input("กรอกเลขที่นักเรียน: ")
    name = input("กรอกชื่อนักเรียน: ")
    grade = input("กรอกชั้นการศึกษา (ป.1 - ป.6): ")
    classroom = input("กรอกห้องเรียน (1 - 10): ")
    
    scores = {subject: 0 for subject in subjects_list}
    
    while True:
        print("\nเลือกวิชาที่ต้องการกรอกคะแนน:")
        for i, subject in enumerate(subjects_list, start=1):
            print(f"{i}. {subject}")
        print("0. เสร็จสิ้นการกรอกคะแนน")
        
        choice = int(input("กรอกหมายเลขวิชา: "))
        if choice == 0:
            break
        elif 1 <= choice <= len(subjects_list):
            subject = subjects_list[choice - 1]
            score = float(input(f"กรอกคะแนน {subject}: "))
            scores[subject] = score
        else:
            print("เลือกไม่ถูกต้อง")
    
    students[no] = {"ชื่อ": name, "ชั้น": grade, "ห้อง": classroom, "คะแนน": scores}
    print(f"\nเพิ่มข้อมูลนักเรียน เลขที่ {no} - {name} (ชั้น {grade} ห้อง {classroom}) เรียบร้อยแล้ว!")

# เมนู 2: แสดงรายชื่อนักเรียนตามชั้นและห้อง
def show_students():
    if not students:
        print("ยังไม่มีข้อมูลนักเรียน")
        return
    
    grade = input("กรอกชั้นการศึกษา (ป.1 - ป.6): ")
    classroom = input("กรอกห้องเรียน (1 - 10): ")
    
    print("\n=== ตัวเลือกการเรียงรายชื่อ ===")
    print("1. เรียงตามเลขที่ (น้อยไปมาก)")
    print("2. เรียงตามชื่อ (ก-ฮ)")
    sort_choice = input("เลือกการเรียง (1-2): ")
    
    print(f"\n=== รายชื่อนักเรียน ชั้น {grade} ห้อง {classroom} ===")
    found = False
    
    if sort_choice == "1":
        sorted_keys = sorted(students.keys(), key=lambda x: int(x))
    elif sort_choice == "2":
        sorted_keys = sorted(students.keys(), key=lambda x: students[x]["ชื่อ"])
    else:
        print("เลือกไม่ถูกต้อง → ใช้ค่าเริ่มต้นเรียงตามเลขที่")
        sorted_keys = sorted(students.keys(), key=lambda x: int(x))
    
    for no in sorted_keys:
        info = students[no]
        if info["ชั้น"] == grade and info["ห้อง"] == classroom:
            found = True
            print(f"\nเลขที่ {no} - {info['ชื่อ']}:")
            for subject in subjects_list:
                print(f"  {subject}: {info['คะแนน'][subject]}")
    
    if not found:
        print("ไม่พบข้อมูลนักเรียนในชั้นและห้องนี้")

# เมนู 3: ค้นหาคะแนนนักเรียน
def search_student():
    print("\n=== เมนูค้นหานักเรียน ===")
    print("1. ค้นหาด้วยชื่อ")
    print("2. ค้นหาด้วยเลขที่ + ชั้น + ห้อง")
    
    choice = input("เลือกเมนู (1-2): ")
    
    if choice == "1":
        name = input("กรอกชื่อนักเรียนที่ต้องการค้นหา: ")
        found = False
        for no, info in students.items():
            if info["ชื่อ"] == name:
                found = True
                print(f"\nเลขที่ {no} - {info['ชื่อ']} (ชั้น {info['ชั้น']} ห้อง {info['ห้อง']}):")
                for subject in subjects_list:
                    print(f"  {subject}: {info['คะแนน'][subject]}")
        if not found:
            print("ไม่พบชื่อนักเรียนในระบบ")
    
    elif choice == "2":
        grade_input = input("กรอกชั้นการศึกษา (ป.1 - ป.6): ")
        classroom_input = input("กรอกห้องเรียน (1 - 10): ")
        no_input = input("กรอกเลขที่นักเรียน: ")
        
        if no_input in students:
            info = students[no_input]
            if info["ชั้น"] == grade_input and info["ห้อง"] == classroom_input:
                print(f"\nเลขที่ {no_input} - {info['ชื่อ']} (ชั้น {info['ชั้น']} ห้อง {info['ห้อง']}):")
                for subject in subjects_list:
                    print(f"  {subject}: {info['คะแนน'][subject]}")
            else:
                print("ไม่พบข้อมูลนักเรียนในชั้นและห้องที่ระบุ")
        else:
            print("ไม่พบเลขที่นักเรียนในระบบ")
    else:
        print("เลือกเมนูไม่ถูกต้อง")

# เมนู 4: อัปเดตคะแนนนักเรียน
def update_student():
    print("\n=== เมนูอัปเดตคะแนนนักเรียน ===")
    print("1. อัปเดตด้วยชื่อ")
    print("2. อัปเดตด้วยเลขที่ + ชั้น + ห้อง")
    
    choice = input("เลือกเมนู (1-2): ")
    
    if choice == "1":
        name = input("กรอกชื่อนักเรียนที่ต้องการอัปเดต: ")
        found = None
        for no, info in students.items():
            if info["ชื่อ"] == name:
                found = (no, info)
                break
        if found:
            no, info = found
            print(f"\nเลขที่ {no} - {info['ชื่อ']} (ชั้น {info['ชั้น']} ห้อง {info['ห้อง']})")
            print("=== คะแนนเดิมของนักเรียน ===")
            for idx, subject in enumerate(subjects_list, start=1):
                print(f"{idx}. {subject}: {info['คะแนน'][subject]}")
            
            choice = int(input("\nกรอกหมายเลขวิชาที่ต้องการอัปเดต: "))
            if 1 <= choice <= len(subjects_list):
                subject = subjects_list[choice - 1]
                print(f"คะแนนเดิมของ {subject}: {info['คะแนน'][subject]}")
                new_score = float(input(f"กรอกคะแนนใหม่สำหรับ {subject}: "))
                info["คะแนน"][subject] = new_score
                print(f"อัปเดตคะแนนของ เลขที่ {no} - {info['ชื่อ']} ในวิชา {subject} เป็น {new_score} เรียบร้อยแล้ว!")
            else:
                print("เลือกวิชาไม่ถูกต้อง")
        else:
            print("ไม่พบชื่อนักเรียนในระบบ")
    
    elif choice == "2":
        grade_input = input("กรอกชั้นการศึกษา (ป.1 - ป.6): ")
        classroom_input = input("กรอกห้องเรียน (1 - 10): ")
        no_input = input("กรอกเลขที่นักเรียน: ")
        
        if no_input in students:
            info = students[no_input]
            if info["ชั้น"] == grade_input and info["ห้อง"] == classroom_input:
                print(f"\nเลขที่ {no_input} - {info['ชื่อ']} (ชั้น {info['ชั้น']} ห้อง {info['ห้อง']})")
                print("=== คะแนนเดิมของนักเรียน ===")
                for idx, subject in enumerate(subjects_list, start=1):
                    print(f"{idx}. {subject}: {info['คะแนน'][subject]}")
                
                choice = int(input("\nกรอกหมายเลขวิชาที่ต้องการอัปเดต: "))
                if 1 <= choice <= len(subjects_list):
                    subject = subjects_list[choice - 1]
                    print(f"คะแนนเดิมของ {subject}: {info['คะแนน'][subject]}")
                    new_score = float(input(f"กรอกคะแนนใหม่สำหรับ {subject}: "))
                    info["คะแนน"][subject] = new_score
                    print(f"อัปเดตคะแนนของ เลขที่ {no_input} - {info['ชื่อ']} ในวิชา {subject} เป็น {new_score} เรียบร้อยแล้ว!")
                else:
                    print("เลือกวิชาไม่ถูกต้อง")
            else:
                print("ไม่พบข้อมูลนักเรียนในชั้นและห้องที่ระบุ")
        else:
            print("ไม่พบเลขที่นักเรียนในระบบ")
    else:
        print("เลือกเมนูไม่ถูกต้อง")

# เมนู 5: แสดงผลการจัดเกรด
def show_grades():
    if not students:
        print("ยังไม่มีข้อมูลนักเรียน")
        return
    
    print("\n=== แสดงผลการจัดเกรด ===")
    print("1. ดูเกรดตามชั้นและห้อง")
    print("2. ค้นหาเกรดของนักเรียนเพียงคนเดียว")
    
    choice = input("เลือกเมนู (1-2): ")
    
    if choice == "1":
        grade = input("กรอกชั้นการศึกษา (ป.1 - ป.6): ")
        classroom = input("กรอกห้องเรียน (1 - 10): ")
        
        print(f"\n=== ผลการจัดเกรด ชั้น {grade} ห้อง {classroom} ===")
        found = False
        
        for no in sorted(students.keys(), key=lambda x: int(x)):
            info = students[no]
            if info["ชั้น"] == grade and info["ห้อง"] == classroom:
                found = True
                total_score = sum(info["คะแนน"].values())
                avg_score = total_score / len(subjects_list)
                gpa = calculate_grade(avg_score)
                print(f"\nเลขที่ {no} - {info['ชื่อ']}")
                print(f"  คะแนนเฉลี่ย: {avg_score:.2f} → เกรด: {gpa}")
        
        if not found:
            print("ไม่พบข้อมูลนักเรียนในชั้นและห้องนี้")
    
    elif choice == "2":
        name = input("กรอกชื่อนักเรียนที่ต้องการดูเกรด: ")
        found = False
        
        for no, info in students.items():
            if info["ชื่อ"] == name:
                found = True
                total_score = sum(info["คะแนน"].values())
                avg_score = total_score / len(subjects_list)
                gpa = calculate_grade(avg_score)
                print(f"\nเลขที่ {no} - {info['ชื่อ']} (ชั้น {info['ชั้น']} ห้อง {info['ห้อง']})")
                print(f"  คะแนนเฉลี่ย: {avg_score:.2f} → เกรด: {gpa}")
                print("  คะแนนในแต่ละวิชา:")
                for subject in subjects_list:
                    print(f"    - {subject}: {info['คะแนน'][subject]}")
                break
        
        if not found:
            print("ไม่พบชื่อนักเรียนในระบบ")
    else:
        print("เลือกเมนูไม่ถูกต้อง")

# เมนู 6: ลบข้อมูลนักเรียน
def delete_student():
    if not students:
        print("ยังไม่มีข้อมูลนักเรียน")
        return
    
    print("\n=== เมนูลบข้อมูลนักเรียน ===")
    no = input("กรอกเลขที่นักเรียนที่ต้องการลบ: ")
    
    if no in students:
        confirm = input(f"คุณแน่ใจหรือว่าต้องการลบข้อมูล {students[no]['ชื่อ']} (y/n): ")
        if confirm.lower() == "y":
            del students[no]
            print(f"ลบข้อมูลนักเรียนเลขที่ {no} เรียบร้อยแล้ว!")
        else:
            print("ยกเลิกการลบ")
    else:
        print("ไม่พบเลขที่นักเรียนในระบบ")

# ฟังก์ชันแสดงเมนูหลัก
def main_menu():
    while True:
        print("\n" + "="*50)
        print("│    ระบบจัดการคะแนนนักเรียน")
        print("="*50)
        print("1. เพิ่มข้อมูลนักเรียน")
        print("2. แสดงรายชื่อนักเรียน")
        print("3. ค้นหาคะแนนนักเรียน")
        print("4. อัปเดตคะแนนนักเรียน")
        print("5. แสดงผลการจัดเกรด")
        print("6. ลบข้อมูลนักเรียน")
        print("7. ออกจากระบบ")
        print("="*50)
        
        choice = input("เลือกเมนู (1-7): ")
        
        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            show_grades()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            confirm = input("คุณแน่ใจหรือว่าต้องการออกจากระบบ? (y/n): ")
            if confirm.lower() == "y":
                print("\nขอบคุณที่ใช้ระบบ ลาสวัสดี!")
                break
        else:
            print("เลือกเมนูไม่ถูกต้อง กรุณาลองอีกครั้ง")

# จุดเริ่มต้นของโปรแกรม
if __name__ == "__main__":
    main_menu()