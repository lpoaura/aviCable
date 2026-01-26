export interface Post {
    id: number;
    title: string;
    intro: string;
    private: boolean;
    timestamp_create: string;
    timestamp_update: string | null;
    created_by?: string | object;
    updated_by?: string | object | null;
}

export type Posts = Post[];