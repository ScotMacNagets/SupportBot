
#Services
class ChatServiceText:
    SEND_TO_ADMIN_MESSAGE="Новое сообщение от пользователя: \n\n{text}"


#Handlers
class AdminRegister:
    SUCCESSFUL_REGISTRATION="✅ Вы успешно зарегестрированы\n\n username: {username}\ntelegram_id: {telegram_id}"

class AdminMessage:
    ALREADY_CLOSED="🗂 Диалог уже закрыт"
    ALREADY_TOOK="😒 Ой, уже кто то занял чат"
    CLOSE_YOUR_CURRENT_CHAT="🤔 Сначала заверши свой текущий диалог"
    ACCEPTED_CHAT="✅ Ты принял диалог"
    ACCEPT_THEN_CLOSE="Сначала ✅ прими диалог, а потом нажми кнопку ⛔ закрыть"
    SUCCESSFULLY_CLOSED="✅ Диалог успешно завершен"
    DONT_HAVE_ACTIVE_CHAT="⛔ У тебя нет активного диалога"


#Keyboards
class AdminMessageKeyboard:
    ACCEPT="✅ Принять"
    CLOSE="⛔ Закрыть"



