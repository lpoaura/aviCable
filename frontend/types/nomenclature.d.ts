export interface NomenclatureItem {
  id: number;
  code: string;
  mnemonic: string;
  label: string;
  type: number;
}
export type NomenclatureSerializer = {
  code: string
  id: number
  label: string
  mnemonic: string
  type: any
}

export type SourceSerializer = {
  id: number
  name: string
  version: string
}

export type TypeSerializer = {
  code: string
  id: number
  itemNomenclature: NomenclatureSerializer[]
  label: string
  mnemonic: string
}

