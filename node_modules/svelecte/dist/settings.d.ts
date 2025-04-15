export default settings;
export type i18n_max = (max: number) => string;
export type i18n_fetchQuery = (minQuery: number, inputLength: number) => string;
export type i18n_collapsedSelection = (count: number) => string;
export type i18n_createRowLabel = (value: string) => string;
export type i18n_aria_selection = (opts: string[]) => string;
export type i18n_aria_listActive = (opt: object, labelField: string, resultCount: number) => string;
export type i18n_aria_inputFocus = () => string;
export type i18n_aria_removeItemLabel = (item: object, labelField: string) => string;
export type I18nObject = {
    empty: string;
    nomatch: string;
    max: i18n_max;
    fetchBefore: string;
    fetchQuery: i18n_fetchQuery;
    fetchInit: string;
    fetchEmpty: string;
    collapsedSelection: i18n_collapsedSelection;
    createRowLabel: i18n_createRowLabel;
    emptyCreatable: string;
    aria_selected: i18n_aria_selection;
    aria_listActive: i18n_aria_listActive;
    aria_inputFocused: i18n_aria_inputFocus;
    aria_removeItemLabel: i18n_aria_removeItemLabel;
    aria_label: string;
    aria_describedby: string;
};
export type Settings = {
    valueField: string | null;
    labelField: string | null;
    groupLabelField: string;
    groupItemsField: string;
    disabledField: string;
    placeholder: string;
    valueAsObject: boolean;
    searchable: boolean;
    clearable: boolean;
    highlightFirstItem: boolean;
    selectOnTab: boolean | "select-navigate";
    resetOnBlur: boolean;
    resetOnSelect: boolean;
    fetchProps: object;
    fetchResetOnBlur: boolean;
    fetchDebounceTime: number;
    multiple: boolean;
    closeAfterSelect: boolean | string;
    deselectMode: "native" | "toggle" | "none";
    max: number;
    collapseSelection: "blur" | "always" | null;
    keepSelectionInList: "auto" | boolean;
    creatable: boolean;
    creatablePrefix: string;
    keepCreated: boolean;
    allowEditing: boolean;
    delimiter: string;
    fetchCallback?: Function | undefined;
    minQuery: number;
    lazyDropdown: boolean;
    virtualList: boolean;
    vlItemSize?: number | undefined;
    i18n: I18nObject;
    requestFactory: import("./utils/fetch").RequestFactoryFn;
};
/**
 * @callback i18n_max
 * @param {number} max
 * @returns {string}
 *
 * @callback i18n_fetchQuery
 * @param {number} minQuery
 * @param {number} inputLength
 * @returns {string}
 *
 * @callback i18n_collapsedSelection
 * @param {number} count
 * @returns {string}
 *
 * @callback i18n_createRowLabel
 * @param {string} value
 * @returns {string}
 *
 * @callback i18n_aria_selection
 * @param {string[]} opts
 * @returns {string}
 *
 * @callback i18n_aria_listActive
 * @param {object} opt
 * @param {string} labelField
 * @param {number} resultCount
 * @returns {string}
 *
 * @callback i18n_aria_inputFocus
 * @returns {string}
 *
 * @callback i18n_aria_removeItemLabel
 * @param {object} item
 * @param {string} labelField
 * @returns {string}
 *
 *
 * @typedef {object} I18nObject
 * @property {string} empty
 * @property {string} nomatch
 * @property {i18n_max} max
 * @property {string} fetchBefore
 * @property {i18n_fetchQuery} fetchQuery
 * @property {string} fetchInit
 * @property {string} fetchEmpty
 * @property {i18n_collapsedSelection} collapsedSelection
 * @property {i18n_createRowLabel} createRowLabel
 * @property {string} emptyCreatable
 * @property {i18n_aria_selection} aria_selected
 * @property {i18n_aria_listActive} aria_listActive
 * @property {i18n_aria_inputFocus} aria_inputFocused
 * @property {i18n_aria_removeItemLabel} aria_removeItemLabel
 * @property {string} aria_label
 * @property {string} aria_describedby
 *
 * @typedef {object} Settings
 * @property {string|null} valueField
 * @property {string|null} labelField
 * @property {string} groupLabelField
 * @property {string} groupItemsField
 * @property {string} disabledField
 * @property {string} placeholder
 * @property {boolean} valueAsObject
 * @property {boolean} searchable
 * @property {boolean} clearable
 * @property {boolean} highlightFirstItem
 * @property {boolean|'select-navigate'} selectOnTab
 * @property {boolean} resetOnBlur
 * @property {boolean} resetOnSelect
 * @property {object} fetchProps
 * @property {boolean} fetchResetOnBlur
 * @property {number} fetchDebounceTime
 * @property {boolean} multiple
 * @property {boolean|string} closeAfterSelect
 * @property {'native'|'toggle'|'none'} deselectMode
 * @property {number} max
 * @property {'blur'|'always'|null} collapseSelection
 * @property {'auto'|boolean} keepSelectionInList
 * @property {boolean} creatable
 * @property {string} creatablePrefix
 * @property {boolean} keepCreated
 * @property {boolean} allowEditing
 * @property {string} delimiter
 * @property {function|undefined} [fetchCallback]
 * @property {number} minQuery
 * @property {boolean} lazyDropdown
 * @property {boolean} virtualList
 * @property {number|undefined} [vlItemSize]
 * @property {I18nObject} i18n
 * @property {import("./utils/fetch").RequestFactoryFn} requestFactory
 */
declare const settings: Settings;
