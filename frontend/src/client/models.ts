export type Body_login_login_access_token = {
  grant_type?: string | null
  username: string
  password: string
  scope?: string
  client_id?: string | null
  client_secret?: string | null
}

export type HTTPValidationError = {
  detail?: Array<ValidationError>
}

export type Message = {
  message: string
}

export type NewPassword = {
  token: string
  new_password: string
}

export type OrderCreate = {
  safo_nr?: number | null
  kh_kod?: string
  description?: string | null
}

export type OrderPublic = {
  safo_nr?: number | null
  kh_kod?: string
  description?: string | null
  id: string
  owner_id: string
}

export type OrderUpdate = {
  safo_nr?: number | null
  kh_kod?: string
  description?: string | null
}

export type OrdersPublic = {
  data: Array<OrderPublic>
  count: number
}

export type Token = {
  access_token: string
  token_type?: string
}

export type UpdatePassword = {
  current_password: string
  new_password: string
}

export type UserCreate = {
  ora_id?: string | null
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  oso_kod?: string | null
  fir_kod?: string | null
  password: string
}

export type UserPublic = {
  ora_id?: string | null
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  oso_kod?: string | null
  fir_kod?: string | null
  id: string
}

export type UserRegister = {
  email: string
  password: string
  full_name?: string | null
}

export type UserUpdate = {
  ora_id?: string | null
  email?: string | null
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  oso_kod?: string | null
  fir_kod?: string | null
  password?: string | null
}

export type UserUpdateMe = {
  full_name?: string | null
  email?: string | null
}

export type UsersPublic = {
  data: Array<UserPublic>
  count: number
}

export type ValidationError = {
  loc: Array<string | number>
  msg: string
  type: string
}
