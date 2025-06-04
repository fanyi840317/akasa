
import type { Models } from 'appwrite';
export type User = Models.User<Models.Preferences> & { avatar?: string } | null;

export type Team = {
  $id: string;
  name: string;
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
}