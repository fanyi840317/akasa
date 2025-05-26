import { AFFINE_FORMAT_BAR_WIDGET, AffineFormatBarWidget } from "@blocksuite/blocks";



export function effects() {
    registerSpecs();
  
    stdEffects();
    inlineEffects();
  
    blockListEffects();
    blockParagraphEffects();
    blockEmbedEffects();
    blockSurfaceEffects();
    dataViewEffects();
    blockImageEffects();
    blockDatabaseEffects();
    blockSurfaceRefEffects();
    blockLatexEffects();
  
    componentCaptionEffects();
    componentContextMenuEffects();
    componentDatePickerEffects();
    componentPortalEffects();
    componentRichTextEffects();
    componentToolbarEffects();
    componentDragIndicatorEffects();
    componentToggleButtonEffects();
  
    widgetScrollAnchoringEffects();
    widgetMobileToolbarEffects();
    widgetLinkedDocEffects();
    widgetFrameTitleEffects();
    widgetEdgelessElementToolbarEffects();
    widgetCodeToolbarEffects();
  
    customElements.define('affine-database-title', DatabaseTitle);
    customElements.define(
      'affine-edgeless-bookmark',
      BookmarkEdgelessBlockComponent
    );
    customElements.define('affine-image', ImageBlockComponent);
    customElements.define('data-view-header-area-icon', IconCell);
    customElements.define('affine-database-link-cell', LinkCell);
    customElements.define('affine-database-link-cell-editing', LinkCellEditing);
    customElements.define('affine-bookmark', BookmarkBlockComponent);
    customElements.define('affine-edgeless-image', ImageEdgelessBlockComponent);
    customElements.define('data-view-header-area-text', HeaderAreaTextCell);
    customElements.define(
      'data-view-header-area-text-editing',
      HeaderAreaTextCellEditing
    );
    customElements.define('affine-code-unit', AffineCodeUnit);
    customElements.define('affine-database-rich-text-cell', RichTextCell);
    customElements.define(
      'affine-database-rich-text-cell-editing',
      RichTextCellEditing
    );
    customElements.define('affine-edgeless-text', EdgelessTextBlockComponent);
    customElements.define('center-peek', CenterPeek);
    customElements.define(
      'affine-edgeless-attachment',
      AttachmentEdgelessBlockComponent
    );
    customElements.define('database-datasource-note-renderer', NoteRenderer);
    customElements.define('database-datasource-block-renderer', BlockRenderer);
    customElements.define('affine-attachment', AttachmentBlockComponent);
    customElements.define('affine-latex', LatexBlockComponent);
    customElements.define('affine-page-root', PageRootBlockComponent);
    customElements.define('edgeless-note-mask', EdgelessNoteMask);
    customElements.define('affine-edgeless-note', EdgelessNoteBlockComponent);
    customElements.define('affine-preview-root', PreviewRootBlockComponent);
    customElements.define('affine-page-image', ImageBlockPageComponent);
    customElements.define('affine-code', CodeBlockComponent);
    customElements.define('affine-image-fallback-card', ImageBlockFallbackCard);
    customElements.define('mini-mindmap-preview', MiniMindmapPreview);
    customElements.define('affine-frame', FrameBlockComponent);
    customElements.define('mini-mindmap-surface-block', MindmapSurfaceBlock);
    customElements.define('affine-data-view', DataViewBlockComponent);
    customElements.define('affine-edgeless-root', EdgelessRootBlockComponent);
    customElements.define('affine-divider', DividerBlockComponent);
    customElements.define('edgeless-copilot-panel', EdgelessCopilotPanel);
    customElements.define(
      'edgeless-copilot-toolbar-entry',
      EdgelessCopilotToolbarEntry
    );
    customElements.define(
      'affine-edgeless-surface-ref',
      EdgelessSurfaceRefBlockComponent
    );
    customElements.define(
      'edgeless-color-custom-button',
      EdgelessColorCustomButton
    );
    customElements.define('edgeless-connector-handle', EdgelessConnectorHandle);
    customElements.define('edgeless-zoom-toolbar', EdgelessZoomToolbar);
    customElements.define(
      'affine-edgeless-root-preview',
      EdgelessRootPreviewBlockComponent
    );
    customElements.define('affine-custom-modal', AffineCustomModal);
    customElements.define('affine-database', DatabaseBlockComponent);
    customElements.define('affine-surface-ref', SurfaceRefBlockComponent);
    customElements.define('pie-node-child', PieNodeChild);
    customElements.define('pie-node-content', PieNodeContent);
    customElements.define('pie-node-center', PieNodeCenter);
    customElements.define('pie-center-rotator', PieCenterRotator);
    customElements.define('affine-slash-menu', SlashMenu);
    customElements.define('inner-slash-menu', InnerSlashMenu);
    customElements.define('generating-placeholder', GeneratingPlaceholder);
    customElements.define('ai-finish-tip', AIFinishTip);
    customElements.define('ai-panel-divider', AIPanelDivider);
    customElements.define(NOTE_SLICER_WIDGET, NoteSlicer);
    customElements.define(
      EDGELESS_NAVIGATOR_BLACK_BACKGROUND_WIDGET,
      EdgelessNavigatorBlackBackgroundWidget
    );
    customElements.define('zoom-bar-toggle-button', ZoomBarToggleButton);
    customElements.define(
      EDGELESS_DRAGGING_AREA_WIDGET,
      EdgelessDraggingAreaRectWidget
    );
    customElements.define('icon-button', IconButton);
    customElements.define('affine-pie-menu', PieMenu);
    customElements.define('loader-element', Loader);
    customElements.define('edgeless-brush-menu', EdgelessBrushMenu);
    customElements.define(
      'surface-ref-generic-block-portal',
      SurfaceRefGenericBlockPortal
    );
    customElements.define('edgeless-brush-tool-button', EdgelessBrushToolButton);
    customElements.define(
      'edgeless-connector-tool-button',
      EdgelessConnectorToolButton
    );
    customElements.define('affine-pie-node', PieNode);
    customElements.define(
      'edgeless-default-tool-button',
      EdgelessDefaultToolButton
    );
    customElements.define('surface-ref-note-portal', SurfaceRefNotePortal);
    customElements.define('edgeless-connector-menu', EdgelessConnectorMenu);
    customElements.define('smooth-corner', SmoothCorner);
    customElements.define('toggle-switch', ToggleSwitch);
    customElements.define('ai-panel-answer', AIPanelAnswer);
    customElements.define('ai-item-list', AIItemList);
    customElements.define(
      'edgeless-eraser-tool-button',
      EdgelessEraserToolButton
    );
    customElements.define('edgeless-frame-menu', EdgelessFrameMenu);
    customElements.define('edgeless-frame-tool-button', EdgelessFrameToolButton);
    customElements.define('ai-panel-input', AIPanelInput);
    customElements.define('ai-panel-generating', AIPanelGenerating);
    customElements.define('ai-item', AIItem);
    customElements.define('ai-sub-item-list', AISubItemList);
    customElements.define('edgeless-link-tool-button', EdgelessLinkToolButton);
    customElements.define('embed-card-more-menu', EmbedCardMoreMenu);
    customElements.define('edgeless-mindmap-menu', EdgelessMindmapMenu);
    customElements.define('embed-card-style-menu', EmbedCardStyleMenu);
    customElements.define('edgeless-lasso-tool-button', EdgelessLassoToolButton);
    customElements.define('affine-filterable-list', FilterableListComponent);
    customElements.define('ai-panel-error', AIPanelError);
    customElements.define(
      EDGELESS_SELECTED_RECT_WIDGET,
      EdgelessSelectedRectWidget
    );
    customElements.define('mindmap-import-placeholder', MindMapPlaceholder);
    customElements.define(
      'edgeless-note-senior-button',
      EdgelessNoteSeniorButton
    );
    customElements.define('edgeless-align-panel', EdgelessAlignPanel);
    customElements.define('card-style-panel', CardStylePanel);
    customElements.define(
      'embed-card-caption-edit-modal',
      EmbedCardEditCaptionEditModal
    );
    customElements.define('edgeless-color-button', EdgelessColorButton);
    customElements.define('edgeless-color-panel', EdgelessColorPanel);
    customElements.define('edgeless-text-color-icon', EdgelessTextColorIcon);
    customElements.define('embed-card-create-modal', EmbedCardCreateModal);
    customElements.define('embed-card-edit-modal', EmbedCardEditModal);
    customElements.define(
      'edgeless-mindmap-tool-button',
      EdgelessMindmapToolButton
    );
    customElements.define('edgeless-note-tool-button', EdgelessNoteToolButton);
    customElements.define('edgeless-note-menu', EdgelessNoteMenu);
    customElements.define('edgeless-line-width-panel', EdgelessLineWidthPanel);
    customElements.define('affine-database-link-node', LinkNode);
    customElements.define(
      'edgeless-frame-order-button',
      EdgelessFrameOrderButton
    );
    customElements.define('edgeless-frame-order-menu', EdgelessFrameOrderMenu);
    customElements.define(
      'edgeless-auto-complete-panel',
      EdgelessAutoCompletePanel
    );
    customElements.define(
      'edgeless-navigator-setting-button',
      EdgelessNavigatorSettingButton
    );
    customElements.define('edgeless-present-button', EdgelessPresentButton);
    customElements.define('edgeless-color-picker', EdgelessColorPicker);
    customElements.define('overlay-scrollbar', OverlayScrollbar);
    customElements.define('affine-note', NoteBlockComponent);
    customElements.define('affine-template-loading', AffineTemplateLoading);
    customElements.define(
      'edgeless-color-picker-button',
      EdgelessColorPickerButton
    );
    customElements.define('edgeless-auto-complete', EdgelessAutoComplete);
    customElements.define(
      'edgeless-font-weight-and-style-panel',
      EdgelessFontWeightAndStylePanel
    );
    customElements.define('edgeless-note-shadow-panel', EdgelessNoteShadowPanel);
    customElements.define('edgeless-templates-panel', EdgelessTemplatePanel);
    customElements.define('edgeless-text-menu', EdgelessTextMenu);
    customElements.define('edgeless-template-button', EdgelessTemplateButton);
    customElements.define('edgeless-tool-icon-button', EdgelessToolIconButton);
    customElements.define('edgeless-size-panel', EdgelessSizePanel);
    customElements.define('edgeless-scale-panel', EdgelessScalePanel);
    customElements.define('edgeless-font-family-panel', EdgelessFontFamilyPanel);
    customElements.define('edgeless-shape-panel', EdgelessShapePanel);
    customElements.define('note-display-mode-panel', NoteDisplayModePanel);
    customElements.define('edgeless-toolbar-button', EdgelessToolbarButton);
    customElements.define('frame-preview', FramePreview);
    customElements.define('bookmark-card', BookmarkCard);
    customElements.define('presentation-toolbar', PresentationToolbar);
    customElements.define('edgeless-shape-menu', EdgelessShapeMenu);
    customElements.define('stroke-style-panel', StrokeStylePanel);
    customElements.define('edgeless-shape-tool-button', EdgelessShapeToolButton);
    customElements.define(
      'edgeless-connector-label-editor',
      EdgelessConnectorLabelEditor
    );
    customElements.define('block-zero-width', BlockZeroWidth);
    customElements.define(
      'edgeless-shape-tool-element',
      EdgelessShapeToolElement
    );
    customElements.define('edgeless-shape-text-editor', EdgelessShapeTextEditor);
    customElements.define(
      'edgeless-group-title-editor',
      EdgelessGroupTitleEditor
    );
    customElements.define('affine-drag-preview', DragPreview);
    customElements.define(EDGELESS_TOOLBAR_WIDGET, EdgelessToolbarWidget);
    customElements.define('edgeless-shape-style-panel', EdgelessShapeStylePanel);
    customElements.define(
      'edgeless-frame-title-editor',
      EdgelessFrameTitleEditor
    );
    customElements.define(
      'edgeless-one-row-color-panel',
      EdgelessOneRowColorPanel
    );
    customElements.define('edgeless-text-editor', EdgelessTextEditor);
    customElements.define('affine-image-toolbar', AffineImageToolbar);
    customElements.define('affine-drop-indicator', DropIndicator);
    customElements.define('mini-mindmap-root-block', MindmapRootBlock);
    customElements.define('affine-block-selection', BlockSelection);
    customElements.define('menu-divider', MenuDivider);
    customElements.define('edgeless-slide-menu', EdgelessSlideMenu);
    customElements.define(
      'edgeless-toolbar-shape-draggable',
      EdgelessToolbarShapeDraggable
    );
  
    customElements.define(AFFINE_AI_PANEL_WIDGET, AffineAIPanelWidget);
    customElements.define(AFFINE_EMBED_CARD_TOOLBAR_WIDGET, EmbedCardToolbar);
    customElements.define(AFFINE_INNER_MODAL_WIDGET, AffineInnerModalWidget);
    customElements.define(
      AFFINE_DOC_REMOTE_SELECTION_WIDGET,
      AffineDocRemoteSelectionWidget
    );
    customElements.define(AFFINE_MODAL_WIDGET, AffineModalWidget);
    customElements.define(
      AFFINE_PAGE_DRAGGING_AREA_WIDGET,
      AffinePageDraggingAreaWidget
    );
    customElements.define(AFFINE_DRAG_HANDLE_WIDGET, AffineDragHandleWidget);
    customElements.define(AFFINE_PIE_MENU_WIDGET, AffinePieMenuWidget);
    customElements.define(AFFINE_EDGELESS_COPILOT_WIDGET, EdgelessCopilotWidget);
  
    customElements.define(AFFINE_IMAGE_TOOLBAR_WIDGET, AffineImageToolbarWidget);
    customElements.define(AFFINE_SLASH_MENU_WIDGET, AffineSlashMenuWidget);
    customElements.define(
      AFFINE_EDGELESS_REMOTE_SELECTION_WIDGET,
      EdgelessRemoteSelectionWidget
    );
    customElements.define(
      AFFINE_VIEWPORT_OVERLAY_WIDGET,
      AffineViewportOverlayWidget
    );
    customElements.define(
      AFFINE_EDGELESS_ZOOM_TOOLBAR_WIDGET,
      AffineEdgelessZoomToolbarWidget
    );
    customElements.define(AFFINE_SURFACE_REF_TOOLBAR, AffineSurfaceRefToolbar);
    customElements.define(
      AFFINE_EDGELESS_AUTO_CONNECT_WIDGET,
      EdgelessAutoConnectWidget
    );
    customElements.define(AFFINE_FORMAT_BAR_WIDGET, AffineFormatBarWidget);
  }