export default VirtualList;
type VirtualList = {
    $on?(type: string, callback: (e: any) => void): () => void;
    $set?(props: Partial<$$ComponentProps>): void;
} & {
    resolveItemSize: () => number;
};
declare const VirtualList: import("svelte").Component<{
    itemCount: any;
    maxHeight: any;
    itemHeight?: any;
    scrollToIndex: any;
    children: any;
}, {
    resolveItemSize: () => number;
}, "">;
type $$ComponentProps = {
    itemCount: any;
    maxHeight: any;
    itemHeight?: any;
    scrollToIndex: any;
    children: any;
};
