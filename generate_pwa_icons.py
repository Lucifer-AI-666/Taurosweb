"""
Script per generare le icone PWA per TauroBot 3.0
Crea icone SVG semplici che possono essere convertite in PNG
"""

import os

def create_svg_icon(size, output_path):
    """Crea un'icona SVG per TauroBot"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <!-- Background gradient -->
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="bullGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ffd700;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ffed4e;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background circle -->
  <circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="url(#bgGradient)"/>
  
  <!-- Bull emoji / symbol -->
  <text x="50%" y="50%" 
        font-size="{size*0.6}" 
        text-anchor="middle" 
        dominant-baseline="central"
        fill="url(#bullGradient)"
        font-family="Arial, sans-serif"
        font-weight="bold">🐂</text>
</svg>'''
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✓ Created {output_path}")

def main():
    """Genera tutte le icone necessarie"""
    print("🎨 Generating PWA icons for TauroBot 3.0...")
    
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    for size in sizes:
        create_svg_icon(size, f'icons/icon-{size}x{size}.svg')
    
    print("\n✅ All SVG icons generated!")
    print("\n📝 Note: Le icone SVG sono state create.")
    print("Per convertirle in PNG, usa uno dei seguenti metodi:")
    print("1. Apri ogni SVG in un browser e salva come PNG")
    print("2. Usa ImageMagick: convert icon.svg icon.png")
    print("3. Usa uno strumento online come https://cloudconvert.com/svg-to-png")
    print("\nOppure puoi usare le icone SVG direttamente modificando manifest.json")

if __name__ == '__main__':
    main()
