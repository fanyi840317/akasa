import {
  createAssetsArchive,
  defaultImageProxyMiddleware,
  docLinkBaseURLMiddleware,
  HtmlAdapter,
  titleMiddleware,
} from "@blocksuite/blocks";
import { Block, Doc, Job, toJSON } from "@blocksuite/store";

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

export async function exportDocToJson(doc: Doc) {
  try {
    // 获取文档的 JSON 数据
    const json = toJSON(doc);
    
    // 序列化为字符串
    const jsonStr = JSON.stringify(json);
    
    return jsonStr;
  } catch (error) {
    console.error("导出文档失败:", error);
    throw error;
  }
}

export async function createDocByJson(jsonStr: string) {
  try {
    // 解析 JSON 字符串
    const json = JSON.parse(jsonStr);
    
    // 创建新的文档实例
    const doc = new Doc(json.id || 'doc');
    
    doc.schema.toJSON();
    // 从 JSON 数据恢复文档
    Object.assign(doc, json);
    
    return doc;
  } catch (error) {
    console.error("创建文档失败:", error);
    throw error;
  }
}

export async function exportDoc(doc: any) {
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
