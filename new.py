import requests
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json

API_KEY = "NN6mpiPcWCT8YkI9RoRsSUc0tM9wpY3sazoFH-9HoG8"
API_URL = "https://api.data.street.co.uk/street-data-api/v2/properties/addresses"

def get_property_info(address, postcode):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    payload = {
        "data": {
            "address": address,
            "postcode": postcode
        }
    }
    params = {
        "tier": "premium"
    }

    response = requests.post(API_URL, headers=headers, json=payload, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def format_property_info(data):
    attributes = data['data']['attributes']
    info = {}
    
    # Street Group Format
    info["Address"] = attributes['address']['street_group_format']['address_lines']
    info["Postcode"] = attributes['address']['street_group_format']['postcode']
    
    # Localities
    info["Localities"] = attributes['localities']
    
    # Location
    info["Location"] = attributes['location']['coordinates']
    
    # Property Type
    info["Property Type"] = attributes['property_type']['value']
    
    # Construction Age Band
    info["Construction Age Band"] = attributes['construction_age_band']
    
    # Tenure
    info["Tenure"] = attributes['tenure']
    
    # Title Deeds
    info["Title Deeds"] = attributes['title_deeds']['titles']
    
    # Internal Area
    info["Internal Area"] = f"{attributes.get('internal_area_square_metres', 'N/A')} square meters"
    
    return info

def display_info(info):
    popup = tk.Toplevel()
    popup.title("Property Information")
    popup.geometry("800x600")
    
    notebook = ttk.Notebook(popup)
    notebook.pack(expand=True, fill=tk.BOTH)
    
    # General Information
    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="General")
    
    general_text = tk.Text(general_frame, wrap=tk.WORD)
    general_text.pack(expand=True, fill=tk.BOTH)
    general_text.insert(tk.END, f"Address: {info['Address']}\n")
    general_text.insert(tk.END, f"Postcode: {info['Postcode']}\n")
    general_text.insert(tk.END, f"Property Type: {info['Property Type']}\n")
    general_text.insert(tk.END, f"Construction Age Band: {info['Construction Age Band']}\n")
    general_text.insert(tk.END, f"Internal Area: {info['Internal Area']}\n")
    general_text.config(state=tk.DISABLED)
    
    # Localities
    localities_frame = ttk.Frame(notebook)
    notebook.add(localities_frame, text="Localities")
    
    localities_text = tk.Text(localities_frame, wrap=tk.WORD)
    localities_text.pack(expand=True, fill=tk.BOTH)
    for key, value in info['Localities'].items():
        localities_text.insert(tk.END, f"{key.replace('_', ' ').title()}: {value}\n")
    localities_text.config(state=tk.DISABLED)
    
    # Location
    location_frame = ttk.Frame(notebook)
    notebook.add(location_frame, text="Location")
    
    location_text = tk.Text(location_frame, wrap=tk.WORD)
    location_text.pack(expand=True, fill=tk.BOTH)
    location_text.insert(tk.END, f"Latitude: {info['Location']['latitude']}\n")
    location_text.insert(tk.END, f"Longitude: {info['Location']['longitude']}\n")
    location_text.config(state=tk.DISABLED)
    
    # Tenure
    tenure_frame = ttk.Frame(notebook)
    notebook.add(tenure_frame, text="Tenure")
    
    tenure_text = tk.Text(tenure_frame, wrap=tk.WORD)
    tenure_text.pack(expand=True, fill=tk.BOTH)
    for key, value in info['Tenure'].items():
        if isinstance(value, dict):
            tenure_text.insert(tk.END, f"{key.replace('_', ' ').title()}:\n")
            for sub_key, sub_value in value.items():
                tenure_text.insert(tk.END, f"  {sub_key.replace('_', ' ').title()}: {sub_value}\n")
        else:
            tenure_text.insert(tk.END, f"{key.replace('_', ' ').title()}: {value}\n")
    tenure_text.config(state=tk.DISABLED)
    
    # Title Deeds
    title_deeds_frame = ttk.Frame(notebook)
    notebook.add(title_deeds_frame, text="Title Deeds")
    
    title_deeds_text = tk.Text(title_deeds_frame, wrap=tk.WORD)
    title_deeds_text.pack(expand=True, fill=tk.BOTH)
    for title in info['Title Deeds']:
        title_deeds_text.insert(tk.END, f"Title Number: {title['title_number']}\n")
        title_deeds_text.insert(tk.END, f"Class of Title: {title['class_of_title']}\n")
        title_deeds_text.insert(tk.END, f"Estate Interest: {title['estate_interest']}\n\n")
    title_deeds_text.config(state=tk.DISABLED)
    
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack()

def search_property():
    address = simpledialog.askstring("Input", "Enter the address:")
    postcode = simpledialog.askstring("Input", "Enter the postcode:")
    
    if address and postcode:
        data = get_property_info(address, postcode)
        if data:
            info = format_property_info(data)
            display_info(info)
        else:
            messagebox.showerror("Error", "Failed to retrieve property information.")
    else:
        messagebox.showerror("Error", "Please enter both address and postcode.")

root = tk.Tk()
root.title("Property Information Lookup")
root.geometry("300x100")

search_button = tk.Button(root, text="Search Property", command=search_property)
search_button.pack(expand=True)

root.mainloop()