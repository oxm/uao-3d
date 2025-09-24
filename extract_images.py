import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_dir='images'):
    """Extract images from PDF file"""
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Open PDF
        doc = fitz.open(pdf_path)
        image_count = 0
        
        print(f"Processing PDF: {pdf_path}")
        print(f"Total pages: {len(doc)}")
        
        # Iterate through pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            print(f"Page {page_num + 1}: Found {len(image_list)} images")
            
            # Extract images from current page
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Only save RGB/RGBA images
                    if pix.n - pix.alpha < 4:
                        image_filename = f"{output_dir}/image_{image_count:03d}.png"
                        pix.save(image_filename)
                        print(f"Saved: {image_filename}")
                        image_count += 1
                    
                    pix = None  # Free memory
                except Exception as e:
                    print(f"Error extracting image {img_index} from page {page_num + 1}: {e}")
        
        doc.close()
        print(f"\nTotal images extracted: {image_count}")
        return image_count
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return 0

if __name__ == "__main__":
    pdf_file = "统一3D场景理解与生成模型.pdf"
    if os.path.exists(pdf_file):
        extract_images_from_pdf(pdf_file)
    else:
        print(f"PDF file not found: {pdf_file}")