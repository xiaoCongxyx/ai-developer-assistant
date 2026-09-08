from pathlib import Path

# 当前系统允许上传的文件扩展名。
#
# 使用 集合 Set ALLOWED_FILE_EXTENSIONS 是因为我们主要关心：
# “这个扩展名是否存在于允许列表中”。
ALLOWED_FILE_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}

# 当前阶段最大文件大小：
# 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

def validate_file_extension(filename: str) -> None:
    """
    校验文件扩展名。
    """

    suffer = Path(filename).suffix.lower()

    if suffer not in ALLOWED_FILE_EXTENSIONS:
        raise ValueError(
            "不支持的文件类型，仅支持 PDF、TXT、Markdown"
        )

def validate_file_size(file_size: int) -> None:
    """
    校验文件大小。
    """

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            "文件大小不能超过 10 MB"
        )