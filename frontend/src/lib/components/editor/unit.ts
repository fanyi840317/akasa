import { css, html } from 'lit';

export function getTooltipWithShortcut(
    tip: string,
    shortcut?: string,
    postfix?: string
  ) {
    // style for shortcut tooltip
    const styles = css`
      .tooltip-with-shortcut {
        display: flex;
        flex-wrap: nowrap;
        align-items: center;
        gap: 10px;
      }
      .tooltip__shortcut {
        font-size: 12px;
        position: relative;
  
        display: flex;
        align-items: center;
        justify-content: center;
        height: 16px;
        min-width: 16px;
      }
      .tooltip__shortcut::before {
        content: '';
        border-radius: 4px;
        position: absolute;
        inset: 0;
        background: currentColor;
        opacity: 0.2;
      }
      .tooltip__label {
        white-space: pre;
      }
    `;
    return html`<style>
        ${styles}
      </style>
      <div class="tooltip-with-shortcut">
        <span class="tooltip__label">${tip}</span>
        ${shortcut
          ? html`<span class="tooltip__shortcut">${shortcut}</span>`
          : ''}
        ${postfix ? html`<span class="tooltip__postfix">${postfix}</span>` : ''}
      </div>`;
  }