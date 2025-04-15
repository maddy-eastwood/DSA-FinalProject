/**
 *
 * @param {object} item
 * @param {boolean} renderInSelection
 * @param {string} inputValue
 * @param {function} itemRenderer
 * @param {boolean} disableHighlight
 * @returns {string}
 */
export function highlightSearch(item: object, renderInSelection: boolean, inputValue: string, itemRenderer: Function, disableHighlight: boolean): string;
/**
 * Detect Mac device
 *
 * @returns {boolean}
 */
export function iOS(): boolean;
/**
 * Detects if on android device
 *
 * @returns {boolean}
 */
export function android(): boolean;
/**
 * Internal formatter of newly created items
 *
 * @param {string} enteredValue
 * @returns {string}
 */
export function onCreate_helper(enteredValue: string): string;
/**
 * Escape HTML
 * @param {string} html
 * @returns {string}
 */
export function escapeHtml(html: string): string;
