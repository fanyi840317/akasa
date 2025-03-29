export interface MapMarker {
  position: [number, number];
  color?: string;
  category?: string;
  className?: string;
  data?: {
    title?: string;
    location?: string;
    amount?: number;
    [key: string]: any;
  };
} 