metaMAKER — Python application for manually creating and exporting Solana-standard NFT metadata. Designed for artists and developers who want full control over naming, traits, and creator shares while visually previewing both images and metadata in a single sleek interface.
<img width="1394" height="783" alt="Screenshot 2025-10-29 at 9 08 59 AM" src="https://github.com/user-attachments/assets/bf670cd3-d10e-4880-aad5-6d5ac7bf6bba" />

---

**README:**

# ⚡ metaMAKER

metaMAKER is a standalone Python tool for generating and editing NFT metadata files that follow the Solana standard. Built with **Tkinter** and **Pillow**, it combines a bold cyberpunk aesthetic with full control over NFT metadata creation.

---

## ✨ Features

* **Folder-based workflow** — select an image directory and auto-generate `/metadata` folder
* **Visual image preview** — browse and view each image
* **Manual metadata editing** — define name, symbol, description, and seller fees
* **Creator management** — add and remove multiple creator wallets with share percentages
* **Attribute builder** — add trait types and values dynamically
* **JSON preview panel** — real-time preview of generated metadata
* **Save modes**

  * Save current file only
  * Generate metadata for all images automatically

---

## 🧠 How It Works

1. Launch `metaMAKER.py`
2. Click **SELECT** to choose your image folder
3. Add project details, creators, and attributes
4. Click **UPDATE PREVIEW** to view live JSON
5. Choose **SAVE CURRENT** or **GENERATE ALL**

The app creates a `/metadata` folder inside your image directory and saves one JSON file per image.

---

## 🧩 Requirements

* Python 3.9+
* Pillow
* Tkinter (usually included)

---

## ⚙️ Installation

```bash
pip install pillow
python metaMAKER.py
```

---

## 💾 Output Example

Each generated file (`0.json`, `1.json`, etc.) follows Solana’s standard format:

```json
{
  "name": "Collection #0",
  "symbol": "META",
  "description": "Cyberpunk NFT",
  "seller_fee_basis_points": 500,
  "image": "",
  "attributes": [
    {"trait_type": "Background", "value": "Neon Grid"}
  ],
  "properties": {
    "creators": [
      {"address": "YourWalletAddress", "share": 100}
    ]
  }
}
```

---

