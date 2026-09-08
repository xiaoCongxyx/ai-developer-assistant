from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

# 文件实际存储目录。
#
# Path(__file__)：
# 当前 Python 文件路径
#
# parent.parent.parent：
# 回到 backend 目录
#
# / "storage" / "documents"：
# 得到实际文件存储目录。

BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENT_STORSGE_DIR = BASE_DIR / "storage" / "documents"

# 程序启动/第一次保存文件时，
# 如果目录不存在就自动创建。
DOCUMENT_STORSGE_DIR.mkdir(
  parents=True,
  exist_ok=True
)

def generate_storage_filename(original_filename: str) -> str:
    """
    根据原始文件名生成唯一存储文件名。
    """

    # 获取文件扩展名
    suffix = Path(original_filename).suffix.lower()

    # 生成唯一文件名
    filename = f"{uuid4().hex()}{suffix}"

    return filename


async def save_upload_file(file: UploadFile, max_size: int) -> tuple[str, int]:
    """
    保存上传文件。

    返回：
    (文件路径, 文件大小)
    """

    # UploadFile.filename 是客户端提供的原始文件名。
    #
    # 它只能作为“文件信息”使用，
    # 不能直接作为服务器最终保存文件名。

    original_filename = file.filename or "unknown"

    storage_filename = generate_storage_filename(original_filename)

    storage_path = DOCUMENT_STORSGE_DIR / storage_filename

    file_size = 0

    # 保存文件
    # 打开 storage_path 指向的文件，以二进制写入模式操作，并把这个文件对象命名为 buffer；离开代码块后自动关闭文件 
    # storage_path：Path对象  w：write 写入模式 b：binary 二进制模式 ws：以二进制写入模式打开文件 with: 自动管理资源，用完自动释放
    try:
        with storage_path.open("wb") as buffer:
            # 海象运算符（Assignment Expression）chunk = await file.read(1024 * 1024) while chunk:
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)

                # 在真正写入磁盘之前检查大小。
                if file_size > max_size:
                    raise ValueError(
                      "文件大小超过限制"
                    )

                buffer.write(chunk)

    except Exception:
        # 如果保存过程中发生异常，
        # 删除已经创建的临时文件。
        if storage_path.exists():
            storage_path.unlink()

        raise

    # 获取实际文件大小
    file_size = storage_path.stat().st_size

    # 返回相对路径，而不是把服务器绝对路径暴露给前端。
    relative_path = str(
      Path("storage") / "documents" / storage_filename
    )

    return relative_path, file_size

def get_storage_path(relative_path: str) -> Path:
    """
    将数据库保存的相对路径转换为实际文件路径。
    """

    return BASE_DIR / relative_path