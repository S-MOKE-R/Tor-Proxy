#!/usr/bin/env python3
"""
Tor Controller Pro v1.0
Developer: @S_MOKE_R
GitHub: https://github.com/S-MOKE-R
Telegram: https://t.me/S_MOKE_R
Channel: https://t.me/VOID_SMOKER
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import requests
import threading
import time
import os
import json
import psutil
import socket
import re
import webbrowser
from datetime import datetime
import pyperclip

class ModernScrollFrame(tk.Frame):
    def __init__(self, parent, bg='#1a1b26'):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class TorControllerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Tor Controller Pro v1.0 - by @S_MOKE_R")
        
        # SIMPLE WORKING GEOMETRY - FIXED FULL SCREEN
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.resizable(True, True)
        self.root.configure(bg='#1a1b26')
        
        # Variables
        self.timer_running = False
        self.timer_seconds = 0
        self.connection_history = []
        self.max_history = 100
        self.current_status = "OFF"
        self.start_time = None
        self.download_in_progress = False
        
        self.config_file = os.path.expanduser("~/.tor_pro_config.json")
        self.load_config()
        
        self.themes = {
            'dark': {
                'bg': '#0f0f1a', 'bg2': '#1a1b2e', 'bg3': '#24283b', 'bg4': '#2d2d4a',
                'fg': '#c0caf5', 'fg2': '#7aa2f7', 'accent': '#7aa2f7',
                'success': '#9ece6a', 'danger': '#f7768e', 'warning': '#e0af68',
                'info': '#7dcfff', 'border': '#3b4261', 'hover': '#2a2d4e',
                'header_bg': '#161625'
            },
            'light': {
                'bg': '#f0f0f5', 'bg2': '#ffffff', 'bg3': '#e8e8f0', 'bg4': '#d0d0dd',
                'fg': '#2c2c3c', 'fg2': '#555577', 'accent': '#0066cc',
                'success': '#2e7d32', 'danger': '#c62828', 'warning': '#f57f17',
                'info': '#00695c', 'border': '#dddddd', 'hover': '#d0d0dd',
                'header_bg': '#e8e8f0'
            },
            'hacker': {
                'bg': '#0a0a0a', 'bg2': '#1a1a1a', 'bg3': '#2a2a2a', 'bg4': '#3a3a3a',
                'fg': '#00ff41', 'fg2': '#00cc33', 'accent': '#00ff41',
                'success': '#00ff41', 'danger': '#ff0040', 'warning': '#ffaa00',
                'info': '#00ffff', 'border': '#2a2a2a', 'hover': '#1f3f1f',
                'header_bg': '#0f0f0f'
            },
            'blue': {
                'bg': '#0a1628', 'bg2': '#0f2040', 'bg3': '#1a2a4a', 'bg4': '#2a3a5a',
                'fg': '#88ccff', 'fg2': '#66aadd', 'accent': '#4da6ff',
                'success': '#66cc99', 'danger': '#ff6666', 'warning': '#ffcc66',
                'info': '#66ccff', 'border': '#1a3366', 'hover': '#1a2a5a',
                'header_bg': '#0c1a30'
            }
        }
        
        self.colors = self.themes['dark']
        self.current_theme = 'dark'
        
        self.setup_ui()
        self.get_real_ip()
        self.check_tor_status()
        self.update_stats()
        self.check_proxychains()
        
        self.root.after(500, self.show_credits)
        
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {'theme': 'dark', 'auto_start': False, 'timer_preset': 30}
        except:
            self.config = {'theme': 'dark', 'auto_start': False, 'timer_preset': 30}
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def apply_theme(self, theme_name):
        if theme_name in self.themes:
            self.colors = self.themes[theme_name]
            self.current_theme = theme_name
            self.config['theme'] = theme_name
            self.save_config()
            self.refresh_ui()
    
    def refresh_ui(self):
        self.root.configure(bg=self.colors['bg'])
        self.update_widget_theme(self.main_container)
        self.update_status_indicator()
    
    def update_widget_theme(self, widget):
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.PanedWindow)):
                widget.configure(bg=self.colors.get('bg', '#1a1b26'))
            elif isinstance(widget, tk.Label):
                if widget.cget('text') not in ['🌍 Real IP', '🔒 Tor IP']:
                    widget.configure(bg=self.colors.get('bg', '#1a1b26'), 
                                   fg=self.colors.get('fg', '#c0caf5'))
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.colors.get('bg3', '#24283b'), 
                               fg=self.colors.get('fg', '#c0caf5'),
                               activebackground=self.colors.get('hover', '#2a2d4e'))
            elif isinstance(widget, tk.Canvas):
                widget.configure(bg=self.colors.get('bg', '#1a1b26'))
            elif isinstance(widget, tk.Text):
                widget.configure(bg=self.colors.get('bg2', '#1a1b2e'), 
                               fg=self.colors.get('fg', '#c0caf5'))
            for child in widget.winfo_children():
                self.update_widget_theme(child)
        except:
            pass
    
    def setup_ui(self):
        self.main_container = ModernScrollFrame(self.root, bg=self.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        content = self.main_container.scrollable_frame
        content.configure(bg=self.colors['bg'])
        
        self.create_header(content)
        self.create_dashboard(content)
        
        content_row = tk.Frame(content, bg=self.colors['bg'])
        content_row.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        left_col = tk.Frame(content_row, bg=self.colors['bg'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_col = tk.Frame(content_row, bg=self.colors['bg'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_controls(left_col)
        self.create_toggle_button(left_col)
        self.create_download_section(left_col)
        
        self.create_timer_section(right_col)
        self.create_logs_section(right_col)
        
        self.create_footer(content)
        
        self.add_log("🚀 Tor Controller Pro v1.0 initialized", "info")
        self.add_log("💡 Click 'CONNECT TO TOR' to enable proxy", "info")
        self.add_log("📥 Use Download Helper for GitHub files", "info")
    
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['header_bg'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        left_frame = tk.Frame(header_frame, bg=self.colors['header_bg'])
        left_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        tk.Label(left_frame, text="🔒", font=("Segoe UI", 28), 
                bg=self.colors['header_bg']).pack(side=tk.LEFT, padx=(0, 12))
        
        title_container = tk.Frame(left_frame, bg=self.colors['header_bg'])
        title_container.pack(side=tk.LEFT)
        
        tk.Label(title_container, text="Tor Controller Pro",
                font=("Segoe UI", 18, "bold"),
                fg=self.colors['fg'], bg=self.colors['header_bg']).pack(anchor=tk.W)
        
        tk.Label(title_container, text="Professional Proxy Manager • v1.0",
                font=("Segoe UI", 9),
                fg=self.colors['fg2'], bg=self.colors['header_bg']).pack(anchor=tk.W)
        
        right_frame = tk.Frame(header_frame, bg=self.colors['header_bg'])
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(right_frame, text="🎨 Theme:", font=("Segoe UI", 10),
                fg=self.colors['fg'], bg=self.colors['header_bg']).pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_menu = ttk.Combobox(right_frame, textvariable=self.theme_var,
                                 values=['dark', 'light', 'hacker', 'blue'],
                                 state='readonly', width=10)
        theme_menu.pack(side=tk.LEFT, padx=5)
        theme_menu.bind('<<ComboboxSelected>>', 
                       lambda e: self.apply_theme(self.theme_var.get()))
        
        credits_btn = tk.Button(right_frame, text="👨‍💻 Credits", 
                               command=self.show_credits,
                               font=("Segoe UI", 9, "bold"),
                               bg=self.colors['bg3'], fg=self.colors['fg'],
                               relief=tk.FLAT, padx=12, pady=4,
                               cursor='hand2')
        credits_btn.pack(side=tk.LEFT, padx=10)
    
    def create_dashboard(self, parent):
        dash_frame = tk.LabelFrame(parent, text="📊 Dashboard", 
                                  font=("Segoe UI", 12, "bold"),
                                  fg=self.colors['fg'], bg=self.colors['bg'],
                                  padx=15, pady=10)
        dash_frame.pack(fill=tk.X, pady=(0, 15))
        
        status_row = tk.Frame(dash_frame, bg=self.colors['bg'])
        status_row.pack(fill=tk.X, pady=5)
        
        self.status_canvas = tk.Canvas(status_row, width=16, height=16,
                                      bg=self.colors['bg'], highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(0, 10))
        self.status_indicator = self.status_canvas.create_oval(2, 2, 14, 14,
                                                              fill=self.colors['danger'])
        
        self.status_label = tk.Label(status_row, text="OFFLINE",
                                    font=("Segoe UI", 14, "bold"),
                                    fg=self.colors['danger'],
                                    bg=self.colors['bg'])
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.uptime_label = tk.Label(status_row, text="⏱️ Uptime: 00:00:00",
                                    font=("Segoe UI", 10),
                                    fg=self.colors['fg2'],
                                    bg=self.colors['bg'])
        self.uptime_label.pack(side=tk.RIGHT, padx=10)
        
        ip_row = tk.Frame(dash_frame, bg=self.colors['bg'])
        ip_row.pack(fill=tk.X, pady=5)
        
        real_frame = tk.Frame(ip_row, bg=self.colors['bg3'], relief=tk.FLAT,
                             padx=10, pady=5)
        real_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tk.Label(real_frame, text="🌍 Real IP", 
                font=("Segoe UI", 9, "bold"),
                fg=self.colors['fg2'], bg=self.colors['bg3']).pack(side=tk.LEFT)
        
        self.real_ip_label = tk.Label(real_frame, text="Loading...",
                                     font=("Segoe UI", 10, "bold"),
                                     fg=self.colors['fg'], bg=self.colors['bg3'])
        self.real_ip_label.pack(side=tk.LEFT, padx=10)
        
        tor_frame = tk.Frame(ip_row, bg=self.colors['bg3'], relief=tk.FLAT,
                           padx=10, pady=5)
        tor_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tk.Label(tor_frame, text="🔒 Tor IP",
                font=("Segoe UI", 9, "bold"),
                fg=self.colors['fg2'], bg=self.colors['bg3']).pack(side=tk.LEFT)
        
        self.tor_ip_label = tk.Label(tor_frame, text="Not connected",
                                    font=("Segoe UI", 10, "bold"),
                                    fg=self.colors['fg'], bg=self.colors['bg3'])
        self.tor_ip_label.pack(side=tk.LEFT, padx=10)
    
    def create_controls(self, parent):
        control_frame = tk.LabelFrame(parent, text="⚡ Quick Actions",
                                     font=("Segoe UI", 11, "bold"),
                                     fg=self.colors['fg'], bg=self.colors['bg'],
                                     padx=12, pady=8)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_grid = tk.Frame(control_frame, bg=self.colors['bg'])
        btn_grid.pack(fill=tk.X)
        
        buttons = [
            ("🔄 New Identity", self.new_identity, self.colors['info']),
            ("📊 Refresh IP", self.refresh_ips, self.colors['fg2']),
            ("📋 Copy Current", self.copy_current_ip, self.colors['fg2']),
            ("⚙️ Settings", self.show_settings, self.colors['fg2'])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            frame = tk.Frame(btn_grid, bg=self.colors['bg'])
            frame.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)
            
            btn = tk.Button(frame, text=text, command=command,
                          font=("Segoe UI", 10, "bold"),
                          bg=self.colors['bg3'], fg=color,
                          activebackground=self.colors['hover'],
                          relief=tk.FLAT, padx=10, pady=6)
            btn.pack(fill=tk.X)
    
    def create_toggle_button(self, parent):
        self.toggle_btn = tk.Button(parent,
                                   text="🔒 CONNECT TO TOR",
                                   command=self.toggle_tor,
                                   font=("Segoe UI", 16, "bold"),
                                   bg=self.colors['success'],
                                   fg='black',
                                   height=2,
                                   relief=tk.FLAT,
                                   activebackground=self.colors['hover'])
        self.toggle_btn.pack(fill=tk.X, pady=(0, 10))
    
    def create_download_section(self, parent):
        download_frame = tk.LabelFrame(parent, text="📥 Download Helper",
                                     font=("Segoe UI", 11, "bold"),
                                     fg=self.colors['fg'], bg=self.colors['bg'],
                                     padx=12, pady=8)
        download_frame.pack(fill=tk.X, pady=(0, 5))
        
        url_row = tk.Frame(download_frame, bg=self.colors['bg'])
        url_row.pack(fill=tk.X, pady=5)
        
        tk.Label(url_row, text="URL:", font=("Segoe UI", 9),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT, padx=5)
        
        self.url_entry = tk.Entry(url_row, font=("Segoe UI", 9),
                                 bg=self.colors['bg3'], fg=self.colors['fg'],
                                 relief=tk.FLAT, insertbackground=self.colors['fg'])
        self.url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_row = tk.Frame(download_frame, bg=self.colors['bg'])
        btn_row.pack(fill=tk.X, pady=5)
        
        self.download_btn = tk.Button(btn_row, text="⬇️ Download",
                                     command=self.start_download,
                                     font=("Segoe UI", 10, "bold"),
                                     bg=self.colors['accent'], fg='black',
                                     activebackground=self.colors['hover'],
                                     relief=tk.FLAT, padx=10, pady=4)
        self.download_btn.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        
        self.resume_btn = tk.Button(btn_row, text="⏸️ Resume",
                                   command=self.resume_download,
                                   font=("Segoe UI", 10),
                                   bg=self.colors['warning'], fg='black',
                                   activebackground=self.colors['hover'],
                                   relief=tk.FLAT, padx=10, pady=4)
        self.resume_btn.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        
        self.progress_var = tk.StringVar(value="✅ Ready")
        self.progress_label = tk.Label(download_frame, textvariable=self.progress_var,
                                      font=("Segoe UI", 8),
                                      fg=self.colors['fg2'], bg=self.colors['bg'])
        self.progress_label.pack(pady=3)
        
        self.pc_status = tk.Label(download_frame, text="🔍 Checking proxychains...",
                                 font=("Segoe UI", 8),
                                 fg=self.colors['fg2'], bg=self.colors['bg'])
        self.pc_status.pack()
    
    def create_timer_section(self, parent):
        timer_frame = tk.LabelFrame(parent, text="⏱️ Timer",
                                   font=("Segoe UI", 11, "bold"),
                                   fg=self.colors['fg'], bg=self.colors['bg'],
                                   padx=12, pady=8)
        timer_frame.pack(fill=tk.X, pady=(0, 10))
        
        timer_row = tk.Frame(timer_frame, bg=self.colors['bg'])
        timer_row.pack(fill=tk.X, pady=5)
        
        tk.Label(timer_row, text="Auto-Disable:", 
                font=("Segoe UI", 9),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT, padx=3)
        
        self.timer_var = tk.StringVar(value="30")
        timer_spin = tk.Spinbox(timer_row, from_=0, to=3600,
                               textvariable=self.timer_var, width=6,
                               font=("Segoe UI", 9),
                               bg=self.colors['bg3'], fg=self.colors['fg'],
                               relief=tk.FLAT)
        timer_spin.pack(side=tk.LEFT, padx=3)
        
        tk.Label(timer_row, text="sec", 
                font=("Segoe UI", 9),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT, padx=3)
        
        self.timer_btn = tk.Button(timer_row, text="▶️ Start",
                                  command=self.start_timer,
                                  font=("Segoe UI", 10, "bold"),
                                  bg=self.colors['warning'], fg='black',
                                  activebackground=self.colors['hover'],
                                  relief=tk.FLAT, padx=10, pady=3)
        self.timer_btn.pack(side=tk.LEFT, padx=5)
        
        self.timer_display = tk.Label(timer_row, text="",
                                     font=("Segoe UI", 16, "bold"),
                                     fg=self.colors['accent'],
                                     bg=self.colors['bg'])
        self.timer_display.pack(side=tk.LEFT, padx=10)
        
        preset_row = tk.Frame(timer_frame, bg=self.colors['bg'])
        preset_row.pack(fill=tk.X, pady=3)
        
        tk.Label(preset_row, text="Presets:", 
                font=("Segoe UI", 8),
                fg=self.colors['fg2'], bg=self.colors['bg']).pack(side=tk.LEFT, padx=3)
        
        for mins in [5, 10, 15, 30, 60]:
            btn = tk.Button(preset_row, text=f"{mins}m",
                          command=lambda m=mins: self.set_preset_timer(m * 60),
                          font=("Segoe UI", 8),
                          bg=self.colors['bg3'], fg=self.colors['fg'],
                          activebackground=self.colors['hover'],
                          relief=tk.FLAT, padx=8, pady=2)
            btn.pack(side=tk.LEFT, padx=2)
    
    def create_logs_section(self, parent):
        logs_frame = tk.LabelFrame(parent, text="📋 Logs",
                                  font=("Segoe UI", 11, "bold"),
                                  fg=self.colors['fg'], bg=self.colors['bg'],
                                  padx=10, pady=8)
        logs_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        log_control = tk.Frame(logs_frame, bg=self.colors['bg'])
        log_control.pack(fill=tk.X, pady=(0, 5))
        
        self.log_count = tk.Label(log_control, text="0 entries",
                                 font=("Segoe UI", 8),
                                 fg=self.colors['fg2'], bg=self.colors['bg'])
        self.log_count.pack(side=tk.LEFT)
        
        clear_btn = tk.Button(log_control, text="🗑️ Clear",
                            command=self.clear_logs,
                            font=("Segoe UI", 8),
                            bg=self.colors['bg3'], fg=self.colors['fg'],
                            activebackground=self.colors['hover'],
                            relief=tk.FLAT, padx=8, pady=2)
        clear_btn.pack(side=tk.RIGHT)
        
        export_btn = tk.Button(log_control, text="💾 Export",
                             command=self.export_logs,
                             font=("Segoe UI", 8),
                             bg=self.colors['bg3'], fg=self.colors['fg'],
                             activebackground=self.colors['hover'],
                             relief=tk.FLAT, padx=8, pady=2)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        self.log_text = scrolledtext.ScrolledText(logs_frame, 
                                                 font=("Consolas", 8),
                                                 bg=self.colors['bg3'],
                                                 fg=self.colors['fg'],
                                                 height=6,
                                                 relief=tk.FLAT,
                                                 insertbackground=self.colors['fg'])
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=3)
        
        self.log_text.tag_config('info', foreground=self.colors['info'])
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('error', foreground=self.colors['danger'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('accent', foreground=self.colors['accent'])
    
    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg=self.colors['bg2'], height=25)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text="🔒 Tor Controller Pro v1.0 | by @S_MOKE_R",
                font=("Segoe UI", 8),
                fg=self.colors['fg2'], bg=self.colors['bg2']).pack(side=tk.LEFT, padx=15)
        
        # GitHub link (clickable)
        github_btn = tk.Label(footer_frame, text="GitHub", font=("Segoe UI", 8, "underline"),
                              fg=self.colors['accent'], bg=self.colors['bg2'], cursor='hand2')
        github_btn.pack(side=tk.LEFT, padx=5)
        github_btn.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/S-MOKE-R"))
        
        tk.Label(footer_frame, text="|", font=("Segoe UI", 8),
                fg=self.colors['fg2'], bg=self.colors['bg2']).pack(side=tk.LEFT, padx=5)
        
        # Telegram link (clickable)
        tg_btn = tk.Label(footer_frame, text="Telegram", font=("Segoe UI", 8, "underline"),
                          fg=self.colors['accent'], bg=self.colors['bg2'], cursor='hand2')
        tg_btn.pack(side=tk.LEFT)
        tg_btn.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/S_MOKE_R"))
        
        tk.Label(footer_frame, text=f"| Tor: {self.current_status} | {datetime.now().strftime('%H:%M:%S')}",
                font=("Segoe UI", 8),
                fg=self.colors['fg2'], bg=self.colors['bg2']).pack(side=tk.RIGHT, padx=15)
    
    def open_link(self, url):
        webbrowser.open(url)
    
    def show_credits(self):
        credits_window = tk.Toplevel(self.root)
        credits_window.title("👨‍💻 Credits")
        credits_window.geometry("450x300")
        credits_window.configure(bg=self.colors['bg'])
        credits_window.transient(self.root)
        credits_window.grab_set()
        
        tk.Label(credits_window, text="👨‍💻 Credits", 
                font=("Segoe UI", 18, "bold"),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(pady=15)
        
        # Developer (clickable)
        dev_frame = tk.Frame(credits_window, bg=self.colors['bg'])
        dev_frame.pack(pady=5)
        tk.Label(dev_frame, text="Developer: ", font=("Segoe UI", 11),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT)
        dev_label = tk.Label(dev_frame, text="@S_MOKE_R", font=("Segoe UI", 11, "bold"),
                            fg=self.colors['accent'], bg=self.colors['bg'], cursor='hand2')
        dev_label.pack(side=tk.LEFT)
        dev_label.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/S_MOKE_R"))
        
        # GitHub (clickable)
        github_frame = tk.Frame(credits_window, bg=self.colors['bg'])
        github_frame.pack(pady=5)
        tk.Label(github_frame, text="GitHub: ", font=("Segoe UI", 11),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT)
        github_label = tk.Label(github_frame, text="https://github.com/S-MOKE-R", 
                               font=("Segoe UI", 11, "underline"),
                               fg=self.colors['accent'], bg=self.colors['bg'], cursor='hand2')
        github_label.pack(side=tk.LEFT)
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/S-MOKE-R"))
        
        # Telegram (clickable)
        tg_frame = tk.Frame(credits_window, bg=self.colors['bg'])
        tg_frame.pack(pady=5)
        tk.Label(tg_frame, text="Telegram: ", font=("Segoe UI", 11),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT)
        tg_label = tk.Label(tg_frame, text="https://t.me/S_MOKE_R", 
                           font=("Segoe UI", 11, "underline"),
                           fg=self.colors['accent'], bg=self.colors['bg'], cursor='hand2')
        tg_label.pack(side=tk.LEFT)
        tg_label.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/S_MOKE_R"))
        
        # Channel (clickable)
        channel_frame = tk.Frame(credits_window, bg=self.colors['bg'])
        channel_frame.pack(pady=5)
        tk.Label(channel_frame, text="Channel: ", font=("Segoe UI", 11),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT)
        channel_label = tk.Label(channel_frame, text="https://t.me/VOID_SMOKER", 
                                font=("Segoe UI", 11, "underline"),
                                fg=self.colors['accent'], bg=self.colors['bg'], cursor='hand2')
        channel_label.pack(side=tk.LEFT)
        channel_label.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/VOID_SMOKER"))
        
        tk.Frame(credits_window, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(credits_window, text="Tor Controller Pro v1.0", 
                font=("Segoe UI", 10),
                fg=self.colors['fg2'], bg=self.colors['bg']).pack()
        tk.Label(credits_window, text="Open Source - MIT License", 
                font=("Segoe UI", 9),
                fg=self.colors['fg2'], bg=self.colors['bg']).pack()
        
        tk.Button(credits_window, text="Close",
                 command=credits_window.destroy,
                 font=("Segoe UI", 10, "bold"),
                 bg=self.colors['bg3'], fg=self.colors['fg'],
                 relief=tk.FLAT, padx=30, pady=6,
                 cursor='hand2').pack(pady=15)
    
    # ========== FUNCTIONAL METHODS ==========
    
    def check_proxychains(self):
        try:
            result = subprocess.run(["which", "proxychains4"], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                self.pc_status.config(text="✅ proxychains4 installed", fg=self.colors['success'])
                return True
            else:
                self.pc_status.config(text="❌ proxychains4 not found", fg=self.colors['danger'])
                return False
        except:
            self.pc_status.config(text="❌ Error checking proxychains", fg=self.colors['danger'])
            return False
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
        if not self.check_proxychains():
            messagebox.showwarning("Warning", "proxychains4 is not installed.\nRun: sudo apt install proxychains4")
            return
        self.download_in_progress = True
        self.download_btn.config(text="⏳ Downloading...", state=tk.DISABLED)
        self.progress_var.set("⏳ Starting download...")
        thread = threading.Thread(target=self._download_file, args=(url, False))
        thread.daemon = True
        thread.start()
    
    def resume_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
        if not self.check_proxychains():
            messagebox.showwarning("Warning", "proxychains4 is not installed")
            return
        self.download_in_progress = True
        self.resume_btn.config(text="⏳ Resuming...", state=tk.DISABLED)
        self.progress_var.set("⏳ Resuming download...")
        thread = threading.Thread(target=self._download_file, args=(url, True))
        thread.daemon = True
        thread.start()
    
    def _download_file(self, url, resume):
        try:
            filename = os.path.basename(url.split('?')[0]) or "downloaded_file"
            output_path = os.path.join(os.path.expanduser("~/Downloads"), filename)
            self.add_log(f"📥 Downloading: {filename}", "info")
            
            if resume:
                cmd = ["proxychains4", "wget", "-c", "-t", "20", "-O", output_path, url]
                self.add_log("↩️ Resuming download", "info")
            else:
                cmd = ["proxychains4", "wget", "-c", "-t", "20", "-O", output_path, url]
                self.add_log("🆕 Starting new download", "info")
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, bufsize=1)
            for line in process.stdout:
                if "%" in line:
                    match = re.search(r'(\d+)%', line)
                    if match:
                        progress = match.group(1)
                        self.progress_var.set(f"⏳ Downloading... {progress}%")
                        self.add_log(f"📊 Progress: {progress}%", "info")
                if "error" in line.lower() or "failed" in line.lower():
                    self.add_log(f"⚠️ {line.strip()}", "warning")
            
            process.wait()
            if process.returncode == 0:
                self.add_log(f"✅ Download complete: {filename}", "success")
                self.progress_var.set(f"✅ Complete! Saved to: {output_path}")
                if os.path.exists(output_path):
                    size = os.path.getsize(output_path)
                    size_mb = size / (1024 * 1024)
                    self.add_log(f"📦 File size: {size_mb:.2f} MB", "success")
                messagebox.showinfo("Success", f"Download complete!\nSaved to: {output_path}")
            else:
                self.add_log(f"❌ Download failed with code: {process.returncode}", "error")
                self.progress_var.set("❌ Download failed. Check logs.")
                messagebox.showerror("Error", f"Download failed with code {process.returncode}")
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", "error")
            self.progress_var.set("❌ Error occurred")
            messagebox.showerror("Error", str(e))
        finally:
            self.download_in_progress = False
            self.download_btn.config(text="⬇️ Download", state=tk.NORMAL)
            self.resume_btn.config(text="⏸️ Resume", state=tk.NORMAL)
    
    def toggle_tor(self):
        if self.current_status == "OFF":
            self.enable_tor()
        else:
            self.disable_tor()
        self.update_status_indicator()
    
    def enable_tor(self):
        try:
            self.add_log("🔒 Connecting to Tor network...", "info")
            if not self.is_tor_running():
                self.add_log("🔄 Starting Tor service...", "info")
                subprocess.run(["sudo", "systemctl", "start", "tor"], capture_output=True, check=True)
                time.sleep(3)
            subprocess.run(["gsettings", "set", "org.gnome.system.proxy", "mode", "manual"])
            subprocess.run(["gsettings", "set", "org.gnome.system.proxy.http", "host", "127.0.0.1"])
            subprocess.run(["gsettings", "set", "org.gnome.system.proxy.http", "port", "8118"])
            subprocess.run(["gsettings", "set", "org.gnome.system.proxy.https", "host", "127.0.0.1"])
            subprocess.run(["gsettings", "set", "org.gnome.system.proxy.https", "port", "8118"])
            os.environ['http_proxy'] = 'http://127.0.0.1:8118'
            os.environ['https_proxy'] = 'http://127.0.0.1:8118'
            self.current_status = "ON"
            self.start_time = datetime.now()
            tor_ip = self.get_tor_ip()
            if tor_ip:
                self.add_log(f"✅ Connected to Tor! IP: {tor_ip}", "success")
                messagebox.showinfo("Success", f"Connected to Tor!\nYour Tor IP: {tor_ip}")
            else:
                self.add_log("⚠️ Connected but couldn't verify IP", "warning")
            self.toggle_btn.config(text="🔓 DISCONNECT FROM TOR", bg=self.colors['danger'], fg='black')
            self.status_label.config(text="CONNECTED", fg=self.colors['success'])
            self.reset_timer()
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to enable Tor: {str(e)}")
    
    def disable_tor(self):
        try:
            subprocess.run(["gsettings", "set", "org.gnome.system.proxy", "mode", "none"])
            os.environ.pop('http_proxy', None)
            os.environ.pop('https_proxy', None)
            self.current_status = "OFF"
            self.start_time = None
            self.add_log("🔓 Disconnected from Tor", "info")
            self.toggle_btn.config(text="🔒 CONNECT TO TOR", bg=self.colors['success'], fg='black')
            self.status_label.config(text="OFFLINE", fg=self.colors['danger'])
            self.tor_ip_label.config(text="Not connected")
            self.reset_timer()
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", "error")
    
    def is_tor_running(self):
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'tor':
                    return True
            return False
        except:
            return False
    
    def get_real_ip(self):
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            ip = response.text.strip()
            self.real_ip_label.config(text=ip)
            return ip
        except:
            self.real_ip_label.config(text="❌ Error")
            return None
    
    def get_tor_ip(self):
        try:
            proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}
            response = requests.get('https://api.ipify.org', proxies=proxies, timeout=10)
            ip = response.text.strip()
            self.tor_ip_label.config(text=ip, fg=self.colors['success'])
            return ip
        except:
            self.tor_ip_label.config(text="❌ Not connected", fg=self.colors['danger'])
            return None
    
    def refresh_ips(self):
        self.add_log("🔄 Refreshing IP addresses...", "info")
        self.get_real_ip()
        if self.current_status == "ON":
            self.get_tor_ip()
    
    def copy_ip(self, ip):
        if ip and ip not in ["Loading...", "Not connected", "❌ Error", "❌ Not connected"]:
            pyperclip.copy(ip)
            self.add_log(f"📋 Copied IP: {ip}", "info")
            messagebox.showinfo("Copied", f"IP copied to clipboard:\n{ip}")
    
    def copy_current_ip(self):
        if self.current_status == "ON":
            ip = self.tor_ip_label.cget("text")
            if ip and ip not in ["❌ Not connected", "Not connected"]:
                self.copy_ip(ip)
            else:
                messagebox.showwarning("Warning", "No Tor IP available")
        else:
            ip = self.real_ip_label.cget("text")
            if ip and ip != "❌ Error":
                self.copy_ip(ip)
            else:
                messagebox.showwarning("Warning", "No IP available")
    
    def new_identity(self):
        if self.current_status == "OFF":
            messagebox.showwarning("Warning", "Tor is not connected. Enable Tor first.")
            return
        self.add_log("🔄 Requesting new Tor identity...", "info")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 9051))
            s.send(b'AUTHENTICATE ""\n')
            time.sleep(0.1)
            s.send(b'SIGNAL NEWNYM\n')
            time.sleep(0.1)
            response = s.recv(1024)
            s.close()
            if b'250' in response:
                self.add_log("✅ New Tor identity established!", "success")
                time.sleep(2)
                ip = self.get_tor_ip()
                if ip:
                    messagebox.showinfo("New Identity", f"New Tor IP: {ip}")
                else:
                    messagebox.showinfo("New Identity", "New identity established!")
            else:
                self.add_log("⚠️ Failed to get new identity", "warning")
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", "error")
            messagebox.showwarning("Warning", "Could not change identity.\nMake sure Tor control port is enabled.")
    
    def update_status_indicator(self):
        if self.current_status == "ON":
            self.status_canvas.itemconfig(self.status_indicator, fill=self.colors['success'])
            self.status_label.config(text="CONNECTED", fg=self.colors['success'])
        else:
            self.status_canvas.itemconfig(self.status_indicator, fill=self.colors['danger'])
            self.status_label.config(text="OFFLINE", fg=self.colors['danger'])
    
    def check_tor_status(self):
        try:
            result = subprocess.run(["gsettings", "get", "org.gnome.system.proxy", "mode"],
                                  capture_output=True, text=True)
            if "'manual'" in result.stdout:
                self.current_status = "ON"
            else:
                self.current_status = "OFF"
            self.update_status_indicator()
        except:
            pass
    
    def start_timer(self):
        if self.timer_running:
            self.add_log("⏱️ Timer already running", "warning")
            return
        try:
            seconds = int(self.timer_var.get())
            if seconds <= 0:
                self.add_log("⚠️ Please enter a valid time", "warning")
                return
            if self.current_status == "OFF":
                self.add_log("⚠️ Tor is offline. Enable Tor first.", "warning")
                messagebox.showwarning("Warning", "Tor is offline. Enable Tor first.")
                return
            self.timer_seconds = seconds
            self.timer_running = True
            self.timer_btn.config(text="⏹️ Stop", bg=self.colors['danger'], fg='black')
            self.add_log(f"⏱️ Timer started: {seconds} seconds", "info")
            self.update_timer()
        except ValueError:
            self.add_log("⚠️ Please enter a valid number", "error")
    
    def update_timer(self):
        if self.timer_running and self.timer_seconds > 0:
            mins = self.timer_seconds // 60
            secs = self.timer_seconds % 60
            self.timer_display.config(text=f"{mins:02d}:{secs:02d}")
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running and self.timer_seconds == 0:
            self.timer_display.config(text="⏰ Time's up!")
            self.add_log("⏰ Timer expired - Disconnecting Tor", "warning")
            self.disable_tor()
            self.timer_running = False
            self.timer_btn.config(text="▶️ Start", bg=self.colors['warning'], fg='black')
            self.timer_display.config(text="")
            messagebox.showinfo("Timer", "Timer expired! Tor has been disconnected.")
    
    def set_preset_timer(self, seconds):
        self.timer_var.set(str(seconds))
        self.add_log(f"⏱️ Preset set: {seconds} seconds", "info")
        self.start_timer()
    
    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_display.config(text="")
        self.timer_btn.config(text="▶️ Start", bg=self.colors['warning'], fg='black')
    
    def add_log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", ('info'))
        self.log_text.insert(tk.END, f"{message}\n", (level))
        self.log_text.see(tk.END)
        self.connection_history.append({'timestamp': timestamp, 'message': message, 'level': level})
        self.log_count.config(text=f"{len(self.connection_history)} entries")
    
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
        self.connection_history = []
        self.add_log("🗑️ Logs cleared", "info")
    
    def export_logs(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.expanduser(f"~/tor_logs_{timestamp}.txt")
        try:
            with open(filename, 'w') as f:
                f.write(f"Tor Controller Pro Logs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                content = self.log_text.get(1.0, tk.END)
                f.write(content)
            self.add_log(f"💾 Logs exported to: {filename}", "success")
            messagebox.showinfo("Export Complete", f"Logs exported to:\n{filename}")
        except Exception as e:
            self.add_log(f"❌ Error exporting logs: {str(e)}", "error")
    
    def update_stats(self):
        try:
            if self.current_status == "ON" and self.start_time:
                uptime = datetime.now() - self.start_time
                hours = uptime.seconds // 3600
                minutes = (uptime.seconds % 3600) // 60
                seconds = uptime.seconds % 60
                self.uptime_label.config(text=f"⏱️ Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.get_real_ip()
            self.check_tor_status()
        except:
            pass
        self.root.after(5000, self.update_stats)
    
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("450x350")
        settings_window.configure(bg=self.colors['bg'])
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        tk.Label(settings_window, text="⚙️ Settings", 
                font=("Segoe UI", 18, "bold"),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(pady=20)
        
        auto_frame = tk.Frame(settings_window, bg=self.colors['bg'])
        auto_frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(auto_frame, text="Auto-Start Tor:", 
                font=("Segoe UI", 11),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(side=tk.LEFT)
        
        auto_var = tk.BooleanVar(value=self.config.get('auto_start', False))
        auto_check = tk.Checkbutton(auto_frame, variable=auto_var,
                                   bg=self.colors['bg'], fg=self.colors['fg'],
                                   selectcolor=self.colors['bg'],
                                   activebackground=self.colors['bg'])
        auto_check.pack(side=tk.LEFT, padx=10)
        
        def save_settings():
            self.config['auto_start'] = auto_var.get()
            self.save_config()
            self.add_log("⚙️ Settings saved", "info")
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings saved successfully!")
        
        btn_frame = tk.Frame(settings_window, bg=self.colors['bg'])
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="💾 Save Settings",
                 command=save_settings,
                 font=("Segoe UI", 11, "bold"),
                 bg=self.colors['accent'], fg='black',
                 relief=tk.FLAT, padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close",
                 command=settings_window.destroy,
                 font=("Segoe UI", 11),
                 bg=self.colors['bg3'], fg=self.colors['fg'],
                 relief=tk.FLAT, padx=30, pady=8).pack(side=tk.LEFT, padx=5)

def main():
    root = tk.Tk()
    app = TorControllerPro(root)
    
    def on_closing():
        if app.current_status == "ON":
            if messagebox.askyesno("Exit", "Tor is still connected. Disconnect before exiting?"):
                app.disable_tor()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
