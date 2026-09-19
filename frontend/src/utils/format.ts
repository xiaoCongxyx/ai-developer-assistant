/**
 * 
 * @param isoStr 
 * @returns 
 */
export const formatDateTime = (isoStr?: string) => {
  if (!isoStr) return '—'
  return new Date(isoStr).toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  })
}

/**
 * 格式化字节数 → 友好显示
 * 1024 → 1 KB, 2097152 → 2 MB
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}
