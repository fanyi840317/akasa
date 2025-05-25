import { WithDisposable } from '@blocksuite/global/utils';
import { css, html, LitElement, nothing } from 'lit';
import { property, state } from 'lit/decorators.js';
import { repeat } from 'lit/directives/repeat.js';
import { styleMap } from 'lit/directives/style-map.js';

export class EdgelessTemplatePanel extends WithDisposable(LitElement) {
  static override styles = css`
    :host {
      position: absolute;
      z-index: 1;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    .edgeless-templates-panel {
      width: 400px;
      max-height: 500px;
      border-radius: 8px;
      background: white;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
      border: 1px solid #e5e7eb;
    }

    .tabs {
      display: flex;
      border-bottom: 1px solid #e5e7eb;
    }

    .tab {
      padding: 12px 16px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      color: #6b7280;
      border-bottom: 2px solid transparent;
    }

    .tab:hover {
      color: #111827;
    }

    .tab-active {
      color: #111827;
      border-bottom-color: #3b82f6;
    }

    .tab-content {
      padding: 16px;
    }

    .search-bar {
      padding: 12px 16px;
      border-bottom: 1px solid #e5e7eb;
    }

    .search-input {
      width: 100%;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #e5e7eb;
      font-size: 14px;
    }

    .search-input:focus {
      outline: none;
      border-color: #3b82f6;
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }

    .image-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      padding: 8px;
    }

    .image-item {
      aspect-ratio: 16/9;
      border-radius: 4px;
      overflow: hidden;
      cursor: pointer;
      border: 1px solid transparent;
    }

    .image-item:hover {
      border-color: #3b82f6;
    }

    .image-item img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .link-input-container {
      padding: 16px;
    }

    .link-input {
      width: 100%;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #e5e7eb;
      font-size: 14px;
      margin-bottom: 8px;
    }

    .link-input:focus {
      outline: none;
      border-color: #3b82f6;
    }

    .submit-button {
      background: #3b82f6;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 14px;
      cursor: pointer;
    }

    .submit-button:disabled {
      background: #e5e7eb;
      cursor: not-allowed;
    }

    .error-message {
      color: #ef4444;
      font-size: 12px;
      margin-top: 4px;
    }

    .loading-spinner {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100px;
      color: #6b7280;
    }

    .empty-state {
      text-align: center;
      padding: 20px;
      color: #6b7280;
    }

    .upload-button {
      display: block;
      margin: 16px auto 0;
      padding: 8px 16px;
      background: #3b82f6;
      color: white;
      border-radius: 6px;
      text-align: center;
      cursor: pointer;
      width: fit-content;
    }

    .upload-button:hover {
      background: #2563eb;
    }

    .hidden {
      display: none;
    }
  `;

  static templates = builtInTemplates;

  private _fetchJob: null | { cancel: () => void } = null;

  private _closePanel() {
    this.dispatchEvent(new CustomEvent('closepanel'));
  }

  private _fetch(fn: (state: { canceled: boolean }) => Promise<unknown>) {
    if (this._fetchJob) {
      this._fetchJob.cancel();
    }

    this._loading = true;

    const state = { canceled: false };
    const job = {
      cancel: () => {
        state.canceled = true;
      },
    };

    this._fetchJob = job;

    fn(state)
      .catch(() => {})
      .finally(() => {
        if (!state.canceled && job === this._fetchJob) {
          this._loading = false;
          this._fetchJob = null;
        }
      });
  }

  private _getLocalSelectedCategory() {
    return null; // 移除edgeless相关代码
  }

  private async _initCategory() {
    try {
      this._categories = await EdgelessTemplatePanel.templates.categories();
      this._currentCategory =
        this._getLocalSelectedCategory() ?? this._categories[0];
      this._updateTemplates();
    } catch (e) {
      console.error('Failed to load categories', e);
    }
  }

  private _initDragController() {
    // 移除拖拽功能
  }

  private async _insertTemplate(template: Template, bound: Bound) {
    this._loadingTemplate = template;
    try {
      // 简化后的插入逻辑
      this.dispatchEvent(new CustomEvent('insert', { 
        detail: { template, bound }
      }));
    } finally {
      this._loadingTemplate = null;
    }
  }

  private _updateSearchKeyword(inputEvt: InputEvent) {
    this._searchKeyword = (inputEvt.target as HTMLInputElement).value;
    this._updateTemplates();
  }

