/**
 * @typedef {object} ExtButton
 * @property {object?} [bound_item]
 *
 * @param {HTMLElement & ExtButton} node
 * @param {object} selectedObject
 */
export function bindItem(node: HTMLElement & ExtButton, selectedObject: object): {
    destroy: () => void;
};
export type ExtButton = {
    bound_item?: object | null;
};
