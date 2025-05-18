import {
    createAssetsArchive,
    defaultImageProxyMiddleware,
    docLinkBaseURLMiddleware,
    HtmlAdapter,
    MarkdownAdapter,
    titleMiddleware,
  } from "@blocksuite/blocks";
  import { Doc, Job } from "@blocksuite/store";
  
  import { AffineSchemas } from "@blocksuite/blocks/schemas";
  import { DocCollection, Schema } from "@blocksuite/store";
  
  export async function createDocByHtml(html: string) {
    const schema = new Schema().register(AffineSchemas);
    const collection = new DocCollection({ schema });
    collection.meta.initialize();
    // const doc = collection.createDoc();
    const job = new Job({
      collection,
      middlewares: [defaultImageProxyMiddleware, docLinkBaseURLMiddleware],
    });
    const htmlAdapter = new HtmlAdapter(job);
    console.log(html);
    const page = htmlAdapter.toDoc({
      file: html,
      assets: job.assetsManager,
    });
    if (!page) {
      return;
    }
    console.log(page);
    return page;
  }
  
  
  export async function createDocByJson(jsonStr: string,) {
  
    const schema = new Schema().register(AffineSchemas);
    const collection = new DocCollection({ schema });
    collection.meta.initialize();
    const job = new Job({collection});
    const doc = job.snapshotToDoc(JSON.parse(jsonStr));
  
    return doc;
  }
  
  export async function exportDoc(doc: Doc) {
    const job = new Job({
      collection: doc.collection,
      middlewares: [docLinkBaseURLMiddleware, titleMiddleware],
    });
    const snapshot = job.docToSnapshot(doc);
    const adapter = new HtmlAdapter(job);
    if (!snapshot) {
      return;
    }
    const htmlResult = await adapter.fromDocSnapshot({
      snapshot,
      assets: job.assetsManager,
    });
    return { content: htmlResult.file, title: doc.meta?.title };
  }
  
  export async function exportDocToJson(doc: Doc) {
    const job = new Job({
      collection: doc.collection
    });
    const snapshot = job.docToSnapshot(doc);
  
    return JSON.stringify(snapshot);
  }
  
  /**
   * 将文档导出为 Markdown 格式
   * @param doc 要导出的文档
   * @returns 返回包含 Markdown 内容的对象，如果有资源文件则打包为 zip
   */
  export async function exportDocToMarkdown(doc: Doc) {
    const job = new Job({
      collection: doc.collection,
      middlewares: [docLinkBaseURLMiddleware, titleMiddleware],
    });
    const snapshot = job.docToSnapshot(doc);
  
    const adapter = new MarkdownAdapter(job);
    if (!snapshot) {
      return;
    }
  
    const markdownResult = await adapter.fromDocSnapshot({
      snapshot,
      assets: job.assetsManager,
    });
  
    return {
      content: markdownResult.file,
      title: doc.meta?.title || 'Untitled',
      assetsIds: markdownResult.assetsIds,
      assets: job.assets
    };
  }
  
  /**
   * 将文档导出为 Markdown 并下载
   * @param doc 要导出的文档
   */
  export async function downloadDocAsMarkdown(doc: Doc) {
    const job = new Job({
      collection: doc.collection,
      middlewares: [docLinkBaseURLMiddleware, titleMiddleware],
    });
    const snapshot = job.docToSnapshot(doc);
  
    const adapter = new MarkdownAdapter(job);
    if (!snapshot) {
      return;
    }
  
    const markdownResult = await adapter.fromDocSnapshot({
      snapshot,
      assets: job.assetsManager,
    });
  
    let downloadBlob: Blob;
    const docTitle = doc.meta?.title || 'Untitled';
    let name: string;
    const contentBlob = new Blob([markdownResult.file], { type: 'plain/text' });
  
    if (markdownResult.assetsIds.length > 0) {
      if (!job.assets) {
        throw new Error('No assets found');
      }
      const zip = await createAssetsArchive(job.assets, markdownResult.assetsIds);
  
      await zip.file('index.md', contentBlob);
  
      downloadBlob = await zip.generate();
      name = `${docTitle}.zip`;
    } else {
      downloadBlob = contentBlob;
      name = `${docTitle}.md`;
    }
  
    // 创建下载链接并触发下载
    const url = URL.createObjectURL(downloadBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
  
  export async function createDocByMarkdown(markdown: string) {
    const schema = new Schema().register(AffineSchemas);
    const collection = new DocCollection({ schema });
    collection.meta.initialize();
    const job = new Job({
      collection,
      middlewares: [
        defaultImageProxyMiddleware,
        docLinkBaseURLMiddleware,
      ],
    });
    const mdAdapter = new MarkdownAdapter(job);
    const page = mdAdapter.toDoc({
      file: markdown,
      assets: job.assetsManager,
    });
  
    if (!page) {
      return;
    }
    console.log(page);
    return page;
  }
  
