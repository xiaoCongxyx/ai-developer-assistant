from pathlib import Path
import pymupdf

def parse_pdf(file_path) -> str:
    """
    解析 PDF 文件并提取文本。
    """

    path = Path(file_path)

    # 数据库里保存的是相对路径：
    #
    # storage/documents/xxx.pdf
    #
    # 这里需要转换成服务器实际文件路径。
    document = pymupdf.open(path)

    try: 
        pages: list[str] = []

        for page in document:
            text = page.get_text()

            if text:
                pages.append(text)

        return "\n".join(pages)
    finally:
        document.close()


def parse_text_file(file_path: str) -> str:
    """
    解析 TXT / Markdown 文件。
    """

    path = Path(file_path)

    # TXT / Markdown 本质上都是文本文件，
    # 因此可以直接读取。

    return path.read_text(
        encoding="utf-8",
    )
