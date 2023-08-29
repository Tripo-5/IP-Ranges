import os
import tkinter as tk
from tkinter import filedialog
from ipwhois import IPWhois

class IPProfilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Profiler")

        self.ip_folder = ""
        self.ip_list = []
        self.current_ip_index = 0

        self.select_folder_button = tk.Button(root, text="Select IP Folder", command=self.select_ip_folder)
        self.select_folder_button.pack()

        self.prev_button = tk.Button(root, text="Previous", command=self.show_prev_ip)
        self.prev_button.pack()

        self.next_button = tk.Button(root, text="Next", command=self.show_next_ip)
        self.next_button.pack()

        self.ip_label = tk.Label(root, text="IPV4:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        self.address_label = tk.Label(root, text="Address:")
        self.address_label.pack()

        self.address_entry = tk.Entry(root)
        self.address_entry.pack()

        self.registered_date_label = tk.Label(root, text="Registered Date:")
        self.registered_date_label.pack()

        self.registered_date_entry = tk.Entry(root)
        self.registered_date_entry.pack()

        self.cloudflare_label = tk.Label(root, text="Cloudflare:")
        self.cloudflare_label.pack()

        self.cloudflare_entry = tk.Entry(root)
        self.cloudflare_entry.pack()

        self.dns_label = tk.Label(root, text="DNS:")
        self.dns_label.pack()

        self.dns_entry = tk.Entry(root)
        self.dns_entry.pack()

        self.port_scan_label = tk.Label(root, text="Port Scan:")
        self.port_scan_label.pack()

        self.port_scan_entry = tk.Entry(root)
        self.port_scan_entry.pack()

        self.geo_location_label = tk.Label(root, text="Geo Location:")
        self.geo_location_label.pack()

        self.geo_location_entry = tk.Entry(root)
        self.geo_location_entry.pack()

        self.city_label = tk.Label(root, text="City:")
        self.city_label.pack()

        self.city_entry = tk.Entry(root)
        self.city_entry.pack()

        self.domain_name_label = tk.Label(root, text="Domain Name:")
        self.domain_name_label.pack()

        self.domain_name_entry = tk.Entry(root)
        self.domain_name_entry.pack()

        self.request_button = tk.Button(root, text="Request Information", command=self.request_info)
        self.request_button.pack()
        
    def request_info(self):
        ip = self.ip_entry.get().strip()
        if ip:
            self.profile_ip(ip)

    def select_ip_folder(self):
        self.ip_folder = filedialog.askdirectory()
        self.select_folder_button.config(text=f"Selected Folder: {self.ip_folder}")
        self.load_ip_list()

    def load_ip_list(self):
        self.ip_list = []
        for filename in os.listdir(self.ip_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.ip_folder, filename)
                with open(file_path, "r") as file:
                    for line in file:
                        ip = line.strip()
                        self.ip_list.append(ip)
        self.current_ip_index = 0
        self.show_current_ip()

    def show_current_ip(self):
        if 0 <= self.current_ip_index < len(self.ip_list):
            current_ip = self.ip_list[self.current_ip_index]
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, current_ip)
            self.profile_ip(current_ip)

    def show_prev_ip(self):
        if self.current_ip_index > 0:
            self.current_ip_index -= 1
            self.show_current_ip()

    def show_next_ip(self):
        if self.current_ip_index < len(self.ip_list) - 1:
            self.current_ip_index += 1
            self.show_current_ip()

    def profile_ip(self, ip):
        ipwhois = IPWhois(ip)
        result = ipwhois.lookup_rdap()
        self.update_entry(self.address_entry, result.get("network", {}).get("address", ""))
        self.update_entry(self.registered_date_entry, result.get("network", {}).get("registrationDate", ""))
        self.update_entry(self.cloudflare_entry, result.get("network", {}).get("remarks", {}).get("description", ""))
        self.update_entry(self.dns_entry, ", ".join(result.get("network", {}).get("dns", [])))
        self.update_entry(self.port_scan_entry, ", ".join(map(str, result.get("ports", []))))
        self.update_entry(self.geo_location_entry, result.get("network", {}).get("geo", {}).get("country", ""))
        self.update_entry(self.city_entry, result.get("network", {}).get("geo", {}).get("city", ""))
        self.update_entry(self.domain_name_entry, result.get("network", {}).get("name", ""))

    def update_entry(self, entry, value):
        entry.delete(0, tk.END)
        entry.insert(0, value)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPProfilerApp(root)
    root.mainloop()
