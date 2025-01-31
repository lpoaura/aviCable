export interface MediaData {
  id?: number;
  author?: string | null;
  date: string | Date | null;
  remark?: string | null;
  source?: string | null;
  storage: string | File | null;
}

export interface Media extends MediaData{
  id: number;
}

export type Medias = MediaData[];
