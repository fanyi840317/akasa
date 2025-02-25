export interface User {
  id: string;
  name: string;
  avatar: string;
  email: string;
  role: 'investigator' | 'admin' | 'moderator';
  level: number;
  experience: number;
  joinedAt: Date;
  lastActiveAt: Date;
  reputation: number;
  badges: string[];
  teamId?: string;
  bio?: string;
  followers?: number;
  investigations?: number;
  investigationSuccessRate?: number;
  skills?: string[];
  certifications?: string[];
  socialLinks?: {
    website?: string;
    twitter?: string;
    linkedin?: string;
  };
}

export interface Team {
  id: string;
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