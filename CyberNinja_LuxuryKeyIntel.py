"""
CyberNinja Luxury Key Intelligence v2
Professional BMW / Mercedes / Audi / VW Key Programming Reference
Now with KM100 Programming Steps for VW!
Matching CyberNinja Cluster ID aesthetic
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import json
import os
from pathlib import Path
from PIL import Image, ImageTk

# ==========================
# CyberNinja Theme Settings
# ==========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Custom colors - matching Cluster ID
CYBER_CYAN = "#00ffff"
CYBER_GREEN = "#00ff00"
CYBER_MAGENTA = "#ff00ff"
CYBER_DARK = "#0a0a0f"
CYBER_PANEL = "#12121a"
CYBER_ACCENT = "#00ffcc"
CYBER_RED = "#ff0066"
CYBER_YELLOW = "#ffcc00"
CYBER_ORANGE = "#ff9900"
CYBER_BLUE = "#0099ff"

# Risk colors
RISK_LOW = "#00ff00"
RISK_MEDIUM = "#ffcc00"
RISK_HIGH = "#ff6600"
RISK_VERY_HIGH = "#ff0066"


class LuxuryKeyIntel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔑 CyberNinja Luxury Key Intelligence v2 - KM100 Edition")
        self.geometry("1700x1000")
        self.minsize(1500, 900)
        self.configure(fg_color=CYBER_DARK)

        # Database & folders
        self.db_folder = "data"
        self.images_dir = "Key_Images"
        
        os.makedirs(self.db_folder, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        self.load_databases()
        self.current_image = None
        
        self.build_ui()

    # =======================
    # Database Handling
    # =======================
    def load_databases(self):
        """Load all brand JSON databases"""
        self.bmw_data = self.load_json("bmw.json")
        self.benz_data = self.load_json("benz.json")
        self.audi_data = self.load_json("audi.json")
        self.vw_data = self.load_json("vw.json")

    def load_json(self, filename):
        """Load a JSON file, return empty dict if not found"""
        path = os.path.join(self.db_folder, filename)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def get_models_for_make(self, make):
        """Get available models for a make"""
        if make == "BMW":
            return sorted(self.bmw_data.get("BMW", {}).keys())
        elif make == "Mercedes-Benz":
            return sorted(self.benz_data.get("Mercedes-Benz", {}).keys())
        elif make == "Audi":
            return sorted(self.audi_data.get("Audi", {}).keys())
        elif make == "Volkswagen":
            return sorted(self.vw_data.get("Volkswagen", {}).keys())
        return []

    def resolve_vehicle(self, make, model, year, key_status):
        """Resolve vehicle data from database"""
        if make == "BMW":
            brand_data = self.bmw_data.get("BMW", {})
        elif make == "Mercedes-Benz":
            brand_data = self.benz_data.get("Mercedes-Benz", {})
        elif make == "Audi":
            brand_data = self.audi_data.get("Audi", {})
        elif make == "Volkswagen":
            brand_data = self.vw_data.get("Volkswagen", {})
        else:
            return None

        model_data = brand_data.get(model)
        if not model_data:
            return None

        for year_range, info in model_data.items():
            try:
                start, end = map(int, year_range.split("-"))
                if start <= year <= end:
                    eeprom_info = info.get("eeprom_info", {})
                    xhorse_info = info.get("xhorse_tool_support", {})
                    km100_info = info.get("km100_support", {})
                    
                    # Key hardware info (MQB/MLB adapters, OEM keys, SFD)
                    key_hw = info.get("key_hardware", {})
                    oem_key = key_hw.get("oem_key_info", {})
                    sfd = key_hw.get("sfd_info", {})
                    adapters = key_hw.get("solder_free_adapters", {})
                    aftermarket = key_hw.get("aftermarket_key_options", {})
                    key_id_change = key_hw.get("key_id_change", {})
                    
                    return {
                        "platform": info.get("platform", "Unknown"),
                        "immobilizer": info.get("immobilizer", "Unknown"),
                        "key_type": info.get("key_type", "Unknown"),
                        "key_blade": info.get("key_blade", "Unknown"),
                        "chip": info.get("chip", "Unknown"),
                        "programming": info.get("programming", {}).get(key_status, "Unknown"),
                        "module_removal": "Yes" if info.get("module_removal", {}).get(key_status, False) else "No",
                        "akl_supported": info.get("akl_supported", "Unknown"),
                        "risk_level": info.get("risk_level", "Unknown"),
                        "eeprom_chip": eeprom_info.get("chip_type", "N/A"),
                        "backup_method": eeprom_info.get("backup_method", "Standard OBD backup"),
                        "backup_required": eeprom_info.get("backup_required", False),
                        "backup_warning": eeprom_info.get("warning", ""),
                        "notes": info.get("notes", "No additional notes"),
                        "year_range": year_range,
                        # Xhorse tool support
                        "mlb_tool": xhorse_info.get("mlb_tool", False),
                        "mqb_adapter": xhorse_info.get("mqb_adapter", False),
                        "xhorse_notes": xhorse_info.get("mlb_notes", xhorse_info.get("adapter_notes", xhorse_info.get("notes", ""))),
                        "xhorse_workflow": xhorse_info.get("workflow", ""),
                        "recommended_tool": xhorse_info.get("recommended_tool", ""),
                        # KM100 support
                        "km100_supported": km100_info.get("supported", False),
                        "km100_method": km100_info.get("method", ""),
                        "km100_steps": km100_info.get("steps", []),
                        "km100_chip": km100_info.get("chip_needed", ""),
                        "km100_time": km100_info.get("time_estimate", ""),
                        "km100_profit": km100_info.get("profit_estimate", ""),
                        # KEY HARDWARE - NEW!
                        "has_key_hardware": bool(key_hw),
                        "key_style": key_hw.get("key_style", ""),
                        "oem_part_numbers": oem_key.get("part_numbers", []),
                        "oem_fcc_id": oem_key.get("fcc_id", ""),
                        "oem_frequency": oem_key.get("frequency", ""),
                        "oem_keyless_go": oem_key.get("keyless_go", False),
                        "oem_battery": oem_key.get("battery", ""),
                        "oem_buttons": oem_key.get("buttons", ""),
                        "oem_key_check": oem_key.get("key_check", ""),
                        "oem_inductor": oem_key.get("inductor_variants", {}),
                        "oem_manufacturer": oem_key.get("manufacturer", ""),
                        "oem_board_number": oem_key.get("board_number", ""),
                        "adapter_xhorse": adapters.get("xhorse", adapters.get("xhorse_white", {})),
                        "adapter_xhorse_black": adapters.get("xhorse_black", {}),
                        "adapter_keydiy": adapters.get("keydiy", adapters.get("keydiy_white", {})),
                        "adapter_keydiy_black": adapters.get("keydiy_black", {}),
                        "adapter_alger": adapters.get("alger_keys", adapters.get("alger_keys_white", {})),
                        "adapter_alger_black": adapters.get("alger_keys_black", {}),
                        "adapter_warning": adapters.get("warning", ""),
                        "aftermarket_xhorse": aftermarket.get("xhorse", ""),
                        "aftermarket_keydiy": aftermarket.get("keydiy", ""),
                        "aftermarket_oem_refurb": aftermarket.get("oem_refurb", ""),
                        "sfd_required": sfd.get("sfd_required", ""),
                        "sfd2_required": sfd.get("sfd2_required", ""),
                        "sfd_unlock_methods": sfd.get("unlock_methods", []),
                        "tools_for_key_read": key_hw.get("tools_for_key_read", []),
                        "key_id_change_required": key_id_change.get("required_from", ""),
                        "key_id_change_reason": key_id_change.get("reason", ""),
                        "key_id_change_how": key_id_change.get("how", "")
                    }
            except:
                continue
        return None

    # =======================
    # VIN Tools
    # =======================
    def validate_vin(self, vin):
        """Validate VIN and extract info"""
        if not vin:
            return {"valid": False, "message": ""}
        
        vin = vin.upper().strip()
        
        if len(vin) != 17:
            return {"valid": False, "message": f"Need 17 chars (got {len(vin)})"}
        
        invalid = [c for c in vin if c in "IOQ"]
        if invalid:
            return {"valid": False, "message": f"Invalid: {', '.join(invalid)}"}
        
        if not vin.isalnum():
            return {"valid": False, "message": "Must be alphanumeric"}
        
        # WMI decode - added VW
        wmi = vin[:3]
        wmi_map = {
            "WBA": "BMW (Germany)", "WBS": "BMW M", "WBY": "BMW i",
            "4US": "BMW (USA)", "5UX": "BMW X (USA)", "5YM": "BMW M (USA)",
            "WDB": "Mercedes-Benz", "WDC": "Mercedes SUV", "WDD": "Mercedes",
            "4JG": "Mercedes (USA)", "55S": "AMG",
            "WAU": "Audi", "WUA": "Audi Quattro", "TRU": "Audi (Hungary)",
            # VW WMI codes
            "WVW": "Volkswagen (Germany)", "WVG": "VW SUV (Germany)",
            "3VW": "VW (Mexico)", "1VW": "VW (USA)",
            "9BW": "VW (Brazil)", "AAV": "VW (Argentina)"
        }
        manufacturer = wmi_map.get(wmi, "Unknown")
        
        # Year decode
        year_codes = {
            "A": 2010, "B": 2011, "C": 2012, "D": 2013, "E": 2014,
            "F": 2015, "G": 2016, "H": 2017, "J": 2018, "K": 2019,
            "L": 2020, "M": 2021, "N": 2022, "P": 2023, "R": 2024,
            "S": 2025, "T": 2026
        }
        year = year_codes.get(vin[9], None)
        
        # Detect make
        make = None
        if wmi in ["WBA", "WBS", "WBY", "4US", "5UX", "5YM"]:
            make = "BMW"
        elif wmi in ["WDB", "WDC", "WDD", "4JG", "55S"]:
            make = "Mercedes-Benz"
        elif wmi in ["WAU", "WUA", "TRU"]:
            make = "Audi"
        elif wmi in ["WVW", "WVG", "3VW", "1VW", "9BW", "AAV"]:
            make = "Volkswagen"
        
        return {
            "valid": True,
            "message": f"✓ {manufacturer}",
            "manufacturer": manufacturer,
            "year": year,
            "make": make
        }

    # =======================
    # UI Building
    # =======================
    def build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=CYBER_PANEL, height=80, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(expand=True)

        ctk.CTkLabel(
            title_frame,
            text="🔑 CYBERNINJA LUXURY KEY INTELLIGENCE v2",
            font=("Consolas", 26, "bold"),
            text_color=CYBER_CYAN
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            title_frame,
            text="BMW • MERCEDES • AUDI • VW + KM100",
            font=("Consolas", 14),
            text_color=CYBER_MAGENTA
        ).pack(side="left", padx=20)

        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== LEFT PANEL - Vehicle Input =====
        left_panel = ctk.CTkFrame(main_container, fg_color=CYBER_PANEL, width=300, corner_radius=15)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        # Input section title
        ctk.CTkLabel(
            left_panel,
            text="🚗 VEHICLE INPUT",
            font=("Consolas", 16, "bold"),
            text_color=CYBER_CYAN
        ).pack(pady=(20, 5))

        # Separator
        sep1 = ctk.CTkFrame(left_panel, fg_color=CYBER_CYAN, height=2)
        sep1.pack(fill="x", padx=20, pady=10)

        # Make
        ctk.CTkLabel(left_panel, text="Make:", font=("Consolas", 12, "bold"),
                     text_color=CYBER_ACCENT).pack(anchor="w", padx=25, pady=(15, 5))
        self.make_var = ctk.StringVar(value="Select Make")
        self.make_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.make_var,
            values=["Select Make", "BMW", "Mercedes-Benz", "Audi", "Volkswagen"],
            width=250,
            height=40,
            font=("Consolas", 12),
            fg_color="#1a1a2e",
            button_color=CYBER_MAGENTA,
            button_hover_color=CYBER_CYAN,
            dropdown_fg_color=CYBER_PANEL,
            command=self.on_make_changed
        )
        self.make_menu.pack(padx=25)

        # Model
        ctk.CTkLabel(left_panel, text="Model:", font=("Consolas", 12, "bold"),
                     text_color=CYBER_ACCENT).pack(anchor="w", padx=25, pady=(15, 5))
        self.model_var = ctk.StringVar(value="Select Model")
        self.model_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.model_var,
            values=["Select Model"],
            width=250,
            height=40,
            font=("Consolas", 12),
            fg_color="#1a1a2e",
            button_color=CYBER_MAGENTA,
            button_hover_color=CYBER_CYAN,
            dropdown_fg_color=CYBER_PANEL,
            command=self.on_selection_changed
        )
        self.model_menu.pack(padx=25)

        # Year
        ctk.CTkLabel(left_panel, text="Year:", font=("Consolas", 12, "bold"),
                     text_color=CYBER_ACCENT).pack(anchor="w", padx=25, pady=(15, 5))
        self.year_var = ctk.StringVar(value="Select Year")
        years = ["Select Year"] + [str(y) for y in range(2026, 1998, -1)]
        self.year_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.year_var,
            values=years,
            width=250,
            height=40,
            font=("Consolas", 12),
            fg_color="#1a1a2e",
            button_color=CYBER_MAGENTA,
            button_hover_color=CYBER_CYAN,
            dropdown_fg_color=CYBER_PANEL,
            command=self.on_selection_changed
        )
        self.year_menu.pack(padx=25)

        # VIN
        ctk.CTkLabel(left_panel, text="VIN (Optional):", font=("Consolas", 12, "bold"),
                     text_color=CYBER_ACCENT).pack(anchor="w", padx=25, pady=(15, 5))
        self.vin_entry = ctk.CTkEntry(
            left_panel,
            width=250,
            height=40,
            font=("Consolas", 12),
            placeholder_text="17-character VIN",
            fg_color="#1a1a2e",
            border_color=CYBER_CYAN
        )
        self.vin_entry.pack(padx=25)
        self.vin_entry.bind("<KeyRelease>", self.on_vin_changed)

        # VIN Status
        self.vin_status_label = ctk.CTkLabel(
            left_panel,
            text="",
            font=("Consolas", 10),
            text_color=CYBER_ACCENT
        )
        self.vin_status_label.pack(anchor="w", padx=25, pady=(5, 0))

        # Key Status
        ctk.CTkLabel(left_panel, text="Customer Key Status:", font=("Consolas", 12, "bold"),
                     text_color=CYBER_ACCENT).pack(anchor="w", padx=25, pady=(15, 5))
        self.key_status_var = ctk.StringVar(value="Has Working Key")
        self.key_status_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.key_status_var,
            values=["Has Working Key", "Only 1 Key", "AKL (All Keys Lost)"],
            width=250,
            height=40,
            font=("Consolas", 11),
            fg_color="#1a1a2e",
            button_color=CYBER_ORANGE,
            button_hover_color=CYBER_YELLOW,
            dropdown_fg_color=CYBER_PANEL,
            command=self.on_selection_changed
        )
        self.key_status_menu.pack(padx=25)

        # Separator
        sep2 = ctk.CTkFrame(left_panel, fg_color=CYBER_MAGENTA, height=2)
        sep2.pack(fill="x", padx=20, pady=25)

        # Quick Stats
        self.stats_frame = ctk.CTkFrame(left_panel, fg_color="#1a1a2e", corner_radius=10)
        self.stats_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.stats_frame, text="📊 DATABASE STATS",
                     font=("Consolas", 11, "bold"), text_color=CYBER_CYAN).pack(pady=10)

        bmw_count = len(self.bmw_data.get("BMW", {}))
        audi_count = len(self.audi_data.get("Audi", {}))
        vw_count = len(self.vw_data.get("Volkswagen", {}))
        benz_count = len(self.benz_data.get("Mercedes-Benz", {}))
        
        self.stat_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"BMW: {bmw_count} | Audi: {audi_count}\nVW: {vw_count} (KM100!) | Benz: {benz_count if benz_count > 0 else 'Soon'}",
            font=("Consolas", 10),
            text_color=CYBER_ACCENT,
            justify="left"
        )
        self.stat_label.pack(pady=(0, 10))

        # Credits at bottom
        ctk.CTkLabel(
            left_panel,
            text="CyberNinja © 2026\n🔑 6ix Keys - Toronto",
            font=("Consolas", 10),
            text_color="#666"
        ).pack(side="bottom", pady=15)

        # ===== CENTER PANEL - Results =====
        center_panel = ctk.CTkFrame(main_container, fg_color=CYBER_PANEL, corner_radius=15)
        center_panel.pack(side="left", fill="both", expand=True, padx=5)

        # Results title
        ctk.CTkLabel(
            center_panel,
            text="🔐 VEHICLE SECURITY OVERVIEW",
            font=("Consolas", 16, "bold"),
            text_color=CYBER_CYAN
        ).pack(pady=(20, 5))

        sep3 = ctk.CTkFrame(center_panel, fg_color=CYBER_CYAN, height=2)
        sep3.pack(fill="x", padx=20, pady=10)

        # Scrollable results
        self.results_scroll = ctk.CTkScrollableFrame(
            center_panel,
            fg_color="transparent",
            scrollbar_button_color=CYBER_MAGENTA,
            scrollbar_button_hover_color=CYBER_CYAN
        )
        self.results_scroll.pack(fill="both", expand=True, padx=15, pady=10)

        # Result fields
        self.result_labels = {}
        fields = [
            ("Platform / Chassis", "platform", CYBER_CYAN),
            ("Immobilizer System", "immobilizer", CYBER_MAGENTA),
            ("Key Type", "key_type", CYBER_ACCENT),
            ("Key Blade", "blade", CYBER_YELLOW),
            ("Chip Required", "chip", CYBER_ORANGE),
            ("Programming Method", "programming", CYBER_ORANGE),
            ("Module Removal", "module", CYBER_RED),
            ("AKL Supported", "akl", CYBER_GREEN),
            ("Risk Level", "risk", CYBER_RED),
            ("EEPROM Chip", "eeprom_chip", CYBER_YELLOW),
            ("Backup Method", "backup_method", CYBER_ORANGE),
            ("⚠️ BACKUP WARNING", "backup_warning", CYBER_RED),
            ("🔧 RECOMMENDED TOOL", "recommended_tool", CYBER_BLUE),
            ("Notes", "notes", CYBER_ACCENT)
        ]

        for display_name, key, color in fields:
            card = ctk.CTkFrame(self.results_scroll, fg_color="#1a1a2e", corner_radius=10)
            card.pack(fill="x", pady=4, padx=5)

            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(8, 0))

            ctk.CTkLabel(
                header_frame,
                text=display_name,
                font=("Consolas", 11, "bold"),
                text_color=color
            ).pack(side="left")

            value_label = ctk.CTkLabel(
                card,
                text="—",
                font=("Consolas", 12),
                text_color="#e6e6e6",
                wraplength=380,
                justify="left"
            )
            value_label.pack(anchor="w", padx=15, pady=(3, 10))
            self.result_labels[display_name] = value_label

        # ===== RIGHT PANEL - KM100 Steps + Image =====
        right_panel = ctk.CTkFrame(main_container, fg_color=CYBER_PANEL, width=380, corner_radius=15)
        right_panel.pack(side="right", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)

        # ===== KM100 STEPS + KEY HARDWARE SECTION =====
        ctk.CTkLabel(
            right_panel,
            text="📋 KM100 STEPS + KEY HARDWARE",
            font=("Consolas", 14, "bold"),
            text_color=CYBER_GREEN
        ).pack(pady=(15, 5))

        sep_km = ctk.CTkFrame(right_panel, fg_color=CYBER_GREEN, height=2)
        sep_km.pack(fill="x", padx=20, pady=5)

        # KM100 Status indicator
        self.km100_status_frame = ctk.CTkFrame(right_panel, fg_color="#1a1a2e", corner_radius=8)
        self.km100_status_frame.pack(fill="x", padx=15, pady=5)
        
        self.km100_status_label = ctk.CTkLabel(
            self.km100_status_frame,
            text="Select a vehicle to see KM100 steps",
            font=("Consolas", 11),
            text_color="#666"
        )
        self.km100_status_label.pack(pady=8)

        # KM100 Steps scrollable frame
        self.km100_scroll = ctk.CTkScrollableFrame(
            right_panel,
            fg_color="#0a0a15",
            height=280,
            corner_radius=10,
            scrollbar_button_color=CYBER_GREEN,
            scrollbar_button_hover_color=CYBER_CYAN
        )
        self.km100_scroll.pack(fill="x", padx=15, pady=5)

        self.km100_steps_label = ctk.CTkLabel(
            self.km100_scroll,
            text="",
            font=("Consolas", 11),
            text_color=CYBER_ACCENT,
            justify="left",
            wraplength=330
        )
        self.km100_steps_label.pack(anchor="w", padx=10, pady=10)

        # KM100 Quick Info
        self.km100_info_frame = ctk.CTkFrame(right_panel, fg_color="#1a1a2e", corner_radius=8)
        self.km100_info_frame.pack(fill="x", padx=15, pady=5)

        self.km100_info_label = ctk.CTkLabel(
            self.km100_info_frame,
            text="Chip: —\nTime: —\nProfit: —",
            font=("Consolas", 10),
            text_color=CYBER_YELLOW,
            justify="left"
        )
        self.km100_info_label.pack(anchor="w", padx=10, pady=8)

        # Separator
        sep_mid = ctk.CTkFrame(right_panel, fg_color=CYBER_MAGENTA, height=2)
        sep_mid.pack(fill="x", padx=20, pady=10)

        # ===== IMAGE SECTION =====
        ctk.CTkLabel(
            right_panel,
            text="📷 REFERENCE",
            font=("Consolas", 12, "bold"),
            text_color=CYBER_CYAN
        ).pack(pady=(5, 5))

        # Image frame (smaller)
        self.image_frame = ctk.CTkFrame(right_panel, fg_color="#0a0a15", corner_radius=10,
                                         width=200, height=120)
        self.image_frame.pack(pady=5, padx=20)
        self.image_frame.pack_propagate(False)

        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="No Image",
            font=("Consolas", 10),
            text_color="#666",
            cursor="hand2"
        )
        self.image_label.pack(expand=True)
        self.image_label.bind("<Double-Button-1>", self.open_full_image)
        self.current_image_path = None

        # Image type selector
        self.image_type_var = ctk.StringVar(value="Module")
        img_type_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        img_type_frame.pack()

        ctk.CTkRadioButton(
            img_type_frame,
            text="Module",
            variable=self.image_type_var,
            value="Module",
            font=("Consolas", 9),
            fg_color=CYBER_MAGENTA,
            hover_color=CYBER_CYAN
        ).pack(side="left", padx=5)

        ctk.CTkRadioButton(
            img_type_frame,
            text="Key",
            variable=self.image_type_var,
            value="Key",
            font=("Consolas", 9),
            fg_color=CYBER_MAGENTA,
            hover_color=CYBER_CYAN
        ).pack(side="left", padx=5)

        # Add image button
        ctk.CTkButton(
            right_panel,
            text="📁 Add Image",
            width=150,
            height=28,
            font=("Consolas", 10, "bold"),
            fg_color=CYBER_MAGENTA,
            hover_color=CYBER_CYAN,
            command=self.add_custom_image
        ).pack(pady=8)

        # Risk indicator at bottom
        self.risk_indicator = ctk.CTkFrame(right_panel, fg_color="#1a1a2e", corner_radius=10)
        self.risk_indicator.pack(fill="x", padx=15, pady=(5, 15))

        ctk.CTkLabel(
            self.risk_indicator,
            text="⚠️ JOB RISK",
            font=("Consolas", 10, "bold"),
            text_color=CYBER_RED
        ).pack(pady=(8, 3))

        self.risk_bar = ctk.CTkProgressBar(
            self.risk_indicator,
            width=180,
            height=12,
            progress_color=CYBER_GREEN,
            fg_color="#333"
        )
        self.risk_bar.pack(pady=3)
        self.risk_bar.set(0)

        self.risk_text = ctk.CTkLabel(
            self.risk_indicator,
            text="—",
            font=("Consolas", 11, "bold"),
            text_color=CYBER_GREEN
        )
        self.risk_text.pack(pady=(3, 8))

    # =======================
    # Event Handlers
    # =======================
    def on_make_changed(self, make):
        """Update model list when make changes"""
        models = self.get_models_for_make(make)
        if models:
            self.model_menu.configure(values=["Select Model"] + models)
        else:
            self.model_menu.configure(values=["Select Model", "No data available"])
        self.model_var.set("Select Model")
        self.clear_results()

    def on_selection_changed(self, *args):
        """Update results when any selection changes"""
        self.update_results()

    def on_vin_changed(self, event=None):
        """Handle VIN input changes"""
        vin = self.vin_entry.get()
        result = self.validate_vin(vin)
        
        if not vin:
            self.vin_status_label.configure(text="", text_color=CYBER_ACCENT)
            return
        
        if result.get("valid"):
            self.vin_status_label.configure(
                text=result.get("message", ""),
                text_color=CYBER_GREEN
            )
            # Auto-fill make and year if detected
            if result.get("make"):
                self.make_var.set(result["make"])
                self.on_make_changed(result["make"])
            if result.get("year"):
                self.year_var.set(str(result["year"]))
        else:
            self.vin_status_label.configure(
                text=result.get("message", "Invalid VIN"),
                text_color=CYBER_RED
            )

    def clear_results(self):
        """Clear all result fields"""
        for label in self.result_labels.values():
            label.configure(text="—", text_color="#e6e6e6")
        
        self.risk_bar.set(0)
        self.risk_text.configure(text="—", text_color=CYBER_GREEN)
        
        # Clear KM100 section
        self.km100_status_label.configure(
            text="Select a vehicle to see KM100 steps",
            text_color="#666"
        )
        self.km100_steps_label.configure(text="")
        self.km100_info_label.configure(text="Chip: —\nTime: —\nProfit: —")
        
        self.image_label.configure(text="No Image", image=None)

    def update_results(self):
        """Update results based on current selections"""
        make = self.make_var.get()
        model = self.model_var.get()
        year_str = self.year_var.get()
        key_status_display = self.key_status_var.get()

        if "Select" in make or "Select" in model or "Select" in year_str:
            return

        # Map key status display to database key
        key_status_map = {
            "Has Working Key": "has_key",
            "Only 1 Key": "one_key",
            "AKL (All Keys Lost)": "akl"
        }
        key_status = key_status_map.get(key_status_display, "has_key")

        try:
            year = int(year_str)
        except:
            return

        result = self.resolve_vehicle(make, model, year, key_status)
        
        if not result:
            self.clear_results()
            return

        # Update result labels
        field_map = {
            "Platform / Chassis": "platform",
            "Immobilizer System": "immobilizer",
            "Key Type": "key_type",
            "Key Blade": "key_blade",
            "Chip Required": "chip",
            "Programming Method": "programming",
            "Module Removal": "module_removal",
            "AKL Supported": "akl_supported",
            "Risk Level": "risk_level",
            "EEPROM Chip": "eeprom_chip",
            "Backup Method": "backup_method",
            "⚠️ BACKUP WARNING": "backup_warning",
            "🔧 RECOMMENDED TOOL": "recommended_tool",
            "Notes": "notes"
        }

        for display_name, key in field_map.items():
            value = result.get(key, "—")
            if not value:
                value = "—"
            label = self.result_labels.get(display_name)
            if label:
                label.configure(text=value)

                # Color coding
                if display_name == "Risk Level":
                    if "Low" in str(value):
                        label.configure(text_color=RISK_LOW)
                        self.update_risk_bar(0.25, "LOW", RISK_LOW)
                    elif "Medium" in str(value):
                        label.configure(text_color=RISK_MEDIUM)
                        self.update_risk_bar(0.5, "MEDIUM", RISK_MEDIUM)
                    elif "Very High" in str(value):
                        label.configure(text_color=RISK_VERY_HIGH)
                        self.update_risk_bar(1.0, "VERY HIGH", RISK_VERY_HIGH)
                    elif "High" in str(value):
                        label.configure(text_color=RISK_HIGH)
                        self.update_risk_bar(0.75, "HIGH", RISK_HIGH)

                elif display_name == "Module Removal":
                    if value == "Yes":
                        label.configure(text_color=CYBER_YELLOW)
                    else:
                        label.configure(text_color=CYBER_GREEN)

                elif display_name == "AKL Supported":
                    if value == "Yes":
                        label.configure(text_color=CYBER_GREEN)
                    elif "Limited" in str(value) or "Very" in str(value) or "Copy" in str(value):
                        label.configure(text_color=CYBER_YELLOW)
                    elif value == "No" or "dealer" in str(value).lower():
                        label.configure(text_color=CYBER_RED)

                elif display_name == "⚠️ BACKUP WARNING":
                    if value and "CRITICAL" in str(value):
                        label.configure(text_color=CYBER_RED)
                    elif value and "EXTREME" in str(value):
                        label.configure(text_color=CYBER_RED)
                    elif value and ("IMPORTANT" in str(value) or "⚠️" in str(value)):
                        label.configure(text_color=CYBER_ORANGE)
                    elif value and value != "—":
                        label.configure(text_color=CYBER_YELLOW)
                    else:
                        label.configure(text_color=CYBER_GREEN)

        # ===== UPDATE KM100 SECTION =====
        self.update_km100_section(result, make)

        # Try to load reference image
        self.load_reference_image(make, model, result.get("year_range", ""))

    def update_km100_section(self, result, make):
        """Update the KM100 programming steps section AND key hardware info"""
        km100_supported = result.get("km100_supported", False)
        km100_method = result.get("km100_method", "")
        km100_steps = result.get("km100_steps", [])
        km100_chip = result.get("km100_chip", "")
        km100_time = result.get("km100_time", "")
        km100_profit = result.get("km100_profit", "")
        has_key_hw = result.get("has_key_hardware", False)
        
        # Show KM100 for VW and Audi, show key hardware for all brands
        if make not in ("Volkswagen", "Audi", "BMW", "Mercedes-Benz"):
            self.km100_status_label.configure(
                text="Select a supported vehicle",
                text_color="#666"
            )
            self.km100_steps_label.configure(text="")
            self.km100_info_label.configure(text="Chip: —\nTime: —\nProfit: —")
            return
        
        # BMW and Mercedes don't use KM100 — skip KM100 steps but still show key hardware
        if make in ("BMW", "Mercedes-Benz"):
            self.km100_status_label.configure(
                text="❌ KM100 NOT SUPPORTED for BMW",
                text_color=CYBER_RED
            ) if make == "BMW" else self.km100_status_label.configure(
                text="❌ KM100 NOT SUPPORTED for Mercedes",
                text_color=CYBER_RED
            )
            self.km100_info_label.configure(
                text=f"🔹 Use Xhorse KTP, CGDI, or Autel tools",
                text_color=CYBER_ORANGE
            )
            steps_text = ""
            # Skip KM100 steps, jump straight to key hardware below
        else:
            # Build display text for VW/Audi KM100 steps
            steps_text = ""
            
            # Check if KM100 is supported
            if km100_supported == True or km100_supported == "Partial" or km100_supported == "Copy Only":
                if km100_supported == True:
                    status_text = "✅ KM100 SUPPORTED - EASY OBD!"
                    status_color = CYBER_GREEN
                elif km100_supported == "Partial":
                    status_text = "🟡 KM100 PARTIAL - May need BOOT"
                    status_color = CYBER_YELLOW
                elif km100_supported == "Copy Only":
                    status_text = "🟡 KM100 COPY ONLY"
                    status_color = CYBER_YELLOW
                
                self.km100_status_label.configure(text=status_text, text_color=status_color)
                
                steps_text += f"📌 METHOD: {km100_method}\n\n"
                if km100_steps:
                    for step in km100_steps:
                        if step.strip():
                            steps_text += f"{step}\n"
                
                self.km100_info_label.configure(
                    text=f"🔹 Chip: {km100_chip}\n🔹 Time: {km100_time}\n🔹 Profit: {km100_profit}",
                    text_color=CYBER_YELLOW
                )
            else:
                self.km100_status_label.configure(
                    text="❌ KM100 NOT SUPPORTED",
                    text_color=CYBER_RED
                )
                
                steps_text += "📌 METHOD: NOT SUPPORTED\n\n"
                if km100_steps:
                    for step in km100_steps:
                        if step.strip():
                            steps_text += f"• {step}\n"
                else:
                    steps_text += "• Use Xhorse MLB Tool + MQB Adapter\n• Or Key Tool Plus with MQB48\n• Or refer to partner"
                
                self.km100_info_label.configure(
                    text=f"🔹 Chip: {km100_chip if km100_chip else 'MQB48'}\n🔹 Action: Refer out or use Xhorse tools",
                    text_color=CYBER_ORANGE
                )
        
        # ===== KEY HARDWARE SECTION =====
        if has_key_hw:
            steps_text += "\n\n" + "═" * 40
            steps_text += f"\n🔑 KEY HARDWARE INFO\n"
            steps_text += "═" * 40 + "\n\n"
            
            key_style = result.get("key_style", "")
            if key_style:
                steps_text += f"📋 Style: {key_style}\n"
            
            # OEM Part Numbers
            part_nums = result.get("oem_part_numbers", [])
            if part_nums:
                steps_text += f"\n📦 OEM PART NUMBERS:\n"
                for pn in part_nums:
                    steps_text += f"  • {pn}\n"
            
            # FCC ID & Frequency
            fcc = result.get("oem_fcc_id", "")
            freq = result.get("oem_frequency", "")
            if fcc:
                steps_text += f"\n📡 FCC ID: {fcc}"
            if freq:
                steps_text += f"\n📡 Frequency: {freq}"
            
            # Keyless Go
            keyless = result.get("oem_keyless_go", False)
            steps_text += f"\n🔓 Keyless Go: {'YES' if keyless else 'NO'}"
            
            # Battery
            batt = result.get("oem_battery", "")
            if batt:
                steps_text += f"\n🔋 Battery: {batt}"
            
            # Buttons
            buttons = result.get("oem_buttons", "")
            if buttons:
                steps_text += f"\n🔘 Buttons: {buttons}"
            
            # Key Check (visual identification)
            key_check = result.get("oem_key_check", "")
            if key_check:
                steps_text += f"\n\n👁️ KEY CHECK: {key_check}"
            
            # Inductor variants (Golf 8)
            inductor = result.get("oem_inductor", {})
            if inductor:
                steps_text += f"\n\n⚠️ INDUCTOR COLOR CHECK:"
                for k, v in inductor.items():
                    steps_text += f"\n  • {v}"
            
            # Manufacturer / Board
            mfr = result.get("oem_manufacturer", "")
            board = result.get("oem_board_number", "")
            if mfr:
                steps_text += f"\n\n🏭 Manufacturer: {mfr}"
            if board:
                steps_text += f"\n📋 Board #: {board}"
            
            # Solder-Free Adapters
            steps_text += f"\n\n" + "─" * 35
            steps_text += f"\n🔧 SOLDER-FREE ADAPTERS:\n"
            
            adapter_x = result.get("adapter_xhorse", {})
            adapter_xb = result.get("adapter_xhorse_black", {})
            adapter_k = result.get("adapter_keydiy", {})
            adapter_kb = result.get("adapter_keydiy_black", {})
            adapter_a = result.get("adapter_alger", {})
            adapter_ab = result.get("adapter_alger_black", {})
            adapter_warn = result.get("adapter_warning", "")
            
            if isinstance(adapter_x, dict) and adapter_x:
                model = adapter_x.get("model", adapter_x.get("bundle", ""))
                fits = adapter_x.get("fits", "")
                steps_text += f"\n  Xhorse: {model}"
                if fits:
                    steps_text += f" ({fits})"
            
            if isinstance(adapter_xb, dict) and adapter_xb:
                model = adapter_xb.get("model", "")
                fits = adapter_xb.get("fits", "")
                steps_text += f"\n  Xhorse (Black): {model}"
                if fits:
                    steps_text += f" ({fits})"
            
            if isinstance(adapter_k, dict) and adapter_k:
                model = adapter_k.get("model", "")
                steps_text += f"\n  KeyDIY: {model}"
            
            if isinstance(adapter_a, dict) and adapter_a:
                bundle = adapter_a.get("bundle", "")
                if bundle:
                    steps_text += f"\n  Alger Keys: {bundle}"
            
            if adapter_warn:
                steps_text += f"\n\n  ⚠️ {adapter_warn}"
            
            # Aftermarket Key Options
            steps_text += f"\n\n" + "─" * 35
            steps_text += f"\n🔑 AFTERMARKET KEY OPTIONS:\n"
            
            am_xhorse = result.get("aftermarket_xhorse", "")
            am_keydiy = result.get("aftermarket_keydiy", "")
            am_oem = result.get("aftermarket_oem_refurb", "")
            
            if am_xhorse:
                if isinstance(am_xhorse, str):
                    steps_text += f"\n  Xhorse: {am_xhorse}"
            if am_keydiy:
                if isinstance(am_keydiy, dict):
                    for k, v in am_keydiy.items():
                        steps_text += f"\n  KeyDIY {k}: {v}"
                else:
                    steps_text += f"\n  KeyDIY: {am_keydiy}"
            if am_oem:
                steps_text += f"\n  OEM Refurb: {am_oem}"
            
            # SFD Info
            sfd_req = result.get("sfd_required", "")
            sfd2_req = result.get("sfd2_required", "")
            sfd_methods = result.get("sfd_unlock_methods", [])
            
            if sfd_req or sfd2_req:
                steps_text += f"\n\n" + "─" * 35
                steps_text += f"\n🔐 SFD GATEWAY INFO:\n"
                if sfd_req:
                    steps_text += f"\n  SFD1: {sfd_req}"
                if sfd2_req:
                    steps_text += f"\n  SFD2: {sfd2_req}"
                if sfd_methods:
                    steps_text += f"\n\n  Unlock Methods:"
                    for m in sfd_methods:
                        steps_text += f"\n    • {m}"
            
            # Tools for key read
            tools = result.get("tools_for_key_read", [])
            if tools:
                steps_text += f"\n\n" + "─" * 35
                steps_text += f"\n🛠️ TOOLS FOR KEY READ:\n"
                for t in tools:
                    steps_text += f"\n  • {t}"
            
            # Key ID Change
            kid_req = result.get("key_id_change_required", "")
            if kid_req:
                steps_text += f"\n\n" + "─" * 35
                steps_text += f"\n🆔 KEY ID CHANGE:\n"
                steps_text += f"\n  Required from: {kid_req}"
                kid_reason = result.get("key_id_change_reason", "")
                kid_how = result.get("key_id_change_how", "")
                if kid_reason:
                    steps_text += f"\n  Why: {kid_reason}"
                if kid_how:
                    steps_text += f"\n  How: {kid_how}"
        
        self.km100_steps_label.configure(text=steps_text)

    def update_risk_bar(self, value, text, color):
        """Update the risk indicator"""
        self.risk_bar.set(value)
        self.risk_bar.configure(progress_color=color)
        self.risk_text.configure(text=text, text_color=color)

    def load_reference_image(self, make, model, year_range):
        """Try to load a reference image for the vehicle"""
        img_key = f"{make}_{model}_{year_range}".replace(" ", "_").replace("/", "-")
        img_type = self.image_type_var.get().lower()
        
        # Check for existing image
        for ext in [".jpg", ".jpeg", ".png", ".gif"]:
            img_path = os.path.join(self.images_dir, f"{img_key}_{img_type}{ext}")
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img.thumbnail((180, 100))
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 100))
                    self.image_label.configure(image=photo, text="")
                    self.current_image = photo
                    self.current_image_path = img_path
                    return
                except:
                    pass
        
        # No image found
        self.image_label.configure(text="No image", image=None)
        self.current_image_path = None

    def open_full_image(self, event=None):
        """Open the current reference image in a full-size popup window"""
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            return
        
        try:
            img = Image.open(self.current_image_path)
            
            # Get screen size and scale image to fit
            screen_w = self.winfo_screenwidth() - 100
            screen_h = self.winfo_screenheight() - 150
            
            # Scale to fit screen while maintaining aspect ratio
            img_w, img_h = img.size
            scale = min(screen_w / img_w, screen_h / img_h, 1.0)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            
            if scale < 1.0:
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Create popup window
            popup = ctk.CTkToplevel(self)
            popup.title(f"🔑 Key Reference — {os.path.basename(self.current_image_path)}")
            popup.geometry(f"{new_w + 40}x{new_h + 80}")
            popup.configure(fg_color=CYBER_DARK)
            popup.attributes("-topmost", True)
            popup.focus_force()
            
            # Title bar
            title_text = os.path.basename(self.current_image_path).replace("_", " ").replace(".png", "").replace(".jpg", "")
            ctk.CTkLabel(
                popup,
                text=f"📷 {title_text}",
                font=("Consolas", 14, "bold"),
                text_color=CYBER_CYAN
            ).pack(pady=(10, 5))
            
            # Image display
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            img_label = ctk.CTkLabel(popup, image=photo, text="")
            img_label.pack(padx=20, pady=10)
            img_label.image = photo  # Keep reference
            
            # Close hint
            ctk.CTkLabel(
                popup,
                text="Double-click or press ESC to close",
                font=("Consolas", 10),
                text_color="#666"
            ).pack(pady=(0, 10))
            
            # Close on double-click or ESC
            img_label.bind("<Double-Button-1>", lambda e: popup.destroy())
            popup.bind("<Escape>", lambda e: popup.destroy())
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")

    def add_custom_image(self):
        """Add a custom reference image"""
        make = self.make_var.get()
        model = self.model_var.get()
        year = self.year_var.get()

        if "Select" in make or "Select" in model or "Select" in year:
            messagebox.showwarning("Select Vehicle", "Please select a vehicle first")
            return

        file_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                img = Image.open(file_path)
                
                # Save to images folder
                result = self.resolve_vehicle(make, model, int(year), "has_key")
                year_range = result.get("year_range", year) if result else year
                img_key = f"{make}_{model}_{year_range}".replace(" ", "_").replace("/", "-")
                img_type = self.image_type_var.get().lower()
                
                dest_path = os.path.join(self.images_dir, f"{img_key}_{img_type}.jpg")
                
                # Convert and save
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                img.save(dest_path, "JPEG", quality=85)
                
                # Display
                img.thumbnail((180, 100))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 100))
                self.image_label.configure(image=photo, text="")
                self.current_image = photo
                
                messagebox.showinfo("Success", f"Image saved for {make} {model}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image:\n{e}")


# =======================
# Main Entry Point
# =======================
if __name__ == "__main__":
    import subprocess
    import sys
    
    # Check dependencies
    required = ["customtkinter", "Pillow"]
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"Installing missing packages: {missing}")
        for pkg in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    
    app = LuxuryKeyIntel()
    app.mainloop()
