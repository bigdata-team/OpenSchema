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
        query = select(self.model).where(
            self.model.deleted_at == None, 
            self.model.user_id == user_id, self.model.id == id,
        )
        exist = await self.sql.execute(query)
        exist = exist.scalar_one_or_none()
        if exist is None:
            # TODO
            return None
        print(f"TODO >>> delete chat title and its children: {exist}")
        await self.delete(id=id)
        return exist
    
    # chat title
    async def list_chat_title(self, user_id: str) -> list[Chat]:
        query = select(self.model).where(
            self.model.deleted_at == None, 
            self.model.user_id == user_id, self.model.parent_id == None,
        ).order_by(self.model.created_at.desc())
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
    async def create_chat(self, user_id: str, service_id: str, parent_id: str, user_prompt: str) -> Chat:
        chat = self.model(user_id=user_id, service_id=service_id, parent_id=parent_id, user_prompt=user_prompt)
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
        ).order_by(self.model.created_at.asc(), self.model.index.asc())
        list1 = await self.sql.execute(query)

        res = []
        for r1 in list1.scalars().all():
            d1 = r1.model_dump()
            d1.pop("request", None)
            d1.pop("response", None)
            # res.append(d1)

            query = select(self.model).where(
                self.model.deleted_at == None,
                self.model.user_id == user_id, self.model.parent_id == r1.id,
            ).order_by(self.model.index.asc(), self.model.created_at.asc())
            # print(str(query.compile(compile_kwargs={"literal_binds": True})))

            list2 = await self.sql.execute(query)
            children = []
            for r2 in list2.scalars().all():
                d2 = r2.model_dump()
                d2.pop("request", None)
                d2.pop("response", None)
                children.append(d2)

            res.append(ChatChild(
                id=r1.id,
                #
                parent_id=r1.parent_id,
                title=r1.title,
                index=r1.index,
                #
                user_id=r1.user_id,
                service_id=r1.service_id,
                url=r1.url,
                user_prompt=r1.user_prompt,
                answer=r1.answer,
                request=None,
                response=None,
                #
                completion_id=r1.completion_id,
                model_name=r1.model_name,
                prompt_tokens=r1.prompt_tokens,
                completion_tokens=r1.completion_tokens,
                total_tokens=r1.total_tokens,
                is_stream=r1.is_stream,
                system_prompt=r1.system_prompt,
                parameters=r1.parameters, 
                #
                children=children,
            ))

        chatRes = ChatResponse(
            id=exist.id,
            #
            parent_id=exist.parent_id,
            title=exist.title,
            index=exist.index,
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

