
export class Config {
  static get CONFIG() : {[key:string]:string} {
    return {
      API_GATEWAY_URL: '$VITE_API_GATEWAY_URL',
      TEMP_ACCESS_TOKEN: '$VITE_TEMP_ACCESS_TOKEN',
    };
  }

  static value(key: string) {
    if (!(key in this.CONFIG)) {
      console.error(`Config: There is no key named "${key}"`);
      return '';
    }

    const value = this.CONFIG[key];

    if (!value) {
      console.error(`Config: Value for "${key}" is not defined`);
      return '';
    }

    if (!value.startsWith('$VITE_')) {
      // value was already replaced, it seems we are in production (containerized).
      return value;
    }

    // value was not replaced, it seems we are in development.
    // Remove $ and get current value from import.meta.env
    const envName = value.substring(1);
    const envValue = import.meta.env[envName];
    if (!envValue) {
      console.error(`Config: Environment variable "${envName}" is not defined`);
      return '';
    }

    return envValue;
  }

  static valueBool(key: string) {
    const value = Config.value(key);
    if (value === null) {
      return false;
    }

    if (value.toLowerCase() === 'true') {
      return true;
    }

    return false;
  }
}