  private _updateTemplates() {
    this._fetch(async state => {
      try {
        const templates = this._searchKeyword
          ? await EdgelessTemplatePanel.templates.search(this._searchKeyword)
          : await EdgelessTemplatePanel.templates.list(this._currentCategory);

        if (state.canceled) return;

        this._templates = templates;
      } catch (e) {
        if (state.canceled) return;

        console.error('Failed to load templates', e);
      }
    });
  }

  override connectedCallback(): void {
    super.connectedCallback();
    this.addEventListener('keydown', stopPropagation, false);
  }

  override firstUpdated() {
    requestConnectedFrame(() => {
      this._disposables.addFromEvent(document, 'click', evt => {
        if (this.contains(evt.target as HTMLElement)) {
          return;
        }

        this._closePanel();
      });
    }, this);
    this._disposables.addFromEvent(this, 'click', stopPropagation);
    this._disposables.addFromEvent(this, 'wheel', stopPropagation);

    this._initCategory().catch(() => {});
  }

  override render() {
    const { _categories, _currentCategory, _templates } = this;

    return html`
      <div class="edgeless-templates-panel">
        <div class="search-bar">
          <input
            class="search-input"
            type="text"
            placeholder="Search file or anything..."
            @input=${this._updateSearchKeyword}
            @cut=${stopPropagation}
            @copy=${stopPropagation}
            @paste=${stopPropagation}
          />
        </div>
        <div class="template-categories">
          ${repeat(
            _categories,
            cate => cate,
            cate => {
              return html`<div
                class="category-entry ${_currentCategory === cate
                  ? 'selected'
                  : ''}"
                @click=${() => {
                  this._currentCategory = cate;
                  this._updateTemplates();
                }}
              >
                ${cate}
              </div>`;
            }
          )}
        </div>
        <div class="template-viewport">
          <div class="template-scrollcontent" data-scrollable>
            <div class="template-list">
              ${this._loading
                ? html`<affine-template-loading
                    style=${styleMap({
                      position: 'absolute',
                      left: '50%',
                      top: '50%',
                    })}
                  ></affine-template-loading>`
                : repeat(
                    _templates,
                    template => template.name,
                    template => {
                      const preview = template.preview
                        ? template.preview.startsWith('<svg')
                          ? html`${unsafeSVG(template.preview)}`
                          : html`<img
                              src="${template.preview}"
                              class="template-preview"
                              loading="lazy"
                            />`
                        : defaultPreview;

                      return html`
                        <div
                          class=${`template-item ${
                            template === this._loadingTemplate ? 'loading' : ''
                          }`}
                          @click=${() => this._insertTemplate(template, {x:0,y:0,w:0,h:0})}
                        >
                          ${preview}
                          ${template === this._loadingTemplate
                            ? html`<affine-template-loading></affine-template-loading>`
                            : nothing}
                          ${template.name
                            ? html`<affine-tooltip
                                .offset=${12}
                                tip-position="top"
                              >
                                ${template.name}
                              </affine-tooltip>`
                            : nothing}
                        </div>
                      `;
                    }
                  )}
            </div>
          </div>
          <overlay-scrollbar></overlay-scrollbar>
        </div>
        <div class="arrow">${ArrowIcon}</div>
      </div>
    `;
  }

  @state()
  private accessor _categories: string[] = [];

  @state()
  private accessor _currentCategory = '';

  @state()
  private accessor _loading = false;

  @state()
  private accessor _loadingTemplate: Template | null = null;

  @state()
  private accessor _searchKeyword = '';

  @state()
  private accessor _templates: Template[] = [];

  // Cover selector related states
  @state()
  private accessor _activeTab: 'templates' | 'my-images' | 'link' = 'templates';

  @state()
  private accessor _coverLink = '';

  @state()
  private accessor _showLinkError = false;

  @state()
  private accessor _userImages: Array<{
    imageUrl: string;
    thumbnailUrl?: string;
    provider?: string;
  }> = [];

  @state()
  private accessor _isLoadingImages = false;

  // Load user images
  private async _loadUserImages() {
    this._isLoadingImages = true;
    try {
      // In a real implementation, this would fetch from a service
      this._userImages = [
        { imageUrl: 'image1.jpg', thumbnailUrl: 'thumb1.jpg', provider: '本地' },
        { imageUrl: 'image2.jpg', thumbnailUrl: 'thumb2.jpg', provider: '云端' },
      ];
    } catch (error) {
      console.error('Failed to load user images', error);
    } finally {
      this._isLoadingImages = false;
    }
  }

  // Handle file upload
  private _handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      // In a real implementation, this would upload the file
      const imageUrl = URL.createObjectURL(file);
      this._userImages = [
        ...this._userImages,
        { imageUrl, provider: '上传' }
      ];
      input.value = '';
    }
  }

  // Handle cover image selection
  private _handleImageSelect(url: string) {
    this.dispatchEvent(new CustomEvent('select', { detail: url }));
    this._closePanel();
  }

  // Handle link submission
  private _handleLinkSubmit() {
    const trimmedLink = this._coverLink.trim();
    if (!trimmedLink) {
      this._showLinkError = true;
      return;
    }

    try {
      new URL(trimmedLink);
      this._showLinkError = false;
      this.dispatchEvent(new CustomEvent('select', { detail: trimmedLink }));
      this._closePanel();
    } catch (e) {
      this._showLinkError = true;
    }
  }

  // Updated render method to include cover selector tabs
  override render() {
    const { _categories, _currentCategory, _templates } = this;
    // Removed draggable controller related code

    return html`
      <div class="edgeless-templates-panel">
        <div class="tabs">
          <button
            class="tab ${this._activeTab === 'templates' ? 'tab-active' : ''}"
            @click=${() => (this._activeTab = 'templates')}
          >
            模板
          </button>
          <button
            class="tab ${this._activeTab === 'my-images' ? 'tab-active' : ''}"
            @click=${() => (this._activeTab = 'my-images')}
          >
            我的图片
          </button>
          <button
            class="tab ${this._activeTab === 'link' ? 'tab-active' : ''}"
            @click=${() => (this._activeTab = 'link')}
          >
            填写链接
          </button>
        </div>

        ${this._activeTab === 'templates'
          ? html`
              <div class="search-bar">
                <input
                  class="search-input"
                  type="text"
                  placeholder="搜索模板..."
                  @input=${this._updateSearchKeyword}
                />
              </div>
              <div class="template-categories">
                ${repeat(
                  _categories,
                  cate => cate,
                  cate => html`
                    <div
                      class="category-entry ${_currentCategory === cate
                        ? 'selected'
                        : ''}"
                      @click=${() => {
                        this._currentCategory = cate;
                        this._updateTemplates();
                      }}
                    >
                      ${cate}
                    </div>
                  `
                )}
              </div>
              <div class="template-viewport">
                <div class="template-scrollcontent" data-scrollable>
                  <div class="template-list">
                    ${this._loading
                      ? html`<div class="loading-spinner"></div>`
                      : repeat(
                          _templates,
                          template => template.name,
                          template => {
                            const preview = template.preview
                              ? html`<img
                                  src="${template.preview}"
                                  class="template-preview"
                                />`
                              : defaultPreview;
                            return html`
                              <div
                                class="template-item"
                                @click=${() => this._insertTemplate(template, {x:0,y:0,w:0,h:0})}
                              >
                                ${preview}
                              </div>
                            `;
                          }
                        )}
                  </div>
                </div>
              </div>
            `
          : this._activeTab === 'my-images'
          ? html`
              <div class="tab-content">
                ${this._isLoadingImages
                  ? html`<div class="loading-spinner">加载中...</div>`
                  : this._userImages.length === 0
                  ? html`<div class="empty-state">暂无图片</div>`
                  : html`
                      <div class="image-grid">
                        ${repeat(
                          this._userImages,
                          (image) => image.imageUrl,
                          (image) => html`
                            <div
                              class="image-item"
                              @click=${() => this._handleImageSelect(image.imageUrl)}
                            >
                              <img
                                src=${image.thumbnailUrl || image.imageUrl}
                                alt="用户图片"
                              />
                            </div>
                          `
                        )}
                      </div>
                      <input
                        type="file"
                        id="cover-upload"
                        accept="image/*"
                        class="hidden"
                        @change=${this._handleFileUpload}
                      />
                      <label
                        for="cover-upload"
                        class="upload-button"
                      >
                        上传图片
                      </label>
                    `}
              </div>
            `
          : html`
              <div class="link-input-container">
                <input
                  class="link-input"
                  type="text"
                  placeholder="输入图片链接..."
                  .value=${this._coverLink}
                  @input=${(e: InputEvent) => {
                    this._coverLink = (e.target as HTMLInputElement).value;
                    this._showLinkError = false;
                  }}
                />
                ${this._showLinkError
                  ? html`<div class="error-message">请输入有效的图片链接</div>`
                  : nothing}
                <button
                  class="submit-button"
                  ?disabled=${!this._coverLink.trim()}
                  @click=${this._handleLinkSubmit}
                >
                  确认
                </button>
              </div>
            `}
      </div>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'edgeless-templates-panel': EdgelessTemplatePanel;
  }
}
