"""
Script per generare le icone PWA per TauroBot 3.0
Crea icone SVG e le converte automaticamente in PNG
"""

import os
import sys

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
    return svg_content

def convert_svg_to_png(svg_path, png_path):
    """Converte un file SVG in PNG usando cairosvg"""
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        print(f"✓ Converted to {png_path}")
        return True
    except ImportError:
        print("⚠️  cairosvg not installed. Install it with: pip install cairosvg")
        return False
    except Exception as e:
        print(f"✗ Error converting {svg_path}: {e}")
        return False

def main():
    """Genera tutte le icone necessarie"""
    print("🎨 Generating PWA icons for TauroBot 3.0...")
    print()

    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    svg_created = 0
    png_created = 0

    # Check if cairosvg is available
    try:
        import cairosvg
        can_convert = True
        print("✓ cairosvg found - will generate both SVG and PNG files")
    except ImportError:
        can_convert = False
        print("⚠️  cairosvg not installed - will only generate SVG files")
        print("   To enable PNG conversion, run: pip install cairosvg")

    print()

    for size in sizes:
        svg_path = f'icons/icon-{size}x{size}.svg'
        png_path = f'icons/icon-{size}x{size}.png'

        # Create SVG
        create_svg_icon(size, svg_path)
        svg_created += 1

        # Convert to PNG if possible
        if can_convert:
            if convert_svg_to_png(svg_path, png_path):
                png_created += 1

    print()
    print("=" * 50)
    print(f"✅ Generation complete!")
    print(f"   SVG icons created: {svg_created}")
    if can_convert:
        print(f"   PNG icons created: {png_created}")
    print("=" * 50)

    if not can_convert:
        print("\n📝 To convert SVG to PNG manually:")
        print("1. Install cairosvg: pip install cairosvg")
        print("2. Run this script again")
        print("3. Or use ImageMagick: for file in icons/*.svg; do convert \"$file\" \"${file%.svg}.png\"; done")
    else:
        print("\n✅ All icons are ready for use in your PWA!")
        print("   Both SVG and PNG versions are available in the icons/ directory")

if __name__ == '__main__':
    main()
