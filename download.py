import os
import requests
import threading
import tkinter as tk
from tkinter import messagebox, Menu
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_and_download(urls, status_text):
    for index, url in enumerate(urls, start=1):
        output_dir = f"folder_{index}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        status_text.insert(tk.END, f"Processing link {index}: {url}\n")
        status_text.update()

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            status_text.insert(tk.END, f"Error fetching link {url}: {e}\n")
            status_text.update()
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        listing_name_wrap = soup.find(id="listing_name_wrap")
        if listing_name_wrap and listing_name_wrap.find("h1"):
            listing_name = listing_name_wrap.find("h1").text.strip()
            with open(os.path.join(output_dir, "listing_name.txt"), "w", encoding="utf-8") as file:
                file.write(f"URL: {url}\nListing Name: {listing_name}\n")
            status_text.insert(tk.END, f"Listing Name: {listing_name}\n")
        else:
            status_text.insert(tk.END, "Listing name not found.\n")

        room_main_info = soup.find(id="roomMainInfo")
        if not room_main_info:
            status_text.insert(tk.END, "roomMainInfo field not found.\n")
            continue

        photos = room_main_info.find(id="photos")
        if not photos:
            status_text.insert(tk.END, "Photos field not found.\n")
            continue

        carousel = photos.find(id="carousel1")
        if not carousel:
            status_text.insert(tk.END, "Carousel field not found.\n")
            continue

        slide_index = 1
        while True:
            slide_id = f"slide{slide_index}"
            slide = carousel.find(id=slide_id)
            if not slide:
                break

            img_tag = slide.find("img")
            if img_tag and img_tag.get("src"):
                img_url = urljoin(url, img_tag["src"])
                try:
                    img_response = requests.get(img_url, timeout=10)
                    img_response.raise_for_status()
                    img_name = os.path.join(output_dir, f"image_{slide_index}.jpg")
                    with open(img_name, "wb") as img_file:
                        img_file.write(img_response.content)
                    status_text.insert(tk.END, f"Downloaded image {slide_index}: {img_name}\n")
                except requests.exceptions.RequestException as e:
                    status_text.insert(tk.END, f"Error downloading image {slide_index}: {e}\n")
            slide_index += 1

        status_text.insert(tk.END, f"All images for link {index} downloaded.\n\n")
        status_text.update()

def start_scraping():
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    urls = [url.strip() for url in urls if url.strip()]
    if not urls:
        messagebox.showwarning("Warning", "Please enter at least one URL.")
        return
    status_text.delete("1.0", tk.END)
    threading.Thread(target=scrape_and_download, args=(urls, status_text), daemon=True).start()

# ایجاد برنامه Tkinter
root = tk.Tk()
root.title("Web Image Downloader")
root.geometry("600x500")

tk.Label(root, text="Enter URLs (one per line):").pack(pady=5)
url_entry = tk.Text(root, height=5, width=70)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Download", command=start_scraping)
download_button.pack(pady=10)

status_text = tk.Text(root, height=15, width=70)
status_text.pack(pady=5)

# 📌 تابع اضافه کردن منوی کلیک راست
def show_context_menu(event, widget):
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
    context_menu.tk_popup(event.x_root, event.y_root)

# 📌 اتصال منوی کلیک راست به `Text`
url_entry.bind("<Button-3>", lambda event: show_context_menu(event, url_entry))
status_text.bind("<Button-3>", lambda event: show_context_menu(event, status_text))

# 📌 فعال‌سازی `Ctrl+V` و `Ctrl+C`
def enable_shortcuts(widget):
    widget.bind("<Control-v>", lambda event: widget.event_generate("<<Paste>>"))
    widget.bind("<Control-c>", lambda event: widget.event_generate("<<Copy>>"))
    widget.bind("<Control-x>", lambda event: widget.event_generate("<<Cut>>"))

enable_shortcuts(url_entry)
enable_shortcuts(status_text)

root.mainloop()