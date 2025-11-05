import httpx
import json
from fastapi import Depends, Request
from fastapi.responses import Response, StreamingResponse
from fastapi import BackgroundTasks

from common.model.http import create_response
from common.util.password import hash_password
from common.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, SERVICE_ID
from model.sql.chat import Chat
from model.http.chat import ChatCompletionRequest, ChatResponse
from repository.sql.chat import ChatRepository
from common.util.log.log2 import logger


class ChatService:
    def __init__(
        self, 
        request: Request,
        repo: ChatRepository = Depends(ChatRepository)
    ):
        self.request = request
        self.repo = repo
    
    async def stream_parser(self, chat: Chat | None, content: str) -> list:
        """
        chunks = []
        for chunk in content.split("\n\n"):
            if chunk.startswith("data: "):
                chunk = chunk.removeprefix("data: ").strip()
                if chunk != "[DONE]":
                    chunks.append(json.loads(chunk))
        return chunks
        """

        if chat is not None:
            answer_text = ""
            for line in content.splitlines():
                if line.startswith("data: "):
                    b = line.removeprefix("data: ")
                    if not b.strip() == "[DONE]":
                        jsonB = json.loads(b)
                        if "choices" in jsonB and len(jsonB["choices"]) > 0 and "delta" in jsonB["choices"][0] and "content" in jsonB["choices"][0]["delta"]:
                            c = jsonB["choices"][0]["delta"]["content"]
                            answer_text += c
                        if "usage" in jsonB:
                            usage = jsonB["usage"]
                            chat.prompt_tokens = usage.get("prompt_tokens", None)
                            chat.completion_tokens = usage.get("completion_tokens", None)
                            chat.total_tokens = usage.get("total_tokens", None)
                        if chat.completion_id is None and "id" in jsonB:
                            chat.completion_id = jsonB["id"]

            chat.answer = answer_text
            chat.response = content
            print(f"TODO >>>> chat >>> response: {chat.answer}")
            await self.repo.create(chat)
        return []


    async def nonstream_parser(self, chat: Chat | None, content: str) -> dict:
        json_content = json.loads(content)
        if chat is not None:
            chat.response = content
            chat.completion_id = json_content.get("id", None)
            if "choices" in json_content and len(json_content["choices"]) > 0:
                first_choice = json_content["choices"][0]
                if "message" in first_choice and "content" in first_choice["message"]:
                    chat.answer = first_choice["message"]["content"]
            if "usage" in json_content:
                usage = json_content["usage"]
                chat.prompt_tokens = usage.get("prompt_tokens", None)
                chat.completion_tokens = usage.get("completion_tokens", None)
                chat.total_tokens = usage.get("total_tokens", None)
            print(f"TODO >>>> chat >>> response: {chat.answer}")
            await self.repo.create(chat)
        return json_content
    
    async def completions(self, req_body: ChatCompletionRequest, tasks: BackgroundTasks ):
        url = f"{OPENROUTER_BASE_URL}/chat/completions"
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
        body = req_body.model_dump()

        client = httpx.AsyncClient(timeout=600)
        req = client.build_request(
            "POST",
            url,
            headers=headers,
            json=body,
        )
        res = await client.send(req, stream=True)

        content_type = res.headers.get("content-type", "")
        status = res.status_code

        if content_type.startswith("text/event-stream"):

            async def stream_generator():
                accumulated_text = ""
                try:
                    async for b in res.aiter_bytes():
                        accumulated_text += b.decode("utf-8", errors="ignore")
                        yield b
                except Exception as e:
                    print(f"ERROR in stream_generator for model {body.get('model')}: {e}")
                    # raise
                finally:
                    tasks.add_task(self.stream_parser, chat=None, content=accumulated_text)
                    await res.aclose()
                    await client.aclose()

            return StreamingResponse(
                stream_generator(),
                status_code=status,
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                    "Connection": "keep-alive",
                },
            )

        try:
            content = await res.aread()
        except Exception as e:
            print(f"ERROR in non-streaming response for model {body.get('model')}: {e}")
            # raise
        finally:
            tasks.add_task(self.nonstream_parser, chat=None, content=content.decode("utf-8", errors="ignore"))
            response = Response(
                content=content,
                status_code=status,
                media_type=content_type or "application/json",
            )
            await res.aclose()
            await client.aclose()
            return response

    async def conversations(self, req_body: ChatCompletionRequest, tasks: BackgroundTasks ):
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        print(f"TODO >>> conversations >>> {user_id}, {req_body}")

        url = f"{OPENROUTER_BASE_URL}/chat/completions"
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
        body = req_body.model_dump()

        user_prompt = None
        if body.get("messages"):
            for message in reversed(body.get("messages")):
                if message.get("role") == "user":
                    user_prompt = message.get("content")
                    break
        parameters = {
            "temperature": req_body.temperature,
            "top_p": req_body.top_p,
            "top_k": req_body.top_k,
        }
        newChat = Chat(
            # hierarchy
            parent_id=req_body.parent_id,
            index=req_body.index,
            #
            user_id=user_id,
            service_id=SERVICE_ID,
            url=url,
            user_prompt=user_prompt,
            answer=None,
            request=json.dumps(body, ensure_ascii=False),
            response=None,
            completion_id=None,
            model_name=body.get("model"),
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            is_stream=body.get("stream", False),
            system_prompt=req_body.system_prompt,
            parameters=str(parameters),
        )

        client = httpx.AsyncClient(timeout=600)
        req = client.build_request(
            "POST",
            url,
            headers=headers,
            json=body,
        )
        res = await client.send(req, stream=True)

        content_type = res.headers.get("content-type", "")
        status = res.status_code

        if content_type.startswith("text/event-stream"):

            async def stream_generator():
                accumulated_text = ""
                try:
                    async for b in res.aiter_bytes():
                        logger.info(f"TODO >>> receive {b}")
                        accumulated_text += b.decode("utf-8", errors="ignore")
                        yield b
                except Exception as e:
                    print(f"ERROR in stream_generator for user {user_id}, model {body.get('model')}: {e}")
                    # raise
                finally:
                    tasks.add_task(self.stream_parser, chat=newChat, content=accumulated_text)
                    await res.aclose()
                    await client.aclose()

            return StreamingResponse(
                stream_generator(),
                status_code=status,
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                    "Connection": "keep-alive",
                },
            )

        content = ""
        try:
            content = await res.aread()
        except Exception as e:
            print(f"ERROR in non-streaming response for user {user_id}, model {body.get('model')}: {e}")
            # raise
        finally:
            tasks.add_task(self.nonstream_parser, chat=newChat, content=content.decode("utf-8", errors="ignore") if content else "")
            response = Response(
                content=content,
                status_code=status,
                media_type=content_type or "application/json",
            )
            await res.aclose()
            await client.aclose()
            return response


    ##########################################################################
    # chat title
    def create_chat_title(self, title: str) -> Chat:
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        print(f"TODO >>> create_chat_title: {user_id}, {title}")
        return self.repo.create_chat_title(user_id=user_id, service_id=SERVICE_ID, title=title)

    def update_chat_title(self, id: str, title: str) -> Chat:
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        return self.repo.update_chat_title(user_id=user_id, id=id, title=title)

    def delete_chat_title(self, id: str) -> Chat:
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        return self.repo.delete_chat_title(user_id=user_id, id=id)

    def list_chat_title(self) -> list[Chat]:
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        return self.repo.list_chat_title(user_id=user_id)
    

    ##########################################################################
    # chat
    def create_chat(self, parent_id: str, user_prompt: str) -> Chat:
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        return self.repo.create_chat(user_id=user_id, service_id=SERVICE_ID, parent_id=parent_id, user_prompt=user_prompt)

    def get_chat_with_children(self, id: str) -> ChatResponse:
        user_id = None
        token_payload = getattr(self.request.state, 'token_payload', None)
        if token_payload is not None:
            user_id = token_payload.sub
        return self.repo.get_chat_with_children(user_id=user_id, id=id)
