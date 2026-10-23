import argparse
import hashlib
from pathlib import Path
import pymupdf
from app.knowledge import ensure_index, upsert_documents

def chunks(text, size=1100, overlap=180):
    text = ' '.join(text.split())
    step = size-overlap
    return [text[i:i+size] for i in range(0,len(text),step) if len(text[i:i+size]) > 80]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', default='data/Medical_book.pdf')
    args = parser.parse_args()
    pdf = Path(args.pdf)
    if not pdf.exists():
        raise SystemExit(f'PDF not found: {pdf}')
    index_host = ensure_index()
    with pymupdf.open(pdf) as doc:
        batch = []
        for page_number, page in enumerate(doc, start=1):
            for part, content in enumerate(chunks(page.get_text()), start=1):
                key = hashlib.sha256(f'{pdf.name}:{page_number}:{part}:{content}'.encode()).hexdigest()
                batch.append({'_id': key, 'chunk_text': content, 'title': pdf.name, 'page': page_number, 'text': content, 'file': pdf.name})
                if len(batch) >= 50:
                    upsert_documents(index_host, batch)
                    batch = []
            if page_number % 50 == 0:
                print(f'Indexed pages: {page_number}/{len(doc)}',flush=True)
        if batch:
            upsert_documents(index_host, batch)
    print('Ingestion complete')
if __name__ == '__main__': main()