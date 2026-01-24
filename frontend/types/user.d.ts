export interface UserSimple {
    username: string;
    full_name: string | null;
    avatar: string | null;
    dateJoined?: string;
}

export interface Credentials {
    username: string;
    password: string;
}

export interface SignUpFormData {
    username: string;
    password: string;
    first_name: string;
    last_name: string;
    email: string;
    organisms?: string;
    phone?: string;
    areas: number[];
}

export interface Tokens {
    access: string;
    refresh: string;
}