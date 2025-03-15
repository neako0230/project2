import sys
sys.setrecursionlimit(5000)

import gradio as gr
import os
import shutil
import requests
from scholarly import scholarly
from datetime import datetime
import re
import json

def preprocess_topic(topic):
    topic = re.sub(r"[ -]", "_", topic)
    topic = re.sub(r"[^\w]", "", topic)
    return f"paper_{topic}"

def save_results_to_file(results, query, save_format):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_folder = preprocess_topic(query)
    save_dir = os.path.join(os.path.expanduser("~/PAPER"), topic_folder)
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{query}_{timestamp}.{save_format}"
    save_path = os.path.join(save_dir, filename)
    
    try:
        if save_format == "txt":
            with open(save_path, "w", encoding="utf-8") as f:
                for entry in results:
                    f.write(f"論文標題: {entry['title']}\n摘要:\n{entry['abstract']}\n\nAPA 引用:\n{entry['apa_citation']}\n\n")
        elif save_format == "json":
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        
        download_dir = os.path.join(os.getcwd(), "downloaded_files")
        os.makedirs(download_dir, exist_ok=True)
        download_path = os.path.join(download_dir, filename)
        shutil.copy(save_path, download_path)
        
        return download_path
    except Exception as e:
        return str(e)

def get_pdf_url(url):
    arxiv_pattern = r"https://arxiv.org/abs/(\d+\.\d+)"
    arxiv_match = re.match(arxiv_pattern, url)
    if arxiv_match:
        return f"https://arxiv.org/pdf/{arxiv_match.group(1)}"
    return url if url.endswith(".pdf") else ""

def download_paper(title, pdf_url, save_path):
    """下載 PDF 並儲存至指定資料夾"""
    try:
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()
        
        sanitized_title = "".join([c for c in title if c.isalnum() or c in " _-"]).rstrip()
        pdf_filename = f"{sanitized_title}.pdf"
        pdf_path = os.path.join(save_path, pdf_filename)
        
        with open(pdf_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"PDF 下載完成: {pdf_path}")
    except Exception as e:
        print(f"下載 {title} 的 PDF 時發生錯誤: {e}")

def scholarly_search(topic, save_format, upper_limit, download_pdf):
    try:
        search_query = scholarly.search_pubs(topic)
        results = []
        topic_folder = preprocess_topic(topic)
        save_dir = os.path.join(os.path.expanduser("~/PAPER"), topic_folder)
        os.makedirs(save_dir, exist_ok=True)
        
        for paper in search_query:
            title = paper.get("bib", {}).get("title", "未知標題")
            pub_url = paper.get("pub_url", "")
            pdf_url = get_pdf_url(pub_url) if download_pdf else ""
            
            if pdf_url:
                download_paper(title, pdf_url, save_dir)
            
            author = paper.get("bib", {}).get("author", "未知作者")
            if isinstance(author, list):
                author = ", ".join(author)
            journal = paper.get("bib", {}).get("journal", "未知期刊")
            abstract = paper.get("bib", {}).get("abstract", "無摘要")
            
            apa_citation = f"{author}. ({datetime.now().year}). {title}. {journal}."
            
            results.append({
                "title": title,
                "author": author,
                "abstract": abstract,
                "journal": journal,
                "pub_url": pub_url,
                "pdf_url": pdf_url,
                "apa_citation": apa_citation
            })
            
            if len(results) >= upper_limit:
                break
        
        file_path = save_results_to_file(results, topic, save_format)
        return results, file_path if os.path.exists(file_path) else "無法儲存檔案"
    except Exception as e:
        return str(e), None

def download_file(file_path):
    return file_path

iface = gr.Interface(
    fn=scholarly_search,
    inputs=[
        gr.Textbox(label="研究主題"),
        gr.Radio(["txt", "json"], label="儲存格式", value="txt"),
        gr.Slider(10, 200, step=10, label="查詢數量", value=50),
        gr.Checkbox(label="下載 PDF", value=True)
    ],
    outputs=[
        gr.JSON(label="查詢結果"),
        gr.File(label="下載結果檔案")
    ],
    title="論文摘要下載助手",
    description="輸入研究主題，下載 Google Scholar 論文摘要與 APA 引用，儲存至使用者的 PAPER 資料夾，並下載 PDF（若可用）"
)

if __name__ == "__main__":
    iface.launch()
