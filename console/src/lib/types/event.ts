import type { Entity } from './entity';

export type Event = Entity & {
	title?: string;
	content?: string;
	summary?: string;
	categories?: string[];
	tags?: string[];
	date?: string | Date;
	privacy?: string;
	user_id: string;
	cover?: string;
	location_data?: Location | string;
	status?: string;
	entities_data?: string;
	creator_name?: string;
	creator_avatar?: string;
	folder_id?: string;
	likes?: number;
	views?: number;
};
