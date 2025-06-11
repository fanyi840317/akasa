// 直接导出 BlocksuiteEditor 组件
export { default as BlocksuiteEditor } from './blocksuite-editor.svelte';

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