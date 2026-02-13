# Handling Scanned PDFs - Air-Regulation-RK-BALI.pdf Issue

## Problem

The Air-Regulation-RK-BALI.pdf file has **0 chunks** after ingestion because it's a **scanned PDF** (images of pages, not text).

**Evidence from logs:**
```
Processing: Air-Regulation-RK-BALI.pdf
Loaded 348 pages
Created 0 chunks (avg 0.0 words)
```

This means the PDF contains images of text rather than actual text data, so PyPDFLoader cannot extract any text.

---

## Why This Happens

**Text-based PDF:**
- Contains actual text characters
- Can be selected and copied
- PyPDFLoader works ✓

**Scanned PDF (Image-based):**
- Contains images of pages
- Text cannot be selected
- PyPDFLoader extracts nothing ✗
- **Air-Regulation-RK-BALI.pdf is this type**

---

## Solutions

### Option 1: Use OCR (Optical Character Recognition)

Extract text from images using OCR technology.

#### Step 1: Install OCR Dependencies

**On Ubuntu/WSL:**
```bash
# Install Tesseract OCR
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils

# Install Python packages
pip install pdf2image pytesseract pillow
```

**On Windows:**
```bash
# Download and install Tesseract from:
# https://github.com/UB-Mannheim/tesseract/wiki

# Install Python packages
pip install pdf2image pytesseract pillow
```

**On macOS:**
```bash
brew install tesseract
brew install poppler

pip install pdf2image pytesseract pillow
```

#### Step 2: Run OCR Ingestion

I've created `ingest_with_ocr.py` but it's incomplete. Here's the full solution:

```bash
# Install dependencies first
pip install pdf2image pytesseract pillow

# Then run OCR on the specific PDF
python -c "
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

pdf_path = 'documents/Air-Regulation-RK-BALI.pdf'
output_file = 'documents/Air-Regulation-RK-BALI-OCR.txt'

print('Converting PDF to images...')
images = convert_from_path(pdf_path, dpi=300)

print(f'Extracting text from {len(images)} pages...')
all_text = []

for i, image in enumerate(images, 1):
    text = pytesseract.image_to_string(image)
    all_text.append(f'--- Page {i} ---\n{text}\n')
    if i % 10 == 0:
        print(f'Processed {i}/{len(images)} pages')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_text))

print(f'OCR complete! Text saved to {output_file}')
"
```

**Note:** OCR is slow (348 pages may take 30-60 minutes) and accuracy depends on scan quality.

---

### Option 2: Get Text-Based Version (Recommended)

**Best solution:** Obtain a text-based version of the Air-Regulation-RK-BALI.pdf

- Contact document source
- Request digital/text version
- Much faster and more accurate than OCR

---

### Option 3: Manual Extraction

For specific sections only:

1. Open PDF in Adobe Acrobat
2. Use "Export PDF" → "Text"
3. Save as .txt file
4. Create new text-based PDF or add to documents

---

### Option 4: Skip This Document

If the document isn't critical:

1. Remove from documents folder
2. Re-run ingestion
3. System will work with other 7 documents

**Current working documents:**
- Sample test questions.pdf (12 chunks)
- 10-General-Navigation-2014.pdf (716 chunks)
- 11-radio-navigation-2014.pdf (469 chunks)
- 6-mass-and-balance-and-performance-2014.pdf (759 chunks)
- 7-Flight-Planning-and-Monitoring-2014.pdf (386 chunks)
- Instruments.pdf (878 chunks)
- Meteorology full book.pdf (763 chunks)

**Total: 3,983 chunks from 7 documents**

---

## Checking if PDF is Scanned

### Method 1: Try to Select Text
1. Open PDF in viewer
2. Try to select text with mouse
3. If you can't select text → Scanned PDF

### Method 2: Check File Size
- Text-based: Usually smaller (few MB)
- Scanned: Usually larger (tens of MB)
- Air-Regulation-RK-BALI.pdf: Check size

### Method 3: Use pdfinfo
```bash
pdfinfo documents/Air-Regulation-RK-BALI.pdf | grep "Pages\|File size"
```

---

## Quick Fix for Testing

If you just want to test with a few pages:

```python
# Extract first 10 pages with OCR
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path('documents/Air-Regulation-RK-BALI.pdf', 
                          first_page=1, last_page=10, dpi=200)

for i, img in enumerate(images, 1):
    text = pytesseract.image_to_string(img)
    print(f"Page {i}: {len(text)} characters extracted")
```

---

## Why System Still Works

Even without Air-Regulation-RK-BALI.pdf, your system has:
- ✅ 3,983 chunks from 7 documents
- ✅ Covers: Navigation, Meteorology, Mass & Balance, Flight Planning, Instruments
- ✅ Can answer most aviation questions

**Missing:** Air regulations from RK-BALI document

---

## Recommendation

**For production use:**
1. Get text-based version of Air-Regulation-RK-BALI.pdf
2. Or use OCR if no alternative
3. Re-run ingestion with all documents

**For immediate testing:**
- Continue with current 7 documents
- System is fully functional
- Add Air-Regulation document later

---

## Future Prevention

When adding new PDFs:

1. **Check if text-based:**
   ```bash
   pdftotext document.pdf test.txt
   wc -w test.txt  # Should show word count
   ```

2. **If scanned, use OCR before ingestion:**
   - Process with OCR first
   - Save as text-based PDF
   - Then ingest

3. **Request digital versions:**
   - Always prefer born-digital PDFs
   - Better quality, faster processing

---

**Status:** Air-Regulation-RK-BALI.pdf cannot be used without OCR  
**Impact:** Questions about air regulations from this document will return "not available"  
**Solution:** Use OCR or obtain text-based version
