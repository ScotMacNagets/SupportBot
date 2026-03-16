

class ChatService:

    def __init__(self):

        self.chat_repo = ChatRepository()
        self.message_repo = MessageRepository()

    async def process_user_message(self, user_id: int, text: str):