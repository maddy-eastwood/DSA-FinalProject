/**
 * @param {HTMLDivElement} element
 * @param {string} prop
 * @returns {number}
 */
export function pixelGetter(element: HTMLDivElement, prop: string): number;
/**
 * @param {boolean} isOpened
 * @param {HTMLDivElement} scrollContainer
 * @param {boolean} renderDropdown
 * @returns {void}
 */
export function positionDropdown(isOpened: boolean, scrollContainer: HTMLDivElement, renderDropdown: boolean): void;
/**
 * @typedef {object} ScrollParams
 * @property {HTMLDivElement} container
 * @property {HTMLDivElement} scrollContainer
 * @property {boolean} virtualList
 * @property {boolean} center
 *
 * @param {ScrollParams} params
 * @param {number} dropdownIndex
 * @returns
 */
export function scrollIntoView({ container, scrollContainer, virtualList, center }: ScrollParams, dropdownIndex: number): void;
export type outValue = {
    top: boolean;
    left: boolean;
    bottom: boolean;
    right: boolean;
    any: boolean;
};
export type ScrollParams = {
    container: HTMLDivElement;
    scrollContainer: HTMLDivElement;
    virtualList: boolean;
    center: boolean;
};
