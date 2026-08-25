export const generateTitle = (content: string) => {
  // 去除首位空格 合并多余空白
  const title = content.trim().replace(/\s+/g, ' ')

  if(title.length <= 20) {
    return title
  }

  return title.slice(0, 20) + '...'
}