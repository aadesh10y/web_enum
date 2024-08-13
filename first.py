import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import threading
from queue import Queue
import time

class WebEnumerationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Web Enumeration Tool")
        self.root.geometry("800x650")
        self.stop_flag = threading.Event()  # Flag to stop the threads
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Define style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', padding=(10, 5))

        # Target URL
        self.url_label = ttk.Label(self.frame, text="Enter Target URL:")
        self.url_label.grid(column=0, row=0, pady=5, padx=5, sticky=tk.W)
        self.url_entry = ttk.Entry(self.frame, width=40)
        self.url_entry.insert(0, "http://example.com")  # Placeholder
        self.url_entry.grid(column=1, row=0, pady=5, padx=5, sticky=tk.W)

        # Wordlist
        self.wordlist_label = ttk.Label(self.frame, text="Select Wordlist File:")
        self.wordlist_label.grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
        self.wordlist_button = ttk.Button(self.frame, text="Browse", command=self.browse_wordlist)
        self.wordlist_button.grid(column=2, row=1, pady=5, padx=5, sticky=tk.W)
        self.wordlist_path = tk.StringVar()
        self.wordlist_entry = ttk.Entry(self.frame, width=40, textvariable=self.wordlist_path, state="readonly")
        self.wordlist_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)

        # Proxy
        self.proxy_label = ttk.Label(self.frame, text="Proxy (http://ip:port):")
        self.proxy_label.grid(column=0, row=2, pady=5, padx=5, sticky=tk.W)
        self.proxy_entry = ttk.Entry(self.frame, width=40)
        self.proxy_entry.insert(0, "http://127.0.0.1:8080")  # Placeholder
        self.proxy_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tk.W)

        # Number of Threads
        self.threads_label = ttk.Label(self.frame, text="Number of Threads:")
        self.threads_label.grid(column=0, row=3, pady=5, padx=5, sticky=tk.W)
        self.threads_spinbox = ttk.Spinbox(self.frame, from_=1, to=20, width=5)
        self.threads_spinbox.set(10)  # Set a default value
        self.threads_spinbox.grid(column=1, row=3, pady=5, padx=5, sticky=tk.W)

        # Status Code Filter
        self.status_code_label = ttk.Label(self.frame, text="Filter by Status Codes (comma separated):")
        self.status_code_label.grid(column=0, row=4, pady=5, padx=5, sticky=tk.W)
        self.status_code_entry = ttk.Entry(self.frame, width=40)
        self.status_code_entry.insert(0, "200,301,302,404,503,504,500")  # Placeholder
        self.status_code_entry.grid(column=1, row=4, pady=5, padx=5, sticky=tk.W)

        # User-Agent
        self.user_agent_label = ttk.Label(self.frame, text="Custom User-Agent:")
        self.user_agent_label.grid(column=0, row=5, pady=5, padx=5, sticky=tk.W)
        self.user_agent_entry = ttk.Entry(self.frame, width=40)
        self.user_agent_entry.insert(0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")  # Placeholder
        self.user_agent_entry.grid(column=1, row=5, pady=5, padx=5, sticky=tk.W)

        # Buttons
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.grid(column=0, row=6, columnspan=3, pady=10, padx=10, sticky=tk.W)

        self.run_button = ttk.Button(self.button_frame, text="Run", command=self.run_enumeration)
        self.run_button.grid(column=0, row=0, pady=5, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Screen", command=self.clear_screen)
        self.clear_button.grid(column=1, row=0, pady=5, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save Results", command=self.save_results)
        self.save_button.grid(column=2, row=0, pady=5, padx=5)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_enumeration)
        self.stop_button.grid(column=3, row=0, pady=5, padx=5)

        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(column=4, row=0, pady=5, padx=5)

        # Output Text Area
        self.output_frame = ttk.LabelFrame(self.frame, text="Output", padding="10 10 10 10")
        self.output_frame.grid(column=0, row=7, columnspan=3, pady=10, padx=10, sticky=(tk.W, tk.E))
        self.output_text = tk.Text(self.output_frame, width=90, height=20, wrap=tk.WORD)
        self.output_text.grid(column=0, row=0, columnspan=3, pady=5, padx=5, sticky=(tk.W, tk.E))

        # Define text tags for colored output
        self.output_text.tag_configure('success', foreground='green')
        self.output_text.tag_configure('redirect', foreground='blue')
        self.output_text.tag_configure('client_error', foreground='orange')
        self.output_text.tag_configure('server_error', foreground='red')

        # Results
        self.results = []

    def browse_wordlist(self):
        wordlist_path = filedialog.askopenfilename(title="Select Wordlist File", filetypes=(("Text Files", "*.txt"),))
        if wordlist_path:
            self.wordlist_path.set(wordlist_path)

    def run_enumeration(self):
        self.stop_flag.clear()
        url = self.url_entry.get().strip()
        wordlist = self.wordlist_path.get().strip()
        proxy = self.proxy_entry.get().strip()
        threads = int(self.threads_spinbox.get())
        status_codes = self.status_code_entry.get().strip()
        user_agent = self.user_agent_entry.get().strip()

        if not url or not wordlist:
            messagebox.showerror("Error", "Please enter a target URL and select a wordlist file.")
            return

        self.output_text.insert(tk.END, f"Starting enumeration on {url}...\n")
        self.output_text.insert(tk.END, "----------------------------------------------------------------------------------------\n")
        self.root.update_idletasks()

        # Run enumeration in a separate thread
        threading.Thread(target=self.enumerate_directories, args=(url, wordlist, proxy, threads, status_codes, user_agent)).start()

    def enumerate_directories(self, url, wordlist, proxy, threads, status_codes, user_agent):
        try:
            with open(wordlist, "r") as file:
                directories = file.read().splitlines()

            headers = {}
            if user_agent:
                headers['User-Agent'] = user_agent

            proxies = {"http": proxy, "https": proxy} if proxy else None
            queue = Queue()
            status_codes = [int(code) for code in status_codes.split(',')] if status_codes else None

            for directory in directories:
                queue.put(directory)

            def worker():
                while not queue.empty() and not self.stop_flag.is_set():
                    directory = queue.get()
                    full_url = f"{url}/{directory}"
                    start_time = time.time()
                    try:
                        response = requests.get(full_url, headers=headers, proxies=proxies)
                        response_time = time.time() - start_time
                        if not status_codes or response.status_code in status_codes:
                            result = f"{full_url} - Status Code: {response.status_code} - Response Time: {response_time:.2f} seconds\n"
                            self.results.append(result)
                            self.insert_colored_result(result, response.status_code)
                            self.root.update_idletasks()
                    except requests.RequestException as e:
                        self.output_text.insert(tk.END, f"Error: {e}\n")
                        self.root.update_idletasks()
                    queue.task_done()

            for _ in range(threads):
                threading.Thread(target=worker).start()

            queue.join()
        except Exception as e:
            self.output_text.insert(tk.END, f"Error reading wordlist file: {e}\n")
            self.root.update_idletasks()

        self.output_text.insert(tk.END, "Enumeration completed.\n")
        self.output_text.insert(tk.END, "----------------------------------------------------------------------------------------\n")

    def insert_colored_result(self, result, status_code):
        if 200 <= status_code < 300:
            self.output_text.insert(tk.END, result, 'success')
        elif 300 <= status_code < 400:
            self.output_text.insert(tk.END, result, 'redirect')
        elif 400 <= status_code < 500:
            self.output_text.insert(tk.END, result, 'client_error')
        elif 500 <= status_code < 600:
            self.output_text.insert(tk.END, result, 'server_error')
        else:
            self.output_text.insert(tk.END, result)

    def clear_screen(self):
        self.output_text.delete("1.0", tk.END)

    def save_results(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text Files", "*.txt"),))
        if save_path:
            try:
                with open(save_path, "w") as file:
                    file.writelines(self.results)
                messagebox.showinfo("Save Successful", "Results saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the file: {e}")

    def stop_enumeration(self):
        self.stop_flag.set()
        self.output_text.insert(tk.END, "Stopping enumeration...\n")
        self.output_text.insert(tk.END, "----------------------------------------------------------------------------------------\n")
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = WebEnumerationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()