export interface Case {
  $id?: string;
  title: string;
  content: string;
  location: string;
  categories?: string[];
  date: string;
  user_id: string;
  cover?: string;
  location_data?: string;
} 