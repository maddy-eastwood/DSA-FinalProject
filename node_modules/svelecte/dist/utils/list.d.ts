/**
 * @typedef {object} ComponentConfig
 * @property {boolean} optionsWithGroups
 * @property {string} valueField
 * @property {string} labelField
 * @property {string} optLabel
 * @property {string} optItems
 * @property {string[]} optionProps
 */
/**
 * @typedef {object} SortDef
 * @property {string} field
 * @property {'asc'|'desc'} [direction]
 *
 * @typedef {object} SearchProps
 * @property {string|string[]} [fields]
 * @property {string|SortDef[]} [sort]
 * @property {boolean} [keepSelectionInList]
 * @property {boolean} [nesting]
 * @property {'or'} [conjunction]
 * @property {boolean} [skipSort]
 * @property {boolean} [startOnly]
 * @property {boolean} [wordsOnly]
 * @property {boolean} [disabled]
 */
/**
 * @param {string} valueField
 * @param {string} labelField
 * @param {string} optLabel
 * @param {string} optItems
 * @returns {ComponentConfig}
 */
export function createConfig(valueField: string, labelField: string, optLabel: string, optItems: string): ComponentConfig;
/**
 * @param {array} options
 * @param {array|null|object} initialValue
 * @param {boolean} valueAsObject
 * @param {string} valueField
 */
export function initSelection(options: any[], initialValue: any[] | null | object, valueAsObject: boolean, valueField: string): any[];
/**
 *
 * @param {object[]|string[]} options
 * @param {string?} valueField
 * @param {string?} labelField
 * @returns {object[]}
 */
export function ensureObjectArray(options: object[] | string[], valueField: string | null, labelField: string | null): object[];
/**
 *
 * @param {object[]} options
 * @param {ComponentConfig} config
 * @returns
 */
export function flatList(options: object[], config: ComponentConfig): any;
/**
 *
 * @param {object} object
 * @returns {string[]}
 */
export function getFilterProps(object: object): string[];
/**
 *
 * @param {object[]} options
 * @param {?string} inputValue
 * @param {?Set} excludeSelected
 * @param {ComponentConfig} config
 * @param {SearchProps} searchProps
 * @returns {object[]}
 */
export function filterList(options: object[], inputValue: string | null, excludeSelected: Set<any> | null, config: ComponentConfig, searchProps?: SearchProps): object[];
/**
 * Automatic setter for 'valueField' or 'labelField' when they are not set
 *
 * @param {string} type
 * @param {array} options
 * @param {string?} groupItemsField
 */
export function fieldInit(type: string, options: any[], groupItemsField: string | null): string;
export type ComponentConfig = {
    optionsWithGroups: boolean;
    valueField: string;
    labelField: string;
    optLabel: string;
    optItems: string;
    optionProps: string[];
};
export type SortDef = {
    field: string;
    direction?: "asc" | "desc";
};
export type SearchProps = {
    fields?: string | string[];
    sort?: string | SortDef[];
    keepSelectionInList?: boolean;
    nesting?: boolean;
    conjunction?: "or";
    skipSort?: boolean;
    startOnly?: boolean;
    wordsOnly?: boolean;
    disabled?: boolean;
};
