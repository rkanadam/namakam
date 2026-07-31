declare const process: any;

export const environment = {
  production: false,
  enableEditor: (typeof process !== 'undefined' && process?.env?.['ENABLE_EDITOR'] === 'true') || false
};
