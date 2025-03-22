import { AffineEditorContainer,PageEditor } from '@blocksuite/presets';
import { Doc, Schema } from '@blocksuite/store';
import { DocCollection } from '@blocksuite/store';
import { AffineSchemas } from '@blocksuite/blocks';

export interface AppState {
  editor: AffineEditorContainer;
  collection: DocCollection;
}


