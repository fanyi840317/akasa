import type { LocationData } from '$lib/components/ui/map';

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

export interface Event {
  $id?: string;
  $createdAt?: string;
  $updatedAt?: string;
  title: string;
  content: string;
  location: string;
  categories?: string[];
  date: string;
  user_id: string;
  cover?: string;
  location_data?: string;
  status?: string;
  creator_name?: string;
  creator_avatar?: string;
  folder_id?: string;
}

export type Tag = { $id?: string; name: string; };
// Event {
//   id: string;
//   title: string;
//   description: string;
//   category: EventCategory;
//   status: EventStatus;
//   image: string;
//   location: {
//     coordinates: [number, number];
//     address: string;
//     name: string;
//   };
//   // 时间信息
//   occurredAt: Date;
//   reportedAt: Date;
//   lastUpdatedAt: Date;
//   // 参与者信息
//   createdBy: string;
//   witnesses: Witness[];
//   relatedPersons: RelatedPerson[];
//   // 可信度评分
//   credibilityScore: number;
//   evidenceStrength: number;
//   witnessCredibility: number;
//   // 事件进展
//   timeline: TimelineEvent[];
//   evidence: Evidence[];
//   // 社区互动
//   views: number;
//   follows: number;
//   comments: number;
//   // 关联事件
//   relatedEventIds: string[];
//   tags: string[];
//   coverImage: string;
//   investigators?: {
//     id: string;
//     name: string;
//     avatar: string;
//     role: string;
//     joinedAt: Date;
//   }[];
// }