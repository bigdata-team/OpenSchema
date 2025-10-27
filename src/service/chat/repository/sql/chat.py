from fastapi import Depends
from sqlmodel import select

from common.connection import get_session
from common.connection.kafka import KafkaConnection
from common.connection.sql import PostgresConnection
from common.middleware.correlation import get_crid
from common.repository.sql import KafkaSqlRepository
from model.http.chat import ChatResponse, ChatChild
from model.sql.chat import Chat


class ChatRepository(KafkaSqlRepository[Chat]):
    def __init__(
        self,
        sql=Depends(get_session(PostgresConnection)),
        kafka=Depends(get_session(KafkaConnection)),
        crid=Depends(get_crid()),
    ):
        super().__init__(model=Chat, sql=sql, kafka=kafka, crid=crid)

    ##########################################################################
    # chat title
    async def create_chat_title(self, user_id: str, service_id: str, title: str) -> Chat:
        chat = self.model(user_id=user_id, service_id=service_id, title=title)
        await self.create(chat)
        return chat

    # chat title
    async def update_chat_title(self, user_id: str, id: str, title: str) -> Chat:
        query = select(self.model).where(
            self.model.deleted_at == None, 
            self.model.user_id == user_id, self.model.id == id,
        )
        exist = await self.sql.execute(query)
        exist = exist.scalar_one_or_none()
        exist.title = title
        await self.update(id, exist)
        return exist
    
    # chat title
    async def delete_chat_title(self, user_id: str, id: str) -> Chat:
        print(f"TODO >>> delete chat title: id={id}")
        query = select(self.model).where(
            self.model.deleted_at == None, 
            self.model.user_id == user_id, self.model.id == id,
        )
        exist = await self.sql.execute(query)
        exist = exist.scalar_one_or_none()
        if exist is None:
            return None
        print(f"TODO >>> delete chat title: {exist.title}")
        await self.delete(id=id)
        return exist
    
    # chat title
    async def list_chat_title(self, user_id: str) -> list[Chat]:
        query = select(self.model).where(
            self.model.deleted_at == None, 
            self.model.user_id == user_id, self.model.parent_id == None,
        )
        results = await self.sql.execute(query)

        res = []
        for r in results.scalars().all():
            d = {
                "id": r.id,
                "title": r.title,
            }
            res.append(d)
        return res
    
    ##########################################################################
    # chat
    async def create_chat(self, user_id: str, service_id: str, parent_id: str) -> Chat:
        chat = self.model(user_id=user_id, service_id=service_id, parent_id=parent_id)
        await self.create(chat)
        return chat

    # chat
    async def get_chat_with_children(self, user_id: str, id: str) -> ChatResponse:
        query = select(self.model).where(
            self.model.deleted_at == None,
            self.model.user_id == user_id, self.model.id == id,
        )
        exist = await self.sql.execute(query)
        exist = exist.scalar_one_or_none()
        if exist is None:
            return None

        query = select(self.model).where(
            self.model.deleted_at == None,
            self.model.user_id == user_id, self.model.parent_id == exist.id,
        )
        results = await self.sql.execute(query)

        res = []
        for r in results.scalars().all():
            d = r.model_dump()
            d.pop("request", None)
            d.pop("response", None)

            # TODO res.append(d)

            query = select(self.model).where(
                self.model.deleted_at == None,
                self.model.user_id == user_id, self.model.parent_id == r.id,
            )
            list2 = await self.sql.execute(query)
            children = []
            for r in list2.scalars().all():
                d = r.model_dump()
                d.pop("request", None)
                d.pop("response", None)
                children.append(d)
            res.append(ChatChild(
                id=r.id,
                #
                parent_id=r.parent_id,
                title=r.title,
                #
                user_id=r.user_id,
                service_id=r.service_id,
                url=r.url,
                user_prompt=r.user_prompt,
                answer=r.answer,
                request=None,
                response=None,
                #
                completion_id=r.completion_id,
                model_name=r.model_name,
                prompt_tokens=r.prompt_tokens,
                completion_tokens=r.completion_tokens,
                total_tokens=r.total_tokens,
                is_stream=r.is_stream,
                system_prompt=r.system_prompt,
                parameters=r.parameters, 
                #
                children=children,
            ))

        chatRes = ChatResponse(
            id=exist.id,
            #
            parent_id=exist.parent_id,
            title=exist.title,
            #
            user_id=exist.user_id,
            service_id=exist.service_id,
            url=exist.url,
            user_prompt=exist.user_prompt,
            answer=exist.answer,
            request=None,
            response=None,
            #
            completion_id=exist.completion_id,
            model_name=exist.model_name,
            prompt_tokens=exist.prompt_tokens,
            completion_tokens=exist.completion_tokens,
            total_tokens=exist.total_tokens,
            is_stream=exist.is_stream,
            system_prompt=exist.system_prompt,
            parameters=exist.parameters,
            #
            children=res,
            )
        return chatRes

