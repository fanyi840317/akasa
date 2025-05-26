import { LitElement, html, css } from "lit";
import { property } from "lit/decorators.js";
import { getTooltipWithShortcut } from "../../unit";
import "mapbox-gl/dist/mapbox-gl.css";
import mapboxgl from "mapbox-gl";
import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";

export class EdgelessMapToolButton extends LitElement {
  static styles = css`
    :host {
      height: 100%;
      overflow: hidden;

      transition: transform 0.2s ease;
    }
    :host(:hover) {
      transform: scale(1.1) translateY(-10px);
    }
    .map-button {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 94px;
      height: 64px;
      border-radius: 4px;
      background: var(--affine-background-primary-color);
      cursor: pointer;
    }
    #edgeless-map-tool-button-view {
      width: 100%;
      height: 60px;
    }
    /* Remove map-icon style */
  `;

  @property({ type: Boolean })
  declare active: boolean;

  @property({ type: String })
  declare accessToken: string; // Add accessToken property

  @property({ type: Number })
  declare lat: number; // Add lat property

  @property({ type: Number })
  declare lng: number; // Add lng property

  @property({ type: Number })
  declare zoom: number; // Add zoom property

  private map?: mapboxgl.Map;

  constructor() {
    super();
    this.active = false;
    this.accessToken = PUBLIC_MAPBOX_TOKEN || ""; // Initialize accessToken
    this.lat = 39.9; // Initialize lat
    this.lng = 116.4; // Initialize lng
    this.zoom = 10; // Initialize zoom
  }
  firstUpdated() {
    mapboxgl.accessToken = this.accessToken;

    this.map = new mapboxgl.Map({
      attributionControl: false,
      container: this.renderRoot.querySelector('#edgeless-map-tool-button-view') as HTMLElement,
      // style: 'mapbox://styles/mapbox/streets-v11',
      style: "mapbox://styles/mapbox/dark-v11",
      center: [this.lng, this.lat],
      zoom: this.zoom,
      pitch: 0,
      antialias: true,
      interactive: false,
    });

    this.map.on('load', () => {
      console.log('Map loaded');
    });
  }

  updated(changedProps: Map<string | number | symbol, unknown>) {
    if (this.map && (changedProps.has('lat') || changedProps.has('lng') || changedProps.has('zoom'))) {
      this.map.setCenter([this.lng, this.lat]);
      this.map.setZoom(this.zoom);
    }
  }

  render() {
    return html`
      <edgeless-toolbar-button
        class="edgeless-map-button"
        .tooltip=${getTooltipWithShortcut("Map")}
        .tooltipOffset=${4}
      >
        <div class="map-button" data-theme="black">
          <!-- Use MapboxView component -->
          <div id="edgeless-map-tool-button-view"></div>
        </div>
      </edgeless-toolbar-button>
    `;
  }
}
