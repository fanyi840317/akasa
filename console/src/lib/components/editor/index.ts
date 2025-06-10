// 导出包装后的 BlocksuiteEditor 组件
export { default as BlocksuiteEditor } from './blocksuite-wrapper.svelte';

// 导出其他编辑器相关函数
export {
  createDocByHtml,
  createDocByJson,
  exportDoc,
  exportDocToJson,
  exportDocToMarkdown,
  downloadDocAsMarkdown,
  createDocByMarkdown
} from './editor';