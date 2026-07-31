declare const process: any;

export const environment = {
  production: true,
  enableEditor: (typeof process !== 'undefined' && process?.env?.['ENABLE_EDITOR'] === 'true') || false
};
