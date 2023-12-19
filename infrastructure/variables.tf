variable "telegram_token" {
  description = "Telegram token"
  type        = string
  sensitive   = true
}

variable "telegram_chat_id" {
  description = "Telegram owner chat id"
  type        = string
}

variable "zc_username" {
  description = "Username for Zdrowy Catering"
  type        = string
}

variable "zc_password" {
  description = "Password for Zdrowy Catering"
  type        = string
  sensitive   = true
}