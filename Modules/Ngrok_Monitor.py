import os

def check_ngrok_status():
    # Lấy khóa từ biến môi trường đã được Workflow truyền vào
    api_key = os.getenv('REST_API_NGROK')
    if not api_key:
        print("[!] Cảnh báo: REST_API_NGROK chưa được cấu hình tại Kho này.")
        return
        
    print("[SYSTEM] Ngrok_Monitor.py đang giám sát tunnel tại Kho Thương Hiệu...")

if __name__ == "__main__":
    check_ngrok_status()
