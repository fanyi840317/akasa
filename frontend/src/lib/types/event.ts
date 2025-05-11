import type { Location } from './map';

export type EventStatus = 'unverified' | 'confirmed' | 'closed';
export type EventCategory = 'urban' | 'paranormal' | 'supernatural' | 'mysterious' | 'unexplained' | 'phenomena';

export type Evidence = {
  id: string;
  type: 'image' | 'video' | 'document' | 'testimony';
  url: string;
  description: string;
  submittedBy: string;
  submittedAt: Date;
  verificationStatus: 'pending' | 'verified' | 'rejected';
};

export type Witness = {
  id: string;
  name: string;
  credibilityScore: number;
  testimony: string;
  contactInfo?: string;
  anonymous: boolean;
};

export type TimelineEvent = {
  id: string;
  timestamp: Date;
  description: string;
  evidenceIds: string[];
  witnessIds: string[];
};

export type RelatedPerson = {
  id: string;
  name: string;
  role: string;
  description: string;
  anonymous: boolean;
};

export type Hypothesis = {
  id: string;
  title: string;
  description: string;
  evidence: string[];
  createdAt: Date;
};

export type Event = {
  $id?: string;
  $createdAt?: string;
  $updatedAt?: string;
  title: string;
  content: string;
  summary?: string;
  categories?: string[];
  tags?:string[];
  date: string;
  privacy?: string;
  user_id: string;
  cover?: string;
  location_data?: Location;
  status?: string;
  entities_data?: string;
  creator_name?: string;
  creator_avatar?: string;
  folder_id?: string;
}

export type Tag = { $id?: string; name: string; };