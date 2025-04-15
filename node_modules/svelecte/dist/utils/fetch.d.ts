/**
 * Simple debouncer
 *
 * @param {function} fn
 * @param {number} delay
 * @returns fn
 */
export function debounce(fn: Function, delay: number): (...args: any[]) => void;
export function requestFactory(query: string, props: {
    url: string | null;
    parentValue: string | number | null | undefined;
    initial: string | number | string[] | null;
}, fetchProps: RequestInit | object): {
    request: Request;
    controller: AbortController;
};
export type RequestFactoryFn = (query: string, props: {
    url: string | null;
    parentValue: string | number | null | undefined;
    initial: string | number | string[] | null;
}, fetchProps: RequestInit | object) => {
    request: Request;
    controller: AbortController;
};
