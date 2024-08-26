import json
from channels.generic.websocket import AsyncWebsocketConsumer
from messenger.models import Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

var = 0
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Получаем имя комнаты из URL маршрута
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Присоединяемся к комнате по имени группы
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем комнату
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def save_message(self, username, message, room):
        user = User.objects.get(username=username)
        record = Message.objects.create(username=user, message=message, room=room)
        record.save()
        return record.id
    @sync_to_async
    def delete_message(self, messageId):
        Message.objects.get(id = messageId).delete()
    @sync_to_async
    def edit_message(self, messageId, message):
        Message.objects.filter(id = messageId).update(message = message)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        
        if action == "create":
            message = text_data_json["message"]
            username = text_data_json["username"]
            room = text_data_json["room"]
        
            id = await self.save_message(username, message, room)
            # Отправляем сообщение в комнату группы
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "sendMessage",
                    "message": message,
                    "username": username,
                    "room": room,
                    "id":id
                }
                
            )
        elif action == "delete":
            id =  text_data_json["messageId"]
            await self.delete_message(id)
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "deleteMessage",
                        "id":id,
                        "action":"delete"
                    }
                    
                )
        elif action == 'edit':
            id = text_data_json["messageId"]
            message = text_data_json["message"]
            print(id ,message)
            await self.edit_message(id, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type":"editMessage",
                    "id" : id,
                    "message":message,
                    "action":"edit",
                }
            )
            
    # Отправляем сообщение обратно в WebSocket
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]
        id = event["id"]
        await self.send(text_data=json.dumps({
            "action":"create",
            "message": message,
            "username": username,
            "room": room,
            "id":id
        }))
    async def deleteMessage(self, event):
        id = event["id"]
        await self.send(text_data=json.dumps({
            "action":"delete",
            "id":id
        }))
    async def editMessage(self, event):
        print(event)
        id = event["id"]
        message = event["message"]
        await self.send(text_data= json.dumps({
            "action":"edit",
            "id":id,
            "message":message
        }))
        