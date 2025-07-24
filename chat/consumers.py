import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Chat, Message, UserProfile
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']
        
        logger.info(f"WebSocket connect attempt for chat {self.chat_id} by user {self.user}")
        
        if self.user.is_anonymous:
            logger.warning("Anonymous user attempted to connect to WebSocket")
            await self.close()
            return
        
        # Check if user is participant in this chat
        if not await self.is_chat_participant():
            logger.warning(f"User {self.user} is not a participant in chat {self.chat_id}")
            await self.close()
            return
        
        # Join chat group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        
        # Update user online status
        await self.update_user_status(True)
        
        logger.info(f"WebSocket connected successfully for user {self.user} in chat {self.chat_id}")
        await self.accept()
    
    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnect for user {self.user} in chat {self.chat_id}")
        
        # Leave chat group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
        
        # Update user offline status
        await self.update_user_status(False)
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            
            logger.info(f"Received message: {text_data_json}")
            
            if message_type == 'chat_message':
                message_content = text_data_json.get('message', '').strip()
                
                if not message_content:
                    logger.warning("Empty message content received")
                    return
                
                # Save message to database
                message_data = await self.save_message(message_content)
                
                if message_data:
                    # Send message to chat group
                    await self.channel_layer.group_send(
                        self.chat_group_name,
                        {
                            'type': 'chat_message',
                            'message': message_content,
                            'sender': self.user.username,
                            'sender_id': self.user.id,
                            'timestamp': message_data['timestamp'],
                            'message_id': message_data['id'],
                        }
                    )
                    logger.info(f"Message sent to group {self.chat_group_name}")
                else:
                    logger.error("Failed to save message to database")
                    
            elif message_type == 'typing':
                # Handle typing indicator
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'typing_indicator',
                        'user': self.user.username,
                        'user_id': self.user.id,
                        'is_typing': text_data_json.get('is_typing', False),
                    }
                )
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {text_data}")
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")
    
    async def chat_message(self, event):
        # Send message to WebSocket
        try:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': event['message'],
                'sender': event['sender'],
                'sender_id': event['sender_id'],
                'timestamp': event['timestamp'],
                'message_id': event['message_id'],
            }))
            logger.info(f"Message sent to WebSocket for user {self.user}")
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {str(e)}")
    
    async def typing_indicator(self, event):
        # Don't send typing indicator to the sender
        if event['user_id'] != self.user.id:
            try:
                await self.send(text_data=json.dumps({
                    'type': 'typing_indicator',
                    'user': event['user'],
                    'is_typing': event['is_typing'],
                }))
            except Exception as e:
                logger.error(f"Error sending typing indicator: {str(e)}")
    
    @database_sync_to_async
    def is_chat_participant(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return chat.participants.filter(id=self.user.id).exists()
        except Chat.DoesNotExist:
            logger.error(f"Chat {self.chat_id} does not exist")
            return False
        except Exception as e:
            logger.error(f"Error checking chat participant: {str(e)}")
            return False
    
    @database_sync_to_async
    def save_message(self, content):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            message = Message.objects.create(
                chat=chat,
                sender=self.user,
                content=content
            )
            # Update chat's updated_at field
            chat.updated_at = timezone.now()
            chat.save()
            
            logger.info(f"Message saved: {message.id}")
            
            return {
                'id': message.id,
                'timestamp': message.timestamp.strftime('%I:%M %p'),
            }
        except Chat.DoesNotExist:
            logger.error(f"Chat {self.chat_id} does not exist when saving message")
            return None
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            return None
    
    @database_sync_to_async
    def update_user_status(self, is_online):
        try:
            profile, created = UserProfile.objects.get_or_create(user=self.user)
            profile.is_online = is_online
            profile.last_seen = timezone.now()
            profile.save()
            logger.info(f"User {self.user} status updated: online={is_online}")
        except Exception as e:
            logger.error(f"Error updating user status: {str(e)}")
