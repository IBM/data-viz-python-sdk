export const MAX_FILE_SIZE = 20 // MB

export const MAX_FILE_SIZE_TEXT = `${MAX_FILE_SIZE}MB`;

export const DATA_TYPES = [
  { id: 'adjcategory', description: 'Two independent lists (ex: A, A, A, B, B and A, C, B, A, A)' },
  { id: 'category', description: 'category - Items that are grouped/labeled as categories (ex: A, A, A, B, B, B, C, C, ...)' },
  { id: 'currency', description: 'An integer or float with a valid currency symbol' },
  { id: 'date', description: 'Units measured in time as a date (ex: yyyy-mm-dd)' },
  { id: 'datetime', description: 'Units measured in time with a date (ex: yyyy-mm-dd hh:mm:ss)' },
  { id: 'datetimestamp', description: ' Units measured in time (can include milliseconds) with a date (ex: yyyy-mm-dd hh:mm:ss)' },
  { id: 'float', description: 'A decimal value using the . as the decimal separator and a , optional as the thousands separator' },
  { id: 'indcategory', description: 'Two or more columns of independent categoric data i.e. the categories have no relation to each other' },
  { id: 'int', description: 'A whole number value using the , optional as the thousands separator' },
  { id: 'intlfloat', description: 'A decimal value using the , as the decimal separator and a . optional as the thousands separator' },
  { id: 'intlint', description: 'A whole number value using the . optional as the thousands separator' },
  { id: 'nestcategory', description: 'Two or more categoric data nested (ex: A -> a1, A -> a1, A -> a2, B -> b1, B -> b2)' },
  { id: 'subcategory', description: 'Categoric data ordered in sub groups (ex: A -> a, A -> a, A -> b, B -> a, B -> a)' },
  { id: 'time', description: 'units measured in hours, minutes, seconds (ex: hh:mm:ss)' }
];