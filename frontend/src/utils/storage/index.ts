export const storage = {
  set<T>(key: string, value: T) {
    localStorage.setItem(key, JSON.stringify(value))
  },

  get<T>(key: string): T | null {
    const data = localStorage.getItem(key)

    if (!data) return null

    try {
      return JSON.parse(data) as T
    } catch (error) {
      console.error('Storage parse error:', error)
      return null
    }
  },

  remove(key: string) {
    localStorage.removeItem(key)
  },

  clear() {
    localStorage.clear()
  },
}
