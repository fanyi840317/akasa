export interface Category {
    $id: string;
    name: {
        zh: string;
        en: string;
    };
    description: {
        zh: string;
        en: string;
    };
    icon: string;
    color: string;
    parent_id: string | null;
    order: number;
    status: string;
    user_id: string;
    created_at: string;
    updated_at: string;
} 