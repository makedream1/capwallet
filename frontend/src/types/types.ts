
export interface IToken {
  id: string;
  name: string;
  img: string;
  price: number;
  shortName: string;
  amount: number;
  address: string;
  networkName: string;
  networkShortName: string;
  min_withdraw_limit: number;
  gas_fee: number;
}

export interface IFormData {
  user_id: string;
  source: string;
  amount: number;
  gas_fee: number;
  destination: string;
  coin: string;
  network: string;
  query_id: string;
}

export interface ITokenSelectBox {
  onChange?: (value: string) => void;
  tokens: IToken[];
  isDisabled: boolean;
  isRequired: boolean;
}