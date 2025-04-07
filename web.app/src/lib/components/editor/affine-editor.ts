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
import { json } from "@sveltejs/kit";

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


export async function createDocByJson(jsonStr: string) {

  const schema = new Schema().register(AffineSchemas);
  const collection = new DocCollection({ schema });
  collection.meta.initialize();
  const job = new Job({collection});
  const doc = job.snapshotToDoc(JSON.parse(jsonStr));
 
  return doc;
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

export async function exportDocToJson(doc: Doc) {
  const job = new Job({
    collection: doc.collection
  });
  const snapshot = job.docToSnapshot(doc);

  return { content: JSON.stringify(snapshot), title: doc.meta?.title };
}