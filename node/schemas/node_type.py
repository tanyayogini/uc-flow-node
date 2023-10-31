from typing import List

from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, DisplayOptions, OptionValue
from node.schemas.enums import NodeAction


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