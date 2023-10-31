import ujson
import requests
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState, DisplayOptions, OptionValue
from uc_http_requester.requester import Request
from node.enums import NodeAction
from node.utils import generate_jwt


class NodeType(flow.NodeType):
    id: str = 'd3b4f0cf-8e2e-46c0-bad3-a925179792c3'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'Google_upload'
    displayName: str = 'Google_upload'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'google_upload'
    properties: List[Property] = [
        Property(
            displayName='Действие кубика',
            name='node_action',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(
                    name='Авторизация',
                    value=NodeAction.auth,
                    description=''
                ),
                OptionValue(
                    name='Загрузка файла',
                    value=NodeAction.upload_file,
                    description=''
                ),
                OptionValue(
                    name='Получение списка файлов',
                    value=NodeAction.get_file_list,
                    description=''
                ),
            ]
        ),
        Property(
            displayName='private key',
            name='private_key',
            type=Property.Type.JSON,
            default='',
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.auth
                    ],
                },
            ), 
        ),
        Property(
            displayName='auth_result',
            name='auth_result',
            type=Property.Type.JSON,
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.get_file_list,
                        NodeAction.upload_file,
                    ],
                },
            ),     
        ),
        Property(
            displayName='file_info',
            name='file_info',
            type=Property.Type.JSON,
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.auth,
                    ],
                },
            ),

        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            node_action = json.node.data.properties['node_action']

            # Авторизация
            if node_action == NodeAction.auth:
                file_info = json.node.data.properties['file_info']
                private_key = json.node.data.properties['private_key']
                jwt_token = generate_jwt(private_key)

                url = 'https://accounts.google.com/o/oauth2/token'
                auth_data = {
                    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                    'assertion': jwt_token
                    }

                headers = {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        }

                auth_request = Request(
                    url=url,
                    method=Request.Method.post,
                    json=auth_data,
                    headers=headers)
            
                auth_result = await auth_request.execute()
                auth_result_data = auth_result.json()
                
                access_token = auth_result_data['access_token']

                await json.save_result({
                    "access_token": access_token,
                    "file_info": file_info,
                    })
                json.state = RunState.complete
            
            # Загрузка файла
            if node_action == NodeAction.upload_file:
                access_token = json.node.data.properties['auth_result']['access_token']
                file_info = json.node.data.properties['auth_result']['file_info']

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'}

                url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
                file_url = file_info["path"]
                file_name = file_info["name"]

                metadata = {"name": file_name}

                data = {
                    "metadata": (None, f'{metadata}', 'application/json'),
                    "file": (file_name, requests.get(file_url).content),
                    }
      
                request = Request(
                    url=url,
                    method=Request.Method.post,
                    headers=headers,
                    json=data
                    )
            
                result = await request.execute()

                await json.save_result({
                    "result": result.status_code,
                    "access_token": access_token
                    })

                json.state = RunState.complete
            
            # Получение списка файлов
            if node_action == NodeAction.get_file_list:
                access_token = json.node.data.properties['auth_result']['access_token']

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'}

                url = 'https://www.googleapis.com/drive/v3/files/'

                request = Request(
                    url=url,
                    method=Request.Method.get,
                    headers=headers
                    )
            
                result = await request.execute()
                result_data = result.json()

                await json.save_result({
                    "result": result_data
                    })

                json.state = RunState.complete

        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
