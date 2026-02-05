"""
CyberNinja Luxury Key Intelligence
Professional BMW / Mercedes / Audi / VW Key Programming Reference
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
        self.title("🔑 CyberNinja Luxury Key Intelligence - Professional Edition")
        self.geometry("1500x950")
        self.minsize(1300, 850)
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
        self.vw_data = self.load_json("vw.json")  # Added VW

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
                    return {
                        "platform": info.get("platform", "Unknown"),
                        "immobilizer": info.get("immobilizer", "Unknown"),
                        "key_type": info.get("key_type", "Unknown"),
                        "key_blade": info.get("key_blade", "Unknown"),
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
                        "recommended_tool": xhorse_info.get("recommended_tool", "")
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
            text="🔑 CYBERNINJA LUXURY KEY INTELLIGENCE",
            font=("Consolas", 28, "bold"),
            text_color=CYBER_CYAN
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            title_frame,
            text="BMW • MERCEDES • AUDI • VW",
            font=("Consolas", 14),
            text_color=CYBER_MAGENTA
        ).pack(side="left", padx=20)

        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== LEFT PANEL - Vehicle Input =====
        left_panel = ctk.CTkFrame(main_container, fg_color=CYBER_PANEL, width=320, corner_radius=15)
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

        # Make - Added Volkswagen
        ctk.CTkLabel(left_panel, text="Make:", font=("Consolas", 12, "bold"),
                     text_color=CYBER_ACCENT).pack(anchor="w", padx=25, pady=(15, 5))
        self.make_var = ctk.StringVar(value="Select Make")
        self.make_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.make_var,
            values=["Select Make", "BMW", "Mercedes-Benz", "Audi", "Volkswagen"],
            width=260,
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
            width=260,
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
        years = ["Select Year"] + [str(y) for y in range(2026, 2004, -1)]
        self.year_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.year_var,
            values=years,
            width=260,
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
            width=260,
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
            width=260,
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
            text=f"BMW Models: {bmw_count}\nAudi Models: {audi_count}\nVW Models: {vw_count}\nMercedes: {benz_count if benz_count > 0 else 'Coming Soon'}",
            font=("Consolas", 10),
            text_color=CYBER_ACCENT,
            justify="left"
        )
        self.stat_label.pack(pady=(0, 10))

        # Credits at bottom
        ctk.CTkLabel(
            left_panel,
            text="CyberNinja © 2026\n🔑 Kobe's Keys",
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

        # Result fields - Added Xhorse tool fields
        self.result_labels = {}
        fields = [
            ("Platform / Chassis", "platform", CYBER_CYAN),
            ("Immobilizer System", "immobilizer", CYBER_MAGENTA),
            ("Key Type", "key_type", CYBER_ACCENT),
            ("Key Blade", "blade", CYBER_YELLOW),
            ("Programming Method", "programming", CYBER_ORANGE),
            ("Module Removal", "module", CYBER_RED),
            ("AKL Supported", "akl", CYBER_GREEN),
            ("Risk Level", "risk", CYBER_RED),
            ("EEPROM Chip", "eeprom_chip", CYBER_YELLOW),
            ("Backup Method", "backup_method", CYBER_ORANGE),
            ("⚠️ BACKUP WARNING", "backup_warning", CYBER_RED),
            ("🔧 XHORSE TOOL SUPPORT", "xhorse_tools", CYBER_BLUE),
            ("📋 XHORSE WORKFLOW", "xhorse_workflow", CYBER_BLUE),
            ("Notes", "notes", CYBER_ACCENT)
        ]

        for display_name, key, color in fields:
            card = ctk.CTkFrame(self.results_scroll, fg_color="#1a1a2e", corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)

            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(10, 0))

            ctk.CTkLabel(
                header_frame,
                text=display_name,
                font=("Consolas", 11, "bold"),
                text_color=color
            ).pack(side="left")

            value_label = ctk.CTkLabel(
                card,
                text="—",
                font=("Consolas", 13),
                text_color="#e6e6e6",
                wraplength=400,
                justify="left"
            )
            value_label.pack(anchor="w", padx=15, pady=(5, 12))
            self.result_labels[display_name] = value_label

        # ===== RIGHT PANEL - Image =====
        right_panel = ctk.CTkFrame(main_container, fg_color=CYBER_PANEL, width=280, corner_radius=15)
        right_panel.pack(side="right", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)

        ctk.CTkLabel(
            right_panel,
            text="📷 REFERENCE IMAGE",
            font=("Consolas", 14, "bold"),
            text_color=CYBER_CYAN
        ).pack(pady=(20, 10))

        sep4 = ctk.CTkFrame(right_panel, fg_color=CYBER_CYAN, height=2)
        sep4.pack(fill="x", padx=20, pady=5)

        # Image frame
        self.image_frame = ctk.CTkFrame(right_panel, fg_color="#0a0a15", corner_radius=10,
                                         width=240, height=200)
        self.image_frame.pack(pady=15, padx=20)
        self.image_frame.pack_propagate(False)

        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="No Image\n\n📷\n\nSelect vehicle to\nload reference",
            font=("Consolas", 11),
            text_color="#666"
        )
        self.image_label.pack(expand=True)

        # Image type selector
        ctk.CTkLabel(right_panel, text="Image Type:",
                     font=("Consolas", 11, "bold"), text_color=CYBER_ACCENT).pack(pady=(10, 5))

        self.image_type_var = ctk.StringVar(value="Module")
        img_type_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        img_type_frame.pack()

        ctk.CTkRadioButton(
            img_type_frame,
            text="Module/BCM",
            variable=self.image_type_var,
            value="Module",
            font=("Consolas", 10),
            fg_color=CYBER_MAGENTA,
            hover_color=CYBER_CYAN
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            img_type_frame,
            text="Key/Fob",
            variable=self.image_type_var,
            value="Key",
            font=("Consolas", 10),
            fg_color=CYBER_MAGENTA,
            hover_color=CYBER_CYAN
        ).pack(side="left", padx=10)

        # Add image button
        ctk.CTkButton(
            right_panel,
            text="📁 Add Custom Image",
            width=200,
            height=35,
            font=("Consolas", 11, "bold"),
            fg_color=CYBER_MAGENTA,
            hover_color=CYBER_CYAN,
            command=self.add_custom_image
        ).pack(pady=15)

        # Separator
        sep5 = ctk.CTkFrame(right_panel, fg_color=CYBER_MAGENTA, height=2)
        sep5.pack(fill="x", padx=20, pady=10)

        # Quick Info Box
        self.quick_info = ctk.CTkFrame(right_panel, fg_color="#1a1a2e", corner_radius=10)
        self.quick_info.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.quick_info,
            text="⚡ QUICK REFERENCE",
            font=("Consolas", 11, "bold"),
            text_color=CYBER_YELLOW
        ).pack(pady=(10, 5))

        self.quick_info_text = ctk.CTkLabel(
            self.quick_info,
            text="Select a vehicle\nto see quick tips",
            font=("Consolas", 10),
            text_color=CYBER_ACCENT,
            justify="left"
        )
        self.quick_info_text.pack(pady=(0, 10), padx=10)

        # Risk indicator
        self.risk_indicator = ctk.CTkFrame(right_panel, fg_color="#1a1a2e", corner_radius=10)
        self.risk_indicator.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.risk_indicator,
            text="⚠️ JOB RISK LEVEL",
            font=("Consolas", 11, "bold"),
            text_color=CYBER_RED
        ).pack(pady=(10, 5))

        self.risk_bar = ctk.CTkProgressBar(
            self.risk_indicator,
            width=200,
            height=15,
            progress_color=CYBER_GREEN,
            fg_color="#333"
        )
        self.risk_bar.pack(pady=5)
        self.risk_bar.set(0)

        self.risk_text = ctk.CTkLabel(
            self.risk_indicator,
            text="—",
            font=("Consolas", 12, "bold"),
            text_color=CYBER_GREEN
        )
        self.risk_text.pack(pady=(5, 10))

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
        
        if result["valid"]:
            year_text = f" | Year: {result['year']}" if result.get('year') else ""
            self.vin_status_label.configure(
                text=f"{result['message']}{year_text}",
                text_color=CYBER_GREEN
            )
            # Auto-select make if detected
            if result.get("make"):
                self.make_var.set(result["make"])
                self.on_make_changed(result["make"])
        else:
            self.vin_status_label.configure(
                text=f"✗ {result['message']}",
                text_color=CYBER_RED
            )

    def clear_results(self):
        """Clear all result fields"""
        for label in self.result_labels.values():
            label.configure(text="—", text_color="#e6e6e6")
        self.risk_bar.set(0)
        self.risk_text.configure(text="—", text_color=CYBER_GREEN)
        self.quick_info_text.configure(text="Select a vehicle\nto see quick tips")
        self.image_label.configure(
            text="No Image\n\n📷\n\nSelect vehicle to\nload reference",
            image=None
        )

    def update_results(self):
        """Resolve and display vehicle data"""
        make = self.make_var.get()
        model = self.model_var.get()
        year_text = self.year_var.get()
        key_status_ui = self.key_status_var.get()

        if "Select" in make or "Select" in model or "Select" in year_text:
            return

        try:
            year = int(year_text)
        except:
            return

        key_map = {
            "Has Working Key": "has_key",
            "Only 1 Key": "one_key",
            "AKL (All Keys Lost)": "akl"
        }
        key_status = key_map.get(key_status_ui, "has_key")

        result = self.resolve_vehicle(make, model, year, key_status)

        if not result:
            self.clear_results()
            self.result_labels["Notes"].configure(
                text="No data available for this vehicle configuration.",
                text_color=CYBER_YELLOW
            )
            return

        # Build Xhorse tool support text
        xhorse_tools_text = ""
        mlb = result.get("mlb_tool", False)
        mqb = result.get("mqb_adapter", False)
        
        if mlb == True:
            xhorse_tools_text += "✅ MLB Tool (XDMLB0): SUPPORTED\n"
        elif mlb == "Limited" or mlb == "Verify":
            xhorse_tools_text += f"⚠️ MLB Tool: {mlb}\n"
        else:
            xhorse_tools_text += "❌ MLB Tool: Not applicable\n"
            
        if mqb == True:
            xhorse_tools_text += "✅ MQB Adapter (XDMQBAGL): SUPPORTED"
        elif mqb == "Limited":
            xhorse_tools_text += "⚠️ MQB Adapter: Limited support"
        else:
            xhorse_tools_text += "❌ MQB Adapter: Not applicable"
        
        if result.get("recommended_tool"):
            xhorse_tools_text += f"\n🎯 Recommended: {result.get('recommended_tool')}"

        # Build workflow text
        workflow_text = ""
        if result.get("xhorse_notes"):
            workflow_text = result.get("xhorse_notes", "")
        if result.get("xhorse_workflow"):
            if workflow_text:
                workflow_text += "\n"
            workflow_text += result.get("xhorse_workflow", "")
        if not workflow_text:
            workflow_text = "Standard procedures apply"

        # Update result labels
        field_map = {
            "Platform / Chassis": "platform",
            "Immobilizer System": "immobilizer",
            "Key Type": "key_type",
            "Key Blade": "key_blade",
            "Programming Method": "programming",
            "Module Removal": "module_removal",
            "AKL Supported": "akl_supported",
            "Risk Level": "risk_level",
            "EEPROM Chip": "eeprom_chip",
            "Backup Method": "backup_method",
            "⚠️ BACKUP WARNING": "backup_warning",
            "Notes": "notes"
        }

        for display_name, key in field_map.items():
            value = result.get(key, "—")
            label = self.result_labels.get(display_name)
            if label:
                label.configure(text=value)

                # Color coding
                if display_name == "Risk Level":
                    if "Low" in value:
                        label.configure(text_color=RISK_LOW)
                        self.update_risk_bar(0.25, "LOW", RISK_LOW)
                    elif "Medium" in value:
                        label.configure(text_color=RISK_MEDIUM)
                        self.update_risk_bar(0.5, "MEDIUM", RISK_MEDIUM)
                    elif "Very High" in value:
                        label.configure(text_color=RISK_VERY_HIGH)
                        self.update_risk_bar(1.0, "VERY HIGH", RISK_VERY_HIGH)
                    elif "High" in value:
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
                    elif "Limited" in value or "Very" in value:
                        label.configure(text_color=CYBER_YELLOW)
                    elif value == "No" or "dealer" in value.lower():
                        label.configure(text_color=CYBER_RED)

                # Color code EEPROM backup warning
                elif display_name == "⚠️ BACKUP WARNING":
                    if value and "CRITICAL" in value:
                        label.configure(text_color=CYBER_RED)
                    elif value and "EXTREME" in value:
                        label.configure(text_color=CYBER_RED)
                    elif value and "IMPORTANT" in value:
                        label.configure(text_color=CYBER_ORANGE)
                    elif value:
                        label.configure(text_color=CYBER_YELLOW)
                    else:
                        label.configure(text_color=CYBER_GREEN)

        # Update Xhorse tool fields
        self.result_labels["🔧 XHORSE TOOL SUPPORT"].configure(text=xhorse_tools_text, text_color=CYBER_BLUE)
        self.result_labels["📋 XHORSE WORKFLOW"].configure(text=workflow_text, text_color=CYBER_ACCENT)

        # Update quick info
        blade = result.get("key_blade", "—")
        immo = result.get("immobilizer", "—")
        eeprom = result.get("eeprom_chip", "N/A")
        backup_req = "⚠️ YES" if result.get("backup_required", False) else "✓ Optional"
        self.quick_info_text.configure(
            text=f"Blade: {blade}\nSystem: {immo}\nEEPROM: {eeprom}\nBackup: {backup_req}"
        )

        # Try to load reference image
        self.load_reference_image(make, model, result.get("year_range", ""))

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
                    img.thumbnail((220, 180))
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(220, 180))
                    self.image_label.configure(image=photo, text="")
                    self.current_image = photo
                    return
                except:
                    pass
        
        # No image found
        self.image_label.configure(
            text=f"No {img_type} image\n\n📷\n\nClick 'Add Custom Image'\nto add one",
            image=None
        )

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
                img.thumbnail((220, 180))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(220, 180))
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
