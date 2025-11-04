class _storage {
  storage: Storage
  constructor(s: Storage) {
    this.storage = s
  }

  setItem = (name: string, value: any) => {
    if (value === null) {
      this.storage.setItem(name, value)
    } else if (typeof value === 'object') {
      const valueStr = JSON.stringify(value)
      this.storage.setItem(name, valueStr)
    } else {
      this.storage.setItem(name, value)
    }
  }

  getItem = (name: string) => {
    let ret = this.storage.getItem(name)
    if (ret && (ret.startsWith('{') || ret.startsWith('['))) {
      ret = JSON.parse(ret)
    }
    return ret
  }

  removeItem = (name: string) => {
    this.storage.removeItem(name)
  }
}

export const SessionStorage = new _storage(window.sessionStorage)

export const LocalStorage = new _storage(window.localStorage)
