
#Services
class ChatServiceText:
    SEND_TO_ADMIN_MESSAGE="Новое сообщение от пользователя: \n\n{text}"


#Handlers
class AdminMessage:
    ALREADY_CLOSED="🗂 Диалог уже закрыт"
    ALREADY_TOOK="😒 Ой, уже кто то занял чат"
    CLOSE_YOUR_CURRENT_CHAT="🤔 Сначала заверши свой текущий диалог"
    ACCEPTED_CHAT="✅ Ты принял диалог"
    ACCEPT_THEN_CLOSE="Сначала ✅ прими диалог, а потом нажми кнопку ⛔ закрыть"
    SUCCESSFULLY_CLOSED="✅ Диалог успешно завершен"
    DONT_HAVE_ACTIVE_CHAT="⛔ У тебя нет активного диалога"

class AdminRegister:
    INPUT_REGISTER_KEY="Введите <b>уникальный ключ</b> для регистрации"
    SUCCESSFUL_REGISTRATION="✅ Вы успешно зарегестрированы\n\n username: {username}\ntelegram_id: {telegram_id}"
    UNSUCCESSFUL_REGISTRATION=(
        "⚠️ Не удалось вас зарегестрировать.\n\n"
        "Обратитесь к <a href='https://t.me/{admin_username}'>администратору</a> " 
        "для получения доступа."
    )
    ALREADY_REGISTERED="Админ с таким именем уже зарегестрирован. Попробуйте позже"

class AdminSuperuser:
    ADMIN_LIST="👥 Список админов:"
    WELCOME_TO_SUPERUSER_MENU="📌 Доброе пожаловать в меню супер-пользователя:"
    NOT_ENOUGH_RIGHTS= "⛔ У тебя нет доступа к этому меню"
    NEW_KEY_GENERATED="Новый ключ сгенерирован: \n\n- <code>{new_key}</code>"
    CANNOT_GENERATE_THE_KEY="⛔ Не удалось сгенерировать новый ключ, попробуйте позже"
    ADMIN_FORMAT_DETAIL=(
        "👤 <b>Админ</b>\n\n"
        "ID: <code>{telegram_id}</code>\n"
        "Username: @{username}\n"
        "Создан: {created_at}"
    )
    ADMIN_NOT_FOUND="🔎 Админ не найден, попробуйте позже"
    SUCCESSFULLY_DELETED="✅ Админ: {username} успешно удален"
    ADMIN_IS_BUSY="Админ уже начал с кем то диалог, попробуйте позже"



#Keyboards
class AdminMessageKeyboard:
    ACCEPT="✅ Принять"
    CLOSE="⛔ Закрыть"

class AdminSuperuserKeyboard:
    REALISE_NEW_KEY="🔑 Выпустить новый ключ"
    ADMIN_LIST="💾 Список админов"
    CONFIRM_DELETE="⛔ Удалить"
    ADMIN_BUTTON_FORMAT="👤 Username: @{username} | 📄 Создан: {created_at}"
    BACK_TO_THE_MAIN_MENU= "🔙 Вернуться в главное меню"







