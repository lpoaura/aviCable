export interface NomenclatureItem {
  id: number;
  code: string;
  mnemonic: string;
  label: string;
  type: number;
}

export type Nomenclature = {
  code: string
  id: number
  label: string
  mnemonic: string
  type: any
}

export type Source = {
  id: number
  name: string
  version: string
}

export type Type = {
  code: string
  id: number
  itemNomenclature: Nomenclature[]
  label: string
  mnemonic: string
}
