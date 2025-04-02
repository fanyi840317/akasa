import type { Event } from "./event-types";
import type { HtmlDoc } from "./doc-types";
import type { DateValue } from "@internationalized/date";

export interface EventDetailProps {
  Event?: Omit<Event, "$id" | "$createdAt" | "$updatedAt"> & {
    IsPublic?: boolean;
  };
}

export interface TimePreset {
  Label: string;
  Value: string;
}

export interface EventDetailState {
  DateValue: DateValue | undefined;
  IsPublishing: boolean;
  NewDoc: HtmlDoc;
  IsTimeUnknown: boolean;
  StartDate: DateValue | undefined;
  EndDate: DateValue | undefined;
  TimePreset: 'exact' | 'preset' | 'unknown';
  IsPublic: boolean;
  ShowPreview: boolean;
  PreviewContent: string;
  ShowShareMenu: boolean;
  ShowQRCode: boolean;
  ShareUrl: string;
  CoverImage: string;
  IsUploading: boolean;
  ShowContent: boolean;
}

export interface EventDetailEvents {
  Close: CustomEvent<{ result: Event }>;
  Save: CustomEvent<{ result: Event }>;
} 