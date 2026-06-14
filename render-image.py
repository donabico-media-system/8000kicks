#!/usr/bin/env python3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--affiliate_link", required=True)
    parser.add_argument("--image1", required=True)
    parser.add_argument("--image2", required=True)
    parser.add_argument("--image3", required=True)
    parser.add_argument("--image4", required=True)
    args = parser.parse_args()

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Thay thế các biến
    content = content.replace("{{AFFILIATE_LINK}}", args.affiliate_link)
    content = content.replace("{{IMAGE_1}}", args.image1)
    content = content.replace("{{IMAGE_2}}", args.image2)
    content = content.replace("{{IMAGE_3}}", args.image3)
    content = content.replace("{{IMAGE_4}}", args.image4)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Đã cập nhật index.html thành công với 4 hình ảnh!")
