import { LitElement, html, css } from "lit";
import { property } from "lit/decorators.js";
import { getTooltipWithShortcut } from "../../unit";

export class EdgelessMapToolButton extends LitElement {
  static styles = css`
    :host {
      height: 100%;
      overflow-y: hidden;
      transition: transform 0.2s ease;
    }
    :host(:hover) {
      transform: scale(1.1) translateY(-10px);
    }
    .map-button {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 32px;
      height: 32px;
      border-radius: 4px;
      background: var(--affine-background-primary-color);
      cursor: pointer;
    }
    .map-icon {
      width: 20px;
      height: 20px;
      color: var(--affine-text-primary-color);
    }
  `;

  @property({ type: Boolean })
  declare active: boolean;

  constructor() {
    super();
    this.active = false;
  }

  render() {
    return html`
      <edgeless-toolbar-button
        class="edgeless-map-button"
        .tooltip=${getTooltipWithShortcut("Map")}
        .tooltipOffset=${4}
      >
        <div class="map-button" data-theme="black">
          <svg class="map-icon" viewBox="0 0 24 24">
            <path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5s2.5 1.12 2.5 2.5s-1.12 2.5-2.5 2.5z"/>
          </svg>
        </div>
      </edgeless-toolbar-button>
    `;
  }
}
