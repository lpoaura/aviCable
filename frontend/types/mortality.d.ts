declare interface MortalityData {
  properties: {
    id: number;
    vernacular_name: string;
    scientific_name: string;
    death_cause?: string;
    default: boolean | undefined;
  };
}
