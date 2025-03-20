import { AffineEditorContainer,PageEditor } from '@blocksuite/presets';
import { Doc, Schema } from '@blocksuite/store';
import { DocCollection } from '@blocksuite/store';
import { AffineSchemas } from '@blocksuite/blocks';

export interface AppState {
  editor: AffineEditorContainer;
  collection: DocCollection;
}

// export class test extends AffineEditorContainer {
    
// }

export function initEditor(docId: string = 'page1') {
  const schema = new Schema().register(AffineSchemas);
  const collection = new DocCollection({ schema });
  collection.meta.initialize();

  const doc = collection.createDoc({ id: docId });
  doc.load(() => {
    const pageBlockId = doc.addBlock('affine:page', {});
    doc.addBlock('affine:surface', {}, pageBlockId);
    const noteId = doc.addBlock('affine:note', {}, pageBlockId);
    doc.addBlock('affine:paragraph', {}, noteId);
  });

  const editor = new PageEditor();
  
  // Apply custom style
  
  editor.doc = doc;
//   editor.slots.docLinkClicked.on(({ docId }) => {
//     const target = <Doc>collection.getDoc(docId);
//     editor.doc = target;
//   });
  return { editor, collection };
}
