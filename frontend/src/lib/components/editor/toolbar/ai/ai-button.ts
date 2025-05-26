import { LitElement, html, css } from "lit";
import { getTooltipWithShortcut } from "./../../unit";
import { property } from "lit/decorators.js";

export class EdgelessAIToolButton extends LitElement {
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
    .ai-button {
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      overflow: hidden;
      width: 90px;
      padding: 4px;
      height: 64px;
      z-index: 50;
      border-radius: 8px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: 2px solid transparent;
      cursor: pointer;
    }
    
    .ai-button:hover {
      background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
      border-color: rgba(255, 255, 255, 0.3);
    }

    .ai-icon {
      width: 32px;
      height: 32px;
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
    }

    .ai-badge {
      position: absolute;
      bottom: 4px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(255, 255, 255, 0.9);
      color: #333;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 10px;
      font-weight: 600;
      white-space: nowrap;
    }

    .pulse-animation {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.3);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% {
        transform: translate(-50%, -50%) scale(0.8);
        opacity: 1;
      }
      100% {
        transform: translate(-50%, -50%) scale(1.4);
        opacity: 0;
      }
    }

    .sparkle {
      position: absolute;
      width: 4px;
      height: 4px;
      background: white;
      border-radius: 50%;
      animation: sparkle 1.5s infinite;
    }

    .sparkle:nth-child(1) {
      top: 10px;
      right: 15px;
      animation-delay: 0s;
    }

    .sparkle:nth-child(2) {
      top: 20px;
      left: 10px;
      animation-delay: 0.5s;
    }

    .sparkle:nth-child(3) {
      bottom: 15px;
      right: 20px;
      animation-delay: 1s;
    }

    @keyframes sparkle {
      0%, 100% {
        opacity: 0;
        transform: scale(0);
      }
      50% {
        opacity: 1;
        transform: scale(1);
      }
    }
  `;

  @property({ type: Boolean })
  declare active: boolean;

  @property({ type: Boolean })
  declare loading: boolean;

  constructor() {
    super();
    this.active = false;
    this.loading = false;
  }

  private _handleClick() {
    this.dispatchEvent(
      new CustomEvent("ai-click", {
        bubbles: true,
        composed: true,
      })
    );
  }

  render() {
    return html`
      <edgeless-toolbar-button
        class="edgeless-ai-button"
        .tooltip=${getTooltipWithShortcut("AI Assistant")}
        .tooltipOffset=${4}
        .disabled=${this.loading}
      >
        <div 
          class="ai-button" 
          @click=${this._handleClick}
        >
          ${this.loading ? html`<div class="pulse-animation"></div>` : ''}
          
          <!-- AI Brain SVG Icon -->
          <svg class="ai-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2Z" fill="#FFD700"/>
            <path d="M12 6C15.31 6 18 8.69 18 12C18 15.31 15.31 18 12 18C8.69 18 6 15.31 6 12C6 8.69 8.69 6 12 6Z" fill="#FF6B6B"/>
            <circle cx="9" cy="10" r="1.5" fill="#4ECDC4"/>
            <circle cx="15" cy="10" r="1.5" fill="#4ECDC4"/>
            <path d="M9 14C9 14 10.5 15.5 12 15.5C13.5 15.5 15 14 15 14" stroke="#45B7D1" stroke-width="2" stroke-linecap="round"/>
            <path d="M8 8L10 6" stroke="#96CEB4" stroke-width="2" stroke-linecap="round"/>
            <path d="M16 8L14 6" stroke="#96CEB4" stroke-width="2" stroke-linecap="round"/>
            <path d="M6 12L4 12" stroke="#FFEAA7" stroke-width="2" stroke-linecap="round"/>
            <path d="M18 12L20 12" stroke="#FFEAA7" stroke-width="2" stroke-linecap="round"/>
            <path d="M8 16L10 18" stroke="#DDA0DD" stroke-width="2" stroke-linecap="round"/>
            <path d="M16 16L14 18" stroke="#DDA0DD" stroke-width="2" stroke-linecap="round"/>
          </svg>

          <!-- Sparkle effects -->
          <div class="sparkle"></div>
          <div class="sparkle"></div>
          <div class="sparkle"></div>

          <div class="ai-badge">AI</div>
        </div>
      </edgeless-toolbar-button>
    `;
  }
}
