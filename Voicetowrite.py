import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pygetwindow as gw
from pynput import keyboard as pynput_keyboard
import threading

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("โปรแกรมรับพูดและเขียน")
root.geometry("300x200")
root.attributes('-topmost', 1)

# สร้างเครื่องมือแปลงข้อความเป็นเสียง
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # ตั้งค่าความเร็วในการพูด
engine.setProperty('voice', 'thai')  # ตั้งค่าให้รองรับเสียงภาษาไทย

# สถานะการรับฟัง
listening = False

# ฟังก์ชันสำหรับรับคำพูดและพิมพ์ลงในหน้าต่างที่เมาส์ชี้อยู่
def listen_and_type():
    global listening
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while listening:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language="th-TH")
                current_window = gw.getActiveWindow()
                current_window.activate()
                for char in text:
                    pynput_keyboard.Controller().type(char)
                pynput_keyboard.Controller().type('\n')
            except sr.UnknownValueError:
                print("ไม่สามารถเข้าใจคำพูด")
            except sr.RequestError:
                print("เกิดข้อผิดพลาดในการเชื่อมต่อ")
            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")

# ฟังก์ชันสำหรับเริ่มการฟัง
def start_listening():
    global listening
    listening = True
    listen_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    threading.Thread(target=listen_and_type, daemon=True).start()

# ฟังก์ชันสำหรับหยุดการฟัง
def stop_listening():
    global listening
    listening = False
    listen_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# ฟังก์ชันสำหรับสลับสถานะการฟัง
def toggle_listening():
    if listening:
        stop_listening()
    else:
        start_listening()

# ส่วนติดต่อผู้ใช้
listen_button = tk.Button(root, text="เริ่มการฟัง", command=start_listening)
listen_button.pack(pady=20)

stop_button = tk.Button(root, text="หยุดการฟัง", command=stop_listening, state=tk.DISABLED)
stop_button.pack(pady=20)

# ฟังก์ชันสำหรับจับการกดปุ่ม F3
def on_press(key):
    try:
        if key == pynput_keyboard.Key.f3:
            toggle_listening()
    except AttributeError:
        pass

# เริ่มฟังการกดปุ่ม F3
listener = pynput_keyboard.Listener(on_press=on_press)
listener.start()

# เริ่มโปรแกรม
root.mainloop()
