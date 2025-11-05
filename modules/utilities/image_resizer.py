"""
Image Resizer Module
Batch resize, compress, convert, and optimize images
"""

from PIL import Image
import os
from datetime import datetime
import glob

class ImageResizer:
    def __init__(self):
        self.output_dir = "data/resized_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    def resize_image(self, image_path, width=None, height=None, maintain_aspect=True, output_path=None):
        """Resize a single image"""
        try:
            if not os.path.exists(image_path):
                return f"❌ Image not found: {image_path}"
            
            img = Image.open(image_path)
            original_size = img.size
            
            if width is None and height is None:
                return "❌ Please specify width and/or height"
            
            if maintain_aspect:
                if width and height:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                elif width:
                    ratio = width / original_size[0]
                    new_height = int(original_size[1] * ratio)
                    img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                elif height:
                    ratio = height / original_size[1]
                    new_width = int(original_size[0] * ratio)
                    img = img.resize((new_width, height), Image.Resampling.LANCZOS)
            else:
                new_width = width or original_size[0]
                new_height = height or original_size[1]
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            if output_path is None:
                basename = os.path.basename(image_path)
                name, ext = os.path.splitext(basename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(self.output_dir, f"{name}_resized_{timestamp}{ext}")
            
            img.save(output_path, quality=95, optimize=True)
            
            new_size = img.size
            original_file_size = os.path.getsize(image_path)
            new_file_size = os.path.getsize(output_path)
            
            result = f"\n{'='*60}\n"
            result += f"🖼️ IMAGE RESIZED\n"
            result += f"{'='*60}\n\n"
            result += f"Original: {original_size[0]}x{original_size[1]} ({original_file_size/1024:.2f} KB)\n"
            result += f"New: {new_size[0]}x{new_size[1]} ({new_file_size/1024:.2f} KB)\n"
            result += f"Saved to: {output_path}\n"
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to resize image: {str(e)}"
    
    def resize_batch(self, folder_path, width=None, height=None, maintain_aspect=True, format_filter=None):
        """Resize all images in a folder"""
        try:
            if not os.path.exists(folder_path):
                return f"❌ Folder not found: {folder_path}"
            
            image_files = []
            for ext in self.supported_formats:
                image_files.extend(glob.glob(os.path.join(folder_path, f"*{ext}")))
                image_files.extend(glob.glob(os.path.join(folder_path, f"*{ext.upper()}")))
            
            if format_filter:
                image_files = [f for f in image_files if f.lower().endswith(format_filter.lower())]
            
            if not image_files:
                return "ℹ️ No images found in folder"
            
            results = []
            total_original_size = 0
            total_new_size = 0
            
            for image_path in image_files:
                try:
                    img = Image.open(image_path)
                    original_size = img.size
                    original_file_size = os.path.getsize(image_path)
                    total_original_size += original_file_size
                    
                    if maintain_aspect:
                        if width and height:
                            img.thumbnail((width, height), Image.Resampling.LANCZOS)
                        elif width:
                            ratio = width / original_size[0]
                            new_height = int(original_size[1] * ratio)
                            img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                        elif height:
                            ratio = height / original_size[1]
                            new_width = int(original_size[0] * ratio)
                            img = img.resize((new_width, height), Image.Resampling.LANCZOS)
                    else:
                        new_width = width or original_size[0]
                        new_height = height or original_size[1]
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    basename = os.path.basename(image_path)
                    name, ext = os.path.splitext(basename)
                    output_path = os.path.join(self.output_dir, f"{name}_resized{ext}")
                    
                    img.save(output_path, quality=95, optimize=True)
                    
                    new_file_size = os.path.getsize(output_path)
                    total_new_size += new_file_size
                    
                    results.append({
                        "name": basename,
                        "original": f"{original_size[0]}x{original_size[1]}",
                        "new": f"{img.size[0]}x{img.size[1]}",
                        "saved": output_path
                    })
                except Exception as e:
                    results.append({
                        "name": os.path.basename(image_path),
                        "error": str(e)
                    })
            
            summary = f"\n{'='*60}\n"
            summary += f"🖼️ BATCH IMAGE RESIZE\n"
            summary += f"{'='*60}\n\n"
            summary += f"Processed: {len(results)} images\n"
            summary += f"Original Total: {total_original_size/(1024*1024):.2f} MB\n"
            summary += f"New Total: {total_new_size/(1024*1024):.2f} MB\n"
            summary += f"Space Saved: {(total_original_size-total_new_size)/(1024*1024):.2f} MB\n\n"
            
            for i, result in enumerate(results[:10], 1):
                if "error" in result:
                    summary += f"{i}. ❌ {result['name']}: {result['error']}\n"
                else:
                    summary += f"{i}. ✅ {result['name']}: {result['original']} → {result['new']}\n"
            
            if len(results) > 10:
                summary += f"\n... and {len(results) - 10} more images\n"
            
            summary += f"\n{'='*60}\n"
            summary += f"Output folder: {self.output_dir}\n"
            summary += f"{'='*60}\n"
            
            return summary
        
        except Exception as e:
            return f"❌ Failed to batch resize: {str(e)}"
    
    def compress_image(self, image_path, quality=85, output_path=None):
        """Compress image to reduce file size"""
        try:
            if not os.path.exists(image_path):
                return f"❌ Image not found: {image_path}"
            
            img = Image.open(image_path)
            original_size = os.path.getsize(image_path)
            
            if output_path is None:
                basename = os.path.basename(image_path)
                name, ext = os.path.splitext(basename)
                output_path = os.path.join(self.output_dir, f"{name}_compressed{ext}")
            
            if image_path.lower().endswith('.png'):
                img.save(output_path, optimize=True, compress_level=9)
            else:
                img.save(output_path, quality=quality, optimize=True)
            
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size) * 100
            
            result = f"\n{'='*60}\n"
            result += f"📦 IMAGE COMPRESSED\n"
            result += f"{'='*60}\n\n"
            result += f"Original: {original_size/1024:.2f} KB\n"
            result += f"Compressed: {new_size/1024:.2f} KB\n"
            result += f"Reduction: {reduction:.1f}%\n"
            result += f"Saved to: {output_path}\n"
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to compress image: {str(e)}"
    
    def convert_format(self, image_path, target_format, output_path=None):
        """Convert image to different format"""
        try:
            if not os.path.exists(image_path):
                return f"❌ Image not found: {image_path}"
            
            target_format = target_format.lower().lstrip('.')
            
            if f".{target_format}" not in self.supported_formats:
                return f"❌ Unsupported format: {target_format}\nSupported: {', '.join(self.supported_formats)}"
            
            img = Image.open(image_path)
            
            if img.mode in ('RGBA', 'LA') and target_format in ('jpg', 'jpeg'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            if output_path is None:
                basename = os.path.basename(image_path)
                name, _ = os.path.splitext(basename)
                output_path = os.path.join(self.output_dir, f"{name}.{target_format}")
            
            img.save(output_path, quality=95, optimize=True)
            
            original_size = os.path.getsize(image_path)
            new_size = os.path.getsize(output_path)
            
            result = f"\n{'='*60}\n"
            result += f"🔄 IMAGE FORMAT CONVERTED\n"
            result += f"{'='*60}\n\n"
            result += f"From: {os.path.splitext(image_path)[1]} ({original_size/1024:.2f} KB)\n"
            result += f"To: .{target_format} ({new_size/1024:.2f} KB)\n"
            result += f"Saved to: {output_path}\n"
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to convert format: {str(e)}"
    
    def create_thumbnail(self, image_path, max_size=200, output_path=None):
        """Create thumbnail of image"""
        try:
            if not os.path.exists(image_path):
                return f"❌ Image not found: {image_path}"
            
            img = Image.open(image_path)
            original_size = img.size
            
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            if output_path is None:
                basename = os.path.basename(image_path)
                name, ext = os.path.splitext(basename)
                output_path = os.path.join(self.output_dir, f"{name}_thumb{ext}")
            
            img.save(output_path, quality=90, optimize=True)
            
            result = f"\n{'='*60}\n"
            result += f"🖼️ THUMBNAIL CREATED\n"
            result += f"{'='*60}\n\n"
            result += f"Original: {original_size[0]}x{original_size[1]}\n"
            result += f"Thumbnail: {img.size[0]}x{img.size[1]}\n"
            result += f"Saved to: {output_path}\n"
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to create thumbnail: {str(e)}"
    
    def rotate_image(self, image_path, angle, output_path=None):
        """Rotate image by specified angle"""
        try:
            if not os.path.exists(image_path):
                return f"❌ Image not found: {image_path}"
            
            img = Image.open(image_path)
            rotated = img.rotate(-angle, expand=True)
            
            if output_path is None:
                basename = os.path.basename(image_path)
                name, ext = os.path.splitext(basename)
                output_path = os.path.join(self.output_dir, f"{name}_rotated{ext}")
            
            rotated.save(output_path, quality=95, optimize=True)
            
            result = f"✅ Rotated image {angle}° and saved to: {output_path}"
            return result
        
        except Exception as e:
            return f"❌ Failed to rotate image: {str(e)}"
    
    def crop_image(self, image_path, left, top, right, bottom, output_path=None):
        """Crop image to specified coordinates"""
        try:
            if not os.path.exists(image_path):
                return f"❌ Image not found: {image_path}"
            
            img = Image.open(image_path)
            cropped = img.crop((left, top, right, bottom))
            
            if output_path is None:
                basename = os.path.basename(image_path)
                name, ext = os.path.splitext(basename)
                output_path = os.path.join(self.output_dir, f"{name}_cropped{ext}")
            
            cropped.save(output_path, quality=95, optimize=True)
            
            result = f"✅ Cropped image to {cropped.size[0]}x{cropped.size[1]} and saved to: {output_path}"
            return result
        
        except Exception as e:
            return f"❌ Failed to crop image: {str(e)}"

if __name__ == "__main__":
    resizer = ImageResizer()
    
    print("Testing Image Resizer...")
    print("Image resizer module loaded successfully")
