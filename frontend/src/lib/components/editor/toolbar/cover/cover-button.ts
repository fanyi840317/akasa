import { LitElement, html, css } from "lit";
import { getTooltipWithShortcut } from "./../../unit";
import { property } from "lit/decorators.js";

export class EdgelessCoverToolButton extends LitElement {
  static styles = css`
    :host {
      height: 100%;
      overflow-y: hidden;
      transition: transform 0.2s ease;
      z-index: 10000;
    }
    :host(:hover) {
      transform: scale(1.1) translateY(-10px);
    }
    .cover-button {
      display: flex;
      justify-content: center;
      align-items: flex-end;
      position: relative;
      overflow: hidden;
      width: 90px;
      padding: 4px;
      height: 64px;
      z-index: 50;
    }
    .cover-img {
      border-radius: 4px;
      border: 1px solid var(--affine-border-color);
      width: 90%;
      height: 90%;
      object-fit: cover;
    }
    .default-icon {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background: var(--affine-background-secondary-color);
      color: var(--affine-text-secondary-color);
      font-size: 24px;
    }

    .progress-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      font-size: 12px;
      justify-content: center;
      align-items: center;
      background: rgba(0, 0, 0, 0.5);
      color: white;
    }

    .progress-bar {
      width: 80%;
      height: 4px;
      background: var(--affine-background-secondary-color);
      margin-top: 8px;
      border-radius: 2px;
      overflow: hidden;
    }

    .progress-value {
      height: 100%;
      background: var(--affine-primary-color);
      transition: width 0.3s ease;
    }

    .loading-spinner {
      width: 24px;
      height: 24px;
      border: 3px solid rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      border-top-color: white;
      animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
    .url-badge {
      position: absolute;
      bottom: 4px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.7);
      color: white;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 10px;
      max-width: 80%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .delete-btn {
      position: absolute;
      top: 0;
      right: 0;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--affine-error-color);
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 12px;
      cursor: pointer;
      border: 2px solid white;
      /* transform: translate(50%, -50%); */
      opacity: 0;
      transition: opacity 0.2s;
      z-index: 100;
    }
    :host(:hover) .delete-btn {
      opacity: 1;
    }
    .eraser-button:hover ,
    .eraser-button.active {
      transform: translateY(0);
    }
  `;

  @property({ type: String, reflect: true })
  declare url: string;
  @property({ type: Number })
  declare uploadProgress: number;

  @property()
  declare showUploadProgress: boolean;

  @property()
  declare showImageLoading: boolean;

  private _handleDelete(e: Event) {
    e.stopPropagation();
    this.dispatchEvent(
      new CustomEvent("delete", {
        bubbles: true,
        composed: true,
      })
    );
    this.url = "";
  }
  private _panel?: HTMLElement;

  constructor() {
    super();
    this.url = "";
    this.uploadProgress = 0;
    this.showUploadProgress = false;
    this.showImageLoading = false;
  }

  attributeChangedCallback(name: string, _old: string | null, value: string | null) {
    super.attributeChangedCallback(name, _old, value);
    if (name === 'url' && value && value !== '') {
      this.showImageLoading = true;
    }
  }


  render() {
    const disabled = this.showUploadProgress || this.showImageLoading;

    return html`
      <edgeless-toolbar-button
        class="edgeless-cover-button"
        .tooltip=${getTooltipWithShortcut("Cover")}
        .tooltipOffset=${4}
        .disabled=${disabled}
      >
        <div 
          class="cover-button" 
          data-theme="black"
        >
          ${this.showUploadProgress
            ? html`
                <div class="progress-container">
                  Uploading...
                  <div class="progress-bar">
                    <div
                      class="progress-value"
                      style="width: ${this.uploadProgress}%"
                    ></div>
                  </div>
                </div>
              `
            : this.showImageLoading
            ? html`
                <div class="progress-container">
                  <div class="loading-spinner"></div>
                </div>
              `
            : this.url
            ? html`
                <img
                  class="cover-img"
                  src=${this.url}
                  alt="Cover"
                  @load=${() => (this.showImageLoading = false)}
                  @error=${() => (this.showImageLoading = false)}
                />
                <div class="url-badge">${this.url}</div>
                <div class="delete-btn" @click=${this._handleDelete}>×</div>
              `
            : html`<div class="default-icon">+</div>`}
        </div>
      </edgeless-toolbar-button>
    `;
  }
}
