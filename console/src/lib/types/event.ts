import type { Entity } from './entity';

export interface Event extends Entity {
	content?: string;
	summary?: string;
	categories?: string[];
	tags?: string[];
	date?: string | Date;
	privacy?: 'public' | 'private';
	user_id?: string;
	cover?: string;
	location_data?: Record<string, unknown>;
	status?: 'published' | 'draft' | 'archived';
	entities_data?: Record<string, unknown>;
	creator_name?: string;
	creator_avatar?: string;
	folder_id?: string;
}

export interface CreateEventRequest {
	name: string;
	content?: string;
	summary?: string;
	categories?: string[];
	tags?: string[];
	date?: string | Date;
	privacy?: 'public' | 'private';
	user_id?: string;
	cover?: string;
	location_data?: Record<string, unknown>;
	status?: 'published' | 'draft' | 'archived';
	entities_data?: Record<string, unknown>;
	creator_name?: string;
	creator_avatar?: string;
	folder_id?: string;
}

export interface UpdateEventRequest extends Partial<CreateEventRequest> {
	status?: 'published' | 'draft' | 'archived';
}

export interface EventListResponse {
	events: Event[];
	total: number;
	page: number;
	limit: number;
}

export interface EventFilters {
	categories?: string[];
	status?: 'published' | 'draft' | 'archived';
	tags?: string[];
	search?: string;
	user_id?: string;
	privacy?: 'public' | 'private';
}