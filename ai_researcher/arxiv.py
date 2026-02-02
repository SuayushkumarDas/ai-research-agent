import requests
import xml.etree.ElementTree as ET


def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    query = "+".join(topic.lower().split())

    url = (
        "https://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )

    headers = {
        "User-Agent": "ai-researcher/0.1"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return parse_arxiv_xml(response.text)


def parse_arxiv_xml(xml_data: str) -> dict:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)
    entries = []

    for entry in root.findall("atom:entry", ns):
        authors = [
            author.findtext("atom:name", "", ns).strip()
            for author in entry.findall("atom:author", ns)
        ]

        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")

        entries.append({
            "title": entry.findtext("atom:title", "", ns).strip(),
            "summary": entry.findtext("atom:summary", "", ns).strip(),
            "authors": authors,
            "pdf": pdf_link,
        })

    return {"entries": entries}
