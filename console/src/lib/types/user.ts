import type { Entity } from './entity';

export type User = Entity & {
	email: string;
	avatar?: string;
};

export type Team = Entity & {
	description: string;
	logo: string;
	level: number;
	rating: number;
	foundedAt: Date;
	memberIds: string[];
	leaderId: string;
	specialties: string[];
	completedInvestigations: number;
	status: 'active' | 'inactive' | 'suspended';
	verificationStatus: 'pending' | 'verified' | 'rejected';
};
